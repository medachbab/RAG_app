import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from src.data_loader import load_all_documents
import logging


class EmbeddingPipeline:
    def __init__(self, model_name: str="all-MiniLM-L6-v2", chunk_size: int=1000, chunk_overlap: int= 200):
        self.model_name=model_name
        self.model=None
        self._load_model()
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
    def _load_model(self):
        try:
            logging.debug(f"loading the embedding model:{self.model_name}")
            self.model=SentenceTransformer(self.model_name)
            logging.info(f"the model: {self.model_name} is loaded successfuly, embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            logging.error(f"error loading the model: {self.model_name}: {e}")
            raise
    def split_documents(self, documents: List[Any]) -> List[Any]:
        """
        this function, takes the list of documents
        and returns the resulting chunks documents using the "RecursiveCharacterTextSplitter" of langchain
        """
        text_splitter= RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        logging.debug(f"Splitting documents into chunks")
        split_docs=text_splitter.split_documents(documents)
        logging.info(f"splitted {len(documents)} into {len(split_docs)} chunks")
        return split_docs
    def embedding_chunks_texts(self, chunks: List[Any])->np.ndarray:
        """
        this function, takes the chunks to retrieve the list of the corresponding page_content to embed
        and returns the numpy array of embeddings with shape(len(texts), embedding_dimention(384 in this case))
        """
        if not self.model:
            raise ValueError("model not loaded")
        texts= [doc.page_content for doc in chunks]
        logging.debug(f"generating embeddings for {len(texts)} chunks")
        embeddings= self.model.encode(texts, show_progress_bar=True)
        logging.info(f"generated embeddings with shape: {embeddings.shape}")
        return embeddings