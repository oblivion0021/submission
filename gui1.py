import remi.gui as gui
from remi import start, App
import numpy as np
import matplotlib.pyplot as plt
import pywt
from io import BytesIO
import base64

plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文字体
plt.rcParams['axes.unicode_minus'] = False  # 处理负号问题

def generate_placeholder_image():
    """ 生成默认占位图 """
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    ax.text(0.5, 0.5, "等待数据传入", fontsize=15, ha='center', va='center')
    ax.axis("off")
    return fig_to_base64(fig)

def fig_to_base64(fig):
    """ 将 matplotlib 图表转换为 base64 字符串 """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")

class PumpFaultDetectionApp(App):
    def main(self):
        self.data = None
        self.placeholder_img = generate_placeholder_image()

        # 主容器
        self.container = gui.VBox(width="100%", height="100%", margin="10px")
        
        # 左上角返回按钮
        self.back_button = gui.Button("返回主界面", width="15%", height="50px")
        self.back_button.onclick.do(self.show_main_view)
        
        self.button_container = gui.HBox(width="100%", height="auto", margin="10px")
        self.analysis_btn = gui.Button("时频域分析", width="33%", height="50px")
        self.diagnosis_btn = gui.Button("故障诊断", width="33%", height="50px")
        self.history_btn = gui.Button("读取诊断记录", width="33%", height="50px")
        self.analysis_btn.onclick.do(self.show_analysis_view)
        self.diagnosis_btn.onclick.do(self.show_diagnosis_view)
        self.history_btn.onclick.do(self.show_records_view)
        
        self.button_container.append(self.analysis_btn)
        self.button_container.append(self.diagnosis_btn)
        self.button_container.append(self.history_btn)
        
        self.info_label = gui.Label("欢迎使用离心泵故障诊断系统", width="100%", height="50px", style={"text-align": "center", "font-size": "20px"})
        
        self.file_uploader = gui.FileUploader(width="100%", height="auto")
        self.file_uploader.onsuccess.do(self.on_file_upload)
        
        # 分析界面（默认隐藏）
        self.analysis_container = gui.VBox(width="100%", height="60%")
        self.canvas_container = gui.HBox(width="100%",height="60%")
        self.time_domain_canvas = gui.Image(self.placeholder_img, width="100%", height="90%")
        self.freq_domain_canvas = gui.Image(self.placeholder_img, width="100%", height="90%")
        self.start_analysis_btn = gui.Button("开始分析", width="30%", height="50px")
        self.start_analysis_btn.onclick.do(self.perform_analysis)
        
        self.canvas_container.append(self.time_domain_canvas)
        self.canvas_container.append(self.freq_domain_canvas)
        self.analysis_container.append(self.canvas_container)
        self.analysis_container.append(self.start_analysis_btn)
        
        #诊断界面
        self.judge_button = gui.Button("开始诊断", width="50%", height="50px")
        #self.judge_button.onclick.do()
        self.save_button = gui.Button("导出诊断结果",width="50%", height="50px")
        #self.save_button.onclick.do()

        #查看记录界面
        # 创建下拉菜单 (DropDown)
        self.dropdown = gui.DropDown(width="200px", height="30px")
        
        # 向下拉菜单中添加选项
        self.dropdown.append("选项1")
        self.dropdown.append("选项2")
        self.dropdown.append("选项3")
        
        # 为下拉菜单绑定选择事件
        #self.dropdown.onchange.do(self.on_dropdown_change)

        # 标签，显示选择的值
        self.dropdown_label = gui.Label("选择的选项: ", width="100%", height="30px")

        # 添加组件
        self.container.append(self.button_container)
        self.container.append(self.info_label)
        self.container.append(self.file_uploader)
        
        return self.container

    def show_main_view(self, widget=None):
        self.container.empty()
        self.container.append(self.button_container)
        self.container.append(self.info_label)
        self.info_label.set_text("欢迎使用离心泵故障诊断系统")
        self.container.append(self.file_uploader)

    def show_analysis_view(self, widget):
        self.container.empty()
        self.container.append(self.back_button)
        self.container.append(self.button_container)
        self.container.append(self.info_label)
        self.info_label.set_text("请点击‘开始分析’以查看结果")
        self.container.append(self.analysis_container)

    def show_diagnosis_view(self,widget):
        self.container.empty()
        self.container.append(self.back_button)
        self.container.append(self.button_container)
        self.judge_button = gui.Button("开始诊断", width="50%", height="50px")

        self.save_button = gui.Button("导出诊断结果",width="50%", height="50px")

    def show_records_view(self,widget):
        self.container.empty()
        self.container.append(self.back_button)
        self.container.append(self.button_container)
        self.container.append(self.dropdown)
        self.container.append(self.dropdown_label)

    def on_file_upload(self, widget, filename):
        self.info_label.set_text(f"已选择文件: {filename}")

    def perform_analysis(self, widget):
        # 生成信号数据
        fs = 1000  # 采样率
        t = np.linspace(0, 1, fs)
        signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
        
        # 计算 CWT 变换
        scales = np.arange(1, 128)
        coefficients, frequencies = pywt.cwt(signal, scales, 'cmor', sampling_period=1/fs)
        
        # 绘制时频图
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.imshow(np.abs(coefficients), aspect='auto', extent=[0, 1, 1, 128], cmap='jet')
        ax.set_title("时频分析（CWT）")
        ax.set_xlabel("时间 (s)")
        ax.set_ylabel("尺度")
        
        self.time_domain_canvas.set_image(fig_to_base64(fig))

# 运行应用
start(PumpFaultDetectionApp, address='0.0.0.0', port=8081, start_browser=True)
