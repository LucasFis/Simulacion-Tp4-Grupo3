from sqlite3.dbapi2 import Date

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

llamadas_viernes = llamadas[
    (llamadas["fecha_ocurrencia"].dt.month == 4) &
    (llamadas["fecha_ocurrencia"].dt.dayofweek == 4)
]

# Preparacion de datos viernes maniana:
llamadas_viernes_noche = (
    llamadas_viernes
    .set_index("fecha_ocurrencia")
    .between_time("16:00", "21:00")
    .reset_index()
)

llamadas_viernes_noche["fecha_solo"] = (
    llamadas_viernes_noche["fecha_ocurrencia"].dt.date
)

llamadas_viernes_noche["IA_min"] = (
    llamadas_viernes_noche
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_viernes_noche = llamadas_viernes_noche.dropna(subset=["IA_min"])

#Grafico histograma

# llamadas_viernes_noche.hist('IA_min', bins=200)
# plt.show()

#Fdp viernes tarde:

# fdp_viernes_noche_ia = Fitter(llamadas_viernes_noche.IA_min)
# fdp_viernes_noche_ia.fit()
# print(fdp_viernes_noche_ia.summary(10))
# print(fdp_viernes_noche_ia.get_best(method="sumsquare_error"))

b = 8.802605357768954
c = 1.86975146455312
loc = -68.98608797880931
scale = 68.98608797836727
#
fdp_viernes_noche_ia_truncpareto = stats.truncpareto.rvs(b, c, loc, scale, 10000)
#
plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_viernes_noche_ia_truncpareto, bins=200)
plt.show()






