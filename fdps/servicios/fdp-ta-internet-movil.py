from fitter import Fitter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Carga de datos
llamadas = pd.read_csv('../../../call_center.csv', sep=";")

#Preparacion de datos

llamadas["TA_numerico"] = pd.to_numeric(
    llamadas["T. Atencion"],
    errors="coerce"
)

llamadas_intmovil = llamadas[
    (llamadas["Cola"] == "tortu-imowi") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO") &
    (llamadas["TA_numerico"] > 20)
]

llamadas_intmovil = llamadas_intmovil.dropna(subset=["TA_numerico"])

llamadas_intmovil["TA_min"] = llamadas_intmovil["TA_numerico"] / 60
print(llamadas_intmovil.value_counts())
#Grafico histograma

# llamadas_intmovil.hist('TA_min', bins=200)
# plt.show()

#Fdp TA Internet movil:

# fdp_internet_movil_ta = Fitter(llamadas_intmovil.TA_min)
# fdp_internet_movil_ta.fit()
# print(fdp_internet_movil_ta.summary(3))
# print(fdp_internet_movil_ta.get_best(method="sumsquare_error"))

a = 1.2824763189951953
loc = 0.3529866902558564
scale = 2.7430708499927383

fdp_internet_movil_ta_erlang = stats.erlang.rvs(a, loc, scale, 200)
print(fdp_internet_movil_ta_erlang.min(), fdp_internet_movil_ta_erlang.max())

#
# plt.title("Histograma")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.xlim(0, 60)
# # plt.ylim(0, 1300)
# plt.hist(fdp_internet_ta_recipinvgauss, bins=200)
# plt.show()

#Grafico continua
# x = np.linspace(0, 50, 500)
#
# y = stats.recipinvgauss.pdf(x, mu, loc=loc, scale=scale)
#
# plt.plot(x, y)
# plt.title("Distribución recipinvgauss")
# plt.xlabel("Tiempo")
# plt.ylabel("Densidad")
# plt.grid(True)
# plt.show()