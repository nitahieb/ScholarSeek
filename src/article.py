from entrezpy.base.result import EutilsResult


class ArticleRecord:
    # Class to store a single article
    def __init__(self):
        self.title = None
        self.language = None
        self.date = None
        self.emails = set()
        self.people = []
        self.pmid = None


class ArticleResult(EutilsResult):
    def __init__(self, response, request):
        super().__init__(request.eutil, request.query_id, request.db)
        self.articles = []

    def size(self):
        return len(self.articles)

    def isEmpty(self):
        if not self.articles:
            return True
        return False

    def get_link_parameter(self, reqnum=0):
        print("{} has no elink capability".format(self))
        return {}

    def dump(self):
        return {
            self: {
                "dump": {
                    "article_records": [x for x in self.articles],
                    "query_id": self.query_id,
                    "db": self.db,
                    "eutil": self.function,
                }
            }
        }
    def add_article_record(self, article_record):
        self.articles.append(article_record)
