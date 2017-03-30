def parsePodInputInterpretation(pods):
    """Get short name and short description from "Input Interpretation" box. Returns (name, description)"""

    personDescStr = pods['Input']['subpods'][0]['plaintext']  # Get the short summarized name & description
    personDescList = personDescStr[:-1].split('  (')
    name = personDescList[0]  # Get short name
    description = personDescList[1]  # Get description - get only the description from the parenthesis, not the name

    return name, description

