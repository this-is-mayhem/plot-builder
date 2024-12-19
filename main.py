from csv_plotter import csv_plotter

if __name__ == "__main__":
    csvplt = csv_plotter("./", "config_test.yaml")
    csvplt.set_msword_fonts()
    csvplt.plot_data()
