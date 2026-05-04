import math

from TAs import ta_cable, ta_internet_movil, ta_internet, ta_telefonia
from IAs import generar_intervalo_arribo
from elecciones import eleccion_cola, elegir_puesto, se_arrepiente, redondear

class Contexto:
    def __init__(self, cInt, cTel, cTv, cIm, TF, DIA, TURNO):
        self.HV = 51240412412

        # Tiempos
        self.T = 0
        self.TF = TF

        #Ambiente
        self.DIA = DIA
        self.TURNO = TURNO

        # Servidores
        self.NINT = cInt
        self.NTEL = cTel
        self.NTV = cTv
        self.NIM = cIm

        # Estadísticas
        self.STLLINT = 0
        self.STLLTEL = 0
        self.STLLTV = 0
        self.STLLIM = 0

        self.STSINT = 0
        self.STSTEL = 0
        self.STSTV = 0
        self.STSIM = 0

        self.STAINT = 0
        self.STATEL = 0
        self.STATV = 0
        self.STAIM = 0

        # Ocupación
        self.STOINT = [0] * self.NINT
        self.STOTEL = [0] * self.NTEL
        self.STOTV = [0] * self.NTV
        self.STOIM = [0] * self.NIM
        self.ITOINT = [0] * self.NINT
        self.ITOTEL = [0] * self.NTEL
        self.ITOTV = [0] * self.NTV
        self.ITOIM = [0] * self.NIM
        self.NTINT = 0
        self.NTTEL = 0
        self.NTTV = 0
        self.NTIM = 0

        # Eventos futuros
        self.TPLL = 0
        self.TPSINT = [self.HV] * self.NINT
        self.TPSTEL = [self.HV] * self.NTEL
        self.TPSTV = [self.HV] * self.NTV
        self.TPSIM = [self.HV] * self.NIM

        # Colas
        self.NSINT = 0
        self.NSTEL = 0
        self.NSTV = 0
        self.NSIM = 0

        self.SarrInt = 0
        self.SarrTV = 0
        self.SarrIM = 0
        self.SarrTel = 0

def buscar_minimo(TPSArray):
    min_val = TPSArray[0]
    min_index = 0

    for i in range(len(TPSArray)):
        if TPSArray[i] < min_val:
            min_val = TPSArray[i]
            min_index = i

    return min_index

