import remi.gui as gui
from remi import start, App
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import scipy.fftpack as fft


def generate_signal():
    """ 生成模拟离心泵故障信号（50Hz + 120Hz 叠加信号） """
    fs = 1000  # 采样频率
    t = np.linspace(0, 1, fs)  # 时间向量
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
    return t, signal


def fig_to_base64(fig):
    """ 将 matplotlib 图表转换为 base64 字符串用于前端显示 """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")


class PumpFaultDetectionApp(App):
    def __init__(self, *args):
        super(PumpFaultDetectionApp, self).__init__(*args)
        self.data = None

    def main(self):
        # 主容器（垂直布局，填满屏幕）
        container = gui.VBox(width="100%", height="100%", margin="10px")

        # 上传文件按钮
        self.upload_btn = gui.FileUploader(width="100%", height="auto")
        self.upload_btn.onsuccess.do(self.on_file_upload)

        # 时域图 & 频域图（并排布局）
        canvas_container = gui.HBox(width="100%", height="60%")
        
        # 时域图部分
        time_domain_canvas_container = gui.VBox(width="40%", height="100%")
        self.time_domain_canvas = gui.Image(width="100%", height="90%")
        time_domain_canvas_container.append(gui.Label("时域分析", style={"font-size": "20px", "text-align": "center"}))
        time_domain_canvas_container.append(self.time_domain_canvas)

        # 频域图部分
        freq_domain_canvas_container = gui.VBox(width="40%", height="100%")
        self.freq_domain_canvas = gui.Image(width="100%", height="90%")
        freq_domain_canvas_container.append(gui.Label("频域分析", style={"font-size": "20px", "text-align": "center"}))
        freq_domain_canvas_container.append(self.freq_domain_canvas)

        canvas_container.append(time_domain_canvas_container)
        canvas_container.append(freq_domain_canvas_container)

        # 按钮容器（放置 "故障检测" & "保存数据"）
        button_container = gui.HBox(width="100%", height="auto", margin="10px")
        self.detection_btn = gui.Button("进行故障检测", width="40%", height="50px")
        self.save_btn = gui.Button("保存分析结果", width="40%", height="50px")
        self.detection_btn.onclick.do(self.on_fault_detection)
        self.save_btn.onclick.do(self.on_save)
        button_container.append(self.detection_btn)
        button_container.append(self.save_btn)

        # 组装界面
        container.append(self.upload_btn)
        container.append(canvas_container)
        container.append(button_container)

        return container

    def on_file_upload(self, widget, filename):
        """ 文件上传回调函数，加载数据 """
        # 这里可以替换为从上传文件中读取数据
        t, signal = generate_signal()
        self.data = (t, signal)
        self.update_time_domain_plot(t, signal)
        self.update_freq_domain_plot(t, signal)

    def update_time_domain_plot(self, t, signal):
        """ 绘制时域信号波形 """
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, signal)
        ax.set_title("时域分析")
        ax.set_xlabel("时间 (s)")
        ax.set_ylabel("信号幅度")
        ax.grid()
        self.time_domain_canvas.set_image(fig_to_base64(fig))

    def update_freq_domain_plot(self, t, signal):
        """ 绘制频域信号波形（FFT 变换） """
        fs = 1000  # 采样频率
        n = len(signal)
        freq = np.fft.fftfreq(n, 1/fs)
        fft_signal = np.abs(fft.fft(signal))

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(freq[:n//2], fft_signal[:n//2])  # 只绘制正频率部分
        ax.set_title("频域分析")
        ax.set_xlabel("频率 (Hz)")
        ax.set_ylabel("幅度")
        ax.grid()
        self.freq_domain_canvas.set_image(fig_to_base64(fig))

    def on_fault_detection(self, widget):
        """ 检测故障 """

    def on_save(self, widget):
        """ 数据保存操作 """


# 运行应用
start(PumpFaultDetectionApp, address='0.0.0.0', port=8081, start_browser=True)
