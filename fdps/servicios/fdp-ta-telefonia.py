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
    (llamadas["Estado"] != "ABANDONO") &
    (llamadas["TA_numerico"] > 20)
]

llamadas_telefonia = llamadas_telefonia.dropna(subset=["TA_numerico"])

llamadas_telefonia["TA_min"] = llamadas_telefonia["TA_numerico"] / 60

print(llamadas_telefonia.value_counts())

#Grafico histograma
#
# llamadas_telefonia.hist('TA_min', bins=200)
# plt.show()

#Fdp TA internet:

#fdp_telefonia_ta = Fitter(llamadas_telefonia.TA_min)
#fdp_telefonia_ta.fit()
#print(fdp_telefonia_ta.summary(3))
#print(fdp_telefonia_ta.get_best(method="sumsquare_error"))

a = 0.25272397442857464
b = 0.9149481236528247
c = 1.965332216326705
loc = 0.4166666624026105
scale = 2.1216173497193322

fdp_internet_ta_genexpon = stats.genexpon.rvs(a, b, c, loc, scale, 300)
print(fdp_internet_ta_genexpon.min(), fdp_internet_ta_genexpon.max())

#plt.title("Histograma")
#plt.xlabel("X axis")
#plt.ylabel("Y axis")
#plt.xlim(0, 20)
#plt.ylim(0, 300)
#plt.hist(fdp_internet_ta_dpareto_lognorm, bins=200)
#plt.show()

#Grafico continua
x = np.linspace(0, 50, 500)

y = stats.genexpon.cdf(x, a, b, c, loc=loc, scale=scale)

plt.plot(x, y)
plt.title("Distribución")
plt.xlabel("Tiempo")
plt.ylabel("Densidad")
plt.grid(True)
plt.show()

