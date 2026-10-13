import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats 

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

# ОЦЕНКА ДИСПЕРСИИ И РАЗБРОСА
print("=" * 60)
print("АНАЛИЗ РАЗБРОСА И ДИСПЕРСИИ")
print("=" * 60)

# Описательная статистика
stats_summary = data_clean.describe()
print("\n--- Описательная статистика ---")
print(stats_summary)

print("\n--- Детальные метрики разброса ---")
for col in data_clean.columns:
    variance = data_clean[col].var()
    std_dev = data_clean[col].std()
    mean_val = data_clean[col].mean()
    cv = (std_dev / mean_val) * 100
    
    print(f"\nПоказатель: {col}")
    print(f"  Среднее значение:          {mean_val:.2f}")
    print(f"  Дисперсия:                 {variance:.2f}")
    print(f"  Стандартное отклонение:    {std_dev:.2f}")
    print(f"  Коэффициент вариации (CV): {cv:.2f}%")
    
    if cv > 33:
        print("  Вывод: Выборка неоднородная (высокий разброс).")
    else:
        print("  Вывод: Выборка однородная (умеренный разброс).")

# ПРОВЕРКА ГИПОТЕЗЫ О РАВЕНСТВЕ ДИСПЕРСИЙ (F-тест)
print("\n" + "=" * 60)
print("ПРОВЕРКА ГИПОТЕЗЫ О РАВЕНСТВЕ ДИСПЕРСИЙ (F-тест)")
print("=" * 60)

var14 = data_clean["Столбец_14"].var()
var15 = data_clean["Столбец_15"].var()

if var14 > var15:
    f_stat = var14 / var15
    df1 = len(data_clean["Столбец_14"]) - 1
    df2 = len(data_clean["Столбец_15"]) - 1
else:
    f_stat = var15 / var14
    df1 = len(data_clean["Столбец_15"]) - 1
    df2 = len(data_clean["Столбец_14"]) - 1

p_value = 2 * (1 - stats.f.cdf(f_stat, df1, df2))

print(f"Дисперсия Столбца 14: {var14:.2f}")
print(f"Дисперсия Столбца 15: {var15:.2f}")
print(f"F-статистика: {f_stat:.4f}")
print(f"p-value: {p_value:.4e}")

alpha = 0.05
if p_value < alpha:
    print(f"\nРезультат: p-value < {alpha}. Отвергаем H0.")
    print("Вывод: Дисперсии статистически значимо различаются.")
else:
    print(f"\nРезультат: p-value >= {alpha}. Нет оснований отвергнуть H0.")
    print("Вывод: Статистически значимых различий в дисперсиях не обнаружено.")


plt.figure(figsize=(8, 6))
data_clean.boxplot()
plt.title("Диаграмма размаха (Boxplot) для 14 и 15 столбцов")
plt.ylabel("Значение показателя")
plt.grid(True)
plt.savefig(
    "results/boxplot_variance.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()


# График рассеяния
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
plt.close()

# Гистограммы
data_clean.hist(figsize=(10, 5))
plt.suptitle("Распределение показателей")
plt.tight_layout()
plt.savefig(
    "results/histograms.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

