from flask import Flask, request, render_template, redirect, jsonify, render_template_string

from analyzer   import Analyzer

from pathlib    import Path
from time       import time
from json       import loads

from utility    import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@app.post('/analyze')
def analyze():

    data = str(request.data)[2:-1]
    headers = request.headers

    success, why, errcode = validate('headers', headers)
    if not success: return why, errcode

    success, why, errcode = validate('data', data)
    if not success: return why, errcode

    analyzer = Analyzer('Undefined', data)

    try:
        returndata = analyzer.analyze()
    
    except BaseException as Error:
        return f'Internal Server Error [{Error}] Try refactoring the data', 400
    
    sequence = generate_sequence(returndata)

    while Path(f'./templates/reports/{sequence}.html').exists():
        sequence = generate_sequence(returndata)

    storedata(sequence, returndata, json_conv_html(loads(returndata), sequence))
    storesource(sequence, data.replace('\\n', '\n'))
    
    return jsonify({'Sequence': sequence})

@app.route('/report')
def fetchreport():
    sequence = request.args.get('seq')

    try:
        assert sequence != None
        assert len(sequence) == 12
    
    except:
        return 'Invalid or Missing Parameter: seq', 422
    
    if not Path(f'./reports/{sequence}.html').exists():
        # if sequence in processes():
            # return f'Report is in Generation: Analyzation in Process', 200
        
        # else:
        return 'Internal Server Error: Report not Found', 500
    
    return render_template_string(open(f'./reports/{sequence}.html', 'r').read()), 200

@app.route('/json')
def fetchjson():
    sequence = request.args.get('seq')

    try:
        assert sequence != None
        assert len(sequence) == 12
    
    except:
        return 'Invalid or Missing Parameter: seq', 422
    
    if not Path(f'./json/{sequence}.json').exists():
        # if sequence in processes():
            # return f'Report is in Generation: Analyzation in Process', 200
        
        # else:
        return 'Internal Server Error: JSON Analysis not Found', 500
    
    return jsonify(loads(open(f'./json/{sequence}.json', 'r').read())), 200

@app.route('/source')
def fetchsource():
    from html import escape
    sequence = request.args.get('seq')

    try:
        assert sequence != None
        assert len(sequence) == 12
    
    except:
        return 'Invalid or Missing Parameter: seq', 422
    
    if not Path(f'./sources/{sequence}.txt').exists():
        # if sequence in processes():
            # return f'Report is in Generation: Analyzation in Process', 200
        
        # else:
        return 'Internal Server Error: JSON Analysis not Found', 500
    
    return render_template_string(
        "<pre><code>" +
            escape(open(f'./sources/{sequence}.txt', 'r').read()) 
        + "</code></pre>"
    ), 200
        
if __name__ == '__main__': app.run()