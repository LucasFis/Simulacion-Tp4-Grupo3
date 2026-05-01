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

llamadas_lunes = llamadas[
    (llamadas["fecha_ocurrencia"].dt.month == 4) &
    (llamadas["fecha_ocurrencia"].dt.dayofweek == 0)
]

# Preparacion de datos lunes maniana:
llamadas_lunes_maniana = (
    llamadas_lunes
    .set_index("fecha_ocurrencia")
    .between_time("08:30", "13:30")
    .reset_index()
)

llamadas_lunes_maniana["fecha_solo"] = (
    llamadas_lunes_maniana["fecha_ocurrencia"].dt.date
)

llamadas_lunes_maniana["IA_min"] = (
    llamadas_lunes_maniana
    .groupby("fecha_solo")["fecha_ocurrencia"]
    .diff()
    .dt.total_seconds() / 60
)

llamadas_lunes_maniana = llamadas_lunes_maniana.dropna(subset=["IA_min"])

#Grafico histograma

llamadas_lunes_maniana.hist('IA_min', bins=200)
plt.show()

#Fdp lunes maniana:

# fdp_lunes_maniana_ia = Fitter(llamadas_lunes_maniana.IA_min)
# fdp_lunes_maniana_ia.fit()
# fdp_lunes_maniana_ia.summary(10)

#print(fdp_lunes_maniana_ia.get_best(method="sumsquare_error"))

# df = 0.6473329065381139
# loc = -1.6478587279550768e-28
# scale = 7.66636374789493
#
# fdp_lunes_maniana_ia_chi = stats.chi.rvs(df, loc, scale)

# plt.title("Histograma")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.xlim(0, 60)
# # plt.ylim(0, 1300)
# plt.hist(fdp_lunes_maniana_ia_chi, bins=200)
# plt.show()






