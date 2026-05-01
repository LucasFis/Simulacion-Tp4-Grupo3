from fitter import Fitter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Carga de datos
llamadas = pd.read_csv('../call_center.csv', sep=";")

#Preparacion de datos general:
llamadas["fecha_ocurrencia"] = pd.to_datetime(llamadas["Fecha"], format="%d/%m/%Y %H:%M")

llamadas = llamadas.sort_values("fecha_ocurrencia")

llamadas_lunes = llamadas[
    (llamadas["fecha_ocurrencia"].dt.month == 4) &
    (llamadas["fecha_ocurrencia"].dt.dayofweek == 0)
]

#Preparacion de datos lunes tarde:

llamadas_lunes_noche = (
    llamadas_lunes
    .set_index("fecha_ocurrencia")
    .between_time("16:00", "21:00")
    .reset_index()
)

llamadas_lunes_noche["fecha_solo"] = (
    llamadas_lunes_noche["fecha_ocurrencia"].dt.date
)

llamadas_lunes_noche["IA_min"] = (
    llamadas_lunes_noche
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_lunes_noche = llamadas_lunes_noche.dropna(subset=["IA_min"])

#Grafico histograma

# llamadas_lunes_noche.hist('IA_min', bins=200)
# plt.show()

#Fdp lunes noche:
# fdp_lunes_noche_ia = Fitter(llamadas_lunes_noche.IA_min)
# fdp_lunes_noche_ia.fit()
# print(fdp_lunes_noche_ia.summary(10))
#
# print(fdp_lunes_noche_ia.get_best(method="sumsquare_error"))

c = 15.772219690442558
s = 2.0188407126934353
loc = -0.2584689362182534
scale = 199.46475939297915

fdp_lunes_noche_ia_powerlognorm = stats.powerlognorm.rvs(c, s, loc, scale, 10000)
print(fdp_lunes_noche_ia_powerlognorm.min(), fdp_lunes_noche_ia_powerlognorm.max())

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_lunes_noche_ia_powerlognorm, bins=200)
plt.show()