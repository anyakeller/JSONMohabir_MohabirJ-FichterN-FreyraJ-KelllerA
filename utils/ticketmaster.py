import urllib2, json, requests, dateutil.parser, sorts
from requests import auth
from requests.auth import HTTPBasicAuth

#
#    Input: Single word query
#  Returns: List of events relevant to the query in New York and information separated in a list of entries
#
#           [organization, event, performance, url, time, ticket type, price, seat]
#
def ticketmaster(query):

   #yq = query.split("")[0]

    fullList = []

    link = "https://app.ticketmaster.com/discovery/v2/events.json?keyword="+query+"&dmaId=345&apikey=pH93aoYEABgaNXBfcWGS5fS9cid3QuAw"
    u = urllib2.urlopen(link)
    response = u.read()
    data = json.loads(response)
    events = data['_embedded']['events']

    for i in events:

        orgName = "Ticketmaster"
        eventName = i['name']
        perfName = i['name']
        url = i['url']
        time = i['dates']['start']['localDate']
        if(i['dates']['start']['timeTBA']):
            time += " Time TBA"
        elif(i['dates']['start']['noSpecificTime']):
            time += " Time N/A"
        else:
            time = i['dates']['start']['dateTime']

        ticket_type = "N/A"
        price = "N/A"
        seat = "N/A"
        if('priceRanges' in i):
            for p in i['priceRanges']:
                entry = []
                ticket_type = p['type']
                price = round(float(p['min']),2)

                entry.append(orgName)
                entry.append(eventName)
                entry.append(perfName)
                entry.append(url)
                entry.append(dateutil.parser.parse(time))
                entry.append(ticket_type)
                entry.append(price)
                entry.append(seat)

                fullList.append(entry)
                
        else:
            
            entry.append(orgName)
            entry.append(eventName)
            entry.append(perfName)
            entry.append(url)
            entry.append(time)
            entry.append(ticket_type)
            entry.append(999999) # let undefined prices sink to the bottom
            entry.append(seat)

            fullList.append(entry)


    return fullList


def byPriceAsc(query):

    orderedList = []
    fullList = ticketmaster(query)

    orderedList = sorted(fullList, key=lambda entry: round(float(entry[6]),2))

    for i in orderedList:
        if i[6] == 999999:
            i[6] = "N/A: Price not Defined"

    return orderedList


def byPriceDes(query):

    orderedList = []
    fullList = ticketmaster(query)

    orderedList = sorted(fullList, key=lambda entry: round(float(entry[6]),2))

    for i in orderedList:
        if i[6] == 999999:
            i[6] = "N/A: Price not Defined"

    return orderedList

def byAlphaEvent(query):

    orderedList = []
    fullList = ticketmaster(query)

    orderedList = sorted(fullList, key=lambda entry: round(float(entry[6]),2))

    for i in orderedList:
        if i[6] == 999999:
            i[6] = "N/A: Price not Defined"

    return orderedList


def byAlphaPerf(query):

    orderedList = []
    fullList = ticketmaster(query)

    orderedList = sorted(fullList, key=lambda entry: round(float(entry[6]),2), reverse=True)

    for i in orderedList:
        if i[6] == 999999:
            i[6] = "N/A: Price not Defined"

    return orderedList

def priceRange(olist,minP,maxP):

    flist = olist
    orderedList = []
    
    for i in flist:
        if i[6] != "N/A: Price notDefined":
            if i[6] >= minP and i[6] <= maxP:
                orderedList.append(i)
        else:
            orderedList.append(i)

    return orderedList

## TESTING ##

def main():
    fullList = ticketmaster("music")
    orderedList = sorts.byDateAsc(fullList)
    priceRange = sorts.priceRange(orderedList,10,140)
    for i in priceRange:
        print(i[1] + " | Price:" + str(i[6]) + " | Time:" + str(i[4]) )


main()
