class Url():
    localUrl = "http://localhost:8000"
    herokuUrl = "https://reservegd.herokuapp.com"
    def __init__(self,isLocal):
        self.isLocal = isLocal
    
    def getUrl(self):
        if self.isLocal == True:
            return self.localUrl
        else:
            return self.herokuUrl
    