
import pandas as pd

# Leggi il DataFrame dal file CSV
df = pd.read_csv('test_general_sa_1.csv')

# Rinomina la colonna "Treshold" in "Thresholds"
df.drop(df.columns[0], axis=1, inplace=True)


# Salva il DataFrame modificato nello stesso file CSV
df.to_csv('test_general_sa_1.csv', index=False)

