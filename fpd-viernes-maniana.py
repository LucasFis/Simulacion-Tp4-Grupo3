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
llamadas_viernes_maniana = (
    llamadas_viernes
    .set_index("fecha_ocurrencia")
    .between_time("08:30", "13:30")
    .reset_index()
)

llamadas_viernes_maniana["fecha_solo"] = (
    llamadas_viernes_maniana["fecha_ocurrencia"].dt.date
)

llamadas_viernes_maniana["IA_min"] = (
    llamadas_viernes_maniana
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_viernes_maniana = llamadas_viernes_maniana.dropna(subset=["IA_min"])

#Grafico histograma

# llamadas_viernes_maniana.hist('IA_min', bins=200)
# plt.show()

#Fdp viernes maniana:

# fdp_viernes_maniana_ia = Fitter(llamadas_viernes_maniana.IA_min)
# fdp_viernes_maniana_ia.fit()
# print(fdp_viernes_maniana_ia.summary(10))
# print(fdp_viernes_maniana_ia.get_best(method="sumsquare_error"))

b = 3.2268293314082763
c = 5.9871932705168724
loc = -13.033395258844632
scale = 13.03339525833951
#
fdp_viernes_maniana_ia_truncpareto = stats.truncpareto.rvs(b, c, loc, scale, 10000)
#
plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_viernes_maniana_ia_truncpareto, bins=200)
plt.show()






