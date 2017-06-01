from gensim import corpora, models, similarities
from models import Article

class ArticleCorpus(corpora.TextCorpus):
    def get_texts(self):
        for text in self.input:
            yield text

    def __len__(self):
        return len(self.input)


def create_article_corpus():
    headlines = [article.headline for article in Article.objects.all()]
    tokenized_headlines = [tokenize(headline) for headline in headlines]
    corpus = ArticleCorpus(tokenized_headlines)

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lsi = models.LsiModel(corpus, id2word=corpus.dictionary, num_topics=300)
    corpus_lsi = lsi[corpus]

    index = similarities.MatrixSimilarity(lsi[corpus])
    similarity_table = index[[to_lsi_vector(corpus, lsi, headline) for headline in headlines]]

    for i, sims in enumerate(similarity_table):
        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        similarity = sorted_sims[1]
        print(str(similarity[1]) + ': ' + headlines[i] + ' is most similar to ' + headlines[similarity[0]])

def to_lsi_vector(corpus, lsi, headline):
    vec_bow = corpus.dictionary.doc2bow(tokenize(headline))
    vec_lsi = lsi[vec_bow]
    return vec_lsi

def tokenize(text):
    #return text.split()
    stoplist = set('for a of the and to in'.split())
    return [word for word in text.lower().split() if word not in stoplist]
