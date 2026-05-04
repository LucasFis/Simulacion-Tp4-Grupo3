import random

def eleccion_cola():
    r = random.random()  # número entre 0 y 1

    if r < 0.6161:
        return "INT"
    elif r < 0.6161 + 0.1197:
        return "TEL"
    elif r < 0.6161 + 0.1197 + 0.1781:
        return "TV"
    else:
        return "SIM"

def elegir_puesto(TPS, STO, HV):
    libres = [i for i in range(len(TPS)) if TPS[i] == HV]



    return max(libres, key=lambda i: STO[i])

def se_arrepiente():
    r = random.random()

    return r < 0.1

def redondear(valor, decimales):
    factor = 10 ** decimales
    if valor >= 0:
        return int(valor * factor + 0.5) / factor
    else:
        return int(valor * factor - 0.5) / factor