# GeeTest Challenger

通过观看 [QIN2DIM's Challenger](https://www.wolai.com/pbhA77godFuXjofA1QC7JG?theme=light) 了解本项目的工作范围

## Introduction

[ArmourGeeTest](https://github.com/QIN2DIM/armour-geetest) 是一种针对 [GeeTest滑动验证 ](https://www.geetest.com/) 的高通过率解决方案；引入`动量收敛` 以及 `震荡` 等仿生算法解决二维空间中的像素对齐问题。当这个难倒了大批爬虫玩家的问题被抽象成`缺口识别`以及`像素对齐`两个指标时使用本方案进行百次实验：

- 当`缺口识别率`为100%时，`gt3`通过率为92%。失败案例中超半数由收敛超时引发，剩下的被怪兽吃掉了；
- 当`缺口识别率`为100%时，`gt2`通过率100%。仅在缺口被遮挡时失败，但此时倾向认为`缺口识别率`<100%；

## Preview

1. 本项目依赖 `google-chrome` 完成挑战，请确保您的设备中已装有 **最新版谷歌浏览器**！
2. 本项目由 `webdriver-manager` 实现驱动托管。因此，你不需要关心浏览器驱动的存放路径问题，只要你的设备上装了谷歌浏览器，`webdriver-manager` 可以自动下载版本匹配的驱动并放置到绝对索引路径。

## Usage

1. Clone project

   ```bash
   git clone https://github.com/QIN2DIM/armour-geetest.git armor-geetest
   ```

2. Initialize workspace

   ```bash
   cd armor-geetest/ && pip install -r requirements.txt && cd src
   ```

3. Run the demo

   ```bash
   # armor-geetest/src/
   python main.py demo --version=3 --debug=True --silence=False
   ```
