import os
import sys
from tabnanny import check
sys.path.append(os.pardir)

import dearpygui.dearpygui as dpg
from dearpygui.demo import _hsv_to_rgb
from bates import bates

dpg.create_context()

def callback(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)


def check_dir(sender, app_data):
    dirname = app_data['file_path_name']
    if os.path.split(dirname)[-1] == 'docs':
        print(f'{sender} is the correct directory')
        print(f'Stamping files in directory {dirname}')


def stamp_files(sender, app_data):
    print('Stamping docs now!')


def show_group(sender, app_data, user_data):
    if dpg.get_value(sender):
        dpg.show_item(user_data)
    else:
        dpg.hide_item(user_data)


dpg.add_file_dialog(directory_selector=True, show=False, callback=check_dir, tag="file_dialog_id")

with dpg.window(label="Bates Stamp", width=800, height=300):
    
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_input_text(label="Bates Prefix")
    
    with dpg.group(tag="position", show=False):
        # TODO make these buttons visible only if the checkbox is ticked.
        xpos = dpg.add_input_int(label='x (int)', default_value=300)
        ypos = dpg.add_input_int(label='y (int)', default_value=30)
        rotation = dpg.add_input_int(label='rotation', default_value=0, max_value=360)
    
    dpg.add_checkbox(label="Set text position manually", tag="checkbox", before="position",
                     callback=show_group, user_data="position")


    with dpg.theme(tag='rounded'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, _hsv_to_rgb(3/7.0, 0.7, 0.7))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3*5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3*3, 3*3)
    
    dpg.add_button(label='Stamp!', callback=stamp_files, pos=(150, 200), tag='stamp')
    dpg.bind_item_theme('stamp', 'rounded')
    
dpg.configure_app(manual_callback_management=True)

dpg.create_viewport(title='Bates Stamp', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
# dpg.start_dearpygui()
while dpg.is_dearpygui_running():
    jobs = dpg.get_callback_queue()
    dpg.run_callbacks(jobs)
    dpg.render_dearpygui_frame()

dpg.destroy_context()

