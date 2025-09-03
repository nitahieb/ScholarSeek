import json
from entrezpy.base.analyzer import EutilsAnalyzer
import re
from article import ArticleRecord, ArticleResult
from lxml import etree

from researcher import Researcher


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


    #TODO finish this, have regex parsing
    #Once done probably want to break this down into more functions/files
    def analyze_result(self, response, request):
        self.init_result(response, request)
        parser = etree.XMLParser(ns_clean=True, recover=True)
        root = etree.fromstring(response.getvalue(), parser)
        
        # self.title = None
        # self.language = None
        # self.date = None
        # self.emails = set()
        # self.people = []
        # self.pmid = None

        for article in root.xpath('//PubmedArticle'):
            pmid = article.findtext('.//PMID')
            title = article.findtext('.//ArticleTitle')
            language = article.findtext('.//Language')
            publishInf = article.find('.//PubDate')
            publishDate = ""
            if publishInf is not None:
                year = publishInf.findtext('Year')
                month = publishInf.findtext('Month')
                day = publishInf.findtext('Day')
                publishDate = "-".join(filter(None, [year, month, day]))

            authors = []
            emails = set()
            for author in article.findall('.//Author'):
                lastName = author.findtext('LastName')
                firstName = author.findtext('ForeName')
                initials = author.findtext('Initials')
                email = None
                affiliation = author.findtext('.//Affiliation')
                if affiliation:
                    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+',affiliation)
                    if match:
                        email = match.group(0)
                        emails.add(email)
                
                researcher = Researcher(lastName,firstName,initials,affiliation,email)
                authors.append(researcher)
                
            record = ArticleRecord(title,language,publishDate,emails,authors,pmid)
            self.result.add_article_record(record)
            

    
