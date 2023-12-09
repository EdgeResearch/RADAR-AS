import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

node_range = [0.10, 0.20, 0.30]

markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

path = "test/test_sa_4/test_sa_4_2_results/"
df1 = pd.read_csv(path + 'test_1.csv')
df2 = pd.read_csv(path + 'test_2.csv')
df3 = pd.read_csv(path + 'test_3.csv')
df4 = pd.read_csv(path + 'test_4.csv')
df5 = pd.read_csv(path + 'test_5.csv')
df6 = pd.read_csv(path + 'test_6.csv')
df7 = pd.read_csv(path + 'test_7.csv')
df8 = pd.read_csv(path + 'test_8.csv')
df9 = pd.read_csv(path + 'test_9.csv')
df10 = pd.read_csv(path + 'test_10.csv')
df11 = pd.read_csv(path + 'test_11.csv')
df12 = pd.read_csv(path + 'test_12.csv')
df13 = pd.read_csv(path + 'test_13.csv')
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)


x_values = []
y_values = []

for i in range(len(node_range)):
    x = df.loc[df['Node Range'] == node_range[i]]
    x_values.append(x.loc[:, "Network Polarization"])
    y_values.append(x.loc[:, "Virality"])

fig=plt.figure(figsize=(10, 5))
plt.rcParams.update({'font.size': 13})
ax=plt.subplot(111)

for i in range (len(node_range)):
    if (i > 4 and i < 10):
        ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=node_range[i], color = colorarray[i])
    else:
        ax.plot(x_values[i], y_values[i], markers[i], label=node_range[i], color = colorarray[i])


plt.ylabel("Virality (Global Cascade fraction)")
plt.xlabel("Pn (Network Polarization)")

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Node Range")
plt.grid(visible=True,linewidth=0.2)

filepath = Path(path + 'test_sa_4_3_T342.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)




