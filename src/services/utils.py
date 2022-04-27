# -*- coding: utf-8 -*-
# Time       : 2022/4/26 21:51
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description:
import os
import sys
from typing import Optional

from loguru import logger
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


class ToolBox:
    """可移植的工具箱"""

    @staticmethod
    def runtime_report(
        action_name: str, motive: str = "RUN", message: str = "", **params
    ) -> str:
        """格式化输出"""
        flag_ = f">> {motive} [{action_name}]"
        if message != "":
            flag_ += f" {message}"
        if params:
            flag_ += " - "
            flag_ += " ".join([f"{i[0]}={i[1]}" for i in params.items()])

        return flag_

    @staticmethod
    def init_log(**sink_path):
        """初始化 loguru 日志信息"""
        event_logger_format = (
            "<g>{time:YYYY-MM-DD HH:mm:ss}</g> | "
            "<lvl>{level}</lvl> - "
            # "<c><u>{name}</u></c> | "
            "{message}"
        )
        logger.remove()
        logger.add(
            sink=sys.stdout,
            colorize=True,
            level="DEBUG",
            format=event_logger_format,
            diagnose=False,
        )
        if sink_path.get("error"):
            logger.add(
                sink=sink_path.get("error"),
                level="ERROR",
                rotation="1 week",
                encoding="utf8",
                diagnose=False,
            )
        if sink_path.get("runtime"):
            logger.add(
                sink=sink_path.get("runtime"),
                level="DEBUG",
                rotation="20 MB",
                retention="20 days",
                encoding="utf8",
                diagnose=False,
            )
        return logger


def get_ctx(silence: Optional[bool] = None, fast: Optional[bool] = False):
    """普通的 Selenium 驱动上下文，用于常规并发任务"""

    silence = True if silence is None or "linux" in sys.platform else silence

    options = ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    # 统一挑战语言
    os.environ["LANGUAGE"] = "zh"
    options.add_argument(f"--lang={os.getenv('LANGUAGE', '')}")

    if silence is True:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
    if fast is True:
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-javascript")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    chrome_pref = {
        "profile.default_content_settings": {"Images": 2, "javascript": 2},
        "profile.managed_default_content_settings": {"Images": 2},
    }
    options.experimental_options["prefs"] = chrome_pref
    d_c = DesiredCapabilities.CHROME
    d_c["pageLoadStrategy"] = "none"

    service = Service(ChromeDriverManager(log_level=0).install())
    return Chrome(service=service, options=options, desired_capabilities=d_c)  # noqa
