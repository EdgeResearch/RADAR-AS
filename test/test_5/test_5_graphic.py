import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

opinion_metric_steps = opinion_metric_steps = [0.01, 0.04, 0.08, 0.10 , 0.12, 0.16, 0.20, 0.33, 0.66]

markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

path = "test/test_5/test_5_3_results/"
df1 = pd.read_csv(path + 'test_5_1.csv')
df2 = pd.read_csv(path + 'test_5_2.csv')
df3 = pd.read_csv(path + 'test_5_3.csv')
df4 = pd.read_csv(path + 'test_5_4.csv')
df = pd.concat([df1, df2, df3, df4], ignore_index=True)


x_values = []
y_values = []

for i in range(len(opinion_metric_steps)):
    x = df.loc[df['Opinion Metric Step'] == opinion_metric_steps[i]]
    x_values.append(x.loc[:, "Network Polarization"])
    y_values.append(x.loc[:, "Virality"])

fig=plt.figure(figsize=(12, 5))
plt.rcParams.update({'font.size': 13})
ax=plt.subplot(111)

for i in range (len(opinion_metric_steps)):
    if (i > 4 and i < 10):
        ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=opinion_metric_steps[i], color = colorarray[i])
    else:
        if (i == 3):
            ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=opinion_metric_steps[i], color = "green")
        else:
            ax.plot(x_values[i], y_values[i], markers[i], label=opinion_metric_steps[i], color = colorarray[i])
    
plt.ylabel("Virality (Global Cascade fraction)")
plt.xlabel("Pn (Network Polarization)")

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Opinion Metric Step")
plt.grid(visible=True,linewidth=0.2)

filepath = Path(path + 'test_5_3_T414.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)




