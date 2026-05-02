import numpy as np
from scipy import stats

def ia_lunes_maniana():
    df = 0.6473329065381139
    loc = -1.6478587279550768e-28
    scale = 7.66636374789493
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.chi.ppf(u, df, loc, scale)
    return x

def ia_lunes_tarde():
    a = 1.9868010751079173
    loc = -2.0636279622915342e-10
    scale = 4.955277601907699
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.kappa3.ppf(u, a, loc, scale)
    return x

def ia_lunes_noche():
    c = 15.772219690442558
    s = 2.0188407126934353
    loc = -0.2584689362182534
    scale = 199.46475939297915
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.powerlognorm.ppf(u, c, s, loc, scale)
    return x

def ia_viernes_maniana():
    b = 3.2268293314082763
    c = 5.9871932705168724
    loc = -13.033395258844632
    scale = 13.03339525833951
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.truncpareto.ppf(u, b, c, loc, scale)
    return x

def ia_viernes_tarde():
    nu = 0.26518687794498164
    loc = 0.9999999999999999
    scale = 13.94852112368078
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.nakagami.ppf(u, nu, loc, scale)
    return x

def ia_viernes_noche():
    b = 8.802605357768954
    c = 1.86975146455312
    loc = -68.98608797880931
    scale = 68.98608797836727
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.truncpareto.ppf(u, b, c, loc, scale)
    return x



