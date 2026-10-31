# 60043
import os
import shutil
import sys
import warnings

import matplotlib

wybrane = int(sys.argv[1]) if len(sys.argv) > 1 else None
if wybrane is not None:
    matplotlib.use("Agg")
    warnings.filterwarnings("ignore", message=".*non-interactive.*")


def zadanie(numer):
    if wybrane is None:
        return
    if numer > wybrane:
        sys.exit()
    sys.stdout = sys.__stdout__ if numer == wybrane else open(os.devnull, "w")


# 1
zadanie(1)
import kagglehub
import numpy as np
import pandas as pd

pd.set_option("display.width", shutil.get_terminal_size().columns - 2)
pd.set_option("display.max_columns", 30)

# 2
zadanie(2)
obiad_slownik = pd.DataFrame(
    {
        "danie": ["Rosół", "Schabowy", "Pierogi", "Sałatka"],
        "kalorie": [150, 650, 450, 200],
        "cena": [12, 32, 24, 18],
    }
)
print(obiad_slownik)

# 3
zadanie(3)
obiad_lista = pd.DataFrame(
    [
        ["Kebab", 750, 25],
        ["Pizza", 900, 35],
        ["Zapiekanka", 550, 15],
        ["Hot dog", 400, 10],
    ],
    columns=["danie", "kalorie", "cena"],
)
print(obiad_lista)

# 4
zadanie(4)
sciezka = kagglehub.dataset_download("ulrikthygepedersen/fastfood-nutrition")
print(sciezka)
df = pd.read_csv(f"{sciezka}/fastfood.csv")
df.to_excel("fastfood.xlsx", index=False)
df_excel = pd.read_excel("fastfood.xlsx")
print(df_excel.shape)

# 5
zadanie(5)
print(df.head(3).T)

# 6
zadanie(6)
print(df.head(10))

# 7
zadanie(7)
print(df.tail(10))
