import streamlit as st
from keybert import KeyBERT

st.set_page_config(
    page_title="Hello",
    page_icon="🚀",
)

st.write("# Welcome to Product fdsfdsfsPass Social Media Analysis Results! 🚀")

with st.expander("ℹ️ - About this app", expanded=True):
    st.write(
        """     
-   2121254The *BERT Keyword Extractor* app is an easy-to-use interface built in Streamlit for the amazing [KeyBERT](https://github.com/MaartenGr/KeyBERT) library from Maarten Grootendorst!
-   It uses a minimal keyword extraction technique that leverages multiple NLP embeddings and relies on [Transformers] (https://huggingface.co/transformers/) 🤗 to create keywords/keyphrases that are most similar to a document.
	    """
    )

    st.markdown("")


#
# st.sidebar.success("Select a demo above.")

# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )
#

def main():
    st.header("This is the main page")
    st.write("Here you can find some information about our company.")


# Create a page with a header and some text
def ifixit():
    st.header("This is the ifixit page")
    st.write("Here you can find some information about our company.")


# Create another page with a header and some text
def youtube():
    st.header("This is the YouTube Transcript Sentiment Analysis page")
    st.write("Our company was founded in 2020 with the mission of making data science more accessible.")

    st.markdown("## **📌 Paste document **")
    with st.form(key="my_form"):
        ce, c1, ce, c2, c3 = st.columns([0.07, 1, 0.07, 5, 0.07])
        with c1:
            ModelType = st.radio(
                "Choose your model",
                ["DistilBERT (Default)", "Flair"],
                help="At present, you can choose between 2 models (Flair or DistilBERT) to embed your text. More to come!",
            )
            if ModelType == "Default (DistilBERT)":
                # kw_model = KeyBERT(model=roberta)

                @st.cache(allow_output_mutation=True)
                def load_model():
                    return KeyBERT(model=roberta)

                kw_model = load_model()
            else:
                @st.cache(allow_output_mutation=True)
                def load_model():
                    return KeyBERT("distilbert-base-nli-mean-tokens")

                kw_model = load_model()

            top_N = st.slider(
                "# of results",
                min_value=1,
                max_value=30,
                value=10,
                help="You can choose the number of keywords/keyphrases to display. Between 1 and 30, default number is 10.",
            )
            min_Ngrams = st.number_input(
                "Minimum Ngram",
                min_value=1,
                max_value=4,
                help="""The minimum value for the ngram range.""")


# Add a sidebar to the app with links to the two pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "IFixIt Analysis", "YouTube Sentiment Analysis Results"])

if page == "Main":
    main()
elif page == "IFixIt Analysis":
    ifixit()
elif page == "YouTube Sentiment Analysis Results":
    youtube()
