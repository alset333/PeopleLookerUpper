from urllib.request import urlopen  # For downloading file. FancyURLopener will follow redirects, URLopener will not
import json
import os, sys

from Utilities import eprint

apiKeyFile = open(os.path.normpath(sys.path[0] + "/WOLFRAM_ALPHA_API_KEY.txt"))
WOLFRAM_ALPHA_API_KEY = apiKeyFile.read()
apiKeyFile.close()

def getSrcCodeOf(url):
    print('Getting Source Code of', url)
    f = urlopen(url)
    contentsByte = f.read()
    f.close()
    contentsStr = contentsByte.decode('utf-8') # Bytes to string
    return contentsStr

def modifyJson(startingJsonDict):
    oldJsonDict = startingJsonDict  # Get the old dictionary
    newJsonDict = startingJsonDict  # Create a new dictionary based on the old one


    podsList = oldJsonDict['pods']  # Get the list of pods
    podsDict = {}                   # Create a dictionary to add the pods to

    for pod in podsList:
        podId = pod['id']
        podsDict[podId] = pod

    newJsonDict['pods'] = podsDict  # Replace the pods in the new dictionary with the ones we just organized

    print(newJsonDict)
    return newJsonDict

def wolfram(query):  # Returns False if fails, otherwise returns the 'queryresult' part of the JSON

    queryModified = query.replace('  ', ' ').replace(' ', '%20')
    jsonString = getSrcCodeOf("https://api.wolframalpha.com/v2/query?format=image,plaintext&output=JSON&appid=" + WOLFRAM_ALPHA_API_KEY + "&input=" + queryModified)
    parsedJson = json.loads(jsonString)['queryresult']

    if parsedJson['success']:
        modifiedJson = modifyJson(parsedJson)
        return modifiedJson
    else:
        eprint("Wolfram Lookup of \"" + query + "\" failed")
        return False

#class Networking:
#    def __init__(self):
#        None
