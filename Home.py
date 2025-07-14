import streamlit as st
from hr_policy_bot import generate
import uuid
import os
from supabase import create_client, Client
from datetime import datetime

url= os.environ.get("SUPABASE_URL")
key= os.environ.get("SUPABASE_KEY")
supabase= create_client(url, key)

def main_chat(uid=None, questions=None, answers=None, sources=None):

    st.title("askHR")
    st.write("*:grey[Your Digital HR Partner for Professional Support]*")
    
    #Generating session_id for each session

    if "session_id" not in st.session_state and uid==None:
        st.session_state.session_id = str(uuid.uuid4())

    elif (uid):
        st.session_state.session_id = uid
        st.session_state.messages = []
        st.session_state.sources = []
        for q in questions.data:
            st.session_state.messages.append({"role":"user", "content":q['question']})
            a = supabase.table("chat_history").select('answer').eq("question", q['question']).execute()
            st.session_state.messages.append({"role":"assistant", "content":a.data[0]['answer']})
            s = supabase.table("chat_history").select('sources').eq("question", q['question']).execute()
            st.session_state.sources.append({"role":"assistant", "content":s.data[0]['sources']})
    
    if "messages" not in st.session_state:
        st.session_state['messages'] = []
        with st.chat_message("assistant"):
            st.markdown(generate("What is the dress code")[2]) #using a dummy question to invoke the faq method

    if "sources" not in st.session_state:
        st.session_state['sources'] = []
     # Display chat messages from history on app rerun
    i = 1
    j = 0
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        i = i+1
        k = 0
        if i==3:
            for src in st.session_state.sources:
                if (k==j):
                    with st.expander("View sources"):
                        with st.expander("Chunk 1: "):
                            st.markdown(src['content'][0])
                        with st.expander("Chunk 2: "):
                            st.markdown(src['content'][1])
                        with st.expander("Chunk 3: "):
                            st.markdown(src['content'][2])
                        with st.expander("Chunk 4: "):
                            st.markdown(src['content'][3])
                    i = 1
                    j=j+1
                    break
                else:
                    k=k+1
                    continue
    
    if prompt := st.chat_input("Hi! How may I assist you today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.status('Finding sources...') as stat:
            response = generate(prompt)[0]
            stat.update(label = 'Generating response...')
            source = generate(prompt)[1]
            stat.update(label="Done.", state="complete")
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.expander("View sources"):
            with st.expander("Chunk 1: "):
                st.markdown(source[0])
            with st.expander("Chunk 2: "):
                st.markdown(source[1])
            with st.expander("Chunk 3: "):
                st.markdown(source[2])
            with st.expander("Chunk 4: "):
                st.markdown(source[3])
        st.session_state.sources.append({"role": "assistant", "content": source})

        data= supabase.table("chat_history").insert({"id":st.session_state.session_id, "created_at": str(datetime.now()), "question":prompt, "answer": response, "sources":source}).execute()

def create_chat(id):
    questions = supabase.table("chat_history").select("question").eq("id", id).execute()
    answers = supabase.table("chat_history").select("answer").eq("id", id).execute()
    sources = supabase.table("chat_history").select("sources").eq("id", id).execute()
    main_chat(uid=id, questions=questions, answers=answers, sources=sources)

def pick_uid():
    list = []
    data = supabase.table("chat_history").select("id").execute()
    for i in data.data:
        if i['id'] not in list:
            list.append(i['id'])
    return list

if __name__ == "__main__":
    st.logo("logo.png", size='large', icon_image=None)
    # st.sidebar.image("logo.png")
    st.set_page_config("HR Chat Bot", layout='wide' )

    st.markdown(
        """<style>
    div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
        
        height: 200px;
        margin-top: 30px;
        margin-left: -20px;
        padding-left: 0;
    }
    
    .st-emotion-cache-auzihx{
        height: 150px;
        margin-left: -20px;
        margin-top: 10px;
    }

    </style>
    """, unsafe_allow_html=True
    )

    un = pick_uid()
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    if 'uid' not in st.session_state:
        st.session_state.uid = ""

    for u in un:
        questions = supabase.table("chat_history").select("question").eq("id", u).execute()
        name = questions.data[0]['question']
        if st.sidebar.button(f"{name}", key=u, use_container_width=True):
            st.session_state.clicked = True
            st.session_state.uid = u

    if st.sidebar.button("New Chat", type="primary", use_container_width=True):
        st.session_state.clicked = False
        del st.session_state.messages
        del st.session_state.sources
        
    if st.session_state.clicked:
        create_chat(st.session_state.uid)
    else:
        main_chat()
