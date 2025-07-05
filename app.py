import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import re


@st.cache_resource(show_spinner=False)
def load_model():
    llm = HuggingFaceEndpoint(
        repo_id='HuggingFaceH4/zephyr-7b-beta',
        task='text-generation',
        huggingfacehub_api_token="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"
    )
    return ChatHuggingFace(llm=llm)

model = load_model()

# Function to extract video id from YouTube URL
def extract_video_id(url):
    # Handles multiple YouTube URL formats
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Main app UI
st.title("Talk to Your YouTube Video")

youtube_url = st.text_input("Enter YouTube Video URL:")
question = st.text_input("Enter your question about the video:")

if st.button("Get Answer"):

    if not youtube_url or not question:
        st.warning("Please provide both a YouTube video URL and a question.")
    else:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
        else:
            with st.spinner("Fetching transcript and processing..."):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    transcript = ' '.join(chunk['text'] for chunk in transcript_list)
                except TranscriptsDisabled:
                    st.error("No captions available for this video.")
                    transcript = ""

                if transcript:
                    # Split transcript into chunks
                    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                    chunks = splitter.create_documents([transcript])

                    # Generate embeddings
                    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

                    # Create FAISS vector store
                    vector_store = FAISS.from_documents(chunks, embeddings)
                    retriever = vector_store.as_retriever(search_kwargs={'k': 5})

                    prompt = PromptTemplate.from_template("""
                    <|system|> You are a helpful assistant. Use only the transcript context provided.
                    If unsure, respond with "I don't know." Avoid guessing.

                    <|user|>
                    Context:
                    {context}

                    Question:
                    {question}

                    <|assistant|>
                    """)

                    # Retrieve relevant chunks
                    retrieved_docs = retriever.invoke(question)
                    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
                    final_prompt = prompt.invoke({"context": context_text, "question": question})
                    answer = model.invoke(final_prompt)

                    st.subheader("Answer:")
                    st.write(answer.content)



                else:
                    st.error("Transcript could not be processed.")
