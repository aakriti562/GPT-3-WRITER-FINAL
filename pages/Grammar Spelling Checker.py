import streamlit as st
import cohere
from difflib import SequenceMatcher
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

# Load Lottie animations
lottie_intro = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_pqqv4u2e.json")  # Typing animation
lottie_correct = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_v6z72gux.json")  # Correcting animation

# Function to compare original and corrected text and highlight differences
def highlight_differences(original, corrected):
    original_words = original.split()
    corrected_words = corrected.split()
    
    # Using SequenceMatcher to find differences
    s = SequenceMatcher(None, original_words, corrected_words)
    highlighted_text = ""

    for opcode, i1, i2, j1, j2 in s.get_opcodes():
        if opcode == 'equal':  # Words that are the same (green)
            highlighted_text += ' '.join([f'<span style="color:green">{word}</span>' for word in original_words[i1:i2]]) + ' '
        elif opcode in ('replace', 'insert'):  # Words that are replaced or inserted (red)
            highlighted_text += ' '.join([f'<span style="color:red; font-weight:bold">{word}</span>' for word in corrected_words[j1:j2]]) + ' '
        elif opcode == 'delete':  # Words deleted from original text (red)
            highlighted_text += ' '.join([f'<span style="color:red; text-decoration: line-through;">{word}</span>' for word in original_words[i1:i2]]) + ' '

    return highlighted_text

# Streamlit app UI
st.title("📝 Grammar and Spelling Checker")
st.write("Enter the text you'd like to check for grammar and spelling mistakes:")

# Display intro animation
if lottie_intro:
    st_lottie(lottie_intro, height=150, key="intro_animation")

# Text input from the user
user_input = st.text_area("Input Text", height=300)

# Button to perform grammar and spelling check
if st.button("🔍 Check Grammar and Spelling"):
    if user_input:
        # Display loading animation while checking
        with st.spinner("Checking for grammar and spelling errors..."):
            # Call the Cohere API to check grammar and spelling
            try:
                response = co.generate(
                    model='command-xlarge-nightly',
                    prompt=f"Correct the grammar and spelling in the following text:\n\n{user_input}",
                    max_tokens=300,  # Limit the corrected text length
                    temperature=0.3,  # A lower temperature to ensure accurate corrections
                    k=0,
                    stop_sequences=[]
                )

                # Extract the corrected text from the response
                corrected_text = response.generations[0].text.strip()
                
                # Highlight the differences
                highlighted_text = highlight_differences(user_input, corrected_text)

                # Display the corrected and highlighted text
                st.subheader("✅ Corrected Text with Highlights:")
                st.markdown(highlighted_text, unsafe_allow_html=True)

                # Display success animation
                if lottie_correct:
                    st_lottie(lottie_correct, height=150, key="correct_animation")

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter some text to check.")

# Sidebar with instructions
st.sidebar.title("Instructions 📖")
st.sidebar.info(
    "This tool checks and corrects grammar and spelling. \n\n"
    "1. **Input Text**: Type or paste the text you want to check in the main text area.\n"
    "2. **Check**: Click the 'Check Grammar and Spelling' button.\n"
    "3. **View Results**: See the corrected text with highlighted changes.\n\n"
    "🔴 Red words indicate corrections, and green words are unchanged."
)
