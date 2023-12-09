import matplotlib.pyplot as plt
from pathlib import Path 
import pandas as pd


if __name__ == "__main__":
    colorarray=['black','dimgrey','grey','darkgrey','lightgrey','darkslategrey','lightslategrey','slategrey', 'silver', 'gainsboro']

    nodes = [100,200,300,400,500]
    nodes = [75, 100, 125, 150, 175, 200, 225]

    markers = ['o-', 's--', 'D:', "^-", "v--", "o--", "s-", "D--", "^:", "v-", "o--", "s:"]

    path = "test/test_2/test_2_4_results/"
    df1 = pd.read_csv(path + 'test_2_1.csv')
    df2 = pd.read_csv(path + 'test_2_2.csv')
    df3 = pd.read_csv(path + 'test_2_3.csv')
    df4 = pd.read_csv(path + 'test_2_4.csv')
    df5 = pd.read_csv(path + 'test_2_5.csv')
    df6 = pd.read_csv(path + 'test_2_6.csv')
    df7 = pd.read_csv(path + 'test_2_7.csv')
    df8 = pd.read_csv(path + 'test_2_8.csv')
    df9 = pd.read_csv(path + 'test_2_9.csv')
    df10 = pd.read_csv(path + 'test_2_10.csv')
    df11 = pd.read_csv(path + 'test_2_11.csv')
    df12 = pd.read_csv(path + 'test_2_12.csv')
    df13 = pd.read_csv(path + 'test_2_13.csv')
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13], ignore_index=True)


    x_values = []
    y_values = []

    for i in range(len(nodes)):
        x = df.loc[df['Nodes'] == nodes[i]]
        x_values.append(x.loc[:, "Network Polarization"])
        y_values.append(x.loc[:, "Virality"])

    fig=plt.figure(figsize=(10, 5))
    plt.rcParams.update({'font.size': 15})
    ax=plt.subplot(111)

    for i in range (len(nodes)):
        if (i > 4 and i < 10):
            ax.plot(x_values[i], y_values[i], markers[i], fillstyle = "none" , label=nodes[i], color = colorarray[i])
        else:
            ax.plot(x_values[i], y_values[i], markers[i], label=nodes[i], color = colorarray[i])


    plt.ylabel("Virality (Global Cascade fraction)")
    plt.xlabel("Pn (Network Polarization)")

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Nodes")
    plt.gray()
    plt.grid(visible=True,linewidth=0.2)
    #plt.show()



    filepath = Path(path + 'test_2_t270_75_225.pdf')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, bbox_inches='tight')
