#rotas do site aqui

from app import app
from flask import render_template, request
import pandas as pd

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

