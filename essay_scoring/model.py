import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Sample dataset
data = {
    "essay": [
        "this is a good essay",
        "this essay is average",
        "poor writing and poor structure",
        "excellent content and strong arguments",
        "bad grammar and weak ideas"
    ],
    "score": [8, 5, 3, 9, 2]
}

df = pd.DataFrame(data)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["essay"])
y = df["score"]

# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Export objects so Flask can import them
__all__ = ["vectorizer", "model"]
