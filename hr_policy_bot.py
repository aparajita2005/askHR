import os
from dotenv import load_dotenv, dotenv_values
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from docx import Document
import docx2txt


def read_docx(file_path):
    my_text = docx2txt.process(file_path)
    return (my_text)  

def generate(question):
    directory_path = "./hr_docs/"
    loader = DirectoryLoader(directory_path, glob="./*.docx", loader_cls=Docx2txtLoader)
    data = loader.load()

    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
    chunks = splitter.split_documents(data)
    vector_store = FAISS.from_documents(chunks, embeddings)

    llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens = None, timeout = None, api_key = st.secrets["OPENAI_API_KEY"])
    retriever = vector_store.as_retriever(search_kwargs={'k':4})
    qa_chain = ConversationalRetrievalChain.from_llm(llm = llm, retriever = retriever)

    def find_source(question):
        relevant_docs = vector_store.similarity_search(question, k = 4)
        src = []
        for i, doc in enumerate(relevant_docs):
            res = ""
            res = res + "\n" + f'{doc.page_content}' + "\n\n"
            res = res + "\n" + (f'Source: {doc.metadata['source'][8:len(doc.metadata['source'])-5]}') + "\n"
            src.append(res)
        return src

    chat_history = []
    #Giving a response
    response = qa_chain({'question':question, 'chat_history':chat_history})
    history = (response['question'], response['answer'])
    chat_history.append(history)
    return [response['answer'], find_source(question)]

# ques = "What is the dress code"
# print(generate(ques)[1])

print(read_docx("./hr_docs/Dress Code Policy.docx"))
