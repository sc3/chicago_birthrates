from flask import Flask, render_template
import requests
import csv
import StringIO
import os

app = Flask(__name__)

SOCRATA_DATA_URL = 'https://data.cityofchicago.org/api/views/4arr-givg/rows.csv?accessType=DOWNLOAD'

@app.route('/')
def index():

    data = open(os.path.join(os.path.dirname(__file__), 'data', 'chicago-birthrates-1999-2009.csv'), 'r')
    
    # Uncomment the next 2 lines to use live data
    # response = requests.get(SOCRATA_DATA_URL) # Get data
    # data = StringIO.StringIO(response.text) # Magic Python code to convert text

    # Build up data structure like ('Edgewater', (2008, 500), (2009, 450), ... )
    table = []
    for row in csv.DictReader(data): # row is a dict like: {'Community Area Name': 'EDGEWATER', 'Births 2005': '709'}
        table_row = [ row['Community Area Name'], ]
        for year in range(1999, 2010):
            key = 'Birth Rate %s' % year # Construct key name
            table_row.append( row[key] )
        table.append(table_row)
    #import ipdb; ipdb.set_trace()
    return render_template('index.html', table=table)

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
