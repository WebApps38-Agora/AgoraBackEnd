from gensim import corpora, models, similarities
from topics.models import Article, Topic

SIMILARITY_THRESHOLD = 0.25


class ArticleCorpus(corpora.TextCorpus):
    def get_texts(self):
        for text in self.input:
            yield text

    def __len__(self):
        return len(self.input)


def create_all_topics():
    '''Creates/updates topics based on all the articles currently in the DB.'''

    create_topics(None)


def create_topics(new_articles):
    '''Creates/updates topics based the given articles, which should have
    already been added to the database.'''

    articles = Article.objects.all()

    if new_articles is None:
        new_articles = articles

    # Create a corpus using tokenized headlines
    headlines = [article.headline for article in articles]
    corpus = ArticleCorpus([tokenize(headline) for headline in headlines])

    # Create a TFIDF model for the corpus
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # Create an LSI model based on the TFIDF model
    lsi = models.LsiModel(corpus_tfidf, id2word=corpus.dictionary, num_topics=Topic.objects.count() or len(headlines))
    corpus_lsi = lsi[corpus]

    # Create a similarity matrix and a table of all similarities
    index = similarities.MatrixSimilarity(corpus_lsi)
    similarity_table = index[[to_lsi_vector(corpus, lsi, tokenize(article.headline))
                             for article in new_articles]]

    # Group and add to DB
    group_articles_using_similarities(articles, new_articles, similarity_table)


def group_articles_using_similarities(articles, new_articles, similarity_table):
    '''Takes a 2D table of similarities between articles, and groups them using
    a dictionary mapping article IDs to a set of all articles which should be
    placed under the same topic.'''

    # sims contains a list of similarity values in the range 0 to 1, between
    # all pairs of articles. Therefore, similarity_table[i][i] = 1 for all i,
    # as an article is similar to itself with a value of 1. The first index
    # matches the index of the new_articles array, and the second matches the
    # articles array.
    for article_id, sims in enumerate(similarity_table):
        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # Take the second-highest similarity (which will be the most
        # similar headline other than the same article itself)
        similarity = sorted_sims[1]

        # Extract value and ID as a result of enumerate()
        similar_article_id = similarity[0]
        sim_value = similarity[1]

        # Get actual article objects pointed to by the IDs
        article = new_articles[article_id]
        similar_article = articles[similar_article_id]

        if sim_value > SIMILARITY_THRESHOLD:
            # Group the two together under the same, potentially new topic
            topic = similar_article.topic
            if topic == None:
                topic = Topic()
                topic.save()

            article.topic = topic
            similar_article.topic = topic
        else:
            # Create a new topic for just this article alone
            topic = Topic()
            topic.save()
            article.topic = topic

        article.save()
        similar_article.save()


def to_lsi_vector(corpus, lsi, tokenized_headline):
    vec_bow = corpus.dictionary.doc2bow(tokenized_headline)
    vec_lsi = lsi[vec_bow]
    return vec_lsi


def tokenize(text):
    '''Extract the features from the article title, using bag-of-words method.'''

    stoplist = set('for a of the and to in'.split())
    return [word for word in text.lower().split() if word not in stoplist]