def simular(cInt, cTel, cTv, cIm, TF, DIA, TURNO):
    ctx = Contexto(cInt, cTel, cTv, cIm, TF, DIA, TURNO)

    def determinar_evento():

        eventos = []

        eventos.append(("LL", ctx.TPLL, None))

        if ctx.TPSINT:
            i_int = buscar_minimo(ctx.TPSINT)
            eventos.append(("SINT", ctx.TPSINT[i_int], i_int))

        if ctx.TPSTEL:
            i_tel = buscar_minimo(ctx.TPSTEL)
            eventos.append(("STEL", ctx.TPSTEL[i_tel], i_tel))

        if ctx.TPSTV:
            i_tv = buscar_minimo(ctx.TPSTV)
            eventos.append(("STV", ctx.TPSTV[i_tv], i_tv))

        if ctx.TPSIM:
            i_sim = buscar_minimo(ctx.TPSIM)
            eventos.append(("SIM", ctx.TPSIM[i_sim], i_sim))

        tipo, tiempo, index = min(eventos, key=lambda x: x[1])

        return tipo, index

    # ------ COMIENZO LLEGADAS -----------
    def operar_llegada():
        ctx.T = ctx.TPLL

        IA = generar_intervalo_arribo(ctx.DIA, ctx.TURNO)

        ctx.TPLL = ctx.T + IA

        c = eleccion_cola()

        if c == "INT":
            manejar_llegada_internet()
        elif c == "TEL":
            manejar_llegada_telefonia()
        elif c == "TV":
            manejar_llegada_cable()
        else:
            manejar_llegada_internet_movil()

    def manejar_llegada_internet():
        ctx.NSINT += 1

        if ctx.NSINT <= ctx.NINT:
            ctx.STLLINT += ctx.T

            j = elegir_puesto(ctx.TPSINT, ctx.STOINT, ctx.HV)
            ctx.STOINT[j] += ctx.T - ctx.ITOINT[j]
            ta_int = ta_internet()
            ctx.STAINT += ta_int
            ctx.TPSINT[j] = ctx.T + ta_int
            ctx.NTINT += 1
        elif not se_arrepiente():
            ctx.STLLINT += ctx.T
            ctx.NTINT += 1
        else:
            ctx.NSINT -= 1
            ctx.SarrInt += 1

    def manejar_llegada_telefonia():
        ctx.NSTEL += 1

        if ctx.NSTEL <= ctx.NTEL:
            ctx.STLLTEL += ctx.T
            j = elegir_puesto(ctx.TPSTEL, ctx.STOTEL, ctx.HV)
            ctx.STOTEL[j] += ctx.T - ctx.ITOTEL[j]
            ta_tel = ta_telefonia()
            ctx.STATEL += ta_tel
            ctx.TPSTEL[j] = ctx.T + ta_tel
            ctx.NTTEL += 1
        elif not se_arrepiente():
            ctx.STLLTEL += ctx.T
            ctx.NTTEL += 1
        else:
            ctx.NSTEL -= 1
            ctx.SarrTV += 1

    def manejar_llegada_cable():
        ctx.NSTV += 1

        if ctx.NSTV <= ctx.NTV:
            ctx.STLLTV += ctx.T

            j = elegir_puesto(ctx.TPSTV, ctx.STOTV, ctx.HV)
            ctx.STOTV[j] += ctx.T - ctx.ITOTV[j]
            ta_tv = ta_cable()
            ctx.STATV += ta_tv
            ctx.TPSTV[j] = ctx.T + ta_tv
            ctx.NTTV += 1
        elif not se_arrepiente():
            ctx.STLLTV += ctx.T
            ctx.NTTV += 1
        else:
            ctx.NSTV -= 1
            ctx.SarrTV += 1

    def manejar_llegada_internet_movil():

        ctx.NSIM += 1

        if ctx.NSIM <= ctx.NIM:
            ctx.STLLIM += ctx.T
            j = elegir_puesto(ctx.TPSIM, ctx.STOIM, ctx.HV)
            ctx.STOIM[j] += ctx.T - ctx.ITOIM[j]
            ta_sim = ta_internet_movil()
            ctx.STAIM += ta_sim
            ctx.TPSIM[j] = ctx.T + ta_sim
            ctx.NTIM += 1

        elif not se_arrepiente():
            ctx.STLLIM += ctx.T
            ctx.NTIM += 1
        else:
            ctx.NSIM -= 1
            ctx.SarrIM += 1

    # ------ COMIENZO SALIDAS -----------

    def operar_salida_internet(index):

        ctx.T = ctx.TPSINT[index]

        ctx.STSINT += ctx.T
        ctx.NSINT -= 1
        if ctx.NSINT >= ctx.NINT:
            ta_int = ta_internet()
            ctx.STAINT += ta_int
            ctx.TPSINT[index] = ctx.T + ta_int
        else:
            ctx.ITOINT[index] = ctx.T
            ctx.TPSINT[index] = ctx.HV

    def operar_salida_cable(index):

        ctx.T = ctx.TPSTV[index]
        ctx.STSTV += ctx.T
        ctx.NSTV -= 1
        if ctx.NSTV >= ctx.NTV:
            ta_TV = ta_cable()
            ctx.STATV += ta_TV
            ctx.TPSTV[index] = ctx.T + ta_TV
        else:
            ctx.ITOTV[index] = ctx.T
            ctx.TPSTV[index] = ctx.HV

    def operar_salida_telefonia(index):

        ctx.T = ctx.TPSTEL[index]
        ctx.STSTEL += ctx.T
        ctx.NSTEL -= 1
        if ctx.NSTEL >= ctx.NTEL:
            ta_TEL = ta_telefonia()
            ctx.STATEL += ta_TEL
            ctx.TPSTEL[index] = ctx.T + ta_TEL
        else:
            ctx.ITOTEL[index] = ctx.T
            ctx.TPSTEL[index] = ctx.HV

    def operar_salida_internet_movil(index):

        ctx.T = ctx.TPSIM[index]
        ctx.STSIM += ctx.T
        ctx.NSIM -= 1
        if ctx.NSIM >= ctx.NIM:
            ta_IM = ta_internet_movil()
            ctx.STAIM += ta_IM
            ctx.TPSIM[index] = ctx.T + ta_IM
        else:
            ctx.ITOIM[index] = ctx.T
            ctx.TPSIM[index] = ctx.HV

    def procesar_resultados():
        stats = []

        # -------- INTERNET --------
        PECINT = redondear((ctx.STSINT - ctx.STLLINT - ctx.STAINT) / ctx.NTINT if ctx.NTINT > 0 else 0, 5)
        PTOINT = [0] * ctx.NINT
        PARRINT = ctx.SarrInt * 100 / (ctx.NTINT + ctx.SarrInt)
        for i in range(ctx.NINT):
            PTOINT[i] = redondear((ctx.STOINT[i] * 100) / ctx.T if ctx.T > 0 else 0, 5)

        stats.append(Stat(PECINT, PTOINT, PARRINT, "Internet", ctx.NINT))

        # -------- TELEFONIA --------

        PECTEL = redondear((ctx.STSTEL - ctx.STLLTEL - ctx.STATEL) / ctx.NTTEL if ctx.NTTEL > 0 else 0, 5)
        PTOTEL = [0] * ctx.NTEL
        PARRTEL = ctx.SarrTel * 100 / (ctx.NTTEL + ctx.SarrTel)
        for i in range(ctx.NTEL):
            PTOTEL[i] = redondear((ctx.STOTEL[i] * 100) / ctx.T if ctx.T > 0 else 0, 5)

        stats.append(Stat(PECTEL, PTOTEL, PARRTEL, "Telefonia", ctx.NTEL))

        # -------- TV --------

        PECTV = redondear((ctx.STSTV - ctx.STLLTV - ctx.STATV) / ctx.NTTV if ctx.NTTV > 0 else 0, 5)
        PTOTV = [0] * ctx.NTV
        PARRTV = ctx.SarrTV * 100 / (ctx.NTTV + ctx.SarrTV)
        for i in range(ctx.NTV):
            PTOTV[i] = redondear((ctx.STOTV[i] * 100) / ctx.T if ctx.T > 0 else 0, 5)

        stats.append(Stat(PECTV, PTOTV, PARRTV, "Television", ctx.NTV))

        # -------- IM --------

        PECSIM = redondear((ctx.STSIM - ctx.STLLIM - ctx.STAIM) / ctx.NTIM if ctx.NTIM > 0 else 0, 5)
        PTOSIM = [0] * ctx.NIM
        PARRIM = ctx.SarrIM * 100 / (ctx.NTIM + ctx.SarrIM)
        for i in range(ctx.NIM):
            PTOSIM[i] = redondear((ctx.STOIM[i] * 100) / ctx.T if ctx.T > 0 else 0, 5)

        stats.append(Stat(PECSIM, PTOSIM, PARRIM, "Internet movil", ctx.NIM))

        return stats

    class Stat:
        def __init__(self, PEC, PTO, PARR, servicio, var_control):
            self.PEC = PEC
            self.PTO = PTO
            self.PARR = PARR
            self.servicio = servicio
            self.control = var_control

        def __str__(self):
            string = f"Servicio: {self.servicio}"

            string += f"\nPromedio de espera en cola: {math.floor(self.PEC)}:{math.floor((self.PEC - math.floor(self.PEC))*60)} (mm:ss)"
            for i in range(self.control):
                string += f"\nPuesto {i + 1}: {self.PTO[i]} % ocioso"

            string += f"\nPorcentaje de abandonos: {self.PARR} %\n"
            return string

    while True:
        evento, index = determinar_evento()
        if evento == "LL":
            operar_llegada()
        elif evento == "SINT":
            operar_salida_internet(index)
        elif evento == "STEL":
            operar_salida_telefonia(index)
        elif evento == "STV":
            operar_salida_cable(index)
        else:
            operar_salida_internet_movil(index)

        if not ctx.T <= ctx.TF:
            if ctx.NSINT > 0 or ctx.NSTEL > 0 or ctx.NSTV > 0 or ctx.NSIM > 0:
                ctx.TPLL = ctx.HV
            else:
                return procesar_resultados()

