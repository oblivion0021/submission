import numpy as np
import matplotlib.pyplot as plt
import pywt
import io
import base64

def generate_cwt_image(signal=None, fs=1000, wavelet='cmor', width=6, height=3):
    """
    生成时频域分析（CWT）图像并返回 Base64 编码的图片数据。
    
    参数：
    - signal: 输入信号，默认生成一个正弦波
    - fs: 采样频率，默认为 1000 Hz
    - wavelet: 选择的小波函数，默认 'cmor'
    - width, height: 生成图片的尺寸
    """
    # 生成测试信号（如果没有提供）
    if signal is None:
        t = np.linspace(0, 1, fs)
        signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

    # 计算小波变换
    scales = np.arange(1, 128)
    coefficients, frequencies = pywt.cwt(signal, scales, wavelet, 1/fs)

    # 绘制时频分析图
    fig, ax = plt.subplots(figsize=(width, height), dpi=100)
    ax.imshow(np.abs(coefficients), aspect='auto', cmap='jet', extent=[0, 1, frequencies[-1], frequencies[0]])
    ax.set_ylabel("频率 (Hz)")
    ax.set_xlabel("时间 (s)")
    ax.set_title("时频域分析 (CWT)")
    ax.invert_yaxis()
    
    # 保存为 Base64 编码的图片
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    plt.close(fig)

    return "data:image/png;base64," + base64.b64encode(img_buffer.getvalue()).decode()


def diagnose_fault():
    """
    模拟离心泵故障诊断，计算信号能量并返回是否故障。

    """

