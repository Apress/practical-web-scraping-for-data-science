from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import dataset
import matplotlib.pyplot as plt

db = dataset.connect('sqlite:///reviews.db')
reviews = db['reviews'].all()

analyzer = SentimentIntensityAnalyzer()

sentiment_by_stars = [[] for r in range(1,6)]

for review in reviews:
    full_review = review['title'] + '. ' + review['review']
    sentence_list = tokenize.sent_tokenize(full_review)
    cumulative_sentiment = 0.0
    for sentence in sentence_list:
        vs = analyzer.polarity_scores(sentence)
        cumulative_sentiment += vs["compound"]
    average_score = cumulative_sentiment / len(sentence_list)
    sentiment_by_stars[int(review['rating'])-1].append(average_score)

plt.violinplot(sentiment_by_stars,
               range(1,6),
               vert=False, widths=0.9,
               showmeans=False, showextrema=True, showmedians=True,
               bw_method='silverman')
plt.axvline(x=0, linewidth=1, color='black')
plt.show()