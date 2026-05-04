import random

def eleccion_servicio():
    r = random.random()  # número entre 0 y 1

    if r < 0.568:
        return "INT"
    elif r < 0.568 + 0.255:
        return "TV"
    elif r < 0.568 + 0.255 + 0.105:
        return "TEL"
    else:
        return "IM"

def elegir_puesto(TPS, STO, HV):
    libres = [i for i in range(len(TPS)) if TPS[i] == HV]

    for i in libres:
        if STO[i] == 0:
            return i

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