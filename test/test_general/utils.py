import datetime
import io
import json
import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import pandas as pd


# Classe per la gestione e redirect dell'output su terminale e file di log
class Tee:
    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.stdout = sys.stdout
        self.string_buffer = io.StringIO()

    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)
        self.string_buffer.write(message)

    def flush(self):
        self.stdout.flush()
        self.file.flush()
        self.string_buffer.flush()

    def close(self):
        self.file.close()
        self.string_buffer.close()

    def get_value(self):
        return self.string_buffer.getvalue()



# Classe per la gestione manuale dell'output su terminale e file di log
class LogManager:
    def __init__(self, filepath):
        self.filepath = filepath
        # Assicurarsi che il file esista e sia vuoto all'inizio
        with open(self.filepath, 'w') as file:
            pass

    def insert_line(self, message):
        """Inserisce una nuova riga nel file di log."""
        with open(self.filepath, 'a') as file:
            file.write(message + '\n')

    def get_contents(self):
        """Recupera tutto il contenuto testuale del file di log."""
        with open(self.filepath, 'r') as file:
            return file.read()

    def clear_log(self):
        """Svuota il contenuto del file di log."""
        with open(self.filepath, 'w') as file:
            pass

def setup_data_for_chart(dataframe, dataLabel):
    print(">> Stampo il dataframe:")
    print(dataframe)
    dataValues = dataframe[dataLabel].unique().tolist()  # Recupera i valori univoci di threshold
    network_polarization = dataframe["Network Polarization"].unique().tolist()  # Recupera i valori univoci di Network Polarization
    datasets = []
    for data in dataValues:
        dataset = []
        for index, row in dataframe.iterrows():
            if row[dataLabel] == data:
                dataset.append(row["Virality"])
        datasets.append(dataset)

    data_for_chart = {"thresholds" : dataValues, "datasets" : datasets, "network_polarization" : network_polarization}
    return json.dumps(data_for_chart)


def send_results(receiver_email, files):
    # Carica le variabili dal file .env
    load_dotenv()
    api_key = os.getenv('API_KEY')

    # Impostazioni SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.getenv('EMAIL_USERNAME')
    sender_password = os.getenv('EMAIL_KEY')

    # Recupera data ed ora
    string_date = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    format_date = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")

    # Creazione dell'oggetto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f'RADAR-AS - Test Result'



    # Corpo del messaggio
    body = f'Your simulation on the spread of Fake News using the RADAR-AS platform has been successfully completed on {string_date}.\nYou can find the results attached to this email.'

    msg.attach(MIMEText(body, 'plain'))



    for filename in files:

        print(filename)
        # Allegato
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)

        display_name = format_date + "_" +  str(filename).split(os.path.sep).pop()
        part.add_header('Content-Disposition', f'attachment; filename= {display_name}')

        msg.attach(part)
        attachment.close()

    # Connessione al server SMTP e invio dell'email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        server.quit()



