# SpectraLight

Describe: Earthquake response spectrum solver and drawer

Version: 0.1.0

Last update: 2019.01.21

Author: CJ

## 使用说明

1. 将``EW.txt`` ``NS.txt`` ``UD.txt``放在``SpectraLight.py``同目录

2. 在``SpectraLight.py``中可修改基本设置
    - n: 快速傅里叶变换点数，应大于地震动点数，取2的整数次幂
    - zeta: 阻尼比
    - dT: 反应谱点周期间隔
    - Tmax: 反应谱最大周期
    - cp: 场地类型
    - gp: 设计地震分组
    - inp: 规范反应谱