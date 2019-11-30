from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import os

if __name__ == '__main__':
    try:
        while True:
            ## your code, typically one function call

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

            i = 0
            for entry in data:
                if len(entry) > 1 and (entry[1] != "Dachau Bf." and entry[1] != "Karlsfelder Str."):
                    if (len(entry)==3):
                        print(entry[0], "to", entry[1], "in", entry[2], "mins")
                    else:
                        print("#####", entry[0], "at", entry[1], "LIVE!")
                i+=1
                if (i>7):
                    break

            r = urlopen(
                'http://www.mvg-live.de/ims/dfiStaticAnzeige.svc?haltestelle=Feldmoching+Bf.&ubahn=&bus=&tram=&sbahn=checked');
            soup = BeautifulSoup(r, "html.parser");

            # data = []
            # table = soup.find('table', attrs={'class': 'departureTable departureView'})
            # rows = table.find_all('tr')
            # for row in rows:
            #     cols = row.find_all('td')
            #     cols = [ele.text.strip() for ele in cols]
            #     data.append([ele for ele in cols if ele])  # Get rid of empty values
            #
            # for entry in data:
            #     if len(entry) > 1: #and (entry[1] != "München Ost"):
            #         if (len(entry)==3):
            #             print(entry[0], "to", entry[1], "in", entry[2], "mins")
            #         else:
            #             print("#####", entry[0], "at", entry[1], "PLANNED!")

            r = urlopen('https://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=3938&protocol=https:&rt=1&input=M%FCnchen-Feldmoching%238004147&boardType=dep&time=actual&productsFilter=11111&start=yes&');
            soup = BeautifulSoup(r, "html.parser");
            print("##### Feldmoching Bahnhof LIVE!")

            data2=[]
            table = soup.find_all('tr', attrs={'id': lambda L: L and 'journeyRow' in L})
            for row in table:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data2.append([ele for ele in cols if ele])  # Get rid of empty values

            from datetime import datetime
            curTime = datetime.now().strftime('%H:%M')

            for entry in data2:
                if ("Flughafen" in entry[2]):
                    if (len(entry)>4):
                        try:
                            tdelta = str((datetime.strptime(entry[4], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds/60)[:-2]
                            print("S1 to #Airport# scheduled:", entry[0], "-->", entry[4], "in", tdelta, "mins")
                        except ValueError:
                            print("S1 to #Airport# scheduled:",entry[0], "-->", entry[4])
                    else:
                        tdelta = str((datetime.strptime(entry[0], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds/60)[:-2]
                        print("S1 to #Airport# scheduled:", entry[0], "in", tdelta, "mins")
                elif ("Ost" in entry[2]):
                    if (len(entry) > 4):
                        try:
                            tdelta = str((datetime.strptime(entry[4], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds/60)[:-2]
                            print("S1 to #City# scheduled:", entry[0], "-->", entry[4], "in", tdelta, "mins")
                        except ValueError:
                            print("S1 to #City# scheduled:",entry[0], "-->", entry[4])
                    else:
                        tdelta = str((datetime.strptime(entry[0], '%H:%M') - datetime.strptime(curTime, '%H:%M')).seconds/60)[:-2]
                        print("S1 to #City# scheduled:", entry[0], "in", tdelta, "mins")

            time.sleep(30)
            os.system("clear")

    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        print("Press Enter to continue ...")
        input()