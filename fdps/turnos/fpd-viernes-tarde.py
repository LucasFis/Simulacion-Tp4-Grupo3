from sqlite3.dbapi2 import Date

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

llamadas_viernes = llamadas[
    (llamadas["fecha_ocurrencia"].dt.month == 4) &
    (llamadas["fecha_ocurrencia"].dt.dayofweek == 4)
]

# Preparacion de datos viernes maniana:
llamadas_viernes_tarde = (
    llamadas_viernes
    .set_index("fecha_ocurrencia")
    .between_time("13:30", "16:00")
    .reset_index()
)

llamadas_viernes_tarde["fecha_solo"] = (
    llamadas_viernes_tarde["fecha_ocurrencia"].dt.date
)

llamadas_viernes_tarde["IA_min"] = (
    llamadas_viernes_tarde
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_viernes_tarde = llamadas_viernes_tarde.dropna(subset=["IA_min"])

#Grafico histograma

llamadas_viernes_tarde.hist('IA_min', bins=200)
plt.show()

#Fdp viernes tarde:

fdp_viernes_tarde_ia = Fitter(llamadas_viernes_tarde.IA_min)
fdp_viernes_tarde_ia.fit()
print(fdp_viernes_tarde_ia.summary(3))
print(fdp_viernes_tarde_ia.get_best(method="sumsquare_error"))

nu = 0.26518687794498164
loc = 0.9999999999999999
scale = 13.94852112368078
#
fdp_viernes_tarde_ia_nakagami = stats.nakagami.rvs(nu, loc, scale, 150)
#
plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_viernes_tarde_ia_nakagami, bins=200)
plt.show()

#Grafico continuo
x = np.linspace(0, 50, 500)

y = stats.nakagami.pdf(x, nu, loc=loc, scale=scale)

plt.plot(x, y)
plt.title("Distribución nakagami")
plt.xlabel("Tiempo")
plt.ylabel("Densidad")
plt.grid(True)
plt.show()





