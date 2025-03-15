import remi.gui as gui
from remi import start, App
from utils import generate_cwt_image
from main_gui import MainApp

class AnalysisApp(App):
    def __init__(self, *args):
        super(AnalysisApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width="100%", height="100%", margin="10px")

        self.back_btn = gui.Button("返回主界面", width="15%", height="40px")
        self.back_btn.onclick.do(self.return_to_main)

        self.time_domain_canvas = gui.Image(generate_cwt_image(), width="100%", height="90%")
        self.start_analysis_btn = gui.Button("开始分析", width="100%", height="40px")
        self.start_analysis_btn.onclick.do(self.perform_analysis)

        container.append(self.back_btn)
        container.append(self.time_domain_canvas)
        container.append(self.start_analysis_btn)

        return container

    def return_to_main(self, widget):
        self.close()
        start(MainApp, address="0.0.0.0", port=8081, start_browser=True, multiple_instance=True)

    def perform_analysis(self, widget):
        self.time_domain_canvas.set_image(generate_cwt_image())

start(AnalysisApp, address="0.0.0.0", port=8081, start_browser=True)
