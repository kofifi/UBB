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

# 17
zadanie(17)
print(df[~df["item"].str.contains("Chicken")].head())

# 18
zadanie(18)
df["rodzaj"] = np.select(
    [df["item"].str.contains("Salad"), df["item"].str.contains("Chicken")],
    ["sałatka", "kurczak"],
    default="inne",
)
print(df["rodzaj"].value_counts())

# 19
zadanie(19)
df = df.drop(columns=["salad"])
print(df.columns.tolist())

# 20
zadanie(20)
df = df.rename(columns={"restaurant": "restauracja"})
print(df.columns.tolist())

# 21
zadanie(21)
df.to_csv("fastfood_czyste.csv", index=False)

# 22
zadanie(22)
print(df["calories"].mean(), df["calories"].max(), df["calories"].min())

# 23
zadanie(23)
print(len(df))

# 24
zadanie(24)
print(df["restauracja"].unique())

# 25
zadanie(25)
print(df["restauracja"].value_counts())

# 26
zadanie(26)
print(df.sort_values("calories").head())
print(df.sort_values("calories", ascending=False).head())

# 27
zadanie(27)
print(df.nlargest(10, "calories"))
print(df.nsmallest(10, "calories"))

# 28
zadanie(28)
print(df[df["restauracja"].isin(["Subway", "Taco Bell"])].nlargest(10, "calories"))

# 29
zadanie(29)
grupy = df.groupby(["restauracja", "rodzaj"]).mean(numeric_only=True)
print(grupy)

# 30
zadanie(30)
statystyki = df.groupby("restauracja").agg(
    {
        "calories": "mean",
        "protein": "mean",
        "sodium": ["count", "median"],
        "sugar": ["count", "median"],
    }
)
print(statystyki)

# 31
zadanie(31)
print(grupy.index.names)
print(statystyki.columns.tolist())

# 32
zadanie(32)
print(grupy.sort_index(level="rodzaj"))
print(statystyki.sort_values(("calories", "mean"), ascending=False))

# 33
zadanie(33)
tabela = pd.pivot_table(df, values="calories", index="restauracja", columns="rodzaj", aggfunc="mean")
print(tabela)

# 34
zadanie(34)
print(tabela.index)
print(tabela.columns)

# 35
zadanie(35)
tabela_zlozona = pd.pivot_table(df, values="calories", index=["restauracja", "rodzaj"], aggfunc="mean")
print(tabela_zlozona.index)

# 36
zadanie(36)
import matplotlib.pyplot as plt

# 37
zadanie(37)
from IPython import get_ipython

zeszyt = get_ipython()
if zeszyt is not None:
    zeszyt.run_line_magic("matplotlib", "inline")

# 38
zadanie(38)
tabela.plot(kind="bar", figsize=(11, 5), width=0.8, color=["#2a78d6", "#eb6834", "#1baf7a"], edgecolor="white")
plt.title("Średnia kaloryczność dań w sieciach fast food")
plt.xlabel("Restauracja")
plt.ylabel("Średnia liczba kalorii")
plt.xticks(rotation=30, ha="right")
plt.legend(title="Rodzaj dania")
plt.tight_layout()
plt.savefig("wykres38.png")
plt.show()
najciezsza = df.groupby("restauracja")["calories"].mean().idxmax()
print(f"Najbardziej kaloryczne menu ma średnio {najciezsza}, a sałatki nie zawsze są najlżejszym wyborem.")

# 39
zadanie(39)
df["calories"].plot(kind="hist", bins=30, figsize=(9, 5), color="#2a78d6", edgecolor="white")
plt.title("Rozkład kaloryczności dań")
plt.xlabel("Kalorie")
plt.ylabel("Liczba dań")
plt.tight_layout()
plt.savefig("wykres39.png")
plt.show()
print("Około 80% dań ma od 200 do 800 kalorii, a tylko jedno przekracza 2000.")
