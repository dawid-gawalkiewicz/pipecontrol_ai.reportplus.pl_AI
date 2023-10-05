import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

load_dotenv()  # load your env file

st.set_page_config(page_title="Report+ PDF AI Chatbot",
                   page_icon=":robot_face:")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "conversation" not in st.session_state:
    st.session_state.conversation = None

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def add_message_to_chat(message, is_user):
    template = user_template if is_user else bot_template
    st.write(template.replace("{{MSG}}", message), unsafe_allow_html=True)

def handle_userinput(user_question):
    if st.session_state.conversation:
        add_message_to_chat(user_question, is_user=True)
        
        response = st.session_state.conversation({'question': user_question})
        bot_reply = response['chat_history'][-1].content
        add_message_to_chat(bot_reply, is_user=False)

        # Update session state chat history
        st.session_state.chat_history.extend([user_question, bot_reply])
    else:
        st.warning("Proszę najpierw wgrać plik/pliki PDF.")

def main():
    # Inject CSS
    st.write(css, unsafe_allow_html=True)

    # 1. "Czatuj z plikami PDF" at the top
    st.header("Czatuj z plikami PDF :books:")

    # Sidebar for uploading PDFs
    with st.sidebar:
        st.subheader("Twoje dokumenty")
        pdf_docs = st.file_uploader(
            "Prześlij tutaj swoje pliki PDF i kliknij „Przetwarzaj”", accept_multiple_files=True)
        if st.button("Przetwarzaj"):
            with st.spinner("Przetwarzanie dokumentów..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success("Twoje pliki PDF zostały pomyślnie przetworzone!")

    # 2. Render the chat window (messages) in the middle
    for index, message in enumerate(st.session_state.chat_history):
        add_message_to_chat(message, index % 2 == 0)

    # 3. "Zadaj pytanie" and the input at the bottom
    # Before rendering the input box:
    st.markdown('<div style="position: relative;">', unsafe_allow_html=True)

    user_question = st.text_input("Zadaj pytanie dotyczące Twoich dokumentów:")

    if user_question and user_question not in st.session_state.chat_history:
        handle_userinput(user_question)

    # Close the div after the input box:
    st.markdown('</div>', unsafe_allow_html=True)
        
if __name__ == '__main__':
    main()
