import numpy as np
from scipy import stats

def ta_internet():
    a = 2.051524387177043
    b = 5.456008966942054
    loc = 0.2902148888942779
    scale = 6.396128391941712

    u = np.random.uniform(0.000001, 0.999999)
    x = stats.betaprime.ppf(u, a, b, loc, scale)
    return x


def ta_telefonia():
    a = 0.25272397442857464
    b = 0.9149481236528247
    c = 1.965332216326705
    loc = 0.4166666624026105
    scale = 2.1216173497193322
    z = np.random.uniform(0.000001, 0.999999)
    x = stats.genexpon.ppf(z, a, b, c, loc, scale)
    return x


def ta_internet_movil():
    a = 1.2824763189951953
    loc = 0.3529866902558564
    scale = 2.7430708499927383
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.erlang.ppf(u, a, loc, scale)
    return x

def ta_cable():
    k = 1.120685328694003
    s = 2.5868147327627664
    loc = 0.36162384506728507
    scale = 4.867007896499102
    u = np.random.uniform(0.000001, 0.999999)
    x = stats.mielke.ppf(u, k, s, loc, scale)
    return x

