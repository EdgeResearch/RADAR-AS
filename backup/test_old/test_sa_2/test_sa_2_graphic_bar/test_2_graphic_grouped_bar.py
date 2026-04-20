import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np 
import pandas as pd
from matplotlib.lines import Line2D

colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro', 'dimgrey', 'grey', 'darkgrey']

tresholds = [0.270, 0.342, 0.414]

path = "test/test_3/test_3_1_results/"
df1 = pd.read_csv(path + 'test_3_1.csv')
df2 = pd.read_csv(path + 'test_3_2.csv')
df3 = pd.read_csv(path + 'test_3_3.csv')
df4 = pd.read_csv(path + 'test_3_4.csv')
df_no_sa_0 = pd.concat([df1, df2, df3, df4], ignore_index=True)

path = "test/test_3/test_3_2_results/"
df1 = pd.read_csv(path + 'test_3_1.csv')
df2 = pd.read_csv(path + 'test_3_2.csv')
df3 = pd.read_csv(path + 'test_3_3.csv')
df4 = pd.read_csv(path + 'test_3_4.csv')
df_no_sa_15 = pd.concat([df1, df2, df3, df4], ignore_index=True)

path = "test/test_3/test_3_3_results/"
df1 = pd.read_csv(path + 'test_3_1.csv')
df2 = pd.read_csv(path + 'test_3_2.csv')
df3 = pd.read_csv(path + 'test_3_3.csv')
df4 = pd.read_csv(path + 'test_3_4.csv')
df_no_sa_27 = pd.concat([df1, df2, df3, df4], ignore_index=True)

path = "test/test_sa_1/test_sa_1_3_results/"
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
df_0 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)

path = "test/test_sa_2/test_sa_2_1_results/"
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
df_15 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)

path = "test/test_sa_2/test_sa_2_2_results/"
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
df_27 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df9, df10, df11, df12, df13], ignore_index=True)




scores_no_sa_0 = []
scores_no_sa_15 = []
scores_no_sa_27 = []
scores_sa_0 = []
scores_sa_15 = []
scores_sa_27 = []
df = [df_no_sa_0, df_no_sa_15, df_no_sa_27, df_0, df_15, df_27]


for i in range(len(tresholds)):
    for j in range(len(df)):
        x = df[j].loc[df[j]['Treshold'] == tresholds[i]]
        y = x.loc[:, "Virality"]
        y = np.mean(y)

        if (j == 0):
            scores_no_sa_0.append(y)
        elif(j == 1):
            scores_no_sa_15.append(y)
        elif(j == 2):
            scores_no_sa_27.append(y)
        elif(j == 3):
            scores_sa_0.append(y)
        elif(j == 4):
            scores_sa_15.append(y)
        elif(j == 5):
            scores_sa_27.append(y)

x = np.arange(len(tresholds))  # the label locations
width = 0.1  # the width of the bars

r1 = x
r2 = [x + width+0.03 for x in r1]
r3 = [x + width+0.03 for x in r2]
r4 = [x + width+0.03 for x in r3]
r5 = [x + width+0.03 for x in r4]
r6 = [x + width+0.03 for x in r5]

fig, ax = plt.subplots()
plt.rcParams.update({'font.size': 10})

rects1 = ax.bar(r1, scores_no_sa_0, width, label='No sa PO = 0', color='black', hatch='//')
rects2 = ax.bar(r2, scores_sa_0, width, label='sa PO = 0', color='dimgrey', hatch='x', zorder=0)
rects3 = ax.bar(r3, scores_no_sa_15, width, label='No sa PO = 0.15', color='grey', hatch='xx')
rects4 = ax.bar(r4, scores_sa_15, width, label = "sa PO = 0.15", color="darkgrey", hatch='/'), 
rects5 = ax.bar(r5, scores_no_sa_27, width, label = "No sa PO = 0.27", color='darkslategrey', hatch='*'), 
rects6 = ax.bar(r6, scores_sa_27, width, label = "sa PO = 0.27", color='lightslategrey', hatch='+'), 

threshold = 0.50
linea=plt.axhline(y=threshold,linewidth=1, color='k',linestyle='--', label = "Virality 0.5")
plt.ylim([0,0.9])
ax.yaxis.set_tick_params(labelsize=15)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Virality', fontsize = 15)
#ax.set_title('Comparison between the best results', fontweight='bold')
width += (0.2)
ax.set_xticks(x+width)
ax.set_xticklabels(tresholds,rotation=45, fontsize = 15)
ax.set_xlabel("\u03B8 (threshold)", fontsize = 15)

colors = ['black']
lines = [Line2D([0], [0], color=c, linewidth=1, linestyle='--') for c in colors]
labels = ['Single-view']
ax.legend()
#ax.legend([rects1, rects2, rects3, rects4, rects5, rects6, linea],('No sa PO = 0.27','sa PO = 0.27', 'Virality 0.5'))

fig.set_figheight(7)
fig.set_figwidth(14)
fig.tight_layout()

filepath = Path('test/test_sa_2/test_sa_2_graphic_bar/test_sa_po_difference.png')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
fig.savefig(filepath)

plt.show()
