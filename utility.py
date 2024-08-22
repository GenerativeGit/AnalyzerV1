from hashlib import sha256

def json_conv_html(json_data, sequence_id):
    rmf = lambda line: line[1:] if line[0] == '-' else line

    html = """
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
            body {
                font-family: 'Roboto Mono', monospace;
                font-size: 16px;
            }
            .card {
                background-color: #f7f7f7;
                padding: 20px;
                margin: 20px;
                border: 1px solid #ddd;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .card-title {
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 10px;
            }
            .answer {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
    
            <h2 align=center> EthereumVM Contract Analyzer | Stealth Research </h2>
            <p align=center> Sequence ID: """ + f"{sequence_id} </p>"
    
    for item in json_data:
        if item["title"] != "Compliance":
            html += """
            <div class="card">
                <h2 class="card-title">{}</h2>
                <ul>
            """.format(item["title"])
            for answer in item["answers"]:
                html += """
                <li class="answer">{}</li>
                """.format(rmf(answer))
            html += """
                </ul>
            </div>
            """
   
    html += """
    </body>
    </html>
    """
    
    return html

def storedata(sequence, data, html):
    with open(f'./json/{sequence}.json', 'w') as seqjson:
        seqjson.write(data)
    
    with open(f'./reports/{sequence}.html', 'w') as seqhtml:
        seqhtml.write(html)

def generate_sequence(data: str):
    sequence = sha256(data.encode()).hexdigest()
    return sequence[:12]

def processes():
    with open('processes.txt') as file:
        processes = file.readlines()
        
    return list(map(lambda x: x.replace('\n', str()), processes))

def validate(type: str, value: any):
    if type == 'headers':
        if not value.get('Content-Type') == 'application/text':
            return False, 'Invalid Header: Content-Type. Supported Content-Type: "application/text"', 415
        
        if not value.get('Authorization') == 'f9b8e6e2f3b932cf5650986ab19a5db1aa1046109fe1912528942789b7c2675b':
            return False, 'Invalid Authorization: Key Not Valid', 403
    
    # if type == 'data':
        # if not value.replace('\n', '\\n').count('\n') <= 750:
            # return False, 'Code Size Too Large to Handle', 400
        
    return True, str(), 200

def storesource(sequence, source):
    with open(f'./sources/{sequence}.txt', 'w') as sourcefile:
        sourcefile.write(source)