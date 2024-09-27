import streamlit as st
import cohere
from streamlit_lottie import st_lottie
import requests as req

# Load Lottie animations
def load_lottieurl(url: str):
    r = req.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animation for visual effect
lottie_loading = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_UxDkZW.json")  # Loading animation

# Initialize Cohere API (replace with your actual API key)
cohere_api_key = 'your_cohere_api_key'  # Replace with your Cohere API key
co = cohere.Client(cohere_api_key)

# Streamlit app UI
st.title("📝 Text Summarizer")
st.write("Enter the text you'd like to summarize:")

# Text input from the user
user_input = st.text_area("Input Text", height=300)

# Button to perform summarization
if st.button("🔍 Summarize"):
    if user_input:
        with st.spinner("Summarizing..."):
            if lottie_loading:
                st_lottie(lottie_loading, height=150, key="loading_animation")
            # Call the Cohere summarize API
            try:
                response = co.summarize(
                    text=user_input,
                    length='medium',  # Can also be 'short' or 'long'
                    format='paragraph',  # Can also be 'bullet'
                    model='command-r-plus-08-2024',  # Using the largest summarization model
                    temperature=0.5  # Controls the "creativity" of the output
                )

                # Extract the summary from the response
                summary = response.summary
                
                # Display the summary
                st.subheader("🗒️ Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter some text to summarize.")

# Sidebar with instructions
st.sidebar.title("Instructions 📖")
st.sidebar.info(
    "This tool summarizes text using Cohere's summarization model. \n\n"
    "1. **Input Text**: Paste the text you want to summarize in the text area.\n"
    "2. **Click 'Summarize'**: Press the 'Summarize' button to generate a summary.\n"
    "3. **View Summary**: Check the summary displayed below."
)
