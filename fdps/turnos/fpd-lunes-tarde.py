from fitter import Fitter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Carga de datos
llamadas = pd.read_csv('../../../call_center.csv', sep=";")

#Preparacion de datos general:
llamadas["fecha_ocurrencia"] = pd.to_datetime(llamadas["Fecha"], format="%d/%m/%Y %H:%M")

llamadas = llamadas.sort_values("fecha_ocurrencia")

llamadas_lunes = llamadas[
    (llamadas["fecha_ocurrencia"].dt.month == 4) &
    (llamadas["fecha_ocurrencia"].dt.dayofweek == 0)
]

#Preparacion de datos lunes tarde:

llamadas_lunes_tarde = (
    llamadas_lunes
    .set_index("fecha_ocurrencia")
    .between_time("13:30", "16:00")
    .reset_index()
)

llamadas_lunes_tarde["fecha_solo"] = (
    llamadas_lunes_tarde["fecha_ocurrencia"].dt.date
)

llamadas_lunes_tarde["IA_min"] = (
    llamadas_lunes_tarde
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_lunes_tarde = llamadas_lunes_tarde.dropna(subset=["IA_min"])

#Grafico histograma

llamadas_lunes_tarde.hist('IA_min', bins=200)
plt.show()

# Fdp lunes tarde:
fdp_lunes_tarde_ia = Fitter(llamadas_lunes_tarde.IA_min)
fdp_lunes_tarde_ia.fit()
print(fdp_lunes_tarde_ia.summary(3))
print(fdp_lunes_tarde_ia.get_best(method="sumsquare_error"))

a = 1.9868010751079173
loc = -2.0636279622915342e-10
scale = 4.955277601907699

fdp_lunes_tarde_ia_kappa3 = stats.kappa3.rvs(a, loc, scale, 150)
print(fdp_lunes_tarde_ia_kappa3.min(), fdp_lunes_tarde_ia_kappa3.max())

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_lunes_tarde_ia_kappa3, bins=200)
plt.show()