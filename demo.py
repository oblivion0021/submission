import remi.gui as gui
from remi import start, App
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import scipy.fftpack as fft

# 模拟离心泵信号数据（实际应用中应导入文件）
def generate_signal():
    fs = 1000  # 采样频率
    t = np.arange(0, 1, 1/fs)  # 时间向量
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)  # 50Hz + 120Hz 混合信号
    return t, signal

# 转换图像为 base64 编码
def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return "data:image/png;base64," + img_str

class PumpFaultDetectionApp(App):
    def __init__(self, *args):
        super(PumpFaultDetectionApp, self).__init__(*args)
        self.data = None

    def main(self):
        # 文件导入按钮
        self.upload_btn = gui.FileUploader(width=200, height=30)
        self.upload_btn.onsuccess.do(self.on_file_upload)

        # 时域图显示区域
        self.time_domain_canvas = gui.Image(width=400, height=300)

        # 频域图显示区域
        self.freq_domain_canvas = gui.Image(width=400, height=300)

        # 故障检测按钮
        self.detection_btn = gui.Button("进行故障检测", width=200, height=50)
        self.detection_btn.onclick.do(self.on_fault_detection)

        # 数据保存按钮
        self.save_btn = gui.Button("保存分析结果", width=200, height=50)
        self.save_btn.onclick.do(self.on_save)

        # 布局
        vbox = gui.VBox()
        vbox.append(self.upload_btn)
        vbox.append(gui.Label("时域分析图"))
        vbox.append(self.time_domain_canvas)
        vbox.append(gui.Label("频域分析图"))
        vbox.append(self.freq_domain_canvas)
        vbox.append(self.detection_btn)
        vbox.append(self.save_btn)

        return vbox

    def on_file_upload(self, widget, filename):
        # 在这里加载和处理上传的文件（例如 CSV 或 TXT）
        # 模拟生成数据
        t, signal = generate_signal()
        self.data = (t, signal)
        self.update_time_domain_plot(t, signal)
        self.update_freq_domain_plot(t, signal)

    def update_time_domain_plot(self, t, signal):
        fig, ax = plt.subplots()
        ax.plot(t, signal)
        ax.set_title("时域分析")
        ax.set_xlabel("时间 (s)")
        ax.set_ylabel("信号幅度")
        img_data = fig_to_base64(fig)
        self.time_domain_canvas.set_image(img_data)

    def update_freq_domain_plot(self, t, signal):
        fs = 1000  # 采样频率
        n = len(signal)
        freq = np.fft.fftfreq(n, 1/fs)
        fft_signal = np.abs(fft.fft(signal))

        fig, ax = plt.subplots()
        ax.plot(freq[:n//2], fft_signal[:n//2])  # 显示正频率部分
        ax.set_title("频域分析")
        ax.set_xlabel("频率 (Hz)")
        ax.set_ylabel("幅度")
        img_data = fig_to_base64(fig)
        self.freq_domain_canvas.set_image(img_data)

    def on_fault_detection(self, widget):
        # 故障检测逻辑（简单的阈值示例）
        if self.data is not None:
            t, signal = self.data
            mean_signal = np.mean(signal)
            if mean_signal > 0.3:
                gui.GenericDialog("故障检测", "检测到故障", width=300, height=200).show(self)
            else:
                gui.GenericDialog("故障检测", "无故障", width=300, height=200).show(self)

    def on_save(self, widget):
        # 保存图像和结果的逻辑（这里简化为弹出保存成功提示）
        gui.GenericDialog("保存", "分析结果已保存", width=300, height=200).show(self)

start(PumpFaultDetectionApp, address='0.0.0.0', port=8081, start_browser=True)
