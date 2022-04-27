# -*- coding: utf-8 -*-
# Time       : 2021/7/21 17:39
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 识别GeeTest_v3滑动验证的示例
import base64
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .core import SliderValidator


class GeeTest3(SliderValidator):
    def __init__(self, path_full_img=None, path_notch_img=None, debug=False):
        super().__init__(
            debug=debug,
            path_full_img=path_full_img,
            path_notch_img=path_notch_img,
            action_name="GeeTest_v3",
        )

    def download_challenge_images(self, ctx):
        """Get notch image and full image."""

        def get_base64img_by_canvas(class_name):
            bg_img = ""
            while len(bg_img) < 5000:
                get_img_js = (
                    'return document.getElementsByClassName("'
                    + class_name
                    + '")[0].toDataURL("image/png");'
                )
                bg_img = ctx.execute_script(get_img_js)
                time.sleep(0.5)

            return bg_img[bg_img.find(",") + 1 :]

        def save_base64img(data, path_):
            with open(path_, "wb") as f:
                f.write(base64.b64decode(data))

        touch_loop = {
            (self.notch_img_path, "geetest_canvas_bg geetest_absolute"),
            (self.full_img_path, "geetest_canvas_fullbg geetest_fade geetest_absolute"),
        }

        for tl_path, tl_class_name in touch_loop:
            stream = get_base64img_by_canvas(tl_class_name)
            save_base64img(stream, tl_path)

    @staticmethod
    def activate_validator(ctx):
        # 加载窗体
        WebDriverWait(ctx, 15, ignored_exceptions=StaleElementReferenceException).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "geetest_radar_tip"))
        ).click()

        # 加载图片和滑块
        WebDriverWait(ctx, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_slice"))
        )
        WebDriverWait(ctx, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_fullbg"))
        )

    def is_success(self, ctx) -> bool:
        try:
            WebDriverWait(ctx, 5).until(
                EC.text_to_be_present_in_element(
                    locator=(By.CLASS_NAME, "geetest_success_radar_tip_content"),
                    text_="验证成功",
                )
            )
            resp = True
        except TimeoutException:
            resp = False

        if bool(self.debug):
            print(f"--->{self.action_name}：{'驗證成功' if resp is True else '驗證失敗'}")
        return resp

    def run(self, ctx) -> bool:
        # 唤醒挑战 等待必要组件加载完成
        self.activate_validator(ctx)

        # 获取挑战图片
        self.download_challenge_images(ctx)

        # 识别缺口左边界坐标
        boundary = self.identify_boundary()

        # debug模式下 可视化识别结果
        self.check_boundary(boundary)

        # 生成轨迹
        track, position = self.generate_track(
            # 轨迹生成器解决方案
            solution=self.operator_sport_v1,
            # 计算所需的物理量初始值字典
            phys_params={
                "boundary": boundary,
                "current_coordinate": 0,
                "mid": boundary * 3.3 / 4,
                "t": 0.5,
                "alpha_factor": 3.4011,
                "beta_factor": 3.5211,
            },
        )

        # 获取滑块对象
        slider = ctx.find_element(By.CLASS_NAME, "geetest_slider_button")

        # 根据轨迹拖动滑块
        self.drag_slider(
            ctx=ctx,
            track=track,
            slider=slider,
            position=position,
            boundary=boundary,
            use_imitate=True,
            is_hold=False,
            momentum_convergence=False,
        )

        # 返回執行狀態
        return self.is_success(ctx)


class GeeTestV3Utils:
    @staticmethod
    def switch_to_v3_demo(ctx):
        time.sleep(2)
        WebDriverWait(ctx, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='滑动拼图验证']/parent::div")
            )
        ).click()

        try:
            WebDriverWait(ctx, 5).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[@style='display: block;']")
                )
            )
        except TimeoutException:
            pass
