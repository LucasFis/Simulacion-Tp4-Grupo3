from fitter import Fitter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Carga de datos
llamadas = pd.read_csv('../call_center.csv', sep=";")

#Preparacion de datos

llamadas["TA_numerico"] = pd.to_numeric(
    llamadas["T. Atencion"],
    errors="coerce"
)

llamadas_tv = llamadas[
    (llamadas["Cola"] == "iptv") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO")
]

llamadas_tv = llamadas_tv.dropna(subset=["TA_numerico"])

llamadas_tv["TA_min"] = llamadas_tv["TA_numerico"] / 60

#Grafico histograma

# llamadas_tv.hist('TA_min', bins=200)
# plt.show()

#Fdp TA Internet movil:

# fdp_tv_ta = Fitter(llamadas_tv.TA_min)
# fdp_tv_ta.fit()
# print(fdp_tv_ta.summary(10))
# print(fdp_tv_ta.get_best(method="sumsquare_error"))

c = 1.6971927282569945
d = 2.0086650709449665
loc = -0.051670023524274175
scale = 5.382486631799211

fdp_tv_ta_burr12= stats.burr12.rvs(c, d, loc, scale, 10000)

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_tv_ta_burr12, bins=200)
plt.show()
