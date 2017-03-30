import Utilities
import WolframPerson

class Lookup:
    givenInfo = {}
    results = {} # Based on the given, but will be built on as we go.

    def __init__(self, infoDict): # Take in the info and initialize variables
        self.givenInfo = infoDict
        for key in infoDict:
            self.results[key] = (infoDict[key],) # Store in tuples
        print("infoDict:\t\t\t", infoDict)


    def storeResult(self, key, value):
        if key in self.givenInfo: # If a value was given, don't change it in the results
            return "Result Ignored"
        elif key in self.results: # If the value wasn't given, but we already have a result
            self.results[key] += (value,)
            return "Result Appended"
        else:
            self.results[key] = (value,)
            return "Result Stored"

    def getResult(self, key):
        if key in self.results:
            mostCommonResult = Utilities.most_common(self.results[key])
            return mostCommonResult
        else:
            return ""


    def getResults(self):
        return self.results

    def runLookup(self):
        self.lookupByName()



    def lookupByName(self):
        name = self.getResult('name')
        #wiki = net.getSrcCodeOf("https://en.wikipedia.org/wiki/" + fName + " " + mName + " " + lName + " (disambiguation)")
        #duck = net.getSrcCodeOf("https://en.wikipedia.org/wiki/" + fName + " " + mName + " " + lName + " (disambiguation)")
        wolframPerson = WolframPerson.WolframPerson(self, name)

