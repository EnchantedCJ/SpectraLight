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
    print('------ 计算谱 ------')
    method = conf['settings']['method']
    nfft = conf['settings']['nfft']

    specConfs = conf['spectrums']
    for specConf in specConfs:
        ID = specConf['ID']
        type = specConf['type']
        if type == 'code':
            continue
        dT = specConf['dT']
        Tmax = specConf['Tmax']
        zeta = specConf['zeta']
        epconf = specConf['elastoplastic']

        print('Calculating spectrum:', type)

        # check
        if not type in ['SA', 'SV', 'SD', 'PSA', 'PSV', 'FOURIER', 'ESV', 'PLSA', 'PLSV', 'PLSD', 'PLENG']:
            print('Error: undefined spectrum type!')
            exit(0)
        if not method in ['fft', 'cdm']:
            print('Error: undefined method!')
            exit(0)

        for gm in gms:
            if gm.writeSpec or gm.drawSpec:
                print(gm.name)
                x = 0
                y = 0
                label = ''
                if type in ['SA', 'SV', 'SD', 'PSA', 'PSV', 'ESV']:
                    if method == 'fft':
                        x, y = solver.elastic_spectrum_fft(type, gm.t, gm.ag, nfft, zeta, dT, Tmax)
                    if method == 'cdm':
                        x, y = solver.elastic_spectrum_cdm(type, gm.t, gm.ag, zeta, dT, Tmax)
                    label = gm.name + ' ' + type + ' h=' + str(zeta)
                if type in ['FOURIER']:
                    x, y = solver.fourier_spectrum(gm.t, gm.ag, nfft)
                    label = gm.name + ' ' + type
                if type in ['PLSA', 'PLSV', 'PLSD', 'PLENG']:
                    if not method == 'cdm':
                        print('Error: Elastoplastic spectrum can only be calculated using central difference method!')
                        exit(0)
                    R = epconf['R']  # 承载力降低系数
                    beta = epconf['beta']  # 强化系数
                    x, y = solver.elastoplastic_spectrum_cdm(type, gm.t, gm.ag, zeta, dT, Tmax, R, beta)
                    label = gm.name + ' ' + 'R=' + str(R) + ' ' + 'beta=' + str(beta)
                spec = ground_motion.Spectrum(x, y, label)
                spec.ID = ID
                spec.zeta = zeta
                spec.type = type
                gm.specs.append(spec)


def write_spectrums(gms, conf):
    print('------ 输出谱 ------')
    dir = conf['settings']['outputDir']
    if not os.path.exists(dir):
        os.mkdir(dir)

    for gm in gms:
        if gm.writeSpec:
            print(gm.name)
            for spec in gm.specs:
                filename = dir + gm.name + '-' + str(spec.ID) + '-' + spec.type + '-h' + str(spec.zeta) + '.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    for i in range(spec.x.size):
                        f.write('{x:.2f}'.format(x=spec.x[i]))
                        f.write('\t')
                        f.write('{y:.6f}'.format(y=spec.y[i]))
                        f.write('\n')


def draw_spectrums(gms, conf):
    print('------ 绘制谱 ------')

    dir = conf['settings']['outputDir']
    drawIn1 = conf['settings']['drawIn1']['draw']
    name = conf['settings']['drawIn1']['name']
    xlabel = conf['settings']['drawIn1']['xlabel']
    ylabel = conf['settings']['drawIn1']['ylabel']
    specConfs = conf['spectrums']
    drawCode = conf['code']['draw']
    if not os.path.exists(dir):
        os.mkdir(dir)

    # default code
    code = {'cp': 'I0',
            'gp': '1',
            'inp': []}

    if not drawIn1:
        # one type in one figure
        for specConf in specConfs:
            ID = specConf['ID']
            type = specConf['type']
            print('Drawing spectrum:', type)

            if drawCode and type in ['SA', 'PSA']:
                code['cp'] = conf['code']['cp']
                code['gp'] = conf['code']['gp']
                code['inp'] = conf['code']['inp']

            # set x,y label
            xyLabel = ['', '']
            if type == 'SA':
                xyLabel = ['Periods (s)', 'Sa (m/s^2)']
            if type == 'SV':
                xyLabel = ['Periods (s)', 'Sv (m/s)']
            if type == 'SD':
                xyLabel = ['Periods (s)', 'Sd (m)']
            if type == 'PSA':
                xyLabel = ['Periods (s)', 'Pseudo Sa (m/s^2)']
            if type == 'PSV':
                xyLabel = ['Periods (s)', 'Pseudo Sv (m/s)']
            if type == 'FOURIER':
                xyLabel = ['Peirods (s)', 'Amplitude (m/s)']

            # get all spectrums in this type
            xList = []
            yList = []
            labelList = []
            for gm in gms:
                if gm.drawSpec:
                    print(gm.name)
                    for spec in gm.specs:
                        if spec.ID == ID:
                            xList.append(spec.x)
                            yList.append(spec.y)
                            labelList.append(spec.label)

            filename = dir + str(ID) + '-' + type + '.png'
            drawer.spectrum(xList, yList, labelList, xyLabel, code, filename)
    else:
        # all types in one figure
        if drawCode:
            code['cp'] = conf['code']['cp']
            code['gp'] = conf['code']['gp']
            code['inp'] = conf['code']['inp']

        # set x,y label
        xyLabel = [xlabel, ylabel]

        # get all spectrums in this type
        xList = []
        yList = []
        labelList = []
        for gm in gms:
            if gm.drawSpec:
                print(gm.name)
                for spec in gm.specs:
                    xList.append(spec.x)
                    yList.append(spec.y)
                    labelList.append(spec.label)

        filename = dir + name + '.png'
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
