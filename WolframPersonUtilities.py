import re

def parsePodInputInterpretation(pods):
    """Get short name and short description from "Input interpretation" box.
    Returns (name, description)"""

    personDescStr = pods['Input']['subpods'][0]['plaintext']  # Get the short summarized name & description
    personDescList = personDescStr[:-1].split('  (')
    name = personDescList[0]  # Get short name
    description = personDescList[1]  # Get description - get only the description from the parenthesis, not the name

    return name, description

def parsePodBasicInformation(pods):
    """Get full name, date of birth, place of birth, date of death, and place of death from "Basic information" box.
    Returns (full name, date of birth, place of birth, date of death, place of death)"""

    # Initialize any values that might be returned later, so they are None unless found and overwritten
    basicInfoDict = {'full name': None, 'place of birth': None, 'place of death': None}
    dateOfBirthList = None
    dateOfDeathList = None


    ###############################################################################################################
    #####   Split up the "Basic Information" box into a dictionary   #####

    basicInfoStr = pods['BasicInformation:PeopleData']['subpods'][0]['plaintext']  # Get 'basic info'
    basicInfoStr = basicInfoStr.replace(' \n ', ' ')  # If there's a space before and after a newline, the text should actually be one line
    basicInfoList = re.split(' \| |\n', basicInfoStr)  # Make the info a list

    # Turn the list into a dictionary
    for i in range(0, len(basicInfoList), 2):
        item = basicInfoList[i]
        nextItem = basicInfoList[i + 1]
        basicInfoDict[item] = nextItem
    ###############################################################################################################



    ###############################################################################################################
    #####   Process the date of birth information from the "Basic Information" box   #####
    if 'date of birth' in basicInfoDict:
        dateOfBirthStr = basicInfoDict['date of birth'][:-1]  # Remove trailing ')'
        dateOfBirthList = re.split(' \((?=[\da])', dateOfBirthStr)  # Split into [(plaintext date), (unparsed age OR number of years ago)]

        unparsedElapsedYears = dateOfBirthList[
            1]  # get Second item (string which contains elapsed years since birth somewhere)

        # Extract the int out of the string
        strippedElapsedYears = re.findall("\d+", unparsedElapsedYears)  # Only keeps digits, grouping any consecutive ones
        parsedElapsedYears = int(strippedElapsedYears[0])  # should only be one item in the regex's results, and it should be the first one

        dateOfBirthList[1] = parsedElapsedYears  # Leaves dateOfBirthList as [Date, Years ago].   Write the int back into the list, overwriting the unparsed string
    ###############################################################################################################



    ###############################################################################################################
    #####   Process the date of death information from the "Basic Information" box  #####
    if 'date of death' in basicInfoDict:
        dateOfDeathInfoStr = basicInfoDict['date of death'][:-1]  # Remove trailing ')'
        dateOfDeathInfoList = re.split(' \((?=[\da])', dateOfDeathInfoStr)

        deathDateStr = dateOfDeathInfoList[0]  # Date (string)
        deathYearsAgo = int(dateOfDeathInfoList[2].split(' ')[0])  # keep only first item (remove trailing 'years ago')
        deathAge = int(dateOfDeathInfoList[1].split(' ')[1])  # keep only middle item (remove preceeding 'age')

        dateOfDeathList = [deathDateStr, deathAge, deathYearsAgo]  # Date, Age at time, Years ago
        dead = True
    else:
        dead = False
    ###############################################################################################################

    # Basic information

    fullName = basicInfoDict['full name']
    dob = dateOfBirthList
    pob = basicInfoDict['place of birth']
    dod = dateOfDeathList
    pod = basicInfoDict['place of death']

    return fullName, dob, pob, dod, pod