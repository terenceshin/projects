import latent_semantic_analysis as lsa

def main(text):
    text = text

    # Extracting Sentences
    sentences = lsa.get_sentences(text)

    # Creating bag of words for each sentence
    bag_of_word = lsa.bag_of_words(sentences)

    # Creating IDs for words
    word_to_id, id_to_word = lsa.allwords(bag_of_word)

    # Constructing Coordinates for Sparse Matrix
    row, col, val = lsa.gen_coords(bag_of_word, word_to_id)

    # Calculating SVD
    A = lsa.A_matrix(row, col, val, word_to_id, bag_of_word)
    s0, u0, v0 = lsa.get_svds_largest(A)

    # Getting Ranked Words and Sentences
    ranked_words = lsa.rank_words(u0,v0)
    ranked_sentences = lsa.rank_sentences(u0,v0)

    return sentences, id_to_word, ranked_sentences, ranked_words