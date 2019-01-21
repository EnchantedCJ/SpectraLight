# -*- coding: utf-8 -*-
import numpy as np


def elastic_spectrum_fft(t, ag, n, zeta, dT, Tmax):
    '''
    Compute the elastic response spectrum using FFT method.

    :param t: ndarray
        time

    :param ag: ndarray
        ground motion acceleration

    :param n: int
        number of points of FFT, better be 2^m and larger than sample length

    :param zeta: float
        damping ratio

    :param dT: float
        interval of period of the response spectrum

    :param Tmax: float
        maximum period considered of the response spectrum, should be integer times of dT

    :return:
        (Tn, Sa)
    '''

    sp = np.fft.fft(-ag, n)
    dt = t[1] - t[0]
    freq = np.fft.fftfreq(n, d=dt)
    cf = 2 * np.pi * freq

    Tn = np.linspace(dT, Tmax, int(Tmax / dT))
    cfn = 2 * np.pi / Tn

    Sa = np.array([])
    for cfn1 in cfn:
        H = 1 / (-cf ** 2 + (1j) * 2 * zeta * cfn1 * cf + cfn1 ** 2)
        U = sp * H
        u = np.fft.ifft(U, n)

        Sd1 = np.max(np.abs(u.real))
        Sa1 = (cfn1 ** 2) * Sd1
        Sa = np.append(Sa, Sa1)

    # add initial point
    Tn = np.append(np.array([0]), Tn)
    ag_max = np.max(ag)
    Sa = np.append(np.array([ag_max]), Sa)

    return (Tn, Sa)
