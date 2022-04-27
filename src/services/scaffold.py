# -*- coding: utf-8 -*-
# Time       : 2022/4/26 22:21
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from typing import Optional

from apis.scaffold import challenge
from services.settings import DEMO_SITE, logger


class Scaffold:
    """System scaffolding Top-level interface commands"""

    @staticmethod
    def demo(
        silence: Optional[bool] = False,
        version: Optional[str] = None,
        debug: Optional[bool] = True,
    ):
        """
        Usage: python main.py demo
            - python main.py demo --version=2
            - python main.py demo --version=3
            - python main.py demo --debug=False

        :param debug: Default ``True`` 显示控制台日志，显示切口识别图像。
        :param version: Default ``3`` 切换 v2 v3 的滑块挑战。
        :param silence: Default ``False`` 显示启动浏览器。
        :return:
        """
        version = "3" if version is None else version
        if version in ["2"]:
            logger.warning(
                "[启用]暂未将 GeeTestV2 的测试站点编入设置，请执行 v3 测试 ``python main.py --version=3``"
            )
            raise ImportError
        if version not in ["3"]:
            logger.debug("``python main.py --version=3``")
            return

        challenge.runner(url=DEMO_SITE, v=version, silence=silence, debug=debug)
