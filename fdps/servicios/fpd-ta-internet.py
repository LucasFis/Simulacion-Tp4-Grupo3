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

llamadas_internet = llamadas[
    (llamadas["Cola"] == "tortu-int") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO")
]

llamadas_internet = llamadas_internet.dropna(subset=["TA_numerico"])

llamadas_internet["TA_min"] = llamadas_internet["TA_numerico"] / 60

#Grafico histograma

llamadas_internet.hist('TA_min', bins=200)
plt.show()

#Fdp TA internet:

fdp_internet_ta = Fitter(llamadas_internet.TA_min)
fdp_internet_ta.fit()
print(fdp_internet_ta.summary())
print(fdp_internet_ta.get_best(method="sumsquare_error"))

a = -2.8996295458678
b = 1.3726737511794445
loc = -0.0742865510715616
scale = 0.6081178959478482

fdp_internet_ta_johnsonsu = stats.johnsonsu.rvs(a, b, loc, scale, 10000)

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_internet_ta_johnsonsu, bins=200)
plt.show()

#Grafico continua
x = np.linspace(0, 50, 500)

y = stats.johnsonsu.pdf(x, a, b, loc=loc, scale=scale)

plt.plot(x, y)
plt.title("Distribución johnsonsu")
plt.xlabel("Tiempo")
plt.ylabel("Densidad")
plt.grid(True)
plt.show()
