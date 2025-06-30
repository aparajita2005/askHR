import streamlit as st
from hr_policy_bot import generate
from PIL import Image


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
st.logo("logo.png", size='large', icon_image=None)
# st.sidebar.image("logo.png")
st.set_page_config("askHR", layout='wide' )

st.title("askHR")
st.write("*:grey[Your Digital HR Partner for Professional Support]*")


#with st.sidebar:
# st.page_link(page="Home.py", label="Home")
# st.page_link(page="pages/Anti-Sexual Harassment Policy.py", label = "Anti-Sexual Harrasment Policy")
# st.page_link(page="pages/Code of Conduct Policy.py", label = "Code of Conduct Policy")
# st.page_link(page="pages/Dress Code Policy.py", label = "Dress Code Policy")
# st.page_link(page="pages/Equal Employment Opportunity (EEO) & Non-Discrimination Policy.py", label = "Equal Employment Opportunity (EEO) & Non-Discrimination Policy")
# st.page_link(page="pages/Recruitment and selection policy.py", label = "Recruitment and selection policy")

if "messages" not in st.session_state:
    st.session_state['messages'] = []

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
