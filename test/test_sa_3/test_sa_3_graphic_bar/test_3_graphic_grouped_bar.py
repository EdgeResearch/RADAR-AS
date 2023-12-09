import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np 
import pandas as pd
from matplotlib.lines import Line2D

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

tresholds = [0.270, 0.342, 0.414]
nrsb = [0.05, 0.10, 0.20]

path = "test/test_1/test_1_results/"
df1 = pd.read_csv(path + 'test_1_1.csv')
df2 = pd.read_csv(path + 'test_1_2.csv')
df3 = pd.read_csv(path + 'test_1_3.csv')
df4 = pd.read_csv(path + 'test_1_4.csv')
df_no_sa = pd.concat([df1, df2, df3, df4], ignore_index=True)


path = "test/test_sa_3/test_sa_3_1_results/"
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
df_5 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)

path = "test/test_sa_3/test_sa_3_2_results/"
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
df_10 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)

path = "test/test_sa_3/test_sa_3_3_results/"
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
df_20 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)


scores_no_sa = []
scores_sa_5 = []
scores_sa_10 = []
scores_sa_20 = []
df = [df_no_sa, df_5, df_10, df_20]

for i in range(len(tresholds)):
    for j in range(len(df)):
        if j == 0:
            x = df[j].loc[df[j]['Treshold'] == tresholds[i]]
        else:
            x = df[j].loc[df[j]['Node Range Static B'] == nrsb[i]]
        y = x.loc[:, "Virality"]
        y = np.mean(y)

        if (j == 0):
            scores_no_sa.append(y)
        elif (j == 1):
            scores_sa_5.append(y)
        elif (j == 2):
            scores_sa_10.append(y)
        elif (j == 3):
            scores_sa_20.append(y)


x = np.arange(len(tresholds))  # the label locations
width = 0.2  # the width of the bars

r1 = x
r2 = [x + width+0.03 for x in r1]
r3 = [x + width+0.03 for x in r2]
r4 = [x + width+0.03 for x in r3]

fig, ax = plt.subplots()
plt.rcParams.update({'font.size': 15})

rects1 = ax.bar(r1, scores_no_sa, width, label='No sa', color='black', hatch='//')
rects2 = ax.bar(r2, scores_sa_5, width, label='sa nrsb = 0.5', color='dimgrey', hatch='x', zorder=0)
rects3 = ax.bar(r3, scores_sa_10, width, label='sa nrsb = 0.10', color='grey', hatch='xx')
rects4 = ax.bar(r4, scores_sa_20, width, label = "sa nrsb = 0.20", color="darkgrey", hatch='/'), 
threshold = 0.50
linea=plt.axhline(y=threshold,linewidth=1, color='k',linestyle='--')
plt.ylim([0,0.9])
ax.yaxis.set_tick_params(labelsize=15)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Virality', fontsize = 15)
#ax.set_title('Comparison between the best results', fontweight='bold')
width += (0.15)
ax.set_xticks(x+width)
ax.set_xticklabels(tresholds,rotation=45, fontsize = 15)
ax.set_xlabel("\u03B8 (threshold)", fontsize = 15)
#ax.legend()
colors = ['black']
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='--') for c in colors]
labels = ['Single-view']
ax.legend([rects1,rects2,rects3,rects4,linea],('No sa','sa NRSB = 0.05', 'sa NRSB = 0.10', 'sa NRSB = 0.20','Virality 0.5'))


fig.set_figheight(6)
fig.set_figwidth(12)
fig.tight_layout()

filepath = Path('test/test_sa_3/test_sa_3_graphic_bar/test_sa_nrsb_difference.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)

plt.show()
