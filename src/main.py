from analyzer import ArticleAnalyzer
from format import overviewFormat
from pipeline import Pipeline

#TODO I'll probably make this a simple console tool once it's more formed

def getEmails(search,email="",retmax=10):
    pipeline = Pipeline(email)
    pipeline.addSearch(search,retmax=retmax)
    analyzer = ArticleAnalyzer()
    pipeline.addFetch(analyzer=analyzer)
    results = pipeline.getResults()
    emails = set()
    for article in results.articles:
        emails.update(article.emails)
    return emails

def createMarkdown(articles):
    md = overviewFormat(articles)

    with open("article_summary.md", "w", encoding="utf-8") as f:
        f.write(md)







