import remi.gui as gui

def get_records_ui(main_app):
    """ 创建读取诊断记录界面 """
    container = gui.VBox(width="100%", height="100%")

    back_button = gui.Button("返回主界面", width="20%", height="50px")
    back_button.onclick.do(main_app.show_main_ui)  # 返回主界面

    label = gui.Label("读取诊断记录界面", style={"font-size": "20px", "text-align": "center"})

    container.append(back_button)
    container.append(label)

    return container
