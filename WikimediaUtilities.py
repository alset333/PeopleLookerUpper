from urllib.request import urlopen, quote
import Utilities

FILENAME_CUE = "File:"
IMAGE_LOCATION_CUE = '<div class="fullMedia"><a href="https://upload.wikimedia.org/wikipedia/commons/'
IMAGE_LOCATION_URL_START = 'https://upload.wikimedia.org/wikipedia/commons/'

def directUrlOfFile(mediaPageURL):
    """Returns (success, url)"""

    filenameStart = mediaPageURL.find(FILENAME_CUE) + len(FILENAME_CUE)
    filename = mediaPageURL[filenameStart:]
    filename_percent_encoded = quote(filename)
    print(filename, filename_percent_encoded)

    lines = urlopen(mediaPageURL).readlines()
    for item in lines:
        item = item.decode('utf-8')
        item = item.replace('href="//', 'href="https://')
        if item.find(IMAGE_LOCATION_CUE) == 0\
                and filename_percent_encoded.replace('_','').replace(' ','') in item.replace('_','').replace(' ',''):  # Remove spaces and underscores when checking, they seem inconsistent
            indexOfCueEnd = item.index(IMAGE_LOCATION_CUE) + len(IMAGE_LOCATION_CUE)
            image_location_short = item[indexOfCueEnd : item.find('"', indexOfCueEnd)]
            image_location_full = IMAGE_LOCATION_URL_START + image_location_short
            return True, image_location_full

    return False, None