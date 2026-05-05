import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud
import nltk

# ========== STEP 1: DOWNLOAD NLTK DATA ==========
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ========== STEP 2: SET FIGURE SIZE ==========
plt.rcParams["figure.figsize"] = (8, 5)

# ========== STEP 3: CREATE SMALL DATASET ==========
data = {
    "reviews": [
        "Good product fast delivery",
        "Bad service slow response",
        "Excellent quality",
        "Worst experience ever",
        "Average product",
        "Love this item"
    ]
}

df = pd.DataFrame(data)
print("=" * 50)
print("STEP 3: Original DataFrame (Small Dataset)")
print("=" * 50)
print(df)
print("\n")

# ========== STEP 4: TEXT PREPROCESSING ==========
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

df["clean_reviews"] = df["reviews"].apply(preprocess)

print("=" * 50)
print("STEP 4: Cleaned Reviews")
print("=" * 50)
print(df[['reviews', 'clean_reviews']])
print("\n")

# ========== STEP 5: SENTIMENT ANALYSIS ==========
df["sentiment_score"] = df["clean_reviews"].apply(lambda x: TextBlob(x).sentiment.polarity)
df["sentiment"] = df["sentiment_score"].apply(
    lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral"
)

print("=" * 50)
print("STEP 5: Sentiment Analysis Results")
print("=" * 50)
print(df[['clean_reviews', 'sentiment_score', 'sentiment']])
print("\n")

# ========== STEP 6: SENTIMENT DISTRIBUTION PLOT ==========
print("=" * 50)
print("STEP 6: Sentiment Distribution")
print("=" * 50)
plt.figure()  # Create new figure
sns.countplot(x="sentiment", data=df, order=['Positive', 'Neutral', 'Negative'])
plt.title("Customer Sentiment Distribution (Small Dataset)")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()

# ========== STEP 7: WORD CLOUD ==========
print("=" * 50)
print("STEP 7: Word Cloud")
print("=" * 50)
text = " ".join(df["clean_reviews"])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Reviews", fontsize=16)
plt.show()

# ========== STEP 8: SUMMARY STATISTICS ==========
print("=" * 50)
print("STEP 8: Summary Statistics")
print("=" * 50)
print(df['sentiment'].value_counts())
print(f"\nAverage Sentiment Score: {df['sentiment_score'].mean():.3f}")
print(f"Positive: {(df['sentiment'] == 'Positive').sum()}/6")
print(f"Negative: {(df['sentiment'] == 'Negative').sum()}/6")
print(f"Neutral: {(df['sentiment'] == 'Neutral').sum()}/6")