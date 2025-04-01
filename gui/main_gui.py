import remi.gui as gui
from remi import start, App

import analysis_gui
import diagnosis_gui
import records_gui

class MainApp(App):
    def __init__(self, *args):
        super(MainApp, self).__init__(*args)
        self.main_container = gui.VBox(width="100%", height="100%", margin="10px")
        self.main_container.style['background-color'] = '#f4f4f9'
        self.current_page = None  # 新增页面状态跟踪

    def switch_page(self, new_page):
        """ 统一处理所有页面切换 """
        if self.current_page:
            self.main_container.remove_child(self.current_page)
        self.current_page = new_page
        self.main_container.append(self.current_page)

    def main(self):
        self.main_container = gui.VBox(width="100%", height="100%", margin="10px")
        return self.show_main_ui()

    def show_main_ui(self, widget=None):
        self.main_container.empty()

        # 创建按钮容器
        self.button_container = gui.HBox(width="100%", height="10%")
        self.button_container.style['align-items'] = 'flex-start'
        self.button_container.style['justify-content'] = 'center'  # 按钮居中对齐
        self.button_container.style['margin-top'] = '20px'

        btn_analysis = gui.Button("时频域分析", width="25%", height="50px")
        btn_diagnosis = gui.Button("故障诊断", width="25%", height="50px")
        btn_records = gui.Button("读取诊断记录", width="25%", height="50px")

        # 美化按钮样式
        for btn in [btn_analysis, btn_diagnosis, btn_records]:
            btn.style['background-color'] = '#007BFF'
            btn.style['color'] = 'white'
            btn.style['border'] = 'none'
            btn.style['border-radius'] = '5px'
            btn.style['margin'] = '0 10px'

        # 为按钮绑定点击事件
        btn_analysis.onclick.do(self.show_analysis_ui)
        btn_diagnosis.onclick.do(self.show_diagnosis_ui)
        btn_records.onclick.do(self.show_records_ui)

        # 将按钮添加到容器中
        self.button_container.append(btn_analysis)
        self.button_container.append(btn_diagnosis)
        self.button_container.append(btn_records)

        # 添加到主界面
        label_container = gui.VBox(width="100%", height="30%")
        label_container.style['justify-content'] = 'center'

        label_welcome = gui.Label("欢迎使用离心泵故障诊断系统", style={"font-size": "24px", "text-align": "center", "color": "#333"})
        label_container.append(label_welcome)

        file_upload_container = gui.VBox(width="100%", height="20%")
        file_upload_container.style['align-items'] = 'center'
        file_upload_container.style['margin-top'] = '20px'

        file_uploader = gui.FileUploader(width="50%", height="auto")
        file_uploader.style['border'] = '1px solid #ccc'
        file_uploader.style['border-radius'] = '5px'
        file_uploader.style['padding'] = '10px'

        file_upload_container.append(file_uploader)

        # 将组件添加到主容器中
        self.main_container.append(self.button_container)
        self.main_container.append(label_container)
        self.main_container.append(file_upload_container)

        return self.main_container

    def show_analysis_ui(self, widget=None):
        self.switch_page(analysis_gui.get_analysis_ui(self))

    def show_diagnosis_ui(self, widget=None):
        self.switch_page(diagnosis_gui.get_diagnosis_ui(self))

    def show_records_ui(self, widget=None):
        self.switch_page(records_gui.get_records_ui(self))

# 运行应用
start(MainApp, address='0.0.0.0', port=8081, start_browser=True)
