from flask import Flask
import getData2
from tabulate import tabulate

app = Flask(__name__)

@app.route("/")
def createTable():
    busdata = getData2.getBusData()[1:6]
    sbahndata = getData2.getSbahnData()[:5]
    alldata = busdata + sbahndata
    html_page = tabulate(alldata, headers=["Linie", "Ziel", "Abfahrt in [min]"], tablefmt='html')
    html_page = '<table width="800" style="font-size:40">' + html_page[7:]
    return html_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)