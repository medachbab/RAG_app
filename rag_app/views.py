import os
import logging
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings 
from pathlib import Path

#importing the modular classes in our src folder:
from src.search import RAGSearch
from src.data_loader import load_all_documents
from src.postgres_loader import load_products_from_postgres
from src.vectorStore import FaissVectorStore



@api_view(["POST"])
def rag_query(request):
    """
    POST JSON: { "query": "text", "top_k": 3 }
    """
    try:
        rag_search=RAGSearch(persist_dir="faiss_store_3")
    except Exception as e:
        logging.exception(f"exception in initializing RAGSearch instance: {e}")
        rag_search=None
    if rag_search is None:
        return Response({"error": "ragSearch instance not initialized"}, status=500)
    
    query= request.data.get("query", "")
    top_k= request.data.get("top_k", 3)

    if not query:
        return Response({"error": "query must be provided"}, status=500)
    
    try:
        result= rag_search.search_and_summarize(query, top_k=top_k)
        return Response(result)
    except Exception as e:
        logging.exception("query error")
        return Response({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UploadAndIndexView(View):
    def post(self, request):
        #uploaded_file = request.FILES.get('file')
        uploaded_files = request.FILES.getlist('files')
        
        if not uploaded_files:
            return JsonResponse({'error': 'No file provided'}, status=400)

        try:
            media_root_path = Path(settings.MEDIA_ROOT)
            media_root_path.mkdir(parents=True, exist_ok=True)
            saved_paths = []
            
            for uploaded_file in uploaded_files:
                saved_relative_path = default_storage.save(uploaded_file.name, uploaded_file)
                full_path = str(media_root_path / saved_relative_path)
                saved_paths.append(full_path)
            
            
            vectorStore= FaissVectorStore()
            docs=load_all_documents(media_root_path)
            print(docs)
            vectorStore.build_from_documents(docs) 

            
            for path in saved_paths:
                try:
                    default_storage.delete(Path(path).name)
                except Exception as e:
                    logging.warning(f"Could not delete file {path}: {e}")

            try:
                rag_search=RAGSearch(persist_dir="faiss_store_2")
            except Exception as e:
                logging.exception(f"exception in initializing RAGSearch instance: {e}")
                rag_search=None

            if rag_search is None:
                return JsonResponse({'error': 'RAG system not initialized'}, status=500)
            
            return JsonResponse({'message': f'File {uploaded_file.name} uploaded and indexed successfully.'})
        
        except Exception as e:
            logging.exception("File upload or indexing error")
            return JsonResponse({'error': f"Processing failed: {e}"}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class IndexProductsFromPostgresView(View):
    """
    Fetch products from PostgreSQL and index them into FAISS.
    """
    def post(self, request):
        try:

            docs = load_products_from_postgres()
            if not docs:
                return JsonResponse({'error': 'No products found in database'}, status=404)

            vector_store = FaissVectorStore(persist_dir="faiss_store_3")
            vector_store.build_from_documents(docs)

            try:
                rag_search = RAGSearch(persist_dir="faiss_store_3")
            except Exception as e:
                import logging
                logging.exception(f"exception in initializing RAGSearch instance: {e}")
                return JsonResponse({'error': 'RAG system not initialized'}, status=500)

            return JsonResponse({'message': f'{len(docs)} products indexed successfully.'})

        except Exception as e:
            import logging
            logging.exception("Error indexing products from PostgreSQL")
            return JsonResponse({'error': str(e)}, status=500)
