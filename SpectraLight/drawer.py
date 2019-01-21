# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

times12 = fm.FontProperties(fname='C:/Windows/Fonts/times.ttf', size=12)
times14 = fm.FontProperties(fname='C:/Windows/Fonts/times.ttf', size=14)
times16 = fm.FontProperties(fname='C:/Windows/Fonts/times.ttf', size=16)
arial16 = fm.FontProperties(fname='C:/Windows/Fonts/arial.ttf', size=16)
simsun14 = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc', size=14)
simsun16 = fm.FontProperties(fname='C:/Windows/Fonts/simsun.ttc', size=16)
simhei14 = fm.FontProperties(fname='C:/Windows/Fonts/simhei.ttf', size=14)
simhei16 = fm.FontProperties(fname='C:/Windows/Fonts/simhei.ttf', size=16)
plt.rcParams['axes.unicode_minus'] = False


def history(tHist, hist, label, filename):
    '''

    :param tHist: ndarray
    :param hist: ndarray
    :param label: str
    :param filename: str

    :return:
        none
    '''
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    ax.plot(tHist, hist * 100, zorder=-5, label=label)
    ax.set_axisbelow(True)
    ax.set_xlabel('Time(s)', fontproperties=times16, labelpad=130)
    ax.set_ylabel('Acceleration(cm/s^2)', fontproperties=times16)
    ax.set_xlim(0, np.max(ax.get_xticks()))
    lim_y1 = int(max(np.max(ax.get_yticks()), abs(np.min(ax.get_yticks()))))
    ax.set_ylim(-lim_y1, lim_y1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    plt.xticks(fontproperties=times14)
    plt.yticks(fontproperties=times14)
    # ax.set_yticks(np.arange(-lim_y1, lim_y1 + 200, 200))
    ax.grid(linestyle='--')
    ax.legend(loc='upper right', prop=times14, frameon=True, edgecolor='k', framealpha=1.0, fancybox=False)
    fig.savefig(filename, dpi=300, bbox_inches='tight')


def spectrum(tSpecList, specList, labelList, cp, gp, inp, filename):
    '''

    :param tSpecList: list
    :param specList: list
    :param labelList: list

    :param cp: str
        site type -- I0  I1  II  III  IV

    :param gp: str
        design group -- 1  2  3

    :param inp: list of str
        code spectra

        61--6度多遇  62--6度设防  63--6度罕遇
        71--7度多遇  72--7度设防  73--7度罕遇
        81--8度多遇  82--8度设防  83--8度罕遇
        91--9度多遇  92--9度设防  93--9度罕遇

    :param filename:

    :return:
        none
    '''

    readCh = np.loadtxt('./SpectraLight/code/spectrum-' + cp + '-' + gp + '.csv', dtype=np.str, delimiter=',')
    tSpecCh = readCh[:, 0].astype(np.float)
    specCh = {'61': readCh[:, 1].astype(np.float),
              '62': readCh[:, 2].astype(np.float),
              '63': readCh[:, 3].astype(np.float),
              '71': readCh[:, 4].astype(np.float),
              '72': readCh[:, 5].astype(np.float),
              '73': readCh[:, 6].astype(np.float),
              '81': readCh[:, 7].astype(np.float),
              '82': readCh[:, 8].astype(np.float),
              '83': readCh[:, 9].astype(np.float),
              '91': readCh[:, 10].astype(np.float),
              '92': readCh[:, 11].astype(np.float),
              '93': readCh[:, 12].astype(np.float)}
    specChLabel = {'61': '6度多遇',
                   '62': '6度设防',
                   '63': '6度罕遇',
                   '71': '7度多遇',
                   '72': '7度设防',
                   '73': '7度罕遇',
                   '81': '8度多遇',
                   '82': '8度设防',
                   '83': '8度罕遇',
                   '91': '9度多遇',
                   '92': '9度设防',
                   '93': '9度罕遇'}

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)

    # our spectra
    for i in range(len(tSpecList)):
        ax.plot(tSpecList[i], specList[i] * 100, label=labelList[i])
    # code spectra
    for i in range(len(inp)):
        ax.plot(tSpecCh, specCh[inp[i]] * 980, label=specChLabel[inp[i]])

    ax.set_xlabel('Periods(s)', fontproperties=times16)
    ax.set_ylabel('Sa(cm/s^2)', fontproperties=times16)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, np.max(ax.get_yticks()))
    plt.xticks(fontproperties=times14)
    plt.yticks(fontproperties=times14)
    ax.grid(linestyle='--')
    plt.legend(loc='upper right', prop=simsun14, frameon=True, edgecolor='k', framealpha=1.0, fancybox=False)
    fig.savefig(filename, dpi=300, bbox_inches='tight')
