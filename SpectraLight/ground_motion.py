# -*- coding: utf-8 -*-
import numpy as np


class GroundMotion(object):
    def __init__(self, gmName, gmFile):
        self.name = gmName
        self.filepath = gmFile
        self.t, self.ag = self._read_gmfile(self.filepath)
        self.drawHist = False
        self.writeSpec = False
        self.drawSpec = False
        self.specs = []

    def _read_gmfile(self, filepath):
        temp = np.loadtxt(filepath, dtype='float', delimiter='\t', skiprows=1)
        t = temp[:, 0]
        ag = temp[:, 1]
        return (t, ag)


class Spectrum(object):
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label=label
        self.ID=0
        self.zeta=0
        self.type=''
