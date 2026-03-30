from sklearn.feature_extraction.text import TfidfVectorizer

def basic_features(tokenized_essay):
    total_words = len(tokenized_essay)
    unique_words = len(set(tokenized_essay))

    vocab_richness = unique_words / total_words if total_words != 0 else 0

    return [total_words, vocab_richness]


def tfidf_features(essays):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(essays)
    return tfidf_matrix


def explain_essay(text):
    words = text.split()
    word_count = len(words)
    unique_words = len(set(words))

    vocab_richness = unique_words / word_count if word_count > 0 else 0

    if word_count < 80:
        length_feedback = "Essay is too short"
    elif word_count < 150:
        length_feedback = "Essay length is average"
    else:
        length_feedback = "Essay length is good"

    if vocab_richness < 0.4:
        vocab_feedback = "Vocabulary usage is basic"
    elif vocab_richness < 0.6:
        vocab_feedback = "Vocabulary usage is decent"
    else:
        vocab_feedback = "Vocabulary usage is rich"

    return {
        "word_count": word_count,
        "vocab_richness": round(vocab_richness, 2),
        "length_feedback": length_feedback,
        "vocab_feedback": vocab_feedback
    }
