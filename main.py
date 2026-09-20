import pandas as pd
import matplotlib.pyplot as plt
#with open("WHOLE1.DAT", "r") as file:
#    for i, line in enumerate(file, start=1):
#       data = line.split()
#
#       # 14-й и 15-й столбцы
#        col14 = data[13]
#        col15 = data[14]
#        print(i, col14, col15) 

# Читаем датасет
df = pd.read_csv(
    "WHOLE1.DAT",
    sep=r"\s+",
    header=None,
    na_values="NN"
)

data = df.iloc[:, [13, 14]].copy()
data.columns = ["Столбец_14", "Столбец_15"]

data.to_csv(
    "results/table_14_15.csv",
    index=False,
    encoding="utf-8-sig"
)

data.to_excel(
    "results/table_14_15.xlsx",
    index=False
)

data_clean = data.dropna()


plt.figure(figsize=(8, 6))

plt.scatter(
    data_clean["Столбец_14"],
    data_clean["Столбец_15"],
    alpha=0.5
)

plt.xlabel("14-й столбец")
plt.ylabel("15-й столбец")
plt.title("Зависимость 14-го и 15-го столбцов")
plt.grid()

plt.savefig(
    "results/graph_dependency.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()



data.hist(figsize=(10, 5))

plt.suptitle("Распределение показателей")
plt.tight_layout()

plt.savefig(
    "results/histograms.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()
