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
        (Tn, S)
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
        ag_max = np.max(np.abs(ag))
        S = np.array([ag_max])
    elif type in ['SV', 'SD', 'PSV', 'ESV']:
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
        if type == 'ESV':
            rd = u.real
            rv = np.gradient(rd, dt)
            endtime = ag.size
            rdt = rd[endtime]
            rvt = rv[endtime]
            ESV1 = np.sqrt(np.power(rvt, 2) + np.power(cfn1 * rdt, 2))
            S = np.append(S, ESV1)

    return (Tn, S)


def fourier_spectrum(t, ag, n):
    ag_f = np.fft.fft(ag, n)  # fourier transform of ag, two-sided
    dt = t[1] - t[0]
    freq = np.fft.fftfreq(n, d=dt)

    cut = int((n + 1) / 2)  # n/2-1 for even, (n-1)/2 for odd, both equal to int((n+1)/2)
    S = abs(ag_f)[1:cut] * dt  # get double-sided spectrum, ignore first point at 0s
    T = 1 / freq[1:cut]
    # reverse
    S = np.flip(S)
    T = np.flip(T)
    return (T, S)
    # return (freq, abs(ag_f))


def elastic_spectrum_cdm(type, t, ag, zeta, dT, Tmax):
    '''
    Compute the elastic response spectrum using central difference method.

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

    :param zeta: float
        damping ratio

    :param dT: float
        interval of period of the response spectrum

    :param Tmax: float
        maximum period considered of the response spectrum, should be integer times of dT

    :return:
        (Tn, S)
    '''

    T = np.linspace(dT, Tmax, int(Tmax / dT))
    dt = t[1] - t[0]
    length = ag.size

    # add initial point
    Tn = np.append(np.array([0]), T)
    if type in ['SA', 'PSA']:
        ag_max = np.max(np.abs(ag))
        S = np.array([ag_max])
    elif type in ['SV', 'SD', 'PSV', 'ESV']:
        S = np.array([0])
    else:
        S = np.array([0])
        print('Error: undefined spectrum type!')
        exit(0)

    for i in range(len(T)):
        cf = 2 * np.pi / T[i]
        # Initial condition
        ru = np.zeros(length + 1)
        rv = np.zeros(length)
        ra = np.zeros(length)
        ra[0] = -ag[0] - 2 * cf * zeta * rv[0] - (cf ** 2) * ru[0]
        ru_1 = ru[0] - dt * rv[0] + (dt ** 2) / 2 * ra[0]

        # coefficient
        a1 = 1 / (dt ** 2) + cf * zeta / dt
        a2 = cf ** 2 - 2 / (dt ** 2)
        a3 = 1 / (dt ** 2) - cf * zeta / dt

        # iterating
        j = 0
        ru[j + 1] = (-ag[j] - a2 * ru[j] - a3 * ru_1) / a1
        for j in range(1, length):
            ru[j + 1] = (-ag[j] - a2 * ru[j] - a3 * ru[j - 1]) / a1
            rv[j] = (ru[j + 1] - ru[j - 1]) / 2 / dt
            ra[j] = (ru[j + 1] - 2 * ru[j] + ru[j - 1]) / (dt ** 2)

        # rv=np.gradient(ru,dt)
        # ra=np.gradient(rv,dt)
        ru = ru[:length]
        rv = rv[:length]
        ra = ra[:length]

        if type == 'SA':
            aa = ra + ag
            SA1 = np.max(np.abs(aa))
            S = np.append(S, SA1)
        if type == 'SV':
            SV1 = np.max(np.abs(rv))
            S = np.append(S, SV1)
        if type == 'SD':
            SD1 = np.max(np.abs(ru))
            S = np.append(S, SD1)
        if type == 'PSA':
            SD1 = np.max(np.abs(ru))
            PSA1 = (cf ** 2) * SD1
            S = np.append(S, PSA1)
        if type == 'PSV':
            SD1 = np.max(np.abs(ru))
            PSV1 = cf * SD1
            S = np.append(S, PSV1)
        if type == 'ESV':
            rdt = ru[-1]
            rvt = rv[-1]
            ESV1 = np.sqrt(np.power(rvt, 2) + np.power(cf * rdt, 2))
            S = np.append(S, ESV1)

    return (Tn, S)


