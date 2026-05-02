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

llamadas_telefonia = llamadas[
    (llamadas["Cola"] == "tortu-tel") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO")
]

llamadas_telefonia = llamadas_telefonia.dropna(subset=["TA_numerico"])

llamadas_telefonia["TA_min"] = llamadas_telefonia["TA_numerico"] / 60

#Grafico histograma
#
llamadas_telefonia.hist('TA_min', bins=200)
plt.show()

#Fdp TA internet:

fdp_telefonia_ta = Fitter(llamadas_telefonia.TA_min)
fdp_telefonia_ta.fit()
print(fdp_telefonia_ta.summary(3))
print(fdp_telefonia_ta.get_best(method="sumsquare_error"))

u = 2.4831921870607196
s = 0.5248640126200628
a = 7.853682872770126
b = 1.9938410482735183
loc = -0.031295580192663916
scale = 0.271584523255729

fdp_internet_ta_dpareto_lognorm = stats.dpareto_lognorm.rvs(u, s, a, b, loc, scale, 10000)

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_internet_ta_dpareto_lognorm, bins=200)
plt.show()

#Grafico continua
x = np.linspace(0, 50, 500)

y = stats.dpareto_lognorm.pdf(x, u, s,a, b, loc=loc, scale=scale)

plt.plot(x, y)
plt.title("Distribución dpareto_lognorm")
plt.xlabel("Tiempo")
plt.ylabel("Densidad")
plt.grid(True)
plt.show()

