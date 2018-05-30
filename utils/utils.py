
from dateutil.parser import parse
#Todo resolve this import and uncomment it
import re

def convertDate(date):
    if (date != None):
        date = parse(date)
        date = date.strftime('%d/%m/%Y')
    return date
def getStarts(stars):
    if(stars!=None):
        stars = find_numbers(stars,False)
    return stars

def find_numbers(string, ints=True):
    if(string == ''):
        return
    numexp = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*')  # optional - in front
    numbers = numexp.findall(string)
    numbers = [x.replace(',', '') for x in numbers]
    if ints is True:
        return [int(x.replace(',', '').split('.')[0]) for x in numbers]
    else:
        return numbers[0]