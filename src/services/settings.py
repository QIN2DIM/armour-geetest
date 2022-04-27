# -*- coding: utf-8 -*-
# Time       : 2021/7/22 0:48
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import time
from os.path import dirname, join, exists

from services.geetest_challenger import ToolBox

__all__ = [
    "PROJECT_ROOT",
    "DIR_CACHE",
    "PROJECT_DATABASE",
    "PATH_FULL_IMG",
    "PATH_NOTCH_IMG",
    "DEMO_SITE",
    "BUSINESS_CHALLENGE",
    "logger",
]

#  - 如何知道更多类似的使用geetest滑动验证的站点？请访问：
#   https://github.com/QIN2DIM/sspanel-mining
DEMO_SITE = "https://www.geetest.com/show"
BUSINESS_CHALLENGE = "https://geo.captcha-delivery.com/captcha/?initialCid=AHrlqAAAAAMAFzLgJAHPdNIASt4UGg%3D%3D&hash=4797D6E193ECA8320444B1243C4609&cid=.CzjV1WIKgNPKa.bkwBCb0gvY-~Ta7gMRDzd5CpRG8QpG8ijYuy~vBXHbArVbjler.KdxY~EWK7.gOnsMio3pgf2Kt3ySCJaMmA0ml-mPj4xHRndkLPlc3_0K6HDDaix"
# ---------------------------------------------------
# [√] 項目定位
# ---------------------------------------------------
PROJECT_ROOT = dirname(__file__)
PROJECT_DATABASE = join(PROJECT_ROOT, "../database")
DIR_CACHE = join(PROJECT_DATABASE, "cache")
PATH_FULL_IMG = join(DIR_CACHE, f"full_img_{time.time()}.png")
PATH_NOTCH_IMG = join(DIR_CACHE, f"notch_img_{time.time()}.png")
DIR_LOG = join(PROJECT_DATABASE, "logs")
# ---------------------------------------------------
# [√] 服务器日志配置
# ---------------------------------------------------
logger = ToolBox.init_log(
    error=join(DIR_LOG, "error.log"), runtime=join(DIR_LOG, "runtime.log")
)

# 避免因.gitignore造成的目录残缺引发的FileNotFound错误
for _pending in [PROJECT_DATABASE, DIR_CACHE]:
    if not exists(_pending):
        os.mkdir(_pending)
