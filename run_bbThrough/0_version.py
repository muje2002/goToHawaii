# kiwoom login전에 버전관리가 될 수 있도록 이 스크립트가 불려야 된다.
# 윈도우의 자동프로그램을 이용하여 이 코드가 매일 2시 50분에 돌수 있도록 설정하자.
"""
1. anaconda 32 bit로 설정
2. pywinauto 설치
3. python 을 3.7.5 version으로 down 할것 (혹은 3.8.0)
    > - pycharm - File - settings - project interpreter - conda environment 에서 python을 선택하고 specify version을 3.7.5로 선택하여 install
4. pycharm 을 관리자 권한으로 실행해야 한다.
https://github.com/pywinauto/SWAPY
SWAPY를 통해 윈도우 창의 구성을 확인할 수 있다.
"""
from pywinauto.application import Application
from pywinauto import timings
import time
import os

if __name__ == "__main__":
    app = Application()
    app.start("C:/KiwoomHero4/bin/nkstarter.exe")

    title = "영웅문4 Login"
    dlg = timings.wait_until_passes(20, 0.5, lambda: app.window(title=title))

    pass_ctrl = dlg.Edit2
    pass_ctrl.set_focus()
    pass_ctrl.type_keys('2002id')

    cert_ctrl = dlg.Edit3
    cert_ctrl.set_focus()
    cert_ctrl.type_keys('youngki80!')

    btn_ctrl = dlg.Button0
    btn_ctrl.click()

    time.sleep(180)
    os.system("taskkill /f /im nkrunlite.exe")