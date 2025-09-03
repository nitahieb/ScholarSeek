#Update affiliation in methods

class Researcher():
    def __init__(self,lastName,firstName, initials):
        self.firstName = firstName
        self.lastName = lastName
        self.initials = initials
        self.affiliation = []

    def printResearcher(self):
        print(f'\033[1mName:\033[0m{self.firstName} {self.lastName} \033[1mAffiliation:\033[0m{self.affiliation}')
        
    def asDict(self):
        return {"firstName":self.firstName, "lastName":self.lastName,"initials":self.initials, "affiliation":self.affiliation}