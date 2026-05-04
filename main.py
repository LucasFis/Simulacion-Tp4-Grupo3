from TAs import ta_cable, ta_internet_movil, ta_internet, ta_telefonia
from IAs import generar_intervalo_arribo
from elecciones import eleccion_cola, elegir_puesto, se_arrepiente, redondear

HV=51240412412

#Tiempos
T=0
TF=360 #Turno mañana

#Var. control
NINT = 1
NTEL = 1
NTV = 1
NIM = 1

#Estadisticas
STLLINT = 0
STLLTEL = 0
STLLTV = 0
STLLIM = 0

STSINT = 0
STSTEL = 0
STSTV = 0
STSIM = 0

STAINT = 0
STATEL = 0
STATV = 0
STAIM = 0

STOINT = [0] * NINT
STOTEL = [0] * NTEL
STOTV = [0] * NTV
STOIM = [0] * NIM
ITOINT = [0] * NINT
ITOTEL = [0] * NTEL
ITOTV = [0] * NTV
ITOIM = [0] * NIM

NTINT = 0
NTTEL = 0
NTTV = 0
NTIM = 0


#T.E.F.
TPLL = 0
TPSINT = [HV] * NINT
TPSTEL = [HV] * NTEL
TPSTV = [HV] * NTV
TPSIM = [HV] * NIM

#Colas
NSINT = 0
NSTEL = 0
NSTV = 0
NSIM = 0

def iniciar():
    global T, TF, NINT, NTEL, NTV, NIM, TPLL, TPSINT, TPSTEL, TPSTV, TPSIM, NSINT, NSTEL, NSTV, NSIM
    T=0
    TF = 360  # Turno mañana

    # Var. control
    NINT = 1
    NTEL = 1
    NTV = 1
    NIM = 1

    global STLLINT, STLLTEL, STLLTV, STLLIM, STSINT, STSTEL, STSTV, STSIM, STOINT, STOTEL, STOTV, STOIM, ITOINT, ITOTEL, ITOTV, ITOIM, NTINT, NTTEL, NTTV, NTIM
    # Estadisticas
    STLLINT = 0
    STLLTEL = 0
    STLLTV = 0
    STLLIM = 0

    STSINT = 0
    STSTEL = 0
    STSTV = 0
    STSIM = 0


    global STAINT, STATEL, STATV, STAIM, NTINT, NTTEL, NTTV, NTIM
    STAINT = 0
    STATEL = 0
    STATV = 0
    STAIM = 0

    STOINT = [0] * NINT
    STOTEL = [0] * NTEL
    STOTV = [0] * NTV
    STOIM = [0] * NIM
    ITOINT = [0] * NINT
    ITOTEL = [0] * NTEL
    ITOTV = [0] * NTV
    ITOIM = [0] * NIM

    NTINT = 0
    NTTEL = 0
    NTTV = 0
    NTIM = 0

    # T.E.F.
    TPLL = 0
    TPSINT = [HV] * NINT
    TPSTEL = [HV] * NTEL
    TPSTV = [HV] * NTV
    TPSIM = [HV] * NIM

    # Colas
    NSINT = 0
    NSTEL = 0
    NSTV = 0
    NSIM = 0



def buscar_minimo(TPSArray):
    min_val = TPSArray[0]
    min_index = 0

    for i in range(len(TPSArray)):
        if TPSArray[i] < min_val:
            min_val = TPSArray[i]
            min_index = i

    return min_index

def determinar_evento():
    global T

    eventos = []

    eventos.append(("LL", TPLL, None))

    if TPSINT:
        i_int = buscar_minimo(TPSINT)
        eventos.append(("SINT", TPSINT[i_int], i_int))

    if TPSTEL:
        i_tel = buscar_minimo(TPSTEL)
        eventos.append(("STEL", TPSTEL[i_tel], i_tel))

    if TPSTV:
        i_tv = buscar_minimo(TPSTV)
        eventos.append(("STV", TPSTV[i_tv], i_tv))

    if TPSIM:
        i_sim = buscar_minimo(TPSIM)
        eventos.append(("SIM", TPSIM[i_sim], i_sim))

    tipo, tiempo, index = min(eventos, key=lambda x: x[1])

    return tipo, index

