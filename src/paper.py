#TODO Will probably remove this file, is redundant with ArticleRecord
class Paper():
    def __init__(self,title,language,date,pmid,emails):
        self.title = title
        self.language=language
        self.date=date
        self.emails=emails
        self.researchers = []
        self.pmid=pmid

    def printPaper(self):
        print(f'\033[1mTitle:\033[0m{self.title} \033[1mLanguage:\033[0m{self.language} \033[1mDate:\033[0m{self.date}')
        for researcher in self.researchers:
            researcher.printPaper()

    def asdict(self):
        dictionary = {'title': self.title, 'language': self.language,"emails":self.emails,"PMID":self.pmid, 'date': self.date}
        i=1
        for researcher in self.researchers:
            dictionary["Researcher_"+str(i)] = researcher.asdict()
            i+=1
            
        return dictionary