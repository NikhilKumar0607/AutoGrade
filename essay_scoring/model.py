import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Sample dataset (replace with real dataset later)
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

# TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["essay"])
y = df["score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, predictions)
print("Mean Absolute Error:", mae)

# Test with new essay
new_essay = ["this essay has good structure and content"]
new_vector = vectorizer.transform(new_essay)
predicted_score = model.predict(new_vector)

print("Predicted Score:", round(predicted_score[0], 2))
# Make model reusable for Flask
__all__ = ["vectorizer", "model"]