# ------ COMIENZO LLEGADAS -----------
def operar_llegada():
    global T
    global TPLL
    T = TPLL

    IA = generar_intervalo_arribo(DIA, TURNO)

    TPLL = T + IA

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
    global T, STLLINT, NSINT, STOINT, STAINT, TPSINT, NTINT

    NSINT += 1

    if NSINT <= NINT:
        STLLINT += T

        j = elegir_puesto(TPSINT) #Eleccion ciclica
        STOINT[j] += T-ITOINT[j]
        ta_int = ta_internet()
        STAINT += ta_int
        TPSINT[j] = T+ta_int
        NTINT += 1
    elif not se_arrepiente():
        STLLINT += T
        NTINT += 1
    else:
        NSINT -= 1


def manejar_llegada_telefonia():
    global T, STLLTEL, NSTEL, STOTEL, STATEL, TPSTEL, NTTEL

    NSTEL += 1

    if NSTEL <= NTEL:
        STLLTEL += T
        j = elegir_puesto(TPSTEL)
        STOTEL[j] += T-ITOTEL[j]
        ta_tel = ta_telefonia()
        STATEL += ta_tel
        TPSTEL[j] = T + ta_tel
        NTTEL += 1
    elif not se_arrepiente():
        NTTEL += 1
    else:
        NSTEL -=1

def manejar_llegada_cable():
    global T, STLLTV, NSTV, STOTV, STATV, TPSTV, NTTV
    NSTV += 1

    if NSTV <= NTV:
        STLLTV += T

        j = elegir_puesto(TPSTV)
        STOTV[j] += T - ITOTV[j]
        ta_tv = ta_cable()
        STATV += ta_tv
        TPSTV[j] = T + ta_tv
        NTTV += 1
    elif not se_arrepiente():
        STLLTV += T
        NTTV += 1
    else:
        NSTV -=1

def manejar_llegada_internet_movil():
    global T, STLLIM, NSIM, STOIM, STAIM, TPSIM, NTIM

    NSIM += 1

    if NSIM <= NIM:
        STLLIM += T
        j = elegir_puesto(TPSIM)
        STOIM[j] += T - ITOIM[j]
        ta_sim = ta_internet_movil()
        STAIM += ta_sim
        TPSIM[j] = T + ta_sim
        NTIM += 1

    elif not se_arrepiente():
        STLLIM += T
        NTIM += 1
    else:
        NSIM -= 1


# ------ FIN LLEGADAS -----------


# ------ COMIENZO SALIDAS -----------

def operar_salida_internet(index):
    global T, TPSINT, ITOINT, STSINT, NSINT, NINT, STAINT

    T = TPSINT[index]

    STSINT += T
    NSINT -= 1
    if NSINT >= NINT:
        ta_int = ta_internet()
        STAINT+= ta_int
        TPSINT[index] = T + ta_int
    else:
        ITOINT[index] = T
        TPSINT[index] = HV

def operar_salida_cable(index):
    global T, TPSTV, ITOTV, STSTV, NSTV, NTV, STATV

    T = TPSTV[index]
    STSTV += T
    NSTV -= 1
    if NSTV >= NTV:
        ta_TV = ta_cable()
        STATV+= ta_TV
        TPSTV[index] = T + ta_TV
    else:
        ITOTV[index] = T
        TPSTV[index] = HV

def operar_salida_telefonia(index):
    global T
    global TPSTEL
    global ITOTEL
    global STSTEL
    global NSTEL
    global NTEL
    global STATEL

    T = TPSTEL[index]
    STSTEL += T
    NSTEL -=1
    if NSTEL >= NTEL:
        ta_TEL = ta_telefonia()
        STATEL+= ta_TEL
        TPSTEL[index] = T + ta_TEL
    else:
        ITOTEL[index] = T
        TPSTEL[index] = HV

