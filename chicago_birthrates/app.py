from flask import Flask, render_template
import requests
import csv
import StringIO
import os
import math

app = Flask(__name__) #what flask need to fire up an application (instantiating flask object and name it 'app')

SOCRATA_DATA_URL = 'https://data.cityofchicago.org/api/views/4arr-givg/rows.csv?accessType=DOWNLOAD'
#convention to use all uppercase to represent a constant

@app.route('/') #whatever the functionm it will be available at '/'
def index():

    data = open(os.path.join(os.path.dirname(__file__), 'data', 'chicago-birthrates-1999-2009.csv'), 'r')
    #access a file in the data directory called 'chicago-birthrates-1999-2009.csv' ('r' is for read only)
    
    # Uncomment the next 2 lines to use live data
    # response = requests.get(SOCRATA_DATA_URL) # Get data
    # data = StringIO.StringIO(response.text) # Magic Python code to convert text

    # Build up data structure like ('Edgewater', (2008, 500), (2009, 450), ... )
    context = {
        'max': 0,
        'min': 100,
        'table': [],
    }
    """
    Will create a loop  over 'chicago-birthrates-1999-2009.csv', take the data, extract the part we need and put it in a table. 
    DictReader will take the first row as a header and other rows will be part of the dictionary.

    """
    for row in csv.DictReader(data): # row is a dict like: {'Community Area Name': 'EDGEWATER', 'Births 2005': '709'}
        table_row = [ row['Community Area Name'], ] #create a list with first position 'Community area'
        for year in range(1999, 2010):
            key = 'Birth Rate %s' % year # Construct key name
            value = float(row[key]) #convert the key value to a number
            table_row.append( (year, value) )
            if value > context['max']: 
                context['max'] = value
                context['chart_max'] = math.ceil(value + 1)
                context['max_community'] = row['Community Area Name']
                context['max_year'] = year
            if value < context['min']:
                context['min'] = value
                context['chart_min'] = math.floor(value - 1)
                context['min_community'] = row['Community Area Name']
                context['min_year'] = year
        context['table'].append(table_row)
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.debug=True
    app.run(port=5001)
