from matplotlib import axes
import pandas as pd
from calcAreas.calcArea import findIntersections, calcAreas, createPlotAxis
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Literal
from pathlib import Path
import datetime


def saveAreasPerLinePerAction(
    x,
    y,
    line_support_force: str = "",
) -> dict[str, list]:
    x_sorted, y_sorted, zero_crossings, x_intersections = findIntersections(x=x, y=y)
    areas = calcAreas(x_sorted, y_sorted, zero_crossings)
    return {line_support_force: areas}


def saveAreasPerLine(df_line: pd.DataFrame, line_no: str):
    d: dict = {"line_no": line_no}
    print(d)
    df_line_max = df_line.loc[
        (df_line["line_support_force_label"] == "max") & (df_line["line_no"] == line_no)
    ].copy()
    df_line_max.sort_values(by="location", inplace=True, ascending=True)
    d.update(
        saveAreasPerLinePerAction(
            x=df_line_max["location"].to_numpy(),
            y=df_line_max["line_support_force_p_x"].to_numpy(),
            line_support_force="P_X_max",
        )
    )
    d.update(
        saveAreasPerLinePerAction(
            x=df_line_max["location"].to_numpy(),
            y=df_line_max["line_support_force_p_y"].to_numpy(),
            line_support_force="P_Y_max",
        )
    )

    d.update(
        saveAreasPerLinePerAction(
            x=df_line_max["location"].to_numpy(),
            y=df_line_max["line_support_force_p_z"].to_numpy(),
            line_support_force="P_Z_max",
        )
    )
    df_line_min = df_line.loc[
        (df_line["line_support_force_label"] == "min") & (df_line["line_no"] == line_no)
    ].copy()
    df_line_min.sort_values(by="location", inplace=True, ascending=True)
    d.update(
        saveAreasPerLinePerAction(
            x=df_line_min["location"].to_numpy(),
            y=df_line_min["line_support_force_p_x"].to_numpy(),
            line_support_force="P_X_min",
        )
    )
    d.update(
        saveAreasPerLinePerAction(
            x=df_line_min["location"].to_numpy(),
            y=df_line_min["line_support_force_p_y"].to_numpy(),
            line_support_force="P_Y_min",
        )
    )
    d.update(
        saveAreasPerLinePerAction(
            x=df_line_min["location"].to_numpy(),
            y=df_line_min["line_support_force_p_z"].to_numpy(),
            line_support_force="P_Z_min",
        )
    )
    return d


def saveEveryLine(df: pd.DataFrame) -> pd.DataFrame:
    listOfDict: list[dict] = []
    df.dropna(how="any", subset=["line_no"], inplace=True)

    for line_no in df["line_no"].unique():
        df_line = df.loc[(df["line_no"] == line_no)].copy()
        df_line.sort_values(by="location", inplace=True, ascending=True)
        listOfDict.append(saveAreasPerLine(df_line=df_line, line_no=line_no))
    return pd.DataFrame(listOfDict)


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
    fig, axs = plt.subplots(3, 2, figsize=(20, 18), sharex="col")
    df_line_max = df_line.loc[
        (df_line["line_support_force_label"] == "max") & (df_line["line_no"] == line_no)
    ].copy()
    df_line_max.sort_values(by="location", inplace=True, ascending=True)
    createPlotsPerLinePerAction(
        ax=axs[0, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_x"].to_numpy(),
        forceName="p_x",
        line_no=line_no,
        maxMin="max",
    )
    createPlotsPerLinePerAction(
        ax=axs[1, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_y"].to_numpy(),
        forceName="p_y",
        line_no=line_no,
        maxMin="max",
    )
    createPlotsPerLinePerAction(
        ax=axs[2, 0],
        x=df_line_max["location"].to_numpy(),
        y=df_line_max["line_support_force_p_z"].to_numpy(),
        forceName="p_z",
        line_no=line_no,
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
        line_no=line_no,
        maxMin="min",
    )
    createPlotsPerLinePerAction(
        ax=axs[1, 1],
        x=df_line_min["location"].to_numpy(),
        y=df_line_min["line_support_force_p_y"].to_numpy(),
        forceName="p_y",
        line_no=line_no,
        maxMin="min",
    )
    createPlotsPerLinePerAction(
        ax=axs[2, 1],
        x=df_line_min["location"].to_numpy(),
        y=df_line_min["line_support_force_p_z"].to_numpy(),
        forceName="p_z",
        line_no=line_no,
        maxMin="min",
    )
    fig.suptitle(f"Line n.: {line_no:.0f}  {loadingName}", fontsize=16)
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    if pathToSave is not None:
        plt.savefig(pathToSave / f"Line_{line_no:.0f}.pdf")


if __name__ == "__main__":
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

    today = datetime.datetime.now()
    datestring = today.strftime("%Y-%m-%d-%H-%M")
    output_dir = current_dir / f"Export {datestring}"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_pickle("test5.pkl")
    # plotEveryLine(df=df, pathToSave=output_dir)
    # TODO  sistemare il loadign name. Metterlo nel filtro nel caso nell'excel ce ne sia più di uno
    ddd = saveEveryLine(df=df)
    print(ddd)
