import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# download only once (safe even if already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Tokenization
    tokens = word_tokenize(text)

    # 4. Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens


# TESTING
if __name__ == "__main__":
    sample_essay = "This is a Sample Essay! It has punctuation, and stopwords."
    print(preprocess_text(sample_essay))
