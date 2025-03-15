import remi.gui as gui
from remi import start, App
from analysis_gui import AnalysisApp
from diagnosis_gui import DiagnosisApp
from history_gui import HistoryApp

class MainApp(App):
    def __init__(self, *args):
        super(MainApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width="100%", height="100%", margin="10px")

        self.label = gui.Label("欢迎使用离心泵故障诊断系统", style={"font-size": "20px", "text-align": "center"})
        self.file_uploader = gui.FileUploader(width="100%", height="auto")
        self.file_uploader.onsuccess.do(self.on_file_upload)

        button_row = gui.HBox(width="100%", height="50px", margin="10px")
        self.analyze_btn = gui.Button("时频域分析", width="30%", height="40px")
        self.diagnose_btn = gui.Button("故障诊断", width="30%", height="40px")
        self.history_btn = gui.Button("读取诊断记录", width="30%", height="40px")

        self.analyze_btn.onclick.do(self.open_analysis)
        self.diagnose_btn.onclick.do(self.open_diagnosis)
        self.history_btn.onclick.do(self.open_history)

        button_row.append(self.analyze_btn)
        button_row.append(self.diagnose_btn)
        button_row.append(self.history_btn)

        container.append(self.label)
        container.append(self.file_uploader)
        container.append(button_row)

        return container

    def on_file_upload(self, widget, filename):
        self.label.set_text(f"当前选择文件: {filename}")

    def open_analysis(self, widget):
        self.start_sub_app(AnalysisApp)

    def open_diagnosis(self, widget):
        self.start_sub_app(DiagnosisApp)

    def open_history(self, widget):
        self.start_sub_app(HistoryApp)

    def start_sub_app(self, app_class):
        self.close()
        start(app_class, address="0.0.0.0", port=8081, start_browser=True, multiple_instance=True)

start(MainApp, address="0.0.0.0", port=8081, start_browser=True)