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

llamadas_tv = llamadas[
    (llamadas["Cola"] == "iptv") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO") &
    (llamadas["TA_numerico"] > 20)
]

llamadas_tv = llamadas_tv.dropna(subset=["TA_numerico"])

llamadas_tv["TA_min"] = llamadas_tv["TA_numerico"] / 60
print(llamadas_tv.value_counts())

#Grafico histograma

# llamadas_tv.hist('TA_min', bins=200)
# plt.show()

#Fdp TA Internet movil:

# fdp_tv_ta = Fitter(llamadas_tv.TA_min)
# fdp_tv_ta.fit()
# print(fdp_tv_ta.summary(3))
# print(fdp_tv_ta.get_best(method="sumsquare_error"))

k = 1.120685328694003
s = 2.5868147327627664
loc = 0.36162384506728507
scale = 4.867007896499102

fdp_tv_ta_mielke = stats.mielke.rvs(k, s, loc, scale, 200)
print(fdp_tv_ta_mielke.min(), fdp_tv_ta_mielke.max())

# plt.title("Histograma")
# plt.xlabel("X axis")
# plt.ylabel("Y axis")
# plt.xlim(0, 60)
# # plt.ylim(0, 1300)
# plt.hist(fdp_tv_ta_burr12, bins=200)
# plt.show()

#Grafico continua
# x = np.linspace(0, 50, 500)
#
# y = stats.burr12.pdf(x, c, d, loc=loc, scale=scale)
#
# plt.plot(x, y)
# plt.title("Distribución burr12")
# plt.xlabel("Tiempo")
# plt.ylabel("Densidad")
# plt.grid(True)
# plt.show()
