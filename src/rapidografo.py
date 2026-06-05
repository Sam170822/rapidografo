import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


class Rapidografo:

    def __init__(self, title: str = "", figsize: tuple = (9, 5)):
        self.title = title
        self.figsize = figsize
        self._x_cfg = None
        self._y_cfg = None
        self._y2_cfg = None
        self._series = []

    def configure_x_axis(self, label="", scale=None, log=False):
        self._x_cfg = {
            "label": label,
            "scale": scale,
            "log": log,
        }
        return self

    def configure_y_axis(self, label="", scale=None, log=False):
        self._y_cfg = {
            "label": label,
            "scale": scale,
            "log": log,
        }
        return self

    def configure_y2_axis(self, label="", scale=None, log=False):
        self._y2_cfg = {
            "label": label,
            "scale": scale,
            "log": log,
        }
        return self

    def add_series(self, x, y, *, label="", linestyle="-", 
                   marker="", use_right_axis=False):

        if use_right_axis and self._y2_cfg is None:
            raise ValueError(
                "configure_y2_axis() must be called first."
            )

        self._series.append({"x": x, "y": y, "label": label,
                             "linestyle": linestyle,"marker": marker,
                             "use_right_axis": use_right_axis})

        return self

    def _apply_axis(self, ax, which, cfg):

        scale_type = "log" if cfg["log"] else "linear"
        getattr(ax, f"set_{which}scale")(scale_type)

        if cfg["scale"] is not None:
            getattr(ax, f"set_{which}lim")(
                cfg["scale"][0],
                cfg["scale"][1]
            )

    def plot(self, show=True, save_path: Optional[str] = None):

        if self._x_cfg is None:
            self.configure_x_axis()

        if self._y_cfg is None:
            self.configure_y_axis()

        fig, ax1 = plt.subplots(figsize=self.figsize)

        ax2 = ax1.twinx() if self._y2_cfg else None

        self._apply_axis(ax1, "x", self._x_cfg)
        self._apply_axis(ax1, "y", self._y_cfg)

        if ax2 is not None:
            self._apply_axis(ax2, "y", self._y2_cfg)

        handles = []
        labels = []

        for s in self._series:

            current_ax = (ax2 if s["use_right_axis"] and ax2 is not None
                          else ax1)

            kwargs = {"linestyle": s["linestyle"]}
            kwargs["marker"] = s["marker"]
            kwargs["color"] = "black"

            line, = current_ax.plot(s["x"],s["y"],label=s["label"],**kwargs)

            if s["label"]:
                handles.append(line)
                labels.append(s["label"])

        ax1.set_xlabel(self._x_cfg["label"])

        ax1.set_ylabel(self._y_cfg["label"], color="red")

        ax1.tick_params(axis="y", colors="red")

        if ax2 is not None:

            ax2.set_ylabel(self._y2_cfg["label"], color="blue")

            ax2.tick_params(axis="y", colors="blue")

        if self.title:
            ax1.set_title(self.title)

        if labels:
            ax1.legend(handles, labels)

        ax1.grid(True, linestyle="--", alpha=0.5)

        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150)

        if show:
            plt.show()

        return fig
