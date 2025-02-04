import streamlit as st
import os
import requests
import tempfile
import re
from PyPDF2 import PdfReader
from langchain_ollama import ChatOllama
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import torch
from difflib import SequenceMatcher

# -------------
# (1) Faster Whisper Model Setup
# -------------
# Check if CUDA is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "float16" if torch.cuda.is_available() else "int8"

# Initialize Faster Whisper
whisper_model = WhisperModel(
    model_size_or_path="base",
    device=DEVICE,
    compute_type=COMPUTE_TYPE,
    download_root=None
)

# -------------
# (2) TTS Setup
# -------------
from TTS.api import TTS
tts_engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# -------------
# (3) Enhanced Text Comparison
# -------------
def compare_words(original, spoken):
    """
    Compare words and return a list of tuples containing (word, is_correct)
    """
    original_words = original.lower().strip().split()
    spoken_words = spoken.lower().strip().split()
    
    results = []
    
    # Use dynamic programming to find the best alignment
    for i, orig_word in enumerate(original_words):
        best_match = None
        best_ratio = 0
        
        # Look for the best matching word in the spoken text
        for spoken_word in spoken_words:
            ratio = SequenceMatcher(None, orig_word, spoken_word).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = spoken_word
        
        # Consider it correct if similarity is above 0.8 (80%)
        is_correct = best_ratio > 0.8
        results.append((orig_word, is_correct))
    
    return results

def display_colored_text(word_results):
    """
    Display text with color-coding for correct/incorrect words
    """
    html_parts = []
    
    for word, is_correct in word_results:
        if is_correct:
            color = "green"
        else:
            color = "red"
        
        html_parts.append(f'<span style="color: {color};">{word}</span>')
    
    # Join with spaces and display as HTML
    html_text = " ".join(html_parts)
    st.markdown(f'<p style="font-size: 20px;">{html_text}</p>', unsafe_allow_html=True)

# -------------
# (4) PDF Processing
# -------------
def pdf_to_lines(pdf_file_path):
    lines = []
    try:
        with open(pdf_file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                page_lines = [l.strip() for l in text.split("\n") if l.strip()]
                lines.extend(page_lines)
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return []
    return lines

# -------------
# (5) LLM Integration
# -------------
def get_llm_response_with_context(question, context):
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.1,
    )
    
    prompt = f"""Context: {context}
    Question: {question}
    Please provide a briefly answer based on the given context."""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error getting LLM response: {e}"

# -------------
# (6) Audio Recording
# -------------
def record_audio(duration=5, sample_rate=16000):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate,
                       channels=1,
                       dtype=np.int16)
    sd.wait()
    
    temp_path = "temp_recording.wav"
    write(temp_path, sample_rate, audio_data)
    return temp_path

# -------------
# (7) Streamlit App
# -------------
def main():
    st.title("Enhanced Reading Assistant with PDF Input")
    
    # Sidebar settings
    with st.sidebar:
        st.subheader("Settings")
        recording_duration = st.slider("Recording Duration (seconds)", 3, 10, 5)
        confidence_threshold = st.slider("Speech Recognition Confidence", 0.0, 1.0, 0.7)

    # Upload PDF
    uploaded_pdf = st.file_uploader("Upload a PDF story", type=["pdf"])
    if not uploaded_pdf:
        st.info("Please upload a PDF to begin.")
        return

    # Process PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_pdf.read())
        pdf_path = tmp_file.name

    lines = pdf_to_lines(pdf_path)

    # Session state management
    if 'current_line_idx' not in st.session_state:
        st.session_state.current_line_idx = 0
    if 'word_results' not in st.session_state:
        st.session_state.word_results = None

    # Story navigation
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Restart Story"):
            st.session_state.current_line_idx = 0
            st.session_state.word_results = None
            st.rerun()  # Fixed from experimental_rerun

    # Display current line
    if st.session_state.current_line_idx < len(lines):
        current_line = lines[st.session_state.current_line_idx]
        st.subheader(f"Line {st.session_state.current_line_idx+1}/{len(lines)}")
        
        # Display colored text if we have results, otherwise display normal text
        if st.session_state.word_results:
            display_colored_text(st.session_state.word_results)
        else:
            st.write(current_line)
    else:
        st.success("You have finished reading the story!")
        st.stop()

    # Recording and transcription
    if st.button("Read This Line"):
        # Record audio
        audio_path = record_audio(duration=recording_duration)
        
        try:
            # Transcribe using Faster Whisper
            segments, info = whisper_model.transcribe(
                audio_path,
                beam_size=5,
                word_timestamps=True
            )
            
            # Get the transcription
            user_transcription = " ".join([segment.text for segment in segments])
            st.write(f"You said: {user_transcription}")
            
            # Compare and store results
            word_results = compare_words(current_line, user_transcription)
            st.session_state.word_results = word_results
            
            # Display colored text
            display_colored_text(word_results)
            
            # Calculate overall accuracy
            correct_words = sum(1 for _, is_correct in word_results if is_correct)
            total_words = len(word_results)
            accuracy = (correct_words / total_words) * 100 if total_words > 0 else 0
            
            # Provide feedback
            if accuracy >= 90:
                st.success(f"Excellent! {accuracy:.1f}% accurate! 🌟")
            elif accuracy >= 70:
                st.warning(f"Good effort! {accuracy:.1f}% accurate. Let's practice the red words. 📚")
            else:
                st.error(f"Keep practicing! {accuracy:.1f}% accurate. Listen to the correct pronunciation below. 🎯")
                
                # Provide audio of correct reading
                with st.spinner("Generating correct pronunciation..."):
                    audio_file_path = tts_engine.tts_to_file(
                        text=current_line,
                        file_path="correct_reading.wav"
                    )
                    st.audio("correct_reading.wav")
        
        except Exception as e:
            st.error(f"Error processing audio: {e}")
        
        finally:
            # Cleanup
            if os.path.exists(audio_path):
                os.remove(audio_path)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Line") and st.session_state.current_line_idx > 0:
            st.session_state.current_line_idx -= 1
            st.session_state.word_results = None
            st.rerun()  # Fixed from experimental_rerun
    with col2:
        if st.button("Next Line"):
            st.session_state.current_line_idx += 1
            st.session_state.word_results = None
            st.rerun()  # Fixed from experimental_rerun

    # Questions about the story
    st.subheader("Ask Questions")
    user_question = st.text_input("What would you like to know about the story?")
    
    if st.button("Ask") and user_question:
        story_context = "\n".join(lines)
        response = get_llm_response_with_context(user_question, story_context)
        st.write("Answer:", response)

if __name__ == "__main__":
    main()