# Reading_Assistant
<h1 align="center">📖 Enhanced Reading Assistant with PDF & AI 🚀</h1>

<p align="center">
  <b>An AI-powered reading assistant that helps users read PDFs aloud, transcribe speech, provide pronunciation feedback, and answer questions using LLMs.</b>
</p>

<h2>📖 How It Works</h2>

<p>This <b>Enhanced Reading Assistant</b> processes a <b>PDF story</b> and guides users through an interactive reading experience, line by line.</p>

<ol>
  <li><b>Upload a PDF</b> – The system extracts text and splits it into lines for structured reading.</li>
  <li><b>Read Aloud & Get Feedback</b> – You read a line aloud, and <b>Whisper AI (Speech-to-Text)</b> transcribes your speech.</li>
  <li><b>Pronunciation Analysis</b> – Your spoken words are compared with the original text, and mistakes are highlighted in <b>color-coded feedback</b>.</li>
  <li><b>Text-to-Speech (TTS)</b> – The AI reads the correct pronunciation using <b>Tacotron2-DDC</b> if needed.</li>
  <li><b>Ask Questions</b> – Use the built-in <b>LLM (Llama3.2)</b> to get <b>context-aware answers</b> about the story.</li>
  <li><b>Navigate Easily</b> – Move between lines using <b>Next/Previous buttons</b> to track progress.</li>
</ol>

<p>This tool makes reading <b>interactive and engaging</b>, improving both <b>pronunciation and comprehension</b>! 🚀</p>


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
