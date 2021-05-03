import main as m
import latent_semantic_analysis
import streamlit as st

# Title
st.title('AutoTLDR bot for Medium Articles')
st.header('Extracting the most important sentences & words')
st.text('Skills: Latent Semantic Analysis, SVD')

# Parameters
num_sentences = st.slider('# of sentences', min_value=1, max_value=10, value=5,step=1)
num_words = st.slider('# of words', min_value=1, max_value=10, value=5,step=1)

# User Input
text = st.text_input("Copy and paste article text: ")

# Running main
if text != "":
    sentences, id_to_word, ranked_sentences, ranked_words = m.main(text)
    
    # Results
    st.header("TOP SENTENCES:")
    for sentence in range(0,num_sentences):
        st.text("SENTENCE #" + str(sentence+1))
        st.text(sentences[ranked_sentences[sentence]])


    st.header("TOP WORDS:")
    for word in range (0, num_words):
        st.text(id_to_word[ranked_words[word]])