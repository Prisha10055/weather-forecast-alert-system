"""Generate weather forecast charts using Matplotlib."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from src.config import IMAGES_DIR


def plot_forecast_chart(city: str, forecast_df: pd.DataFrame, output_dir: Path = IMAGES_DIR) -> Path:
    """Create a 2-panel forecast chart (Temperature & Rainfall/Humidity) and save as PNG."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_city = city.strip().lower().replace(" ", "_")
    chart_path = output_dir / f"forecast_chart_{safe_city}.png"

    if forecast_df.empty:
        raise ValueError("Cannot generate chart from an empty forecast DataFrame.")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
    fig.patch.set_facecolor("#F8FAFC")

    # Panel 1: Temperature Trend
    ax1.plot(
        forecast_df["timestamp"],
        forecast_df["temperature_c"],
        marker="o",
        linewidth=2.4,
        color="#E11D48",
        label="Temperature (°C)",
    )
    ax1.fill_between(forecast_df["timestamp"], forecast_df["temperature_c"], alpha=0.12, color="#E11D48")
    ax1.set_title(f"{city.title()} — Weather Forecast Overview", fontsize=14, fontweight="bold", pad=12, color="#0F172A")
    ax1.set_ylabel("Temperature (°C)", fontsize=10, fontweight="bold", color="#334155")
    ax1.grid(True, linestyle="--", alpha=0.45)
    ax1.legend(loc="upper right")

    # Panel 2: Rainfall (bars) & Humidity (line on secondary y-axis)
    ax2_hum = ax2.twinx()
    ax2.bar(
        forecast_df["timestamp"],
        forecast_df["rain_3h_mm"],
        width=0.08,
        color="#2563EB",
        alpha=0.75,
        label="Rain (mm / 3h)",
    )
    ax2_hum.plot(
        forecast_df["timestamp"],
        forecast_df["humidity_pct"],
        marker="s",
        linewidth=1.8,
        linestyle="--",
        color="#0D9488",
        label="Humidity (%)",
    )

    ax2.set_ylabel("Rainfall (mm)", fontsize=10, fontweight="bold", color="#1D4ED8")
    ax2_hum.set_ylabel("Humidity (%)", fontsize=10, fontweight="bold", color="#0F766E")
    ax2_hum.set_ylim(0, 105)
    ax2.grid(True, linestyle="--", alpha=0.45)

    # Format X-axis timestamps
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d\n%H:%M"))
    fig.autofmt_xdate(rotation=0, ha="center")

    # Combined legend for bottom panel
    lines_1, labels_1 = ax2.get_legend_handles_labels()
    lines_2, labels_2 = ax2_hum.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

    plt.tight_layout()
    plt.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path
