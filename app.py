import streamlit as st
import tempfile, os
from PIL import Image
from gtts import gTTS
from moviepy.editor import *

st.set_page_config(page_title="AI Image-to-Video Generator", layout="centered")
st.title("🖼️ AI Image-to-Video with Voiceover & Animation")

uploaded = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
motion = st.text_input("Describe motion (e.g., 'zoom in slowly', 'eyes blink')")
voice = st.text_area("Enter voiceover text")
music = st.file_uploader("Upload background music (optional)", type=["mp3"])

if st.button("Generate Video"):
    if not (uploaded and voice):
        st.warning("Please upload an image and enter voiceover text.")
    else:
        st.spinner("Processing...")
        tmp = tempfile.mkdtemp()
        img_path = os.path.join(tmp, "image.png")
        with open(img_path, "wb") as f: f.write(uploaded.read())

        video_clip = ImageClip(img_path).set_duration(12).resize(width=720)

        tts = gTTS(voice); tts_path = os.path.join(tmp,"voice.mp3"); tts.save(tts_path)
        audio_clips = [AudioFileClip(tts_path)]

        if music:
            mpath = os.path.join(tmp, "music.mp3")
            with open(mpath, "wb") as f: f.write(music.read())
            audio_clips.append(AudioFileClip(mpath).volumex(0.3))

        final_audio = CompositeAudioClip(audio_clips)
        video_clip = video_clip.set_audio(final_audio)

        out = os.path.join(tmp, "out.mp4")
        video_clip.write_videofile(out, fps=24)
        st.video(out)
        with open(out,"rb") as f:
            st.download_button("Download Video", f, file_name="ai_video.mp4")
