# Reading_Assistant
<h1 align="center">📖 Enhanced Reading Assistant with PDF & AI 🚀</h1>

<p align="center">
  <b>An AI-powered reading assistant that helps users read PDFs aloud, transcribe speech, provide pronunciation feedback, and answer questions using LLMs.</b>
</p>

## 🌟 Features  
<ul>
  <li>📜 <b>PDF Text Extraction</b>: Processes and extracts text from uploaded PDF documents.</li>
  <li>🎤 <b>Speech-to-Text (Faster Whisper)</b>: Converts spoken words into text using Whisper AI.</li>
  <li>🗣️ <b>Text-to-Speech (TTS)</b>: Reads the text aloud using Tacotron2-DDC.</li>
  <li>✅ <b>Pronunciation Accuracy</b>: Compares spoken words with the original text and provides color-coded feedback.</li>
  <li>💡 <b>LLM-Powered Q&A</b>: Uses Llama3.2 to answer questions about the story context.</li>
  <li>🔁 <b>Navigation System</b>: Move between PDF lines and track progress.</li>
</ul>

## 🛠️ Tech Stack  
<ul>
  <li>🔹 <b>Python</b></li>
  <li>🔹 <b>Streamlit</b> - Web UI</li>
  <li>🔹 <b>Faster Whisper</b> - Speech-to-Text</li>
  <li>🔹 <b>TTS (Tacotron2-DDC)</b> - Text-to-Speech</li>
  <li>🔹 <b>LangChain</b> & <b>FAISS</b> - Context Handling</li>
  <li>🔹 <b>Ollama (Llama3.2)</b> - Large Language Model</li>
  <li>🔹 <b>PyPDF2</b> - PDF Processing</li>
</ul>

## 🚀 Installation & Setup  
```bash
# Clone the repository
git clone https://github.com/aqib1123/your-repo.git
cd your-repo

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
