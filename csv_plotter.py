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

    def __read_csv(self, file_path, separator=";"):
        """
        Загружает CSV файл с учетом первого ряда:
        - Если первая строка содержит текст, она используется как имена колонок.
        - Если первая строка содержит числа, она используется как данные.
        """
        with open(file_path, 'r', encoding="UTF-8") as f:
            first_line = f.readline().strip()

        # Проверяем, содержит ли первая строка текст
        if any(char.isalpha() for char in first_line):
            # Если есть текст, загружаем с первой строкой как заголовком
            df = pd.read_csv(file_path, header=0, sep=separator)
        else:
            # Если только числа, загружаем без заголовка
            df = pd.read_csv(file_path, header=None, sep=separator)
            # Задаем числовые индексы колонок
            df.columns = [f"col_{i}" for i in range(df.shape[1])]

        return df

    def __prepare_style_dict(self, charts_dict, charts_cnt):
        charts_styles = []
        for i in range(0, charts_cnt):
            curve_style_dict = {}
            if charts_dict["legend"] is not None and charts_dict["legend"][i] is not None:
                curve_style_dict["label"] = charts_dict["legend"][i]
            if charts_dict["style"] is not None and charts_dict["style"][i] is not None:
                curve_style_dict["linestyle"] = charts_dict["style"][i][0]
                curve_style_dict["marker"] = charts_dict["style"][i][1]
                curve_style_dict["linewidth"] = charts_dict["style"][i][2]
                curve_style_dict["markersize"] = charts_dict["style"][i][3]
                curve_style_dict["markeredgewidth"] = charts_dict["style"][i][4]
                #curve_style_dict["markevery"] = 2
            if charts_dict.get("color") and charts_dict["color"][i] is not None:
                curve_style_dict["color"] = charts_dict["color"][i]
            charts_styles.append(curve_style_dict)
        return charts_styles

    def plot_data(self):
        for file_config in self.config:
            file_name = file_config["name"]

            # обработка информации об осях
            axes_labels = file_config["axes"]["labels"]
            axes_precision = file_config["axes"]["precision"]
            single_x_axis = file_config["axes"]["single x axis"]
            x_lim = file_config["axes"]["x limits"]
            y_lim = file_config["axes"]["y limits"]
            ticks_value = file_config["axes"]["ticks value"]
            ticks_max_number = file_config["axes"]["ticks max number"]
            axes_fontsize = file_config["axes"]["font size"]

            # обработка информации о кривых графика
            legend = file_config["charts"]["legend"]
            style = file_config["charts"]["style"]

            # обработка прочей информации
            figure_size = file_config["figure size"]
            figure_dpi = file_config["dpi"]
            legend_fontsize = file_config["charts"]["font size"]

            # Считывание CSV файла
            file_path = os.path.join(self.dir, file_name)
            data = self.__read_csv(file_path)

            # подготовка словарей стилей графиков
            if not single_x_axis:
                curves_cnt = data.shape[1] / 2
            else:
                curves_cnt = data.shape[1] - 1
            charts_styles = self.__prepare_style_dict(file_config["charts"], int(curves_cnt))

            cm = 1 / 2.54  # перевод сантиметров в дюймы для установки размера картинки
            plt.figure(figsize=(figure_size[0] * cm, figure_size[1] * cm))

            lines = []
            labels = legend if legend else []

            if data.shape[1] == 2:
                # Для файлов с двумя столбцами: X и Y
                line, = plt.plot(data.iloc[:, 0], data.iloc[:, 1], **charts_styles[0])
                lines.append(line)
            elif single_x_axis:
                # Общая ось X для Y1, Y2
                for i in range(1, data.shape[1]):
                    line, = plt.plot(data.iloc[:, 0], data.iloc[:, i], **charts_styles[i-1])
                    lines.append(line)
            elif not single_x_axis:
                # Разные оси X для каждой пары (X, Y)
                for i in range(0, data.shape[1], 2):
                    line, = plt.plot(data.iloc[:, i], data.iloc[:, i + 1], **charts_styles[i // 2])
                    lines.append(line)

            # Настройка осей и легенды
            plt.gca().set_xlim(x_lim)
            plt.gca().set_ylim(y_lim)

            plt.xlabel(f"{axes_labels[0]}", fontsize=axes_fontsize)
            plt.ylabel(f"{axes_labels[1]}", fontsize=axes_fontsize)
            plt.tick_params(axis="both", which="major", labelsize=axes_fontsize)

            # число знаков после запятой для числовых подписей оси
            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_x_ticker(x, pos, axes_precision[0])))
            plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: format_y_ticker(y, pos, axes_precision[1])))
            # значение шага по осям

            if ticks_value:
                plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(ticks_value[0]))
                plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(ticks_value[1]))

            # максимальное количество делений по осям
            if ticks_max_number:
                plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(ticks_max_number[0]))
                plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(ticks_max_number[1]))

            # легенда сверху графика
            # if legend and len(legend) == len(lines):
            #     plt.legend(fontsize=legend_fontsize, loc='lower center', bbox_to_anchor=(0.5, 1.), ncol=8,
            #                borderpad=0.2, labelspacing=0.2, columnspacing=0.8, handletextpad=0.1, handlelength=1)

            # легенда справа графика
            # if legend and len(legend) == len(lines):
            #     plt.legend(fontsize=legend_fontsize, loc='center left', bbox_to_anchor=(1.0, 0.5), borderpad=0.2, labelspacing=0.2,
            #                columnspacing=0.8, handletextpad=0.1, handlelength=1)

            # легенда на графике
            if legend and len(legend) == len(lines):
                plt.legend(lines, labels, fontsize=legend_fontsize)
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
