# -*- coding: utf-8 -*-
# Time       : 2021/7/21 17:39
# Author     : QIN2DIM
# Github     : https://github.com/QIN2DIM
# Description: 识别GeeTest_v2滑动验证的示例

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .core import SliderValidator


class GeeTest2(SliderValidator):
    def __init__(self, path_full_img=None, path_notch_img=None, debug=False):
        super().__init__(
            action_name="GeeTest_v2",
            path_full_img=path_full_img,
            path_notch_img=path_notch_img,
            debug=debug,
        )
        self.offset = 60

    def download_challenge_images(self, ctx):
        WebDriverWait(ctx, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@class,'gt_fullbg')]")
            )
        ).screenshot(filename=self.full_img_path)

        ActionChains(ctx).click_and_hold(self.slider).perform()

        WebDriverWait(ctx, 5).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//a[contains(@class,'gt_hide')]")
            )
        ).screenshot(filename=self.notch_img_path)

    def is_success(self, ctx):
        try:
            WebDriverWait(ctx, 5).until(
                EC.text_to_be_present_in_element(
                    locator=(By.CLASS_NAME, "gt_info_type"), text_="通过"
                )
            )
            resp = True
        except TimeoutException:
            resp = False

        if bool(self.debug):
            print(f"--->{self.action_name}：{'驗證成功' if resp is True else '驗證失敗'}")
        return resp

    def run(self, ctx) -> bool:
        self.download_challenge_images(ctx)

        # 识别缺口左边界坐标
        boundary = self.identify_boundary()
        boundary = boundary - 12 if 60 <= boundary <= 63 else boundary

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
                "t": 1.2,
                "alpha_factor": 0.4011,
                "beta_factor": 0.5211,
            },
        )

        # 获取滑块对象
        slider = ctx.find_element(By.XPATH, "//div[contains(@class,'slider_')]")

        # 拖动滑块
        self.drag_slider(
            ctx=ctx,
            track=track,
            slider=slider,
            position=position,
            boundary=boundary,
            use_imitate=False,
            is_hold=True,
            momentum_convergence=True,
        )

        return self.is_success(ctx)
