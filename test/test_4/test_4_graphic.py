import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

tresholds = [0.150, 0.174, 0.198, 0.222, 0.246, 0.270, 0.294, 0.318, 0.342, 0.366, 0.390, 0.414]

markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

path = "test/test_4/test_4_1_results/"
df1 = pd.read_csv(path + 'test_4_1.csv')
df2 = pd.read_csv(path + 'test_4_2.csv')
df3 = pd.read_csv(path + 'test_4_3.csv')
df4 = pd.read_csv(path + 'test_4_4.csv')
df = pd.concat([df1, df2, df3, df4], ignore_index=True)


x_values = []
y_values = []

for i in range(len(tresholds)):
    x = df.loc[df['Treshold'] == tresholds[i]]
    x_values.append(x.loc[:, "Network Polarization"])
    y_values.append(x.loc[:, "Virality"])

fig=plt.figure(figsize=(10, 5))
plt.rcParams.update({'font.size': 13})
ax=plt.subplot(111)

for i in range (len(tresholds)):
    if (i > 4 and i < 10):
        ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=tresholds[i], color = colorarray[i])
    else:
        ax.plot(x_values[i], y_values[i], markers[i], label=tresholds[i], color = colorarray[i])


plt.ylabel("Virality (Global Cascade fraction)")
plt.xlabel("Pn (Network Polarization)")

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="\u03B8 (threshold)")
plt.grid(visible=True,linewidth=0.2)

filepath = Path(path + 'test_4_1_ECF20.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)




