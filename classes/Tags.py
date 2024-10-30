import json

class Tags:

    def __init__(self):
        self.tagsFile = 'storage/tags.json'
        self.tagKeys = []
        self.tagDict = {}
        self.loadTags()
        self.saveTags()

    
    def loadTags(self):
        """
        This method will load the tags from the tags.json file.
        """
        try:
            with open(self.tagsFile, 'r') as file:
                self.tagDict = json.load(file)
                self.tagKeys = self.tagDict.keys()
        except FileNotFoundError as a:
            print(f"Tags File Not Found: {a}")

    def saveTags(self):
        """
        This method will save the tags to the tags.json file.
        """
        with open(self.tagsFile, 'w') as file:
            json.dump(self.tagDict, file)


    
        