def dar_mejor_contexto(estadisticas):
    mejor = estadisticas[0]

    def score(contexto):
        stats = contexto["stats"]

        total_PARR = sum(s.PARR for s in stats)*100 # porcentaje
        total_PEC = sum(s.PEC for s in stats)/0.5 # minutos
        total_PTO = sum(sum(s.PTO) for s in stats)/100 # porcentaje

        return total_PARR * 2 + total_PEC * 3 + total_PTO

    for contexto in estadisticas:
        if score(contexto) < score(mejor):
            mejor = contexto

    return mejor

estadisticas = []
mejor_stat_lunes = None
print("\nLunes - Mañana")
for n_int in range(1,4):
    for n_tel in range(1,4):
        for n_tv in range(1,4):
            for n_im in range(1,4):
                if n_int + n_tel + n_tv + n_im > 7:
                    continue
                else:
                    estadisticas.append({
                        "config": (n_int, n_tel, n_tv, n_im),
                        "stats": simular(n_int, n_tel, n_tv, n_im, 360, "V", "M")
                    })

mejor = dar_mejor_contexto(estadisticas)

print("Mejor configuración:")
print(f"INT={mejor['config'][0]}, TEL={mejor['config'][1]}, TV={mejor['config'][2]}, IM={mejor['config'][3]}")

