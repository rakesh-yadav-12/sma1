import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob

np.random.seed(42)

# ========== STEP 1: Generate synthetic data ==========
print("="*50)
print("STEP 1: Generating synthetic data")
print("="*50)

brands = ["BrandA", "BrandB", "BrandC"]
dates = pd.date_range(start="2025-01-01", periods=100)

data = [[date, brand, f"{brand} launches new product", 
         np.random.randint(100,1000), np.random.randint(10,200), 
         np.random.randint(5,100)] for date in dates for brand in brands]

df = pd.DataFrame(data, columns=['Date','Brand','Post','Likes','Comments','Shares'])
print("First 5 rows:\n", df.head(), "\n")

# ========== STEP 2: Calculate Engagement Score ==========
print("="*50)
print("STEP 2: Calculating engagement score")
print("="*50)

df['Engagement'] = df['Likes'] + df['Comments'] + df['Shares']
print("First 5 rows with engagement:\n", df.head(), "\n")

# ========== STEP 3: Competitor Performance Summary ==========
print("="*50)
print("STEP 3: Competitor performance summary")
print("="*50)

performance = df.groupby('Brand')['Engagement'].mean().reset_index()
print("Average engagement by brand:\n", performance, "\n")

# ========== STEP 4: Engagement Visualization ==========
print("="*50)
print("STEP 4: Creating engagement bar chart")
print("="*50)

plt.figure(figsize=(8,6))
plt.bar(performance['Brand'], performance['Engagement'], color=['#FF6B6B','#4ECDC4','#45B7D1'])
plt.xlabel('Brand'); plt.ylabel('Average Engagement'); plt.title('Competitor Engagement Comparison')
plt.grid(True, alpha=0.3); plt.show()
print("Chart displayed\n")

# ========== STEP 5: Engagement Trend Over Time ==========
print("="*50)
print("STEP 5: Creating engagement trend over time")
print("="*50)

trend = df.groupby(['Date','Brand'])['Engagement'].mean().unstack()
plt.figure(figsize=(10,6))
trend.plot(linewidth=2)
plt.title('Engagement Trend Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12); plt.ylabel('Average Engagement', fontsize=12)
plt.legend(title='Brand'); plt.xticks(rotation=45)
plt.grid(True, alpha=0.3); plt.tight_layout(); plt.show()
print("Trend chart displayed\n")

# ========== STEP 6: Sentiment Analysis ==========
print("="*50)
print("STEP 6: Performing sentiment analysis")
print("="*50)

df['Sentiment'] = df['Post'].apply(lambda t: TextBlob(t).sentiment.polarity)
sentiment_summary = df.groupby('Brand')['Sentiment'].mean().reset_index()
print("Average sentiment score by brand:\n", sentiment_summary)