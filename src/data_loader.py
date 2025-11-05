import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader, JSONLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from pathlib import Path
from typing import List, Any
import logging
def load_all_documents(data_dir: str)-> List[Any]:
    """
    this function load all PDF/TXT/CSV/Excel/word/Json files in the data directory and convert them to document datastructure
    """
    
    data_path=Path(data_dir).resolve()
    logging.debug(f"data path: {data_path}")
    all_documents = []

    #pdf files: 
    pdf_files = list(data_path.glob("**/*.pdf"))
    logging.info(f"number of pdf files found: {len(pdf_files)} \npdf files: {[str(f) for f in pdf_files]}")
    for pdf_file in pdf_files:
        logging.debug(f"loading pdf:{pdf_file.name}")
        try:
            loader=PyPDFLoader(str(pdf_file))
            documents=loader.load()

            #adding source info to metadata:
            for document in documents:
                document.metadata['source_file'] = pdf_file.name
                document.metadata['file_type']='pdf'

            all_documents.extend(documents)
            logging.info(f"loaded {len(documents)} pages")
        except Exception as e:
            logging.error(f"error loading pdf files:{e}")
    logging.info(f"Total of loaded documents:{len(documents)}")

    #txt files: 
    txt_files = list(data_path.glob("**/*.txt"))
    logging.info(f"number of txt files found: {len(txt_files)} files")
    for txt_file in txt_files:
        logging.debug(f"loading the txt file:{txt_file.name}")
        try:
            loader=TextLoader(str(txt_file))
            documents=loader.load()

            #adding source info to metadata:
            for document in documents:
                document.metadata['source_file'] = txt_file.name
                document.metadata['file_type']='txt'

            all_documents.extend(documents)
            logging.info(f"loaded {len(documents)} pages")
        except Exception as e:
            logging.error(f"error loading text files:{e}")
    logging.info(f"Total of loaded documents:{len(documents)}")

    #CSV files:
    csv_files = list(data_path.glob("**/*.csv"))
    print(f"number of csv files found: {len(csv_files)} files")
    for csv_file in csv_files:
        print(f"processing the file:{csv_file.name}")
        try:
            loader=CSVLoader(str(csv_file))
            documents=loader.load()

            #adding source info to metadata:
            for document in documents:
                document.metadata['source_file'] = csv_file.name
                document.metadata['file_type']='csv'

            all_documents.extend(documents)
            print(f"loaded {len(documents)} pages")
        except Exception as e:
            print(f"error loading csv files:{e}")
    print(f"Total of loaded documents:{len(documents)}")
    
    #excel files:
    xls_files = list(data_path.glob("**/*.xls")) + list(data_path.glob("**/*.xlsx"))
    print(f"number of excel files found: {len(xls_files)} files")
    for xls_file in xls_files:
        print(f"processing the file:{xls_file.name}")
        try:
            loader=UnstructuredExcelLoader(str(xls_file))
            documents=loader.load()

            #adding source info to metadata:
            for document in documents:
                document.metadata['source_file'] = xls_file.name
                document.metadata['file_type']='xls/xlsx'

            all_documents.extend(documents)
            print(f"loaded {len(documents)} pages")
        except Exception as e:
            print(f"error loading xls/xlsx files:{e}")
    print(f"Total of loaded documents:{len(documents)}")

    #word files:

    return all_documents