for stat in mejor["stats"]:
    print(stat)


# stats_repeticion = []
# iteraciones = 10
#
# for i in range(iteraciones):
#     stats_repeticion.append(simular(2, 1, 1, 1, 360, "L", "M"))
#
# for servicio in ["Internet", "Television", "Internet movil", "Telefonia"]:
#     suma_pec = 0
#     suma_parr = 0
#     suma_pto = 0
#
#     for simulacion in stats_repeticion:      # cada simulacion es una lista de Stat
#         for stat in simulacion:
#             if stat.servicio == servicio:
#                 suma_pec += stat.PEC
#                 suma_parr += stat.PARR
#                 suma_pto += sum(stat.PTO) / len(stat.PTO)
#
#     print(f"\nServicio: {servicio}")
#     print(f"Espera por persona: {math.floor(suma_pec/iteraciones)}:{math.floor((suma_pec/iteraciones - math.floor(suma_pec/iteraciones))*60)} (minutos:segundos)")
#     print(f"Abandono de llamada: {redondear(suma_parr / iteraciones,2)} %")
#     print(f"Tiempo ocioso: {redondear(suma_pto / iteraciones,2)} %")




# largo_plazo = simular(2, 1, 1, 1, 360, "L", "M")
#
# for servicio in ["Internet", "Television", "Internet movil", "Telefonia"]:
#     for stat in largo_plazo:
#         if stat.servicio == servicio:
#             print(stat)

# TURNO = "T"
# TF=210

# TURNO = "N"
# TF=300