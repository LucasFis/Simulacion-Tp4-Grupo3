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

llamadas_intmovil = llamadas[
    (llamadas["Cola"] == "tortu-imowi") &
    (llamadas["Estado"] != "FUERAHORARIO") &
    (llamadas["Estado"] != "ABANDONO")
]

llamadas_intmovil = llamadas_intmovil.dropna(subset=["TA_numerico"])

llamadas_intmovil["TA_min"] = llamadas_intmovil["TA_numerico"] / 60

#Grafico histograma

# llamadas_intmovil.hist('TA_min', bins=200)
# plt.show()

#Fdp TA Internet movil:

# fdp_telefonia_ta = Fitter(llamadas_intmovil.TA_min)
# fdp_telefonia_ta.fit()
# print(fdp_telefonia_ta.summary(10))
# print(fdp_telefonia_ta.get_best(method="sumsquare_error"))

mu = 2.4831921870607196
loc = -0.031295580192663916
scale = 0.271584523255729

fdp_internet_ta_recipinvgauss = stats.recipinvgauss.rvs(mu, loc, scale, 10000)

plt.title("Histograma")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.xlim(0, 60)
# plt.ylim(0, 1300)
plt.hist(fdp_internet_ta_recipinvgauss, bins=200)
plt.show()
