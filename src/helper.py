import os
import re
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from langchain_openai import ChatOpenAI
from langchain_classic.chains.summarize import load_summarize_chain

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from src.prompt import *

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen= ""
    for page in data:
     question_gen +=page.page_content
    
    #split data into chunks

    splitter_ques_gen = TokenTextSplitter(
    model_name = "gpt-4o-mini",
    chunk_size = 10000,
    chunk_overlap = 200
    )

    chunk_ques_gen = splitter_ques_gen.split_text(question_gen)
#print(type(chunk_ques_gen[0]))

#convert type of chunk_ques_gen items from list of strings to list of document represenation
    document_ques_gen = [Document(page_content = t) for t in chunk_ques_gen]

#print(type(document_ques_gen[0]))
    splitter_ans_gen = TokenTextSplitter(
    model_name = 'gpt-4o-mini',
    chunk_size = 1000,
    chunk_overlap = 100
    )

    document_answer_gen = splitter_ans_gen.split_documents(
        document_ques_gen
    )

    return document_ques_gen, document_answer_gen


def llm_pipeline(file_path):
    document_ques_gen, document_answer_gen = file_processing(file_path)
    #Define LLM

    llm_ques_gen_pipeline = ChatOpenAI(
    model = 'gpt-4o-mini',
    temperature=0.3
    )
    
    PROMPT_QUESTIONS =PromptTemplate(template=prompt_template, input_variables=['text'])

    REFINE_PROMPT_QUESTIONS =PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=refine_template
     )
    
    ques_gen_chain = load_summarize_chain(llm = llm_ques_gen_pipeline,
                                             chain_type = "refine",
                                             verbose = True,
                                             question_prompt=PROMPT_QUESTIONS,
                                             refine_prompt=REFINE_PROMPT_QUESTIONS)

    ques = ques_gen_chain.invoke({
      "input_documents": document_ques_gen
     })
    
    #create embedding model

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)
    llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")

    ques = ques["output_text"]

# Extract only numbered questions
    matches = re.findall(
        r"(?ms)^\s*(\d+)[.)]\s*(.*?)(?=^\s*\d+[.)]\s*|\Z)",
        ques
    )

    ques_list = [
    re.sub(r"\s+", " ", question).strip()
    for _, question in matches
    if question.strip()
    ]


    answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen,
                                                      chain_type = "stuff",
                                                      retriever = vector_store.as_retriever(search_kwargs={"k":3}))
    
    return answer_generation_chain, ques_list
    



