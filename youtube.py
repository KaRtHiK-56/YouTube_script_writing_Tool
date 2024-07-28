import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.chains import LLMChain 
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')

st.title("Youtube Videos and Shorts Script Writing Tool 📽️▶️")
topic = st.text_area("Please enter the topic for which you want to rite script for:")
time = st.text_area("Please enter time in minutes on how long the script should be:")
creativity = st.slider('Creativity limit ✨ - 0 --> Low || 1 --> High', 0.0, 1.0, 0.2,step=0.1)



def script(topic,time,creativity):
    print("*"*60)
    print("inside function")

    searcher = GoogleSerperAPIWrapper()
    
    topic_prompter =  """ Please come up with a title for a YouTube video on the {topic} """
    
    script_prompter = """ Create a script for a YouTube video based on this title for me. TITLE: {topic} of duration: {time} minutes using this search data {search} """

    topic_prompt = PromptTemplate(input_variables=['topic'],template=topic_prompter)

    script_prompt = PromptTemplate(input_variables=['topic','time','search'],template=script_prompter)

    
    llm = Ollama(model='llama3',temperature = creativity)

    topic_chain = LLMChain(llm=llm, prompt=topic_prompt, verbose=True)
    script_chain = LLMChain(llm=llm, prompt=script_prompt, verbose=True)

    final_topic = topic_chain.invoke(topic)

    search_result = searcher.run(topic) 

    final_script = script_chain.run(topic=topic,search=search_result,time=time)
    print("*"*60)
    print("results are generated")

    print("*"*60)
    print("Title",final_topic)

    print("*"*60)
    print("Script",final_script)

    return final_topic,final_script


sumbit = st.button("Generate Script")

if sumbit:
    with st.spinner("Generating...."):
        print("*"*60)
        print(topic,time,creativity)

        topic,script = script(topic,time,creativity)

        st.subheader("Title:🔥")
        st.write(topic)

        st.subheader("Your Video Script:📝")
        st.write(script)
