import os
import streamlit as st
from dotenv import load_dotenv
from pytube import YouTube
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

prompt = """You are a Youtube Video Summarizer. You will be given transcript of the video which 
you need to summarize providing important information in points. Give out the response in around 
300 words taking in account below points : 

1. Give a proper subject line to the video transcript.

2. List all the main important topics covered in the video.

3. Provide summary of the transcript point wise in detail and cover.

4. provide proper explaination as per the information provided in the transcript.

5. In the end provide simple 2-3 line short summary of whole video transcript.

The transcript will be provided here : """


def get_video_id(video_url):
    yt = YouTube(video_url)
    video_id = yt.video_id
    return video_id

def get_transcript(video_id):

    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages = ['en', 'hi', 'gu', 'mr'])    #can give list of video ids if want to fetch youtube transcript from multiple videos
    #with st.expander("transcript"):
        #st.write(transcript_data)
    transcript = ""
    for i in transcript_data:
        transcript = transcript +  " " + i['text']
    return str(transcript)

def gemini_content_generation(video_transcript, prompt):

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + video_transcript)
    return response.text

def gemini_question_answering(video_transcript, prompt1):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt1 + video_transcript)
    return response.text

st.set_page_config("Youtube Video Summarizer")
st.title("Youtube Video Summarizer ✍🏼📋")

st.sidebar.title("Interact with YouTube Video 😎")

option = st.sidebar.selectbox(
    "Choose an option:",
    ["Get YouTube Video Summary", "Talk to YouTube Video"]
)

input = st.text_input("Enter youtube video url here!")
if input:
    video_id = get_video_id(input)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg")

    if option == "Get YouTube Video Summary":
        if st.button("Get Summary"):    
            transcript = get_transcript(video_id)
            response = gemini_content_generation(transcript, prompt)
            st.write(response)

    if option == "Talk to YouTube Video":
            question = st.text_input("Ask question related to youtube video...")
            prompt1 = f"""You are a Youtube Video Question Answering Agent. Based on the transcript of the video you will provide answer to the user question {question}. if the answer is present in youtube video then
            only provide answer else say 'answer was not found in context'.
            """

            if question:
                transcript = get_transcript(video_id)
                response = gemini_question_answering(transcript, prompt1)
                st.write(response)