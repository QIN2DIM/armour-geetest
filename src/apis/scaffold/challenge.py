# -*- coding: utf-8 -*-
# Time       : 2022/4/26 22:25
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
from services.geetest_challenger import GeeTest2, GeeTest3, get_ctx, GeeTestV3Utils
from services.settings import PATH_FULL_IMG, PATH_NOTCH_IMG, logger

__all__ = ["runner"]


@logger.catch()
def runner(url: str, v: str, silence=False, debug=True):
    """

    :param debug:
    :param url:
    :param v:
    :param silence:
    :return:
    """
    if v == "2":
        challenger = GeeTest2(PATH_FULL_IMG, PATH_NOTCH_IMG, debug=debug)
    elif v == "3":
        challenger = GeeTest3(PATH_FULL_IMG, PATH_NOTCH_IMG, debug=debug)
    else:
        raise ValueError

    with get_ctx(silence=silence, fast=True) as ctx:
        ctx.get(url)

        # 演示站点切换 tag
        if "geetest.com" in url:
            GeeTestV3Utils.switch_to_v3_demo(ctx)
            ctx.refresh()
            GeeTestV3Utils.switch_to_v3_demo(ctx)

        while not challenger.run(ctx):
            pass
