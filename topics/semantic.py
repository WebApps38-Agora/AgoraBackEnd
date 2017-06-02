from gensim import corpora, models, similarities
from topics.models import Article, Topic
from collections import defaultdict

SIMILARITY_THRESHOLD = 0.25

class ArticleCorpus(corpora.TextCorpus):
    def get_texts(self):
        for text in self.input:
            yield text

    def __len__(self):
        return len(self.input)


def create_all_topics():
    '''Creates topics based on all the articles currently in the DB.'''

    # Create a corpus using tokenized headlines
    articles = Article.objects.all()
    headlines = [article.headline for article in articles]
    tokenized_headlines = [tokenize(headline) for headline in headlines]
    corpus = ArticleCorpus(tokenized_headlines)

    # Create a TFIDF model for the corpus
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    # Create an LSI model based on the TFIDF model
    lsi = models.LsiModel(corpus_tfidf, id2word=corpus.dictionary, num_topics=len(headlines))
    corpus_lsi = lsi[corpus]

    # Create a similarity matrix and a table of all similarities between the headlines
    index = similarities.MatrixSimilarity(corpus_lsi)
    similarity_table = index[[to_lsi_vector(corpus, lsi, headline) for headline in tokenized_headlines]]

    # Group and add to DB
    groups = group_articles_using_similarities(similarity_table)
    groups_to_topics_db(articles, groups)


def group_articles_using_similarities(similarity_table):
    '''Takes a 2D table of similarities between articles, and groups them using
    a dictionary mapping article IDs to a set of all articles which should be
    placed under the same topic.'''

    groups = defaultdict(set)
    for i, sims in enumerate(similarity_table):
        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # Take the second-highest simularity (which will be the most
        # similar headline other that that of the current article, value 1)
        similarity = sorted_sims[1]
        #print(str(similarity[1]) + ': ' + headlines[i] + ' is most similar to ' + headlines[similarity[0]])

        article_id = similarity[0]
        sim_value = similarity[1]

        groups[i] = set()
        groups[i].add(i)
        if (sim_value > SIMILARITY_THRESHOLD):
            groups[i].add(article_id)
            groups[article_id].add(i)

            groups[i].update(groups[article_id])
            groups[article_id].update(groups[i])

    return groups


def groups_to_topics_db(articles, groups):
    '''Takes a dictionary of article indices mapped to sets of other articles,
    which should be placed under the same topic, and inserts the actual
    topics into the database, updating the relevant articles.'''

    for key, article_set in groups.items():
        a = articles[key]
        if a.topics.count() == 0:
            topic = Topic()
            topic.save()
            for article in article_set:
                a = articles[article]
                a.topics.add(topic)
                a.save()


def to_lsi_vector(corpus, lsi, tokenized_headline):
    vec_bow = corpus.dictionary.doc2bow(tokenized_headline)
    vec_lsi = lsi[vec_bow]
    return vec_lsi


def tokenize(text):
    '''Extract the features from the article title, using bag-of-words method.'''

    stoplist = set('for a of the and to in'.split())
    return [word for word in text.lower().split() if word not in stoplist]
