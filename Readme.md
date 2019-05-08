# SpectraLight

Describe: Earthquake response spectrum solver and drawer

Version: 0.2.0

Last update: 2019-05-08

Author: CJ

## 文件说明

### SpectraLight

​	源代码

### input

​	输入文件

### output

​	输出文件

### config.json

​	配置文件

### SpectraLight.py

​	程序入口

## 使用说明

### 1. 将地震动文件放在``./input``下

地震动文件格式

```
 30000				# number of time steps
 0	-0.0733142		# time acceleration
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

  - **zetas: *list of float***

    ​	阻尼比

  - **dT: *float***

    ​	反应谱周期间隔

  - **Tmax: *float***

    ​	反应谱最大周期

  - **code**

    - **draw: *bool***

    - **cp: *str***

      ​	场地类别 -- I0  I1  II  III  IV

    - **gp: *str***

      ​	设计地震分组 -- 1  2  3

    - **inp: *list of str***

      ​	规范反应谱
      
      ​	61--6度多遇  62--6度设防  63--6度罕遇
      ​	71--7度多遇  72--7度设防  73--7度罕遇
      ​	81--8度多遇  82--8度设防  83--8度罕遇
      ​	91--9度多遇  92--9度设防  93--9度罕遇
    
    - **method: *str***
    
      ​	fft
    
    - **nfft: *int***
    
      ​	快速傅里叶变换点数，应大于地震动点数，取2的整数次幂


### 3. 在`./output`查看输出结果

- 时程曲线
- 反应谱曲线
- 反应谱数据