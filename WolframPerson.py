import Networking as net
from Utilities import eprint
import re
import WolframPersonUtilities as wpu

class WolframPerson:
    def __init__(self, parent, nameToLookup):
        self.parent = parent        #  Parent object, with methods to store values
        self.name = nameToLookup    #  Store the name to lookup
        lookupComplete = False      #  Lookup not completed yet

        self.pods = None            #  Value hasn't been set yet, but the variable exists. This allows for "if not self.pods".

        self.runLookup()            # For now, it automatically runs
        lookupComplete = True       #  Lookup is now complete

    def runLookup(self):
        self.pods = self.requestPods(self.name)    # Requests, checks, and re-requests/exits/continues depending on the result.

        if not self.pods:   # If there was a problem with the lookup (self.pods will be 'False' if the lookup had a problem)
            return False

        else:               # Looks like there were no problems! Let's keep going!
            self.parseAndStorePods()

    def requestPods(self, name, attemptNumber=1):
        """Returns False if it fails, otherwise returns a dictionary of the pods"""

        # Request the name the user gave. Hopefully that works.
        pods = net.wolfram(name)['pods']  # Query the API, get the pods

        if 'BasicInformation:PeopleData' in pods:  # Yay! We found a person!
            return pods

        elif 'BasicInformation:GivenNameData' in pods and attemptNumber == 1:  # Darn, we found a name, but not a person. If we haven't tried this already, let's try to lookup a person with that name.
            notablePplStr = pods['NotablePeopleWithName:GivenNameData']['subpods'][0]['plaintext']  # Get the full names of notable people who matched

            # Parse the first name
            notablePerson1Str = notablePplStr.split('\n')[0]
            notablePerson1NameIndex = notablePerson1Str.find('(')  # First parenthesis in string
            notablePerson1Name = notablePerson1Str[:notablePerson1NameIndex]

            # Try again (recursively) with that name
            return self.requestPods(notablePerson1Name, attemptNumber + 1)

        elif 'BasicInformation:GivenNameData' in pods and attemptNumber > 1:  # We found a name, but not a person. Yet, we've already tried to find the person. We may be in a loop. Let's stop here.
            eprint("Hey, are we looping?\n", pods, "\nattemptNumber:", attemptNumber)
            return False

        else:
            eprint('-----\nNo relevant ID Found among:')
            for key in pods:
                eprint(key)
            eprint('-----')
            return False


    def parseAndStorePods(self):
        """Parses the pods from 'self.pods', and stores each using the 'self.parent' object's 'storeResult' method. """
        store = self.parent.storeResult

        shortName, description          =   wpu.parsePodInputInterpretation(self.pods)
        store("short name", shortName)
        store("description", description)

        fullName, dob, pob, dod, pod    =   wpu.parsePodBasicInformation(self.pods)
        store("full name", fullName)
        store("date of birth", dob)
        store("place of birth", pob)
        store("date of death", dod)
        store("place of death", pod)

#        imageUrl

#        timelineImageUrl

#        notableFacts

#        physicalCharacteristics

#        familialRelationships

#        scientificContributions

#        wikipediaSummary

#        wikipediaPageHitsHistoryImageUrl


