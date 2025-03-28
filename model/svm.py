import numpy as np
import librosa
import pywt
import joblib
from scipy.stats import kurtosis
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 数据加载
def load_data(filename):
    data = np.loadtxt(filename, delimiter='\t')
    features = data[:, :-1]
    labels = data[:, -1]
    return features, labels

# 声学数据特征提取（使用峰度）
def extract_acoustic_features(audio_data):
    # 计算峰度
    kurt_val = kurtosis(audio_data)
    return np.array([kurt_val])  # 返回单个特征值

# 振动数据特征提取
def extract_vibration_features(vibration_data):
    mean_val = np.mean(vibration_data)
    std_val = np.std(vibration_data)
    skew_val = np.mean((vibration_data - mean_val) ** 3) / std_val ** 3
    kurt_val = np.mean((vibration_data - mean_val) ** 4) / std_val ** 4

    coeffs, _ = pywt.cwt(vibration_data, scales=np.arange(1, 21), wavelet='morl')
    cwt_mean = np.mean(coeffs, axis=1)

    return np.hstack([mean_val, std_val, skew_val, kurt_val, cwt_mean])

# 训练 SVM
def train_svm(features, labels, model_name="svm_model.pkl"):
    scaler = StandardScaler()
    features = scaler.fit_transform(features)  
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    model = SVC(kernel='rbf', C=1.0, gamma='scale')
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"SVM 分类准确率: {acc:.4f}")

    joblib.dump((model, scaler), model_name)

# 预测
def predict_svm(feature, model_name="svm_model.pkl"):
    model, scaler = joblib.load(model_name)
    feature = scaler.transform([feature])
    return model.predict(feature)[0]

# 主函数
def main():
    acoustic_features, acoustic_labels = load_data('acoustic_data.txt')
    vibration_features, vibration_labels = load_data('vibration_data.txt')

    print("训练声学数据 SVM...")
    train_svm(acoustic_features, acoustic_labels, "acoustic_svm.pkl")

    print("训练振动数据 SVM...")
    train_svm(vibration_features, vibration_labels, "vibration_svm.pkl")

if __name__ == "__main__":
    main()
