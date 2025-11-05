import os
import faiss
import numpy as np
import pickle
from typing import Any, List
from sentence_transformers import SentenceTransformer
from src.embedding import EmbeddingPipeline
import logging

class FaissVectorStore:
    def __init__(self, persist_dir: str= "faiss_store", model_name: str="all-MiniLM-L6-v2", embedding_model: str="all-MiniLM-L6-v2", chunk_size: int=1000, chunk_overlap: int= 200):
        self.persist_dir= persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        # faiss index is the core data structure of faiss:
        self.index=None
        self.metadata= []
        self.embedding_model=embedding_model
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.model= SentenceTransformer(model_name)
    
    def build_from_documents(self, documents: List[Any]):
        embeddingPipeline= EmbeddingPipeline()
        chunks= embeddingPipeline.split_documents(documents)
        chunk_vectors= embeddingPipeline.embedding_chunks_texts(chunks)
        metadatas=[{"text": chunk.page_content} for chunk in chunks]
        self.add_embeddings(np.array(chunk_vectors).astype('float32'), metadatas)
        self.save()
        logging.info(f"vector store is built and saved in {self.persist_dir}")
    def add_embeddings(self, embeddings: np.ndarray, metadatas: List[any]):
        dim = embeddings.shape[1]
        if self.index is None:
            self.index= faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        logging.info(f"added {embeddings.shape[0]} vectors to faiss index")
    def save(self):
        faiss_path= os.path.join(self.persist_dir, "faiss.index")
        meta_path= os.path.join(self.persist_dir, "metadata.pkl")
        faiss.write_index(self.index, faiss_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        logging.info(f"saved the faiss index in the faiss.index file and the metadata in the metadata.pkl in the directory:{self.persist_dir}")
    def load(self):
        faiss_path= os.path.join(self.persist_dir, "faiss.index")
        meta_path= os.path.join(self.persist_dir, "metadata.pkl")
        self.index= faiss.read_index(faiss_path)
        with open(meta_path, "rb") as f:
            self.metadata= pickle.load(f)
        logging.info(f"loaded the faiss index and metadata from {self.persist_dir}")
    def search(self, query_embedding: np.ndarray, top_k:int=5):
        distances, indices= self.index.search(query_embedding, top_k)
        results=[]
        for index, distance in zip(indices[0], distances[0]):
            content= self.metadata[index] if index<len(self.metadata) else None
            results.append({"index": index, "distance": distance, "metadata": content})
        return results
    def query(self, query_text: str, top_k: int=5):
        logging.info(f"querying vector store for: '{query_text}'")
        query_emb=self.model.encode([query_text]).astype('float32')
        logging.debug(f"embedded the query, result of embedding: {query_emb}")
        return self.search(query_emb, top_k=top_k)

        