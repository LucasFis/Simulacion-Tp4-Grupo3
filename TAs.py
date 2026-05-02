import numpy as np
from scipy import stats

def ta_internet():
    a = -2.8996295458678
    b = 1.3726737511794445
    loc = -0.0742865510715616
    scale = 0.6081178959478482
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.johnsonsu.ppf(u, a, b, loc, scale)
    return x

def ta_telefonia():
    u = 2.4831921870607196
    s = 0.5248640126200628
    a = 7.853682872770126
    b = 1.9938410482735183
    loc = -0.031295580192663916
    scale = 0.271584523255729
    z = np.random.uniform(0.000001, 0.999999)
    x = stats.dpareto_lognorm.ppf(z, u, s, a, b, loc, scale)
    return x

def ta_internet_movil():
    mu = 2.4831921870607196
    loc = -0.031295580192663916
    scale = 0.271584523255729
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.recipinvgauss.ppf(u, mu, loc, scale)
    return x

def ta_tv():
    c = 1.6971927282569945
    d = 2.0086650709449665
    loc = -0.051670023524274175
    scale = 5.382486631799211
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.burr12.ppf(u, c, d, loc, scale)
    return x

