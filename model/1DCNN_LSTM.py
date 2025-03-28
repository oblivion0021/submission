import numpy as np
import librosa
import librosa.display
import pywt
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, LSTM, TimeDistributed
from tensorflow.keras.layers import Dropout, BatchNormalization, Reshape
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib


#  1. 数据处理


# 声学数据特征提取（梅尔频谱）
def extract_acoustic_features(audio_data, sr=16000, n_mels=128):
    mel_spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr, n_mels=n_mels)
    mel_db = librosa.power_to_db(mel_spectrogram, ref=np.max)  # 转换为 dB
    return mel_db

# 振动数据特征提取（小波变换 CWT）
def extract_vibration_features(vibration_data):
    scales = np.arange(1, 64)  # 64 级小波变换
    coeffs, _ = pywt.cwt(vibration_data, scales, wavelet='morl')  # CWT 变换
    return np.abs(coeffs)  # 取绝对值


def load_data(filename):
    data = np.loadtxt(filename, delimiter='\t')
    return data[:, :-1], data[:, -1]  # 返回特征和标签


acoustic_data, acoustic_labels = load_data('acoustic_data.txt')
vibration_data, vibration_labels = load_data('vibration_data.txt')


#  2. 特征提取


acoustic_features = np.array([extract_acoustic_features(sample) for sample in acoustic_data])
vibration_features = np.array([extract_vibration_features(sample) for sample in vibration_data])

# 归一化数据
scaler = StandardScaler()
acoustic_features = scaler.fit_transform(acoustic_features.reshape(len(acoustic_features), -1)).reshape(acoustic_features.shape)
vibration_features = scaler.fit_transform(vibration_features.reshape(len(vibration_features), -1)).reshape(vibration_features.shape)

# 数据标签
labels = to_categorical(acoustic_labels)  # 假设两个数据集的标签一致

# 拆分数据集
X_train_a, X_test_a, y_train, y_test = train_test_split(acoustic_features, labels, test_size=0.2, random_state=42)
X_train_v, X_test_v, _, _ = train_test_split(vibration_features, labels, test_size=0.2, random_state=42)


#  3. CNN + LSTM 模型


def build_cnn_lstm(input_shape):
    model = Sequential([
        # CNN 部分
        TimeDistributed(Conv2D(32, (3,3), activation='relu', padding='same'), input_shape=input_shape),
        TimeDistributed(MaxPooling2D(pool_size=(2,2))),
        TimeDistributed(BatchNormalization()),
        
        TimeDistributed(Conv2D(64, (3,3), activation='relu', padding='same')),
        TimeDistributed(MaxPooling2D(pool_size=(2,2))),
        TimeDistributed(BatchNormalization()),
        
        TimeDistributed(Conv2D(128, (3,3), activation='relu', padding='same')),
        TimeDistributed(MaxPooling2D(pool_size=(2,2))),
        TimeDistributed(Flatten()),  # 展平
        
        # LSTM 部分
        LSTM(100, return_sequences=True),
        LSTM(50),

        # 分类层
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(labels.shape[1], activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 构建模型
input_shape = (None, acoustic_features.shape[1], acoustic_features.shape[2], 1)  # 时序长度不固定
model = build_cnn_lstm(input_shape)


#  4. 训练模型


history = model.fit(
    X_train_a, y_train,
    validation_data=(X_test_a, y_test),
    epochs=20,
    batch_size=16
)

# 保存模型
model.save("cnn_lstm_acoustic_vibration.h5")


#  5. 预测


def predict_fault(audio_sample, vibration_sample):
    # 预处理样本
    audio_feat = extract_acoustic_features(audio_sample)
    audio_feat = scaler.transform(audio_feat.reshape(1, -1)).reshape(1, *audio_feat.shape, 1)
    
    vib_feat = extract_vibration_features(vibration_sample)
    vib_feat = scaler.transform(vib_feat.reshape(1, -1)).reshape(1, *vib_feat.shape, 1)

    # 加载模型
    model = tf.keras.models.load_model("cnn_lstm_acoustic_vibration.h5")
    
    # 预测
    pred = model.predict(audio_feat)
    return np.argmax(pred)

