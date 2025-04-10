from flask import Flask, render_template, request
import pandas as pd
import os
from flask import send_file
from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
import json


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transactions = None

    if request.method == 'POST':
        files = request.files.getlist('file')
        sender_name = request.form['sender']

        if files and sender_name:
            dfs = []

            for file in files:
                df = pd.read_csv(file)
                dfs.append(df)

            all_data = pd.concat(dfs, ignore_index=True)

            filtered = all_data[all_data['Descrição'].str.contains(sender_name, case=False, na=False)]
            transactions = filtered.to_dict(orient='records')

    return render_template('index.html', transactions=transactions)
    

@app.route('/gerar-pdf', methods=['POST'])
def gerar_pdf():
    import json
    data = json.loads(request.form['data'])

    rendered = render_template('pdf_template.html', transactions=data)

    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)

    if pisa_status.err:
        return "Erro ao gerar PDF", 500

    pdf.seek(0)
    return send_file(pdf, as_attachment=True, download_name="transacoes_filtradas.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)