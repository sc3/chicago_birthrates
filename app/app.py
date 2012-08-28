from flask import Flask, render_template
import requests
import csv
import StringIO
app = Flask(__name__)

SOCRATA_DATA_URL = 'https://data.cityofchicago.org/api/views/4arr-givg/rows.csv?accessType=DOWNLOAD'

@app.route('/')
def index():
    response = requests.get(SOCRATA_DATA_URL) # Get data
    response_string = StringIO.StringIO(response.text) # Magic Python code to convert text
    data = []
    for row in csv.DictReader(response_string): # row is a dict like: {'Community Area Name': 'EDGEWATER', 'Births 2005': '709'}
        data_row = [ row['Community Area Name'], ]
        for year in range(1999, 2009):
            key = 'Births %s' % year
            data_row.append( row[key] )
            data.append(data_row)
    import ipdb; ipdb.set_trace()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
