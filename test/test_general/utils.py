
import pandas as pd
import json
import sys
import io

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
        with open(self.filepath, 'a') as file:
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

if __name__ == "__main__":
    dataframe = pd.read_csv("/Users/andrea/Desktop/UNIVERSITÀ/Tirocinio/Software/RADAR-AS/test/test_general/test_general_results/test_general_2/test_general_2.csv")
    print(setup_data_for_chart(dataframe, "Nodes"))
