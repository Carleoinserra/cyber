from flask import Flask, request, make_response, render_template, session
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import mysql.connector
import random
# Configurazione del database MySQL
db_config = {
    'user': 'root',
    'password': 'Test1234',
    'host': 'localhost',
    'database': 'mydatabase',
    'raise_on_warnings': True
}

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chiave segreta per firmare la sessione

@app.route('/')
def index():
    username = session.get('username')
    last_access = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ottenere l'ultimo accesso all'interno di index()
    session['last_access'] = last_access
    if username:
        save_access(username, last_access)  # Inserisce il record nel database
        return f'Ciao {username}! Ultimo accesso: {last_access} <br><a href="/accessi">Visualizza accessi</a>'
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    if username:
        session['username'] = username
        session['last_access'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_access(username, session['last_access'])
        return f'Login effettuato come {username}. <br><a> href="/accessi">Visualizza accessi</a>'
    else:
        return 'Nome utente mancante. Impossibile effettuare il login.'

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('last_access', None)
    return 'Logout effettuato.'

@app.route('/accessi')
def accessi():
    access_dates = get_access_dates()  # Ottiene le date di accesso dal database
    return render_template('accessi.html', access_dates=access_dates)


import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

@app.route('/istogramma')
def istogramma():
    access_dates = get_access_dates()  # Ottiene le date di accesso dal database
    users = get_users()
    # Estrai gli utenti distinti dalla lista di tuple access_dates
    users = list(set([date[1] for date in access_dates]))
    # Crea una lista di colori per gli utenti
    colors = plt.cm.get_cmap('tab20')(range(len(users)))
    # Estrai gli orari degli accessi per ogni utente
    access_times = [date[0].time() for date in access_dates]

    # Converti gli orari in formato HH:MM
    access_times_str = [time.strftime('%H:%M') for time in access_times]


    # Estrai gli orari degli accessi per ogni utente
    access_times = [date[0].time() for date in access_dates]

    # Conta il numero di accessi per ogni utente e crea i dati per il grafico a barre
    access_counts = []
    for user in users:
        count = sum(1 for date, username in access_dates if username == user)
        access_counts.append(count)

    # Genera il grafico a barre
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(users, access_counts, color=colors)

    plt.xlabel('Utente')
    plt.ylabel('Numero di Accessi')
    plt.title('Grafico degli Accessi per Utente')

    # Istogramma del traffico per ora
    plt.subplot(1, 2, 2)
    bins = 24
    plt.hist(access_times_str, bins=bins, edgecolor='black')

    plt.xlabel('Ora')
    plt.ylabel('Numero di Accessi')
    plt.title('Traffico per Ora')

    plt.xticks(rotation=45)
    plt.xlim(0, 23)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return render_template('istogramma.html', image_base64=image_base64)












def save_access(username, access_date):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = "INSERT INTO accessi (username, access_date) VALUES (%s, %s)"
        data = (username, access_date)
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
        connection.close()
        print("Record inserito correttamente nel database.")
    except mysql.connector.Error as error:
        print("Errore durante il salvataggio dell'accesso nel database:", error)

def get_access_dates():
    access_dates = []
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        select_query = "SELECT access_date, username FROM accessi"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            access_date = row[0]
            username = row[1]
            access_dates.append((access_date, username))
        cursor.close()
        connection.close()
        return access_dates
    except mysql.connector.Error as error:
        print("Errore durante il recupero delle date di accesso dal database:", error)
        return access_dates

def get_users():
    users = []
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        select_query = "SELECT DISTINCT username FROM accessi"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            users.append(row[0])
        cursor.close()
        connection.close()
        return users
    except mysql.connector.Error as error:
        print("Errore durante il recupero degli utenti dal database:", error)
        return users

if __name__ == '__main__':
    app.run()
