import os
import pandas as pd
import matplotlib.pyplot as plt
import yaml
from matplotlib import rcParams
import matplotlib.ticker as ticker

def format_x_ticker(x, pos, precision=2):
    return f'{x:.{precision}f}'.replace('.', ',')

def format_y_ticker(y, pos, precision=2):
    return f'{y:.{precision}f}'.replace('.', ',')

class csv_plotter:
    def __init__(self, working_dir, yaml_name="config.yaml"):
        self.dir = working_dir
        self.csv_files = []
        self.config = self.__read_yaml(yaml_name)

    def __read_yaml(self, yaml_name):
        with open(os.path.join(self.dir, yaml_name), "r", encoding="UTF-8") as f:
            return yaml.safe_load(f)

    def plot_data(self):
        for file_config in self.config:
            file_name = file_config["name"]

            # обработка информации об осях
            axes_labels = file_config["axes"]["labels"]
            axes_precision = file_config["axes"]["precision"]
            single_x_axis = file_config["axes"]["single x axis"]
            x_lim = file_config["axes"]["x limits"]
            y_lim = file_config["axes"]["y limits"]

            # обработка информации о кривых графика
            legend = file_config["charts"]["legend"]
            style = file_config["charts"]["style"]

            # обработка прочей информации
            figure_size = file_config["figure size"]
            figure_dpi = file_config["dpi"]

            # Считывание CSV файла
            file_path = os.path.join(self.dir, file_name)
            data = pd.read_csv(file_path, sep=";")

            cm = 1 / 2.54  # перевод сантиметров в дюймы для установки размера картинки
            plt.figure(figsize=(figure_size[0] * cm, figure_size[1] * cm))

            if data.shape[1] == 2:
                # Для файлов с двумя столбцами: X и Y
                plt.plot(data.iloc[:, 0], data.iloc[:, 1])
            elif single_x_axis:
                # Общая ось X для Y1, Y2
                for i in range(1, data.shape[1]):
                    plt.plot(data.iloc[:, 0], data.iloc[:, i],
                             label=f"{legend[i - 1]}",
                             linestyle=style[i // 2][0],
                             marker=style[i // 2][1])
            elif not single_x_axis:
                # Разные оси X для каждой пары (X, Y)
                for i in range(0, data.shape[1], 2):
                    plt.plot(data.iloc[:, i], data.iloc[:, i + 1],
                             label=f"{legend[i // 2]}",
                             linestyle=style[i // 2][0],
                             marker=style[i // 2][1])

            # Настройка осей и легенды
            plt.gca().set_xlim(x_lim)
            plt.gca().set_ylim(y_lim)

            plt.xlabel(f"{axes_labels[0]}", fontsize=14)
            plt.ylabel(f"{axes_labels[1]}", fontsize=14)
            plt.tick_params(axis="both", which="major", labelsize=14)

            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_x_ticker(x, pos, axes_precision[0])))
            plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: format_y_ticker(y, pos, axes_precision[1])))

            if data.shape[1] != 2:
                plt.legend(fontsize=12)
            plt.grid(True)
            plt.tight_layout()

            # Сохранение графика
            output_path = os.path.join(self.dir, f"{os.path.splitext(file_name)[0]}_plot.png")
            plt.savefig(output_path, dpi=figure_dpi)
            plt.close()

        print("Графики успешно созданы.")

    def set_msword_fonts(self):
        rcParams['font.family'] = 'serif'
        rcParams['font.serif'] = 'Times New Roman'
        rcParams["mathtext.fontset"] = 'stix'

    def set_latex_fonts(self):
        rcParams['font.family'] = 'STIXGeneral'
        rcParams["mathtext.fontset"] = 'cm'
