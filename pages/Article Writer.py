import streamlit as st
import cohere
from streamlit_lottie import st_lottie
import requests

# Initialize Cohere client with API key
co = cohere.Client('your_cohere_api_key')  # Replace with your actual API key

# Function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_intro = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_tznz5g0k.json")  # Intro animation
lottie_generate = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_vcpscdlt.json")  # Generate animation
lottie_success = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_5cn5g4h5.json")  # Success animation

# Streamlit App Layout
st.title("📝 Article Writer")
st.subheader("Generate cutting-edge content in less than a minute.")

# Display intro animation
if lottie_intro:
    st_lottie(lottie_intro, height=300, key="intro_animation")

# Sidebar Instructions
st.sidebar.title("Instructions")
st.sidebar.info("""
1. **SEO Keywords**: Enter relevant keywords that you want to optimize for in your article.
2. **Article Title**: Provide a catchy title for your article.
3. **Article Outline**: Fill in the main points you want to cover in article. You can add more outlines by clicking the **Add Outline** button.
4. **Tone**: Select the tone of the article from the dropdown menu.
5. **Generate**: Click the **Generate** button to create your article.
""")

# Input fields for user
seo_keywords = st.text_input("🔑 SEO Keywords", "nextjs tutorial")
article_title = st.text_input("📰 Article Title", "How to create a Next.JS app")

# Initialize outline list
if 'outline' not in st.session_state:
    st.session_state.outline = [
        st.text_input("Outline 1", "What is Next.JS"),
        st.text_input("Outline 2", "What are the benefits of Next.JS")
    ]

# Add option for more outlines
if st.button("➕ Add Outline"):
    new_outline = st.text_input(f"Outline {len(st.session_state.outline) + 1}", "")
    if new_outline:
        st.session_state.outline.append(new_outline)

# Display current outlines
st.subheader("📑 Article Outline")
for idx, point in enumerate(st.session_state.outline, start=1):
    st.write(f"{idx}. {point}")

# Select tone
tone = st.selectbox("🎤 Tone", ["Standard", "Friendly", "Professional", "Casual"])


# Generate button
if st.button("🚀 Generate"):
    if not article_title or not st.session_state.outline:
        st.error("❌ Please provide an article title and at least one outline.")
    else:
        # Display generate animation
        if lottie_generate:
            st_lottie(lottie_generate, height=150, key="generate_animation")

        # Prepare the prompt for Cohere
        prompt = f"Write an article titled '{article_title}' with the following outline:\n"
        for idx, point in enumerate(st.session_state.outline):
            prompt += f"{idx + 1}. {point}\n"
        prompt += f"Tone: {tone}"

        # Cohere API call
        response = co.generate(
            model='command-r-plus-08-2024',
            prompt=prompt,
            max_tokens=500,  # limit of tokens (word count)
            temperature=0.7,
        )

        article = response.generations[0].text

        # Display success animation and generated article
        if lottie_success:
            st_lottie(lottie_success, height=150, key="success_animation")
        
        st.subheader("📃 Generated Article")
        st.write(article)
