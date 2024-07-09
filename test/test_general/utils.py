import pandas as pd
import json

def setup_data_for_chart(dataframe):
    print(">> Stampo il dataframe:")
    print(dataframe)
    thresholds = dataframe["Thresholds"].unique().tolist()  # Recupera i valori univoci di threshold
    network_polarization = dataframe["Network Polarization"].unique().tolist()  # Recupera i valori univoci di Network Polarization
    datasets = []
    for threshold in thresholds:
        dataset = []
        for index, row in dataframe.iterrows():
            if row["Thresholds"] == threshold:
                dataset.append(row["Virality"])
        datasets.append(dataset)

    data_for_chart = {"thresholds" : thresholds, "datasets" : datasets, "network_polarization" : network_polarization}
    return json.dumps(data_for_chart)







if __name__ == "__main__":
    dataframe = pd.read_csv("test_general_results/test_general_1.csv")
    setup_data_for_chart(dataframe)
