%%writefile app.py

from torch import cuda
from huggingface_hub import login
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings import GPT4AllEmbeddings
from llama_index.embeddings import LangchainEmbedding

import tiktoken
from PyPDF2 import PdfReader
from transformers import AutoTokenizer
import transformers
import torch
from transformers import StoppingCriteria, StoppingCriteriaList
from langchain import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
import torch
import time
#personal additions
from slick import pingdm,pingd,internexists
from htmlTemplates import css, bot_template, user_template

err = "No errors"


# Joke
# try:
#     if internexists():
#         pass
#     else:
#         raise Exception('Whoopsie daisy') 
# except:
#     err = "Code's free trial has expired"
#     quit()
# else: 
#     name = "meta-llama/Llama-2-7b-chat-hf"
#     auth_token = "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"
#     openai_api_key="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"

name = "meta-llama/Llama-2-7b-chat-hf"
auth_token = "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"
openai_api_key="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"

##Small conviniences Codes
embc = {1: "OpenAi [#Paid Fastest]", 2: "Instructor [#Rank 1 Slow]", 3: "Minim [#Rank 4 Fast]", 4:"GPT4All [#Rank 3 Balanced]"}
embm = {1: "Llama 2 7b", 2: "Open Ai", 3: "Eleuther",4:"Flan T5",5:"Falcon"}


def format_func(option, data):
    return data.get(option, "Unknown")

class StopOnTokens(StoppingCriteria):
    def __init__(self, stop_ids):
        self.stop_ids = stop_ids

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_id in self.stop_ids:
            if torch.eq(input_ids[0][-len(stop_id):], stop_id).all():
                return True
        return False



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
        chunk_size=600,
        chunk_overlap=160,
        length_function =len
    )

    chunks = text_splitter.split_text(text)
    return chunks


def load_vectorstore(x,pdf_docs):
    global err
    err = "Reached Vector manager"

    if x==1:
        embeddings = OpenAIEmbeddings(openai_api_key)
        try:
            vectorstore = FAISS.load_local("emb/faiss_index ai", embeddings)
            err = "Open Ai : Save found"
        except:
            try:
                text_chunks = get_text_chunks(get_pdf_text(pdf_docs))
                vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
                vectorstore.save_local("emb/faiss_index ai")
            except:
                err = "This failed? Strange... Trace: load vectorstore if else"


    elif x==3 or x==2:
        # Create and dl embeddings instance  
        embeddings=LangchainEmbedding(HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
        try:
            vectorstore = FAISS.load_local("emb/faiss_index mi", embeddings)
            err = "Minim : Save found"
        except:
            try:
                text_chunks = get_text_chunks(get_pdf_text(pdf_docs))
                vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
                vectorstore.save_local("emb/faiss_index mi")
            except:
                err = "Bro how can you mess up twice?? Trace: load vectorstore if else"

    
    elif x==4:
        embeddings = GPT4AllEmbeddings()
        try:
            vectorstore = FAISS.load_local("emb/faiss_index g4", embeddings)
            err = "GPT4All : Save found"
        except:
            try:
                text_chunks = get_text_chunks(get_pdf_text(pdf_docs))
                vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
            except:
                err = "GPT4All Trace: load vectorstore if else"
        pass

    elif x==21:
        #Verbose disabled till i am done sorting the model directory
        st.text_area("Disabled till i am done sorting the program", height=50, disabled=True)
        
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        try:
            vectorstore = FAISS.load_local("emb/faiss_index hi", embeddings)
        except:
            err = "in progress"
    print("#####",err,"#####")
    print(type(vectorstore))
    return vectorstore



def initialize():
    tokenizer = AutoTokenizer.from_pretrained(name)
    stop_list = ['\nHuman:', '\n```\n']
    stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
    device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    print("Stopping Criteria")
    stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]
    stopping_criteria = StoppingCriteriaList([StopOnTokens(stop_token_ids)])
    print("Passed Criteria on to pipeline")

    pipeline = transformers.pipeline(
        task="text-generation", #task
        model=name,
        tokenizer=tokenizer,
        return_full_text=True,  # langchain expects the full text
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=0.2,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        repetition_penalty=1.1,  # without this output begins repeating
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        max_length=4000,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id
        )
    return pipeline


def get_conversation_chain(vectorstore,optm,pipeline=None):
    global err
    print("Reached LLM")
    err = "Reached LLM with the option",optm
    if pipeline==None:
        if optm == 2:
            llm = ChatOpenAI(openai_api_key)
            err = "The OpenAi route"

        elif optm == 4:
            llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
            err = "Loaded Flan T5 from HuggingFaceHub"
        
        elif optm == 5:
            
            pass

        else:
            err = "Llama not chosen"
            return err
        
    else:
        err = "Moving with LLama 🦙"
        llm = HuggingFacePipeline(pipeline = pipeline)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever()

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )

    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    login(token=auth_token)
    st.set_page_config(page_title = "Chat with books cuz you are lonely",page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "message" not in st.session_state:
        st.session_state.message = None


    st.header("Lets begin cuties :purple_heart:")
    user_question = st.text_input("Go on, ask me anything")
    if user_question:
        handle_userinput(user_question)

    
    init = st.empty()
    init.write(user_template.replace("{{MSG}}", "Waiting on you"), unsafe_allow_html=True)

    with st.sidebar:

        st.subheader("Choice of Embedding")
        opte = st.selectbox(label="Embeddings",placeholder="Choose?", options=list(embc.keys()), format_func=lambda x: format_func(x, embc))

        st.subheader("Choose your Model")
        optm = st.selectbox(label="Models",placeholder="Choose?", options=list(embm.keys()), format_func=lambda x: format_func(x, embm))

        st.subheader("We dont have all day")
        pdf_docs = st.file_uploader("Documents",accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing"):

                #Handle files and load vectorstore
                stt = time.time()
                vectorstore = load_vectorstore(opte,pdf_docs)
                ett=time.time()
                timex=ett-stt

                print("Successfully returned vectorizer")
                init.write(user_template.replace("{{MSG}}", str(err)), unsafe_allow_html=True)
                pingd(err,str(timex)[:5])
                
                if optm==1:
                    pipeline = initialize()
                    print("Pipeline initialized")
                    pingd("Pipeline initialized")

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore,optm,pipeline)
                print("Begin")
                init.write(user_template.replace("{{MSG}}","Ask me a Question ?"), unsafe_allow_html=True)



if __name__ == '__main__':
    main()


# st.error("Do you really, really, wanna do this?")
# if st.button("Yes I'm ready to rumble"):
#     run_expensive_function()