import os
import streamlit as st
from dotenv import load_dotenv
from pytube import YouTube
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

prompt = """You are a Youtube Video Summarizer. You will be given transcript of the video which 
you need to summrize providing important information in points. Give out the response in around 
300 words taking in account below points : 

1. Give a proper subject line to the video transcript.

2. List all the technologies and tools used in the video.

3. Provide summary of the transcript point wise in detail and cover.

4. provide proper explaination as per the information provided in the transcript.

5. In the end provide simple 2-3 line short summary of whole video transcript as conclusion.

The transcript will be provided here : """

def get_video_id(video_url):
    yt = YouTube(video_url)
    video_id = yt.video_id
    return video_id

def get_transcript(video_id):

    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages = ['en'])    #can give list of video ids if want to fetch youtube transcript from multiple videos
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

st.set_page_config("Youtube Video Summarizer")
st.title("Youtube Video Summarizer ✍🏼📋")

input = st.text_input("Enter your video url here!")
if input:
    video_id = get_video_id(input)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg")

if st.button("Get Summary"):
    st.markdown("## :green[Summary]")
    transcript = get_transcript(video_id)
    response = gemini_content_generation(transcript, prompt)
    st.write(response)


