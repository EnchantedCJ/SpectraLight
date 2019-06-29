# SpectraLight

Describe: Earthquake response spectrum solver and drawer

Version: 0.3

Last update: 2019-06-29

Author: CJ

## 文件说明

### SpectraLight

​		源代码

### input

​		输入文件

### output

​		输出文件

### config.json

​		配置文件

### SpectraLight.py

​		程序入口

## 使用说明

### 1. 将地震动文件放在``./input``下

​		地震动文件格式
```
30000					# number of time steps
0	-0.0733142			# time acceleration
0.01	-0.0732189
0.02	-0.0731554
...
```

### 2. 在``config.json``中修改基本设置

- **gms**

  - **name: *str***
  - **file: *str***
  - **drawHist: *bool***
  - **writeSpec: *bool***
  - **drawSpec: *bool***

- **spectrums**

  - **ID: *int***

    反应谱ID，不可重复

  - **type: *str***

    - **SA:** 绝对加速度反应谱

    - **SV:** 相对速度反应谱

    - **SD:** 相对位移反应谱

    - **PSA:** 拟加速度反应谱

    - **PSV:** 拟速度反应谱

    - **FOURIER:** 傅里叶幅值谱

      为了与ESV对比，这里是归一化因子为dt的单边谱

    - **ESV: **地震终了时的输入能量等价速度谱

      $$\sqrt{\frac{2E(t)}{m}}=\{[\dot{x}(t)]^2+[\omega x(t)^2]\}^{\frac{1}{2}}$$

    - **PLSA: **弹塑性绝对加速度反应谱

    - **PLSV: **弹塑性相对速度反应谱

    - **PLSD: **弹塑性相对位移反应谱
  
    - **PLENG: **弹塑性势能反应谱
  
  - **dT: *float***
  
    反应谱周期间隔
  
  - **Tmax: *float***
  
    反应谱最大周期
  
  - **zeta: *float***
  
    阻尼比
  
  - **elastoplastic**
  
    弹塑性反应谱参数，type为PLSA、PLSV或PLSD时生效
  
    - **hysteretic: *str***
  
      滞回模型（目前仅支持双线性模型）
  
    - **R: *float***
  
      承载力降低系数
  
    - **beta: *float***
  
      强化系数
  
- **code**

  - **draw: *bool***

  - **cp: *str***

    ​		场地类别 -- I0  I1  II  III  IV

  - **gp: *str***

    ​		设计地震分组 -- 1  2  3

  - **inp: *list of str***

    ​		规范反应谱

    ​		61--6度多遇    62--6度设防    63--6度罕遇 
    
    ​		71--7度多遇    72--7度设防    73--7度罕遇
    
    ​		81--8度多遇    82--8度设防    83--8度罕遇
    
    ​		91--9度多遇    92--9度设防    93--9度罕遇

- **settings**

  - **inputDir: *str***

    输入地震动路径

  - **outputDIr: *str***

    输出结果路径

  - **method: *str***

    - **fft:** 快速傅里叶变换（小阻尼比时误差大）
    - **cdm: **中心差分法（慢，条件稳定）

  - **nfft: *int***

    快速傅里叶变换点数，应大于地震动点数，宜取2的整数次幂

  - **drawIn1**

    - **name: *str***

      输出图片名称

    - **draw: *bool***

      是否将反应谱画在一幅图内

    - **xlabel: *str***

      图片横坐标

    - **ylabel: *str***

      图片纵坐标


### 3. 在`./output`查看输出结果

- 时程曲线
- 反应谱曲线
- 反应谱数据