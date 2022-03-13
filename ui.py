import streamlit as st
import json, datetime

# import shot frames and their timestamps
with open('timestamps.json', 'r') as f:
    frames = json.load(f)

# convert dictionary into list of tuples
frames = sorted(list(frames.items()))

# set page title
st.set_page_config(page_title='Video Shot Boundary Detection System')

# Create introduction
st.title('Video Shot Boundary Detection System')
st.write('Welcome to the Video Shot Boundary Detection System! Using the  \
          drop-down menu below, select \
          the shot you would like to view and click "View this shot\". The \
          app will then display the first frame of the selected shot on the \
          left, along with its frame number. On the right, you can view this \
          shot in the video by pressing the play button.')
st.write('NOTE: Due to Streamlit limitations, the video playback of the shot \
          may not start at the exact right place. This is because Streamlit \
          only accepts integers (i.e seconds) to adjust the starting position \
          of the video. Thus, the exact timestamp the shot starts will be \
          displayed along side the video to verify correctness. The timestamp \
          is displayed in Hours:Minutes:Seconds format.')

# Display shots to choose from
shots = ["Shot " + str(i) for i in range(1, 15, 1)]
option = st.selectbox("Select a shot to view", shots)

# Get the index of the chosen shot to pull out of frames list
option_idx = int(option[-2:]) - 1
checked = st.button("View this shot")

# set up columns for displaying results
left_col, right_col= st.columns(2)

with left_col:
    if checked:
        # Display the first frame of the shot
        st.subheader("First frame of the shot")
        st.image(image="frames/" + frames[option_idx][0], \
                caption="Frame " + frames[option_idx][0][:4],)

with right_col:
    if checked:
        # Display the video
        st.subheader("Video of the shot")
        video = open('soccer.mp4', 'rb')
        video_bytes = video.read()
        st.video('https://youtu.be/THb4_DKkzlU', start_time=round(frames[option_idx][1]))
        st.caption("The shot actually starts at " + \
                   str(datetime.timedelta(seconds=frames[option_idx][1])))  