def elastoplastic_spectrum_cdm(type, t, ag, zeta, dT, Tmax, R, beta):
    '''
    Compute the elastoplastic response spectrum using central difference method.

    :param type: str
        - PLSA: 弹塑性绝对加速度反应谱
        - PLSV: 弹塑性相对速度反应谱
        - PLSD: 弹塑性相对位移反应谱
        - PLENG: 弹塑性势能反应谱

    :param t: ndarray
        time

    :param ag: ndarray
        ground motion acceleration

    :param zeta: float
        damping ratio

    :param dT: float
        interval of period of the response spectrum

    :param Tmax: float
        maximum period considered of the response spectrum, should be integer times of dT

    :param R: float
        承载力降低系数，R=1即弹性

    :param beta: float
        强化系数

    :return:
        (Tn, S)
    '''

    T = np.linspace(0.1, Tmax, int((Tmax - 0.1) / dT) + 1)
    # dt = t[1] - t[0]
    # length = ag.size

    dt = 0.0001
    newt = np.linspace(t[0], t[-1], int((t[-1] - t[0]) / dt + 1))
    ag = np.interp(newt, t, ag)
    length = ag.size

    # add initial point
    Tn = np.append(np.array([0]), T)
    if type in ['PLSA']:
        ag_max = np.max(np.abs(ag))
        S = np.array([ag_max])
    elif type in ['PLSV', 'PLSD', 'PLENG']:
        S = np.array([0])
    else:
        S = np.array([0])
        print('Error: undefined spectrum type in solver!')
        exit(0)

    for i in range(len(T)):
        # print(T[i])
        cf = 2 * np.pi / T[i]
        # Initial condition
        ru = np.zeros(length + 1)
        rv = np.zeros(length)
        ra = np.zeros(length)
        ra[0] = -ag[0] - 2 * cf * zeta * rv[0] - (cf ** 2) * ru[0]
        ru_1 = ru[0] - dt * rv[0] + (dt ** 2) / 2 * ra[0]

        ##### Calculate elastic response, find maximum response #####
        # coefficient
        a1 = 1 / (dt ** 2) + cf * zeta / dt
        a2 = cf ** 2 - 2 / (dt ** 2)
        a3 = 1 / (dt ** 2) - cf * zeta / dt

        # iterating
        j = 0
        ru[j + 1] = (-ag[j] - a2 * ru[j] - a3 * ru_1) / a1
        for j in range(1, length):
            ru[j + 1] = (-ag[j] - a2 * ru[j] - a3 * ru[j - 1]) / a1

        ru = ru[:length]
        de = np.max(abs(ru))
        fe = (cf ** 2) * de

        ##### Calculate elastoplastic response #####
        ru = np.zeros(length + 1)
        rv = np.zeros(length)
        ra = np.zeros(length)
        f = np.zeros(length + 1)

        # Bilinear hysteretic model BL2，随动强化
        gamma = 1  # 卸载刚度系数
        fy = fe / R
        k1 = cf ** 2
        k2 = beta * k1
        k3 = gamma * k1

        # coefficient
        a22 = 2 / (dt ** 2)

        # iterating
        # Steps:
        # 1) 确定新步位移
        # 2) 根据当前状态和位移变化确定新步力
        # 3) 确定新状态

        j = 0
        fmax = fy
        fmin = -fy

        ru[j + 1] = (-ag[j] - f[j] + a22 * ru[j] - a3 * ru_1) / a1
        state = 0  # 0-初始，1-加载，2-强化，3-反向加载（卸载）, 4-反向强化，5-再加载
        if ru[j + 1] > ru[j]:
            f[j + 1] = k1 * (ru[j + 1] - ru[j])
            if f[j + 1] < fmax:
                state = 1
            else:
                state = 2
                fmax = f[j + 1]
        else:
            f[j + 1] = k1 * (ru[j + 1] - ru[j])
            if f[j + 1] > fmin:
                state = 3
            else:
                state = 4
                fmin = f[j + 1]

        for j in range(1, length):
            ru[j + 1] = (-ag[j] - f[j] + a22 * ru[j] - a3 * ru[j - 1]) / a1

            if state == 1:
                if ru[j + 1] > ru[j]:
                    f[j + 1] = f[j] + k1 * (ru[j + 1] - ru[j])
                    if f[j + 1] < fmax:
                        state = 1
                    else:
                        state = 2
                        fmax = f[j + 1]
                else:
                    f[j + 1] = f[j] + k1 * (ru[j + 1] - ru[j])
                    if f[j + 1] > fmin:
                        state = 1
                    else:
                        state = 4
                        fmin = f[j + 1]

            elif state == 2:
                if ru[j + 1] > ru[j]:
                    f[j + 1] = f[j] + k2 * (ru[j + 1] - ru[j])
                    state = 2
                    fmax = f[j + 1]
                else:
                    f[j + 1] = f[j] + k3 * (ru[j + 1] - ru[j])
                    if f[j + 1] > fmax - 2 * fy:
                        state = 3
                    else:
                        state = 4
                        fmin = f[j + 1]

            elif state == 3:
                if ru[j + 1] > ru[j]:
                    f[j + 1] = f[j] + k3 * (ru[j + 1] - ru[j])
                    if f[j + 1] < fmax:
                        state = 3
                    else:
                        state = 2
                        fmax = f[j + 1]
                else:
                    f[j + 1] = f[j] + k3 * (ru[j + 1] - ru[j])
                    if f[j + 1] > fmax - 2 * fy:
                        state = 3
                    else:
                        state = 4
                        fmin = f[j + 1]

            elif state == 4:
                if ru[j + 1] > ru[j]:
                    f[j + 1] = f[j] + k1 * (ru[j + 1] - ru[j])
                    if f[j + 1] < fmin + 2 * fy:
                        state = 5
                    else:
                        state = 2
                        fmax = f[j + 1]
                else:
                    f[j + 1] = f[j] + k2 * (ru[j + 1] - ru[j])
                    state = 4
                    fmin = f[j + 1]

            elif state == 5:
                if ru[j + 1] > ru[j]:
                    f[j + 1] = f[j] + k3 * (ru[j + 1] - ru[j])
                    if f[j + 1] < fmax:
                        state = 5
                    else:
                        state = 2
                        fmax = f[j + 1]
                else:
                    f[j + 1] = f[j] + k3 * (ru[j + 1] - ru[j])
                    if f[j + 1] > fmin:
                        state = 5
                    else:
                        state = 4
                        fmin = f[j + 1]

            rv[j] = (ru[j + 1] - ru[j - 1]) / 2 / dt
            ra[j] = (ru[j + 1] - 2 * ru[j] + ru[j - 1]) / (dt ** 2)

        ru = ru[:length]
        rv = rv[:length]
        ra = ra[:length]
        f = f[:length]

        # # log
        # with open('hyst-' + str(T[i]) + '.txt', 'w', encoding='utf-8') as file:
        #     for j in range(length):
        #         file.write(str(ru[j]))
        #         file.write('\t')
        #         file.write(str(f[j]))
        #         file.write('\n')

        if type == 'PLSA':
            aa = ra + ag
            SA1 = np.max(np.abs(aa))
            S = np.append(S, SA1)
        if type == 'PLSV':
            SV1 = np.max(np.abs(rv))
            S = np.append(S, SV1)
        if type == 'PLSD':
            SD1 = np.max(np.abs(ru))
            S = np.append(S, SD1)
            S = np.append(S, SD1 / de)
        if type == 'PLENG':
            # output potential energy when SD max
            SD1 = np.max(np.abs(ru))
            ENG1 = 1 / 2 * fy / k1 * fy + (SD1 - fy / k1) * fy
            S = np.append(S, ENG1)
    return (Tn, S)
