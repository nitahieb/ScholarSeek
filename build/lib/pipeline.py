from entrezpy.conduit import Conduit

class Pipeline:
    def __init__(self,email):
        self.fetchID= None
        self.searchID=None
        self.conduit = Conduit(email)
        self.pipeline = self.conduit.new_pipeline()

    def addSearch(self, searchTerm, sortBy, retmax, db="pubmed", rettype="uilist",):
        searchQuery = {
            "db": db,
            "term": searchTerm,
            "retmax": retmax,
            "rettype": rettype,
            "sort": sortBy
        }

        self.searchID = self.pipeline.add_search(searchQuery)

    def addFetch(self, analyzer=None, db="pubmed", retmode="xml"):
        fetchQuery = {"db": db, "retmode": retmode}
        self.fetchID = self.pipeline.add_fetch(
                fetchQuery, dependency=self.searchID, analyzer=analyzer
        )

    def getResults(self):
        self.conduit.run(self.pipeline)
        if self.fetchID:
            result = self.conduit.get_result(self.fetchID)
        else:
            result = self.conduit.get_result(self.searchID)
        return result
