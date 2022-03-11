import streamlit as st
import boundary_detection as bd

# ffmpeg -i soccer.avi -vcodec libx264 -acodec aac soccer.mp4



video = open('soccer.mp4', 'rb')
bytes = video.read()

st.video(bytes, start_time=int(34.355643))