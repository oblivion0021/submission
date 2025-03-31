import remi.gui as gui

def get_records_ui(main_app):
    """ 创建读取诊断记录界面 """
    container = gui.VBox(width="100%", height="100%")
    container.style['background-color'] = '#f4f4f9'

    back_button = gui.Button("返回主界面", width="20%", height="50px")
    back_button.style['background-color'] = '#007BFF'
    back_button.style['color'] = 'white'
    back_button.style['border'] = 'none'
    back_button.style['border-radius'] = '5px'
    back_button.style['margin'] = '20px'
    back_button.onclick.do(main_app.show_main_ui)  # 返回主界面

    label = gui.Label("读取诊断记录界面", style={"font-size": "24px", "text-align": "center", "color": "#333"})

    container.append(back_button)
    container.append(label)

    return container
