import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from helpers import smooth


class DataPlotter:
    def __init__(self, ):
        plt.style.use("./plot_style/science.mplstyle")
        
    def format_with_units(self, x, _):
        if x >= 1e6:
            return f'{x/1e6:.1f}M'
        elif x >= 1e3:
            return f'{x/1e3:.1f}K'
        else:
            return f'{x:.0f}'

    def plot_raw_n_smooth(self, x_name, y_name, df, smooth_factor):
        x = df[x_name]
        y = df[y_name]
        y_smooth = smooth(y, smooth_factor)
        if y_name == "Policy / Standard deviation":
            y_title = "Policy Standard deviation"
        else:
            y_title = y_name.split("/")[-1].strip().replace("_", " ").title()

        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=3, alpha=0.2, label="Raw data")
        ax.plot(x, y_smooth, linewidth=4, label="EMA (α = 0.95)")
        ax.set_xlabel("Epoch")
        ax.set_ylabel(y_title)
        ax.set_label("")
        ax.legend(loc="best")

        ax.xaxis.set_major_formatter(FuncFormatter(self.format_with_units))
        self.fig = fig

    def save_plot(self, dir, plot_name):
        if not os.path.isdir(dir):
            os.makedirs(dir)
        self.fig.savefig(f"{dir}/{plot_name}", dpi=600)
        plt.close()
