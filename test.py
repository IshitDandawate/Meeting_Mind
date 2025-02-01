import tempfile
import os
import streamlit as st
import whisper  # For transcription
import google.generativeai as genai  # For Gemini API

# Load Whisper model (loaded only once)
model = whisper.load_model("tiny")

# Transcribe audio file
def transcribe_audio(audio_file):
    if audio_file is None:
        return "No file uploaded."

    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp_file:  # delete=True is cleaner
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name

        result = model.transcribe(tmp_file_path, fp16=True, best_of=1)
    return result["text"]  # Return the transcribed text


# Initialize Gemini API (using secrets)
def initialize_gemini():
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-pro')

# Query Gemini API (improved error handling)
def query_gemini(model, transcript, query):
    try:
        prompt = f"The following is a transcript of a meeting:\n\n{transcript}\n\nQuestion: {query}\n\nAnswer:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while querying Gemini: {e}")
        return ""  # Return empty string to avoid potential issues


# Set up Streamlit app
st.title("Meeting Mind")

# Tabs
tabs = ["Upload", "Transcript", "chatBot"]
selected_tab = st.sidebar.radio("Select a Tab", tabs)

if selected_tab == "Upload":
    st.header("Upload Audio/Video")
    uploaded_file = st.file_uploader("Choose an audio/video file", type=["mp3", "mp4", "wav", "webm"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(uploaded_file)
                st.session_state.transcript = transcript  # Store in session state
                st.success("Successfully Transcribed")

elif selected_tab == "Transcript":
    st.header("Transcript")
    if "transcript" in st.session_state:
        transcript = st.session_state.transcript
        st.text_area("Transcript (Editable)", value=transcript, height=300)

        st.download_button(
            label="Download Transcript",
            data=transcript.encode("utf-8"),
            file_name="transcript.txt",
            mime="text/plain",
        )
    else:
        st.info("Please upload and transcribe an audio/video file first.")

elif selected_tab == "chatBot":
    st.header("Meeting Minutes")
    if "transcript" in st.session_state:
        transcript = st.session_state.transcript

        gemini_model = initialize_gemini()  # Initialize Gemini (using secrets)

        query = st.text_input("Enter your query about the transcript:")

        if query:
            with st.spinner("Generating response..."):
                response = query_gemini(gemini_model, transcript, query)
                if response:
                    st.text_area("ChatBot Response", value=response, height=150)
    else:
        st.info("Please upload and transcribe an audio/video file first.")
