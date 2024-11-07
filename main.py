import json

from read_data import DataLoader
from plot_data import DataPlotter


def main():
    with open("settings.json", "r") as settings:
        settings = json.load(settings)

    loader = DataLoader(settings)
    plotter = DataPlotter()

    smoothing_factor = 0.95

    for training in settings["trainings"]:
        data = loader.get_data_from_all_runs(training)
        for criteria in settings["criteria"]:
            for run in data.keys():
                run_df = data[run]
                plotter.plot_raw_n_smooth("Step", criteria,  run_df, smoothing_factor)
                plotter.save_plot("./figs", f"{run}_{criteria.replace('/', '_')}.png")


if __name__ == "__main__":
    main()