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

# 8
zadanie(8)
df.info()

# 9
zadanie(9)
print(df.shape)

# 10
zadanie(10)
print(df.describe())

# 11
zadanie(11)
print(df.select_dtypes(exclude="number").describe())

# 12
zadanie(12)
print(df.isna().sum())
print(len(df.dropna()))
df = df.drop(columns=["vit_a", "vit_c", "calcium"])
df = df.dropna().drop_duplicates().reset_index(drop=True)
print(df.shape)

# 13
zadanie(13)
print(df["item"].head())
print(df[["item", "calories"]].head())
print(df.loc[0:4, ["restaurant", "item"]])
print(df.loc[3, "item"])
print(df.at[3, "calories"])
print(df.iloc[0:5, 0:3])
print(df.iloc[[0, 2, 4], [1, 2]])
print(df.iat[3, 2])

# 14
zadanie(14)
print(df[df["calories"] > 1000].head())

# 15
zadanie(15)
print(df[(df["restaurant"] == "Mcdonalds") & (df["calories"] < 400) & (df["protein"] > 20)].head())

# 16
zadanie(16)
print(df[df["item"].str.contains("Chicken")].head())
