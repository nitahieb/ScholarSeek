import json
from entrezpy.base.analyzer import EutilsAnalyzer
from article import ArticleRecord, ArticleResult
from parsing import parse_xml, extract_basics, extract_publish_date, extract_authors_and_emails



class ArticleAnalyzer(EutilsAnalyzer):
    def __init__(self):
        super().__init__()

    def init_result(self, response, request):
        if self.result is None:
            self.result = ArticleResult(response, request)

    def analyze_error(self, response, request):
        print(
            json.dumps(
                {
                    __name__: {
                        "Response": {
                            "dump": request.dump(),
                            "error": response.getvalue(),
                        }
                    }
                }
            )
        )


    #TODO finish this
    #Once done probably want to break this down into more functions/files
    def analyze_result(self, response, request):
        self.init_result(response, request)
        root = parse_xml(response)

        for article in root.xpath('//PubmedArticle'):
            pmid, title, language = extract_basics(article)
            publish_date = extract_publish_date(article)
            emails, authors = extract_authors_and_emails(article)
            record = ArticleRecord(title, language, publish_date, emails, authors, pmid)
            self.result.add_article_record(record)

