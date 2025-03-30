import pandas as pd
from calcAreas.calcArea import findIntersections, calcAreas, createPlotAxis
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Literal
from pathlib import Path
import datetime


def plotEveryLine(df: pd.DataFrame, pathToSave: Path) -> None:
    df.dropna(how="any", subset=["line_no"], inplace=True)

    for line_no in df["line_no"].unique():
        df_line = df.loc[(df["line_no"] == line_no)].copy()
        df_line.sort_values(by="location", inplace=True, ascending=True)
        createPlotsPerLine(df_line=df_line, line_no=line_no, pathToSave=pathToSave)


def createPlotsPerLinePerAction(
    x,
    y,
    forceName: str = "",
    maxMin: Literal["max", "min"] = "",
    line_no: str = "",
    ax: Axes | None = None,
) -> Axes:
    x_sorted, y_sorted, zero_crossings, x_intersections = findIntersections(x=x, y=y)
    areas = calcAreas(x_sorted, y_sorted, zero_crossings)

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(12, 7))

    createPlotAxis(
        ax=ax,
        x_sorted=x_sorted,
        y_sorted=y_sorted,
        zero_crossings=zero_crossings,
        x_intersections=x_intersections,
        areas=areas,
    )
    ax.set_title(f"{forceName} - {maxMin}")
    ax.set_xlabel("")
    ax.set_ylabel("")
    return ax


def createPlotsPerLine(
    df_line: pd.DataFrame,
    line_no: str,
    loadingName: str = "",
    pathToSave: Path | None = None,
):
    fig, axs = plt.subplots(3, 2, figsize=(20, 18))
    df_line_max = df_line.loc[
        (df_line["line_support_force_label"] == "max") & (df_line["line_no"] == line_no)
    ].copy()
    df_line_max.sort_values(by="location", inplace=True, ascending=True)
    createPlotsPerLinePerAction(
        ax=axs[0, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_x"].to_numpy(),
        forceName="p_x",
        maxMin="max",
    )
    createPlotsPerLinePerAction(
        ax=axs[1, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_y"].to_numpy(),
        forceName="p_y",
        maxMin="max",
    )
    createPlotsPerLinePerAction(
        ax=axs[2, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_z"].to_numpy(),
        forceName="p_z",
        maxMin="max",
    )
    df_line_min = df_line.loc[
        (df_line["line_support_force_label"] == "min") & (df_line["line_no"] == line_no)
    ].copy()
    df_line_min.sort_values(by="location", inplace=True, ascending=True)
    createPlotsPerLinePerAction(
        ax=axs[0, 1],
        x=df_line_min["location"].to_numpy(),
        y=df_line_min["line_support_force_p_x"].to_numpy(),
        forceName="p_x",
        maxMin="min",
    )
    createPlotsPerLinePerAction(
        ax=axs[1, 1],
        x=df_line_min["location"].to_numpy(),
        y=df_line_min["line_support_force_p_y"].to_numpy(),
        forceName="p_y",
        maxMin="min",
    )
    createPlotsPerLinePerAction(
        ax=axs[2, 1],
        x=df_line_min["location"].to_numpy(),
        y=df_line_min["line_support_force_p_z"].to_numpy(),
        forceName="p_z",
        maxMin="min",
    )
    fig.suptitle(f"Line n.: {line_no:.0f}  {loadingName}")
    if pathToSave is not None:
        plt.savefig(pathToSave / f"Line_{line_no:.0f}.pdf")
