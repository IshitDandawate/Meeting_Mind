# Meeting_Mind
Summarizes meetings (Speech to text)

# Overview

Meeting Mind is a Python-based application that summarizes meetings by generating a transcript from an uploaded .mp3 file. It provides a .txt file download option for users and allows querying the generated transcript to extract relevant information efficiently.

# Features

Upload MP3 Files: Users can upload an .mp3 file containing the meeting audio.

Automatic Transcription: The application processes the audio file and converts speech to text.

Downloadable Transcript: Users can download the full transcript as a .txt file.

Query the Transcript: Users can ask questions based on the transcript to extract specific information.

# Technologies Used 

Python: Core programming language for processing

Speech Recognition (Whisper/Google Speech-to-Text): Converts speech to text

Flask/FastAPI: Backend framework for handling requests

NLTK/OpenAI API: Enables querying and text processing

FFmpeg: Processes audio files for better recognition
