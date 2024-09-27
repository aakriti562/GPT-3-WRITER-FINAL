import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
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

# NLTK Downloads
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Streamlit app UI
st.title("🔍 SEO Analyzer")
st.write("Enter a URL to analyze its SEO performance:")

# Text input for URL
url = st.text_input('URL (without http:// or https://)', placeholder="example.com")

# SEO analysis function
def seo_analysis(url):
    good = []
    bad = []
    
    # Send a GET request to the website
    try:
        response = requests.get("http://" + url)
        
        # Check the response status code
        if response.status_code != 200:
            st.error("🚫 Error: Unable to access the website.")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title and description
        title = soup.find('title').get_text() if soup.find('title') else ""
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else ""

        # Check if the title and description exist
        if title:
            good.append("✅ Title Exists! Great!")
        else:
            bad.append("❌ Title does not exist! Add a Title.")

        if description:
            good.append("✅ Description Exists! Great!")
        else:
            bad.append("❌ Description does not exist! Add a Meta Description.")

        # Grab the Headings
        hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        h_tags = []
        for h in soup.find_all(hs):
            good.append(f"✅ {h.name.upper()} --> {h.text.strip()}")
            h_tags.append(h.name)

        if 'h1' not in h_tags:
            bad.append("❌ No H1 found!")

        # Extract the images without Alt
        for i in soup.find_all('img', alt=''):
            bad.append(f"❌ Image without Alt text: {i['src']}")

        # Extract keywords
        body_text = soup.find('body').text
        words = [i.lower() for i in word_tokenize(body_text)]
        bi_grams = ngrams(words, 2)
        freq_bigrams = nltk.FreqDist(bi_grams)
        bi_grams_freq = freq_bigrams.most_common(10)

        # Grab a list of English stopwords
        sw = nltk.corpus.stopwords.words('english')
        new_words = [i for i in words if i not in sw and i.isalpha()]

        # Extract the frequency of the words and get the 10 most common ones
        freq = nltk.FreqDist(new_words)
        keywords = freq.most_common(10)

        # Print the results in tabs
        tab1, tab2, tab3, tab4 = st.tabs(['🔑 Keywords', '📈 BiGrams', '✅ Good Practices', '❌ Bad Practices'])
        
        with tab1:
            for i in keywords:
                st.text(i)
        
        with tab2:
            for i in bi_grams_freq:
                st.text(i)
        
        with tab3:
            for i in good:
                st.success(i)
        
        with tab4:
            for i in bad:
                st.error(i)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")

# Display loading animation while the analysis runs
if st.button("🔍 Analyze SEO"):
    if url:
        with st.spinner("Analyzing..."):
            if lottie_loading:
                st_lottie(lottie_loading, height=150, key="loading_animation")
            seo_analysis(url)
    else:
        st.warning("⚠️ Please enter a URL to analyze.")

# Sidebar with instructions
st.sidebar.title("Instructions 📖")
st.sidebar.info(
    "This tool analyzes the SEO performance of a website. \n\n"
    "1. **Enter URL**: Type the URL of the website you want to analyze (without 'http://' or 'https://').\n"
    "2. **Analyze SEO**: Click the 'Analyze SEO' button to get insights on title, description, keywords, and more.\n"
    "3. **View Results**: Check the tabs to see the keywords, bi-grams, good practices, and bad practices."
)
