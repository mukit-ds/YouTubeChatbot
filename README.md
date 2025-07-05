# 🎥 Talk to Your YouTube Video

This Streamlit web app lets you **ask questions about the content of any YouTube video**, using its transcript as context. Leveraging **LangChain**, **FAISS**, and a Hugging Face-hosted **LLM**, it retrieves relevant transcript segments and generates accurate, context-aware answers.

---

## 🚀 Features

* 🔗 Accepts any valid **YouTube video URL**
* 🎙️ Automatically **fetches transcript** (English only)
* 🧠 Splits transcript into manageable chunks for semantic search
* 📚 Retrieves the most relevant parts using **FAISS vector store**
* 🤖 Answers questions using **Zephyr-7B** model via Hugging Face endpoint
* ⚠️ Avoids hallucination — replies *"I don't know."* when unsure

---

## 📦 Technologies Used

* [Streamlit](https://streamlit.io/)
* [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
* [LangChain](https://www.langchain.com/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Hugging Face Inference API](https://huggingface.co/inference-api)
* Model: [`HuggingFaceH4/zephyr-7b-beta`](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)
* Embeddings: `sentence-transformers/all-MiniLM-L6-v2`

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/talk-to-youtube-video.git
cd talk-to-youtube-video

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file or set the following environment variable:

```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

Or directly replace the API token in `app.py` (not recommended for production).

---

## ▶️ Running the App

```bash
streamlit run app.py
```

---

## 🧪 Example Usage

1. Paste a YouTube URL (e.g. `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Ask a question like:

   > What is the main topic of the video?
3. Click **"Get Answer"**
4. View AI-generated answer from the transcript.

---

## ⚠️ Limitations

* Only works with videos that have **English subtitles**
* Long videos may increase processing time
* Transcripts must be publicly accessible (no auto-generated captions for some)

---

## 📌 Future Improvements

* Multilingual transcript support
* Summarization and topic extraction
* Memory and chat history
* File download/export

---

## 🙏 Acknowledgements

* Hugging Face for open-source LLMs
* LangChain for seamless orchestration
* Streamlit for rapid UI prototyping

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
