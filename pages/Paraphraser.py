import streamlit as st
import cohere
from streamlit_lottie import st_lottie
import requests

# Initialize Cohere API (replace with your actual API key)
cohere_api_key = 'your_cohere_api_key'  # Replace with your actual Cohere API key
co = cohere.Client(cohere_api_key)

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations for visual effects
lottie_paraphrase = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_p2i5ryrf.json")  # Loading animation
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_j7b7lgtu.json")  # Success animation

# Streamlit app UI
st.title("✍️ Text Paraphraser")
st.write("Enter the text you'd like to paraphrase:")

# Display loading animation
if lottie_paraphrase:
    st_lottie(lottie_paraphrase, height=150, key="loading_animation")

# Text input from the user
user_input = st.text_area("Input Text", height=300)

# Button to perform paraphrasing
if st.button("🔄 Paraphrase"):
    if user_input:
        # Display loading spinner while processing
        with st.spinner("Generating paraphrased text..."):
            try:
                # Call the Cohere API to paraphrase the text
                response = co.generate(
                    model='command-xlarge-nightly',
                    prompt=f"Paraphrase the following text:\n\n{user_input}",
                    max_tokens=200,  # Limits the paraphrased text length
                    temperature=0.7,  # Adjusts creativity
                    k=0,              # No specific sampling limit
                    stop_sequences=[]  # Ensures no stop sequences are enforced
                )

                # Extract the paraphrased text from the response
                paraphrased_text = response.generations[0].text.strip()

                # Display the paraphrased text
                st.subheader("✅ Paraphrased Text:")
                st.write(paraphrased_text)

                # Display success animation
                if lottie_success:
                    st_lottie(lottie_success, height=150, key="success_animation")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter some text to paraphrase.")

# Sidebar with instructions
st.sidebar.title("Instructions 📖")
st.sidebar.info(
    "1. **Input Text**: Type or paste the text you want to paraphrase in the main text area.\n"
    "2. **Paraphrase**: Click the 'Paraphrase' button to generate a paraphrased version.\n"
    "3. **View Results**: See the paraphrased text displayed below the input area."
)
