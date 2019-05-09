# -*- coding: utf-8 -*-
import numpy as np


def elastic_spectrum_fft(type, t, ag, n, zeta, dT, Tmax):
    '''
    Compute the elastic response spectrum using FFT method.

    :param type: str
        - SA:   绝对加速度反应谱
        - SV:   相对速度反应谱
        - SD:   相对位移反应谱
        - PSA:  拟加速度反应谱
        - PSV:  拟速度反应谱

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

    # add initial point
    Tn = np.append(np.array([0]), Tn)
    if type in ['SA', 'PSA']:
        ag_max = np.max(ag)
        S = np.array([ag_max])
    elif type in ['SV', 'SD', 'PSV']:
        S = np.array([0])
    else:
        S = np.array([0])
        print('Error: undefined spectrum type!')
        exit(0)

    for cfn1 in cfn:
        H = 1 / (-cf ** 2 + (1j) * 2 * zeta * cfn1 * cf + cfn1 ** 2)
        U = sp * H
        u = np.fft.ifft(U, n)  # u.real is relative displacement time history

        if type == 'SA':
            rd = u.real
            rv = np.gradient(rd, dt)
            ra = np.gradient(rv, dt)
            ag_zero = np.zeros(ra.shape)
            ag_zero[:ag.size] = ag
            aa = ra + ag_zero
            # aa = ra[:ag.size] + ag
            SA1 = np.max(np.abs(aa))
            S = np.append(S, SA1)
        if type == 'SV':
            rd = u.real
            rv = np.gradient(rd, dt)
            SV1 = np.max(np.abs(rv))
            S = np.append(S, SV1)
            pass
        if type == 'SD':
            SD1 = np.max(np.abs(u.real))
            S = np.append(S, SD1)
        if type == 'PSA':
            SD1 = np.max(np.abs(u.real))
            PSA1 = (cfn1 ** 2) * SD1
            S = np.append(S, PSA1)
        if type == 'PSV':
            SD1 = np.max(np.abs(u.real))
            PSV1 = cfn1 * SD1
            S = np.append(S, PSV1)

    return (Tn, S)
