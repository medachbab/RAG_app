import os
from dotenv import load_dotenv
from src.vectorStore import FaissVectorStore
from langchain_groq import ChatGroq
import logging

load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str= "faiss_store_3", llm_model: str="openai/gpt-oss-20b"):
        self.persist_dir= persist_dir
        self.vectorstore= FaissVectorStore()
        #loading the index and the metadata of the faiss_store:
        #checking if the vector store exists or not:
        faiss_path= os.path.join(self.persist_dir, "faiss.index")
        meta_path= os.path.join(self.persist_dir, "metadata.pkl")
        if not(os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from src.data_loader import load_all_documents
            docs=load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        groq_api_key= os.getenv('groq_api_key')
        self.llm= ChatGroq(groq_api_key=groq_api_key, 
                           model_name= llm_model)
        logging.info(f"groq llm initialized: {llm_model}")
    
    def search_and_summarize(self, query: str, top_k: int= 5):

        results= self.vectorstore.query(query, top_k=top_k)
        texts=[result["metadata"].get("text", "") for result in results]
        context= "\n\n".join(texts)
        if not context:
            return {'answer': 'no relevent context found in the provided files', 'sources':[]}
        prompt = f"""summarize the following context for the query: \n{query}\n\nContext:\n{context}\n\nAnswer:"""

        sources=[{
            'source': result["metadata"],
            'distance': result["distance"],
        } for result in results]
        #generating the answer:
        prompt=f"""Use this following context to answer the question concisely and precisely\nContext:\n{context}\nQuestion:\n{query}\n\nAnswer:"""
        response=self.llm.invoke([prompt.format(context=context, query=query)])
        return {'answer':response.content,'sources': sources}


        
        
