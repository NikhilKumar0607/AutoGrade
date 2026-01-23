from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def plagiarism_score(essay1, essay2):
    essays = [essay1, essay2]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(essays)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(similarity[0][0] * 100, 2)


# TESTING
if __name__ == "__main__":
    e1 = "Artificial intelligence is the future of technology."
    e2 = "Artificial intelligence is the future of modern technology."

    score = plagiarism_score(e1, e2)
    print("plagiarism Similarity:", score, "%")
