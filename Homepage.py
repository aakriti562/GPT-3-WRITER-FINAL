import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Set page config
st.set_page_config(
    page_title="GPT-3 Writer Operations",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation for text operations
lottie_text = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_x62chJ.json")

# Main title and description
st.title("🚀 Welcome to GPT-3 Writer Operations")
st.write("### An all-in-one tool for text processing tasks! ✍️")

# Add some space
st.write("\n")

# Create first row with three columns: Paraphrasing, Summarization, Grammar Check
col1, col2, col3 = st.columns(3)

# Adding interactive buttons for operations with hover effects
def operation_button(col, emoji, title, description):
    with col:
        if st.button(f"{emoji} {title}"):
            st.expander(f"About {title}", expanded=True).write(description)

operation_button(col1, "🔄", "Paraphrasing",
    "Effortlessly rephrase sentences to avoid plagiarism or improve readability.")
operation_button(col2, "📄", "Summarization",
    "Summarize long paragraphs into concise and meaningful text.")
operation_button(col3, "🔍", "Grammar & Spelling Check",
    "Correct grammar mistakes and typos with ease.")

# Create second row with two columns: Article Writing, SEO Analyzer
col4, col5 , col6 = st.columns(3)

operation_button(col4, "📝", "Article Writing",
    "Generate complete, well-structured articles for blogs, reports, and more.")
operation_button(col5, "📊", "SEO Analyzer",
    "Analyze your content's SEO performance and improve keyword usage.")
operation_button(col6, "📄", "HomePage",
    "Look for the best-fit option.")


# Center the two columns
st.markdown(
    """
    <style>
    .stContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    button:hover {
        background-color: #0072B1; /* Change button color on hover */
        color: white; /* Change text color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add Lottie animation for visual effect
if lottie_text:
    st_lottie(lottie_text, height=270, key="text_animation")

# Add a note about using the sidebar
st.markdown(
    """
    **Choose a text operation** from the buttons above to explore different operations on text! 🎯
    """
)

# Sidebar success message
st.sidebar.success("Select a page from the sidebar to start working on text operations.")
