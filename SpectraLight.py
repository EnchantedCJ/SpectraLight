# -*- coding: utf-8 -*-
from SpectraLight import *
import numpy as np
import os


def main():
    # config
    n = 2 ** 15  # FFT
    zeta = 0.05
    dT = 0.01
    Tmax = 6
    # site type -- I0  I1  II  III  IV
    cp = 'II'
    # design group -- 1  2  3
    gp = '2'
    # code spectra
    #
    #         61--6度多遇  62--6度设防  63--6度罕遇
    #         71--7度多遇  72--7度设防  73--7度罕遇
    #         81--8度多遇  82--8度设防  83--8度罕遇
    #         91--9度多遇  92--9度设防  93--9度罕遇
    inp = ['81', '82', '83']

    # input
    t = []
    ag = []
    filenames = ['EW', 'NS', 'UD']
    num = len(filenames)
    for i in range(num):
        temp = np.loadtxt(filenames[i] + '.txt', dtype='float', delimiter='\t', skiprows=1)
        t.append(temp[:, 0])
        ag.append(temp[:, 1])

    # spectrum
    Tn = []
    Sa = []
    for i in range(num):
        print('计算' + filenames[i] + '反应谱...\n')
        Tntemp, Satemp = solver.elastic_spectrum_fft(t[i], ag[i], n, zeta, dT, Tmax)
        Tn.append(Tntemp)
        Sa.append(Satemp)

    # draw
    # history
    for i in range(num):
        print('绘制' + filenames[i] + '时程...\n')
        drawer.history(t[i], ag[i], filenames[i], filenames[i] + '.png')
    # spectrum
    print('绘制反应谱...\n')
    drawer.spectrum(Tn, Sa, filenames, cp, gp, inp, 'spectrum.png')

    # output
    # for i in range(num):
    #     with open(filenames[i]+'-spec.txt', 'w', encoding='utf-8') as f:
    #         for j in range(np.shape(Tn[i])[0]):
    #             f.write('{Tn:.2f}'.format(Tn=Tn[i][j]))
    #             f.write('\t')
    #             f.write('{Sa:.6f}'.format(Sa=Sa[i][j]))
    #             f.write('\n')


if __name__ == '__main__':
    main()
