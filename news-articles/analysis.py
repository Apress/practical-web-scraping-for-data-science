import dataset
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words

db = dataset.connect('sqlite:///news.db')

articles = []

tokenizer = RegexpTokenizer(r'\w+')
stop_words = get_stop_words('en')
p_stemmer = PorterStemmer()

for article in db['articles'].all():
    text = article['title'].lower().strip()
    text += " " + article['textContent'].lower().strip()
    if not text:
        continue
    # Tokenize
    tokens = tokenizer.tokenize(text)
    # Remove stop words and small words
    clean_tokens = [i for i in tokens if not i in stop_words]
    clean_tokens = [i for i in clean_tokens if len(i) > 2]
    # Stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in clean_tokens]
    # Add to list
    articles.append((article['title'], stemmed_tokens))

print(articles[0])

from gensim import corpora
dictionary = corpora.Dictionary([a[1] for a in articles])
corpus = [dictionary.doc2bow(a[1]) for a in articles]

print(corpus[0])

from gensim.models.ldamodel import LdaModel
nr_topics = 5
ldamodel = LdaModel(corpus, num_topics=nr_topics, 
                    id2word=dictionary, passes=20)

print(ldamodel.print_topics())

# Show topics by top-3 terms
for t in range(nr_topics):
    print(ldamodel.print_topic(t, topn=3))

# Show some random articles
from random import shuffle
idx = list(range(len(articles)))
shuffle(idx)
for a in idx[:3]:
    article = articles[a]
    print('==========================')
    print(article[0])
    prediction = ldamodel[corpus[a]][0]
    print(ldamodel.print_topic(prediction[0], topn=3))
    print('Probability:', prediction[1])
