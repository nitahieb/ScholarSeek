from analyzer import ArticleAnalyzer
from format import emailFormat, overviewFormat
from pipeline import Pipeline

def getSummary(search, sortBy, email, retmax):
    pipeline = Pipeline(email)
    pipeline.addSearch(search, retmax=retmax, sortBy=sortBy)
    analyzer = ArticleAnalyzer()
    pipeline.addFetch(analyzer=analyzer)
    results = pipeline.getResults()
    if not results or not results.articles:
        return "No articles found for your search."
    return overviewFormat(results.articles)


def getEmails(search, sortBy, email, retmax):
    pipeline = Pipeline(email)
    pipeline.addSearch(search, retmax=retmax, sortBy=sortBy)
    analyzer = ArticleAnalyzer()
    pipeline.addFetch(analyzer=analyzer)
    results = pipeline.getResults()
    if not results or not results.articles:
        return "No articles found — no emails to display."
    emails = set()
    for article in results.articles:
        emails.update(article.emails)
    return emailFormat(emails)
