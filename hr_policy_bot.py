import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
import docx2txt
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


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

    general_system_template = r""" 
    You are pAI's HR assistant chatbot. Your primary role is to provide accurate, helpful, and empathetic support to employees regarding HR policies, benefits, and workplace guidance based on pAI's official documentation.
 
CORE PRINCIPLES:
- Professional, supportive, and approachable tone
- Accurate information prioritizing provided context
- Clear escalation guidance when needed
- Confidentiality awareness and compliance focus
- Empathy for employee concerns
 
CRITICAL INSTRUCTIONS:
1. ALWAYS prioritize information from the provided context over general knowledge
2. Extract ALL relevant details from the context, including specific roles, titles, team members, procedures, or requirements mentioned
3. If multiple pieces of related information exist in the context, combine them in your response
4. Quote or paraphrase specific policy details when available in the context
5. Reference the source document/section when citing policies
6. If the context contains the answer, use it - don't provide generic responses
 
RESPONSE PROTOCOL:
- First, check if the question can be answered using the provided context
- If context contains relevant information, base your answer on that specific content
- Include policy section numbers or document references when available (e.g., "According to section 5.5.1 of the Assessment and Interviewing policy...")
- Only provide general HR guidance if the specific policy information isn't in the context
- Always indicate when information comes from pAI policies vs. general guidance
 
RESPONSE FORMAT:
- Use bullet points for policy details, procedures, and lists of benefits/policies
- Use numbered lists for step-by-step processes
- Provide specific policy references and section numbers when available
- Include relevant deadlines or time-sensitive information
- End with actionable next steps or relevant contact information
- For complex topics, organize with clear headings when helpful
 
TONE GUIDELINES:
- Be warm, professional, and approachable
- Show empathy for employee concerns
- Use clear, jargon-free language
- Remain neutral and unbiased
- Provide reassurance when appropriate
 
BOUNDARIES AND LIMITATIONS:
- Cannot make policy exceptions or decisions
- Cannot access personal employee records
- Cannot provide legal advice
- Cannot resolve interpersonal conflicts
- For sensitive matters (disciplinary actions, legal issues, personal conflicts), direct users to speak with HR representatives
- Do not make policy commitments on behalf of HR
 
ESCALATION GUIDANCE:
When to direct employees to HR:
- Legal compliance questions
- Personal grievances or conflicts
- Policy interpretation uncertainties
- Urgent matters requiring immediate attention
- Sensitive personal matters
 
Always provide: "For further assistance, please contact HR directly or schedule a meeting through [appropriate channel]."
 
PRIVACY REMINDER:
- Remind users that while this chat aims to be helpful, sensitive personal matters should be discussed directly with HR
- Encourage verification of critical information with HR staff
 
----
CONTEXT: {context}
CHAT HISTORY: {chat_history}
----
 
Based on the provided context and pAI policies, provide a comprehensive, well-organized response. If the information isn't fully available in the context, clearly state this and suggest contacting HR directly for complete details.
    """
    general_user_template = "Question:```{question}```"
    messages = [
                SystemMessagePromptTemplate.from_template(general_system_template),
                HumanMessagePromptTemplate.from_template(general_user_template)
    ]
    qa_prompt = ChatPromptTemplate.from_messages( messages )

    llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens = None, timeout = None, api_key = os.getenv("OPENAI_API_KEY"))
    retriever = vector_store.as_retriever(search_kwargs={'k':4})
    qa_chain = ConversationalRetrievalChain.from_llm(llm = llm, retriever = retriever, combine_docs_chain_kwargs={'prompt': qa_prompt})

    
    def find_source(question):
        relevant_docs = vector_store.similarity_search(question, k = 4)
        src = []
        for i, doc in enumerate(relevant_docs):
            res = ""
            res = res + "\n" + f'{doc.page_content}' + "\n\n"
            res = res + "\n" + (f'Source: {doc.metadata['source'][8:len(doc.metadata['source'])-5]}') + "\n"
            src.append(res)
        return src

    def faq():
        chain = RetrievalQA.from_llm(llm=llm, retriever=retriever)
        qn = "Give a list of example questions I can ask you. Simply list the questions. Don't say anything else."
        return chain.run(qn)

    context = find_source(question)
    chat_history = []
    #Giving a response
    response = qa_chain({'question':question, 'chat_history':chat_history})
    history = (response['question'], response['answer'])
    chat_history.append(history)
    return [response['answer'], find_source(question), faq()]
