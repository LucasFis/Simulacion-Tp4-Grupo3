import math

from TAs import ta_cable, ta_internet_movil, ta_internet, ta_telefonia
from IAs import generar_intervalo_arribo
from elecciones import eleccion_servicio, elegir_puesto, se_arrepiente, redondear

class Contexto:
    def __init__(self, N, TF, DIA, TURNO):
        self.HV = 51240412412

        # Tiempos
        self.T = 0
        self.TF = TF

        #Ambiente
        self.DIA = DIA
        self.TURNO = TURNO

        # Servidores
        self.N = N

        # Estadísticas
        self.STLL = 0

        self.STS = 0

        self.STA = 0

        # Ocupación
        self.STO = [0] * self.N
        self.ITO = [0] * self.N
        self.NT = 0

        # Eventos futuros
        self.TPLL = 0
        self.TPS = [self.HV] * self.N

        # Colas
        self.NS = 0

        self.Sarr = 0

def buscar_minimo(TPSArray):
    min_val = TPSArray[0]
    min_index = 0

    for i in range(len(TPSArray)):
        if TPSArray[i] < min_val:
            min_val = TPSArray[i]
            min_index = i

    return min_index

def calcular_porcentaje_abandono(arrepentidos, atendidos):
    total = atendidos + arrepentidos
    return arrepentidos * 100 / total if total > 0 else 0

def simular(N, TF, DIA, TURNO):
    ctx = Contexto(N, TF, DIA, TURNO)

    def determinar_evento():
        minimo_tps = buscar_minimo(ctx.TPS)

        if ctx.TPLL <= ctx.TPS[minimo_tps]:
            return "LL", 0
        else: return "S", minimo_tps

    # ------ COMIENZO LLEGADAS -----------
    def operar_llegada():
        ctx.T = ctx.TPLL

        IA = generar_intervalo_arribo(ctx.DIA, ctx.TURNO)

        ctx.TPLL = ctx.T + IA

        servicio = eleccion_servicio()

        manejar_llegada(servicio)

    def manejar_llegada(servicio):
        ctx.NS += 1

        if ctx.NS <= ctx.N:
            ctx.STLL += ctx.T

            j = elegir_puesto(ctx.TPS, ctx.STO, ctx.HV)
            ctx.STO[j] += ctx.T - ctx.ITO[j]
            if servicio == "INT":
                ta = ta_internet()
            elif servicio == "TEL":
                ta = ta_telefonia()
            elif servicio == "TV":
                ta = ta_cable()
            else: ta = ta_internet_movil()
            ctx.STA += ta
            ctx.TPS[j] = ctx.T + ta
            ctx.NT += 1
        elif not se_arrepiente():
            ctx.STLL += ctx.T
            ctx.NT += 1
        else:
            ctx.NS -= 1
            ctx.Sarr += 1

    # ------ COMIENZO SALIDAS -----------

    def manejar_salida(index):

        ctx.T = ctx.TPS[index]
        ctx.STS += ctx.T
        ctx.NS -= 1

        servicio = eleccion_servicio()

        if ctx.NS >= ctx.N:
            if servicio == "INT":
                ta = ta_internet()
            elif servicio == "TEL":
                ta = ta_telefonia()
            elif servicio == "TV":
                ta = ta_cable()
            else:
                ta = ta_internet_movil()
            ctx.STA += ta
            ctx.TPS[index] = ctx.T + ta
        else:
            ctx.ITO[index] = ctx.T
            ctx.TPS[index] = ctx.HV


    def procesar_resultados():
        PEC = redondear((ctx.STS - ctx.STLL - ctx.STA) / ctx.NT if ctx.NT > 0 else 0, 5)
        PTO = [0] * ctx.N
        PARR = calcular_porcentaje_abandono(ctx.Sarr, ctx.NT)
        for i in range(ctx.N):
            PTO[i] = redondear((ctx.STO[i] * 100) / ctx.T if ctx.T > 0 else 0, 5)

        return Stat(PEC, PTO, PARR, ctx.N, ctx.NT, ctx.Sarr)

    class Stat:
        def __init__(self, PEC, PTO, PARR, var_control, clientes, arrepentidos):
            self.PEC = PEC
            self.PTO = PTO
            self.PARR = PARR
            self.control = var_control
            self.clientes = clientes
            self.arrepentidos = arrepentidos

        def __str__(self):
            string = f"\nPromedio de espera en cola: {math.floor(self.PEC)}:{math.floor((self.PEC - math.floor(self.PEC))*60)} (mm:ss)"
            for i in range(self.control):
                string += f"\nPuesto {i + 1}: {self.PTO[i]} % ocioso"

            string += f"\nPorcentaje de abandonos: {self.PARR} %\n"
            string += f"Clientes: {self.clientes}\n"
            string += f"Arrepentidos: {self.arrepentidos}\n"
            return string

    while True:
        evento, index = determinar_evento()
        if evento == "LL":
            operar_llegada()
        elif evento == "S":
            manejar_salida(index)

        if not ctx.T <= ctx.TF:
            if ctx.NS > 0:
                ctx.TPLL = ctx.HV
            else:
                return procesar_resultados()

def simular_promedio(N, TF, DIA, TURNO, repeticiones):
    primer_stat = simular(N, TF, DIA, TURNO)

    for _ in range(repeticiones - 1):
        otra_stat = simular(N, TF, DIA, TURNO)
        primer_stat.PEC += otra_stat.PEC
        primer_stat.PARR += otra_stat.PARR
        primer_stat.clientes += otra_stat.clientes
        primer_stat.arrepentidos += otra_stat.arrepentidos
        for i in range(len(otra_stat.PTO)):
            primer_stat.PTO[i] += otra_stat.PTO[i]

    primer_stat.PEC = primer_stat.PEC / repeticiones
    primer_stat.PARR = primer_stat.PARR / repeticiones
    primer_stat.clientes = primer_stat.clientes / repeticiones
    primer_stat.arrepentidos = primer_stat.arrepentidos / repeticiones
    for i in range(len(primer_stat.PTO)):
        primer_stat.PTO[i] = primer_stat.PTO[i] / repeticiones
    return primer_stat

iteraciones = 10
for i in range(iteraciones):
    print(simular(3, 360, "L", "M"))

# probar_optimo("L", "M", 4)
# probar_optimo("V", "M", 4)
# probar_optimo("L", "T", 4)
# probar_optimo("V", "T", 4)
# probar_optimo("L", "N", 4)
# probar_optimo("V", "N", 4)

# resultados = simular(1, 1, 1, 1, 360, "L", "M")
#
# for servicio in ["Internet", "Television", "Internet movil", "Telefonia"]:
#     for stat in resultados:
#         if stat.servicio == servicio:
#             print(stat)

# TURNO = "T"
# TF=210

# TURNO = "N"
# TF=300
