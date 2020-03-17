from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import os

def getBusData():
    r = urlopen(
        'http://www.mvg-live.de/ims/dfiStaticAnzeige.svc?haltestelle=Josef-Frankl-Stra%dfe&ubahn=checked&bus=checked&tram=checked&sbahn=checked');
    soup = BeautifulSoup(r, "html.parser");

    data = []
    table = soup.find('table', attrs={'class': 'departureTable departureView'})

    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    return data

def getSbahnData():
    r = urlopen(
        'https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=3938&protocol=https:&rt=1&input=M%FCnchen-Feldmoching%238004147&boardType=dep&time=actual&productsFilter=11111&start=yes&');
    soup = BeautifulSoup(r, "html.parser");

    data2 = []
    table = soup.find_all('tr', attrs={'id': lambda L: L and 'journeyRow' in L})
    for row in table:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data2.append([ele for ele in cols if ele])  # Get rid of empty values

    from datetime import datetime
    curTime = datetime.now().strftime('%H:%M')

    res = list()
    for entry in data2:
        tmp_res = list()
        tdelta = 0
        if (entry[2].startswith("München Flughafen")):
            tmp_res.append(entry[1])
            tmp_res.append("Flughafen")
            if (len(entry) > 4):
                tdelta = str(
                    (datetime.strptime(entry[4], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds / 60)[:-2]
            else:
                tdelta = str((datetime.strptime(entry[0], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds / 60)[
                         :-2]
            tmp_res.append(tdelta)
            res.append(tmp_res)
        elif (entry[2].startswith("München") and not entry[2].startswith("München Flughafen") and entry[1].startswith("S")):
            tmp_res.append(entry[1])
            tmp_res.append("Ostbahnhof")
            if (len(entry) > 4):
                tdelta = str(
                        (datetime.strptime(entry[4], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds / 60)[:-2]
            else:
                tdelta = str((datetime.strptime(entry[0], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds / 60)[
                         :-2]
            tmp_res.append(tdelta)
            res.append(tmp_res)
    return res
