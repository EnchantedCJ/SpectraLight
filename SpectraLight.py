# -*- coding: utf-8 -*-
from SpectraLight import *
import os


def get_gms(conf):
    print('------ 读取地震动 ------')
    dir = conf['settings']['inputDir']
    gmDatas = conf['gms']

    gms = []
    for gmData in gmDatas:
        gmName = gmData['name']
        gmFile = dir + gmData['file']
        print('Name: {n}\tPath: {p}'.format(n=gmName, p=gmFile))
        gm = ground_motion.GroundMotion(gmName, gmFile)
        gm.drawHist = gmData['drawHist']
        gm.writeSpec = gmData['writeSpec']
        gm.drawSpec = gmData['drawSpec']
        gms.append(gm)
    return gms


def draw_gms(gms, conf):
    print('------ 绘制时程 ------')
    dir = conf['settings']['outputDir']
    if not os.path.exists(dir):
        os.mkdir(dir)

    for gm in gms:
        if gm.drawHist:
            print(gm.name)
            filename = dir + gm.name + '.png'
            drawer.history(gm.t, gm.ag, gm.name, filename)


def cal_spectrums(gms, conf):
    print('------ 计算反应谱 ------')

    zetas = conf['spectrums']['zetas']
    dT = conf['spectrums']['dT']
    Tmax = conf['spectrums']['Tmax']
    method = conf['spectrums']['method']
    nfft = conf['spectrums']['nfft']

    # check
    if not method in ['fft']:
        print('Error: undefined method!')
        exit(0)

    for gm in gms:
        if gm.writeSpec or gm.drawSpec:
            print(gm.name)
            # Spectrums with different zetas
            specs = []
            for zeta in zetas:
                Tn, Sa = solver.elastic_spectrum_fft(gm.t, gm.ag, nfft, zeta, dT, Tmax)
                label = gm.name + ' h=' + str(zeta)
                spec = ground_motion.Spectrum(Tn, Sa, label)
                specs.append(spec)
            gm.specs = specs


def write_spectrums(gms, conf):
    print('------ 输出反应谱 ------')
    dir = conf['settings']['outputDir']
    if not os.path.exists(dir):
        os.mkdir(dir)

    for gm in gms:
        if gm.writeSpec:
            print(gm.name)
            for spec in gm.specs:
                filename = dir + gm.name + '-spec.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    for i in range(spec.x.size):
                        f.write('{x:.2f}'.format(x=spec.x[i]))
                        f.write('\t')
                        f.write('{y:.6f}'.format(y=spec.y[i]))
                        f.write('\n')


def draw_spectrums(gms, conf):
    print('------ 绘制反应谱 ------')
    dir = conf['settings']['outputDir']
    drawCode = conf['spectrums']['code']['draw']
    if not os.path.exists(dir):
        os.mkdir(dir)

    code = {'cp': 'I0',
            'gp': '1',
            'inp': []}
    if drawCode:
        code['cp'] = conf['spectrums']['code']['cp']
        code['gp'] = conf['spectrums']['code']['gp']
        code['inp'] = conf['spectrums']['code']['inp']

    for gm in gms:
        if gm.drawSpec:
            print(gm.name)
            xList = [spec.x for spec in gm.specs]
            yList = [spec.y for spec in gm.specs]
            labelList = [spec.label for spec in gm.specs]
            xyLabel = ['Periods(s)', 'Sa(m/s^2)']
            filename = dir + gm.name + '-spec.png'
            drawer.spectrum(xList, yList, labelList, xyLabel, code, filename)


def main():
    conf = config.read_config('config.json')
    gms = get_gms(conf)
    draw_gms(gms, conf)
    cal_spectrums(gms, conf)
    write_spectrums(gms, conf)
    draw_spectrums(gms, conf)

    # # config
    # n = 2 ** 15  # FFT
    # zeta = 0.05
    # dT = 0.01
    # Tmax = 6
    # # site type -- I0  I1  II  III  IV
    # cp = 'II'
    # # design group -- 1  2  3
    # gp = '2'
    # # code spectra
    # #
    # #         61--6度多遇  62--6度设防  63--6度罕遇
    # #         71--7度多遇  72--7度设防  73--7度罕遇
    # #         81--8度多遇  82--8度设防  83--8度罕遇
    # #         91--9度多遇  92--9度设防  93--9度罕遇
    # inp = ['81', '82', '83']
    #
    # # input
    # t = []
    # ag = []
    # filenames = ['EW', 'NS', 'UD']
    # num = len(filenames)
    # for i in range(num):
    #     temp = np.loadtxt(filenames[i] + '.txt', dtype='float', delimiter='\t', skiprows=1)
    #     t.append(temp[:, 0])
    #     ag.append(temp[:, 1])

    # # spectrum
    # Tn = []
    # Sa = []
    # for i in range(num):
    #     print('计算' + filenames[i] + '反应谱...\n')
    #     Tntemp, Satemp = solver.elastic_spectrum_fft(t[i], ag[i], n, zeta, dT, Tmax)
    #     Tn.append(Tntemp)
    #     Sa.append(Satemp)
    #
    # # draw
    # # history
    # for i in range(num):
    #     print('绘制' + filenames[i] + '时程...\n')
    #     drawer.history(t[i], ag[i], filenames[i], filenames[i] + '.png')
    # # spectrum
    # print('绘制反应谱...\n')
    # drawer.spectrum(Tn, Sa, filenames, cp, gp, inp, 'spectrum.png')


if __name__ == '__main__':
    main()
