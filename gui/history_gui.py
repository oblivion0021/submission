import remi.gui as gui
from remi import start, App
from main_gui import MainApp

class HistoryApp(App):
    def __init__(self, *args):
        super(HistoryApp, self).__init__(*args)

    def main(self):
        container = gui.VBox(width="100%", height="100%", margin="10px")

        self.back_btn = gui.Button("返回主界面", width="15%", height="40px")
        self.back_btn.onclick.do(self.return_to_main)

        self.label = gui.Label("诊断记录界面", style={"font-size": "20px", "text-align": "center"})

        container.append(self.back_btn)
        container.append(self.label)

        return container

    def return_to_main(self, widget):
        self.close()
        start(MainApp, address="0.0.0.0", port=8081, start_browser=True, multiple_instance=True)

start(HistoryApp, address="0.0.0.0", port=8081, start_browser=True)
