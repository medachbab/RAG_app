from src.vectorStore import FaissVectorStore
from src.search import RAGSearch
import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

if __name__== "__main__":
    #docs=load_all_documents("data")
    #store= FaissVectorStore()
    #store.build_from_documents(docs)
    #store.load()    
    #print(store.query("quelles sont les troi façons principales pour envoyer des messages par un producer dans kafka", top_k=5))
    #print(store.query("quelles sont les differents types de données", top_k=5))
    rag_search= RAGSearch()
    query1="quelles sont les differents types de données"
    response= rag_search.search_and_summarize(query1, top_k=3)
    print(f"summarized response: {response}")