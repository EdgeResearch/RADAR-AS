import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd
import numpy as np

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

labels = [str(i*10) for i in range(11)]

path = "test/test_6/test_6_3_results/"
df = pd.read_csv(path + 'test_6_3.csv')

labels = [str(i*10) for i in range(11)]

agents = {
    "A Agents": np.array(df["A Agents"]),
    "B Agents": np.array(df["B Agents"]),
    "Neutral Agents" : np.array(df["Neutral Agents"])
}

width = 0.5

fig, ax = plt.subplots(1, figsize=(12, 7))

ind = np.arange(11) 

vector = np.vectorize(np.float64)
a = np.array(df["A Agents"])
b = np.array(df['B Agents'])
n = np.array(df['Neutral Agents'])
a_var = np.array(df["A Var"])
b_var = np.array(df["B Var"])
n_var = np.array(df["N Var"])

plt.xticks(ind, ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'), fontsize=15)
plt.yticks(np.arange(0, 110, 10), fontsize=15)


ax.bar(labels, a , color='#FF7518', yerr = a_var)
ax.bar(labels, n, bottom = a, color = "#808080", yerr = n_var)
ax.bar(labels, b, bottom = n+a, color= "#0000FF", yerr = b_var)


plt.rcParams.update({'font.size': 15})
plt.rc('axes', titlesize=1)

plt.ylabel("Number of basic agents", fontsize=30)
plt.xlabel("Tick", fontsize=30)
plt.legend(['A Agents', 'Neutral Agents', 'B Agents',], ncol = 3, bbox_to_anchor=([1, 1, 0, 0]))


filepath = Path(path + 'test_6_3_T414.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)