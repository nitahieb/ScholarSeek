#Update affiliation in methods

class Researcher():
    def __init__(self, lastName="", firstName="", initials="", affiliation="", email=""):
        self.firstName = firstName
        self.lastName = lastName
        self.initials = initials
        self.affiliation = affiliation
        self.email = email

    def __repr__(self):
        kvps = [f"{k}={v}" for k, v in vars(self).items()]
        return f"{type(self).__name__}({', '.join(kvps)})"
