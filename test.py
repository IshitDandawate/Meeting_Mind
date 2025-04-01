import tempfile
import os
import streamlit as st
import whisper  # For transcription
import google.generativeai as genai  # For Gemini API

# Load Whisper model
def load_whisper_model():
    return whisper.load_model("tiny")

model = load_whisper_model()

# Transcribe audio file
def transcribe_audio(audio_file):
    if audio_file is None:
        return "No file uploaded."

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())  # Write uploaded file data
        tmp_file_path = tmp_file.name  # Get the temporary file path

    # Transcribe the audio file
    result = model.transcribe(tmp_file_path, fp16=True,best_of=1)

    # Clean up temporary file
    os.remove(tmp_file_path)

    return result["text"]

# Initialize Gemini API
def initialize_gemini():
    # Embed your Gemini API key here
    gemini_api_key = "AIzaSyAXeXcppJ_b1MIq4yDjBKJh7iC4J7N0f2o"  # Replace with your actual Gemini API key
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-1.5-pro')

# Query Gemini API
def query_gemini(model, transcript, query):
    try:
        # Combine the transcript and query for context
        prompt = f"The following is a transcript of a meeting:\n\n{transcript}\n\nQuestion: {query}\n\nAnswer:"
        
        # Generate a response using Gemini
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while querying Gemini: {e}")
        return None

# Set up Streamlit app
st.title("Meeting Mind")

# Tabs
tabs = ["Upload", "Transcript", "chatBot"]
selected_tab = st.sidebar.radio("Select a Tab", tabs)  # Sidebar for tab selection

if selected_tab == "Upload":
    st.header("Upload Audio/Video")
    uploaded_file = st.file_uploader("Choose an audio/video file", type=["mp3", "mp4", "wav", "webm"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcript = transcribe_audio(uploaded_file)
                st.session_state.transcript = transcript  # Store transcript in session state
                st.success("Successfully Transcribed")

elif selected_tab == "Transcript":
    st.header("Transcript")
    if "transcript" in st.session_state:  # Check if transcript exists
        transcript = st.session_state.transcript  # Define transcript variable here
        st.text_area("Transcript (Editable)", value=transcript, height=300)  # Make the transcript editable.

        # Add a download button for the transcript
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

        # Initialize Gemini model
        gemini_model = initialize_gemini()

        # Input for user query
        query = st.text_input("Enter your query about the transcript:")

        if query:
            # Query Gemini API
            with st.spinner("Generating response..."):
                response = query_gemini(gemini_model, transcript, query)
                if response:
                    st.text_area("ChatBot Response", value=response, height=150)

    else:
        st.info("Please upload and transcribe an audio/video file first.")
