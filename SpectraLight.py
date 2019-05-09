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
    type = conf['spectrums']['type']
    method = conf['spectrums']['method']
    nfft = conf['spectrums']['nfft']

    # check
    if not type in ['SA', 'SV', 'SD', 'PSA', 'PSV']:
        print('Error: undefined spectrum type!')
        exit(0)
    if not method in ['fft']:
        print('Error: undefined method!')
        exit(0)

    for gm in gms:
        if gm.writeSpec or gm.drawSpec:
            print(gm.name)
            # Spectrums with different zetas
            specs = []
            for zeta in zetas:
                x, y = solver.elastic_spectrum_fft(type, gm.t, gm.ag, nfft, zeta, dT, Tmax)
                label = gm.name + ' h=' + str(zeta)
                spec = ground_motion.Spectrum(x, y, label)
                spec.zeta = zeta
                spec.type = type
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
                filename = dir + gm.name + '-' + spec.type + '-h' + str(spec.zeta) + '.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    for i in range(spec.x.size):
                        f.write('{x:.2f}'.format(x=spec.x[i]))
                        f.write('\t')
                        f.write('{y:.6f}'.format(y=spec.y[i]))
                        f.write('\n')


def draw_spectrums(gms, conf):
    print('------ 绘制反应谱 ------')
    dir = conf['settings']['outputDir']
    type = conf['spectrums']['type']
    drawCode = conf['spectrums']['code']['draw']
    drawIn1 = conf['spectrums']['drawIn1']
    if not os.path.exists(dir):
        os.mkdir(dir)

    code = {'cp': 'I0',
            'gp': '1',
            'inp': []}
    if drawCode and type in ['SA', 'PSA']:
        code['cp'] = conf['spectrums']['code']['cp']
        code['gp'] = conf['spectrums']['code']['gp']
        code['inp'] = conf['spectrums']['code']['inp']

    # set x,y label
    xyLabel = ['', '']
    if type == 'SA':
        xyLabel = ['Periods(s)', 'Sa(m/s^2)']
    if type == 'SV':
        xyLabel = ['Periods(s)', 'Sv(m/s)']
    if type == 'SD':
        xyLabel = ['Periods(s)', 'Sd(m)']
    if type == 'PSA':
        xyLabel = ['Periods(s)', 'Pseudo Sa(m/s^2)']
    if type == 'PSV':
        xyLabel = ['Periods(s)', 'Pseudo Sv(m/s)']

    if drawIn1:
        xList = []
        yList = []
        labelList = []
        for gm in gms:
            print(gm.name)
            xList = xList + [spec.x for spec in gm.specs]
            yList = yList + [spec.y for spec in gm.specs]
            labelList = labelList + [spec.label for spec in gm.specs]
            filename = dir + type + '.png'
            drawer.spectrum(xList, yList, labelList, xyLabel, code, filename)
    else:
        for gm in gms:
            if gm.drawSpec:
                print(gm.name)
                xList = [spec.x for spec in gm.specs]
                yList = [spec.y for spec in gm.specs]
                labelList = [spec.label for spec in gm.specs]
                filename = dir + gm.name + '-' + type + '.png'
                drawer.spectrum(xList, yList, labelList, xyLabel, code, filename)


def main():
    conf = config.read_config('config.json')
    gms = get_gms(conf)
    draw_gms(gms, conf)
    cal_spectrums(gms, conf)
    write_spectrums(gms, conf)
    draw_spectrums(gms, conf)


if __name__ == '__main__':
    main()
