from pathlib import Path
import datetime
from MY_RFEM.linesSupport import plotEveryLine, saveEveryLine
import pandas as pd

if __name__ == "__main__":
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

    today = datetime.datetime.now()
    datestring = today.strftime("%Y-%m-%d-%H-%M")
    output_dir = current_dir / "Exports" / f"Export {datestring}"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_pickle("test5.pkl")
    plotEveryLine(df=df, pathToSave=output_dir)
    # TODO  sistemare il loadign name. Metterlo nel filtro nel caso nell'excel ce ne sia più di uno
    ddd = saveEveryLine(df=df)
    print(ddd)
