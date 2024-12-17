import os
import pandas as pd
import matplotlib.pyplot as plt
import yaml
from matplotlib import rcParams
import matplotlib.ticker as ticker

def format_x_ticker(x, pos):
    return f'{x:.1f}'.replace('.', ',')

def format_y_ticker(y, pos):
    return f'{y:.0f}'.replace('.', ',')

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
            axis_description = file_config["axis description"]
            single_x_axis = file_config["single x axis"]
            legend = file_config["legend"]
            figure_size = file_config["figure size"]
            figure_dpi = file_config["dpi"]


            # Считывание CSV файла
            file_path = os.path.join(self.dir, file_name)
            data = pd.read_csv(file_path)

            cm = 1 / 2.54  # centimeters in inches
            plt.figure(figsize=(figure_size[0] * cm, figure_size[1] * cm))

            if data.shape[1] == 2:
                # Для файлов с двумя столбцами: X и Y
                #plt.plot(data.iloc[:, 0], data.iloc[:, 1], label=f"{legend[0]}")
                plt.plot(data.iloc[:, 0], data.iloc[:, 1])
            elif single_x_axis:
                # Общая ось X для Y1, Y2
                for i in range(1, data.shape[1]):
                    plt.plot(data.iloc[:, 0], data.iloc[:, i], label=f"{legend[i - 1]}")
            elif not single_x_axis:
                # Разные оси X для каждой пары (X, Y)
                for i in range(0, data.shape[1], 2):
                    plt.plot(data.iloc[:, i], data.iloc[:, i + 1], label=f"{legend[i // 2]}")

            # Настройка осей и легенды
            plt.xlabel(f"{axis_description[0]}", fontsize=14)
            plt.ylabel(f"{axis_description[1]}", fontsize=14)
            plt.tick_params(axis="both", which="major", labelsize=14)

            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_x_ticker))
            plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(format_y_ticker))

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
