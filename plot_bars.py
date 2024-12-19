from csv_plotter import format_x_ticker
from csv_plotter import format_y_ticker
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker

if __name__ == "__main__":
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'
    rcParams["mathtext.fontset"] = 'stix'

    fig, ax = plt.subplots()
    bar_x = [0.394,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85]
    bar_y = [6,5.78,5.53,5.22,4.84,4.41,3.91,3.39,2.9,2.35]
    bar_width = [0.056,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.1159]
    axes_labels = ["$x$, м", "$h$, мм"]
    x_lim = [0.3, 1]

    ax.bar(bar_x, bar_y, align='edge', width=bar_width, edgecolor='black')

    plt.xlabel(f"{axes_labels[0]}", fontsize=14)
    plt.ylabel(f"{axes_labels[1]}", fontsize=14)
    plt.tick_params(axis="both", which="major", labelsize=14)

    plt.gca().set_xlim(x_lim)
    #plt.gca().set_ylim(y_lim)

    cm = 1 / 2.54  # перевод сантиметров в дюймы для установки размера картинки
    #plt.figure(figsize=(16.5 * cm, 10 * cm))
    fig.set_size_inches(16.5 * cm, 10 * cm)
    #fig.set_dpi(300)

    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_x_ticker(x, pos, 1)))
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: format_y_ticker(y, pos, 0)))

    plt.tight_layout()
    plt.savefig("fig.png", dpi=300)
    plt.show()