def operar_salida_internet_movil(index):
    global T
    global TPSIM
    global ITOIM
    global STSIM
    global NSIM
    global NIM
    global STAIM

    T = TPSIM[index]
    STSIM += T
    NSIM -=1
    if NSIM >= NIM:
        ta_IM = ta_internet_movil()
        STAIM+= ta_IM
        TPSIM[index] = T + ta_IM
    else:
        ITOIM[index] = T
        TPSIM[index] = HV

# ------ FIN SALIDAS -----------

def mostrar_resultados():
    global T

    # -------- INTERNET --------
    global STLLINT, STSINT, STAINT, NTINT, NINT, STOINT

    PECINT = redondear((STSINT - STLLINT - STAINT) / NTINT if NTINT > 0 else 0,5)
    PTOINT = [0] * NINT
    for i in range(NINT):
        PTOINT[i] = redondear((STOINT[i] * 100) / T if T > 0 else 0,5)

    print("Internet")
    print(f"Promedio de espera en cola: {PECINT} minutos")
    for i in range(NINT):
        print(f"Puesto {i+1}: {PTOINT[i]} % ocioso")

    # -------- TELEFONIA --------
    global STLLTEL, STSTEL, STATEL, NTTEL, NTEL, STOTEL

    PECTEL = redondear((STSTEL - STLLTEL - STATEL) / NTTEL if NTTEL > 0 else 0,5)
    PTOTEL = [0] * NTEL
    for i in range(NTEL):
        PTOTEL[i] = redondear((STOTEL[i] * 100) / T if T > 0 else 0,5)

    print("Telefonia")
    print(f"Promedio de espera en cola: {PECTEL} minutos")
    for i in range(NTEL):
        print(f"Puesto {i+1}: {PTOTEL[i]} % ocioso")

    # -------- TV --------
    global STLLTV, STSTV, STATV, NTTV, NTV, STOTV

    PECTV = redondear((STSTV - STLLTV - STATV) / NTTV if NTTV > 0 else 0,5)
    PTOTV = [0] * NTV
    for i in range(NTV):
        PTOTV[i] = redondear((STOTV[i] * 100) / T if T > 0 else 0,5)

    print("Television")
    print(f"Promedio de espera en cola: {PECTV} minutos")
    for i in range(NTV):
        print(f"Puesto {i+1}: {PTOTV[i]} % ocioso")


    # -------- SIM --------
    global STLLIM, STSIM, STAIM, NTIM, NIM, STOIM

    PECSIM = redondear((STSIM - STLLIM - STAIM) / NTIM if NTIM > 0 else 0,5)
    PTOSIM = [0] * NIM
    for i in range(NIM):
        PTOSIM[i] = redondear((STOIM[i] * 100) / T if T > 0 else 0,5)

    print("Internet Movil")
    print(f"Promedio de espera en cola: {PECSIM} minutos")
    for i in range(NIM):
        print(f"Puesto {i+1}: {PTOSIM[i]} % ocioso")

def algoritmo_simulador():
    iniciar()
    global T, TPLL, NSINT, NSTEL, NSTV, NSIM
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

        if not T <= TF:
            if NSINT > 0 or NSTEL > 0 or NSTV > 0 or NSIM > 0:
                TPLL = HV
            else:
                mostrar_resultados()
                break
#Contexto de ejecucion
DIA = "L"
TURNO = "M"
print("\nLunes - Mañana")
algoritmo_simulador()

TURNO = "T"
print("\nLunes - Tarde")
algoritmo_simulador()

TURNO = "N"
print("\nLunes - Noche")
algoritmo_simulador()

DIA = "V"
TURNO = "M"
print("\nViernes - Mañana")
algoritmo_simulador()

TURNO = "T"
print("\nViernes - Tarde")
algoritmo_simulador()

TURNO = "N"
print("\nViernes - Noche")
algoritmo_simulador()