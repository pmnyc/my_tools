"""
@author: Man Peng

This program analyses the city name and standardize it
"""

def proessCityName(city, space_substitute="_"):
    """ This funciton is to standardize the name of city and state
    For example, it will return "Los Angeles,CA" if city is given as
        "  los    angeles, ca "
    """
    
    def makeFirstLetterUpper(x):
        if x.find(' ') >=0:
            raise Exception('Name '+x+' should not have blank space!')
        x2 = x.lower()
        return x2[:1].upper() + x2[1:]
    
    space_count = city.count(" ")
    for i in range(space_count):
        city = city.strip().replace("  "," ").replace(" ,",",").replace(", ",",")
    town = city
    state = town[(town.index(",")+1):]
    town = town.replace(","+state,","+state.upper())
    city_ = town[:(town.index(","))]
    city_words = city_.split(' ')
    city_words= map(makeFirstLetterUpper,city_words)
    city_new = space_substitute.join(city_words)
    town= town.replace(city_,city_new)
    return town
