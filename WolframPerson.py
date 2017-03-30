import Networking as net
from Utilities import eprint
import re
import WolframPersonUtilities as wpu

class WolframPerson:
    def __init__(self, parent, nameToLookup):
        self.parent = parent        #  Parent object, with methods to store values
        self.name = nameToLookup    #  Store the name to lookup
        lookupComplete = False      #  Lookup not complete yet

        self.pods = None            #  Value hasn't been set yet, but the variable exists. This allows for "if not self.pods".

        # All the variables we will attempt to find
        self.shortName                          =   None
        self.description                        =   None

        self.fullName                           =   None
        self.dob                                =   None
        self.pob                                =   None
        self.dod                                =   None
        self.pod                                =   None

        self.imageUrl                           =   None

        self.timelineImageUrl                   =   None

        self.notableFacts                       =   None

        self.physicalCharacteristics            =   None

        self.familialRelationships              =   None

        self.scientificContributions            =   None

        self.wikipediaSummary                   =   None

        self.wikipediaPageHitsHistoryImageUrl   =   None


        self.runLookup()            # For now, it automatically runs
        lookupComplete = True       #  Lookup is now complete

    def runLookup(self):
        self.pods = self.requestPods(self.name)    # Requests, checks, and re-requests/exits/continues depending on the result.

        if not self.pods:   # If there was a problem with the lookup (self.pods will be 'False' if the lookup had a problem)
            return False

        else:               # Looks like there were no problems! Let's keep going!
            self.parsePods()

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


    def parsePods(self):
        """Parses the pods from 'self.pods' """
        self.shortName, self.description = wpu.parsePodInputInterpretation(self.pods)












    def wolfProcessBasicInformationBox(self):



        ###############################################################################################################
        #####   Split up the "Basic Information" box into a dictionary   #####

        basicInfoStr = basicInfo['subpods'][0]['plaintext']  # Get 'basic info'
        basicInfoStr = basicInfoStr.replace(' \n ',
                                            ' ')  # If there's a space before and after a newline, the text should actually be one line
        basicInfoList = re.split(' \| |\n', basicInfoStr)  # Make the info a list

        # Turn the list into a dictionary
        basicInfoDict = {}
        for i in range(0, len(basicInfoList), 2):
            item = basicInfoList[i]
            nextItem = basicInfoList[i + 1]
            basicInfoDict[item] = nextItem
        ###############################################################################################################



        ###############################################################################################################
        #####   Process the date of birth information from the "Basic Information" box   #####
        dateOfBirthStr = basicInfoDict['date of birth'][:-1]  # Remove trailing ')'
        print(dateOfBirthStr)
        dateOfBirthList = re.split(' \((?=[\da])',
                                   dateOfBirthStr)  # Split into [(plaintext date), (unparsed age OR number of years ago)]

        unparsedElapsedYears = dateOfBirthList[
            1]  # get Second item (string which contains elapsed years since birth somewhere)

        # Extract the int out of the string
        strippedElapsedYears = re.findall("\d+",
                                          unparsedElapsedYears)  # Only keeps digits, grouping any consecutive ones
        parsedElapsedYears = int(
            strippedElapsedYears[0])  # should only be one item in the regex's results, and it should be the first one

        dateOfBirthList[
            1] = parsedElapsedYears  # Leaves dateOfBirthList as [Date, Years ago].   Write the int back into the list, overwriting the unparsed string
        ###############################################################################################################



        ###############################################################################################################
        #####   Process the date of death information from the "Basic Information" box  #####
        if 'date of death' in basicInfoDict:
            dateOfDeathInfoStr = basicInfoDict['date of death'][:-1]  # Remove trailing ')'
            dateOfDeathInfoList = re.split(' \((?=[\da])', dateOfDeathInfoStr)

            deathDateStr = dateOfDeathInfoList[0]  # Date (string)
            deathYearsAgo = int(
                dateOfDeathInfoList[2].split(' ')[0])  # keep only first item (remove trailing 'years ago')
            deathAge = int(dateOfDeathInfoList[1].split(' ')[1])  # keep only middle item (remove preceeding 'age')

            dateOfDeathList = [deathDateStr, deathAge, deathYearsAgo]  # Date, Age at time, Years ago
            dead = True
        else:
            dead = False
        ###############################################################################################################

        # Input interpretation
        self.storeResult('name', name)
        self.storeResult('description', description)

        # Basic information
        self.storeResult('full name', basicInfoDict['full name'])
        self.storeResult('date of birth', dateOfBirthList)
        self.storeResult('place of birth', basicInfoDict['place of birth'])
        if dead:
            self.storeResult('date of death', dateOfDeathList)
            self.storeResult('place of death', basicInfoDict['place of death'])