import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional

def plot_rapidografo(title: str,series_list: List[Dict[str, Any]], 
                     x_cfg: Optional[Dict[str, Any]] = None, 
                     y1_cfg: Optional[Dict[str, Any]] = None,
                     y2_cfg: Optional[Dict[str, Any]] = None,) -> plt.Figure:

    fig, ax1 = plt.subplots(figsize=(9,5))
    
    has_y2 = any(s.get("use_right", False) for s in series_list) or y2_cfg is not None
    ax2 = ax1.twinx() if has_y2 else None

    def apply_axis_settings(ax, cfg, axis_letter):
        if not cfg: 
            return
        if cfg.get("log"):
            getattr(ax, f"set_{axis_letter}scale")("log")
        if cfg.get("scale"):
            getattr(ax, f"set_{axis_letter}lim")(*cfg["scale"])
        getattr(ax, f"set_{axis_letter}label")(cfg.get("label", ""))

    apply_axis_settings(ax1, x_cfg, "x")
    apply_axis_settings(ax1, y1_cfg, "y")
    if ax2:
        apply_axis_settings(ax2, y2_cfg, "y")

    #graficar
    handles, labels = [], []
    for s in series_list:
        current_ax = ax2 if (s.get("use_right") and ax2) else ax1

        line, = current_ax.plot(
            s["x"], s["y"], 
            label=s.get("label", ""), 
            linestyle=s.get("linestyle", "-"), 
            marker=s.get("marker", "")
        )
        
        if s.get("label"):
            handles.append(line)
            labels.append(s["label"])

    #Titulo
    ax1.set_title(title)
    if labels:
        ax1.legend(handles, labels, loc="upper left")
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    fig.tight_layout()
    plt.show()
    return fig


days = [1, 2, 3, 4, 5]
website_visits = [100, 500, 2500, 12000, 70000]
ad_spend = [50, 60, 150, 400, 900]


my_series = [
    {"x": days, "y": website_visits, "label": "Traffic (Log Scale)", "use_right": False},
    {"x": days, "y": ad_spend, "label": "Budget (Linear)", "use_right": True}
]


x_axis = {"label": "Days of Campaign", "scale": (1, 5), "log": False}
left_y = {"label": "Views", "scale": (10, 100000), "log": True}
right_y = {"label": "USD Spent", "scale": (0, 1000), "log": False}


plot_rapidografo(
    title="Campaign Scaling Metrics",
    series_list=my_series,
    x_cfg=x_axis,
    y1_cfg=left_y,
    y2_cfg=right_y
)
