#!python3.8
import os
import sys
import site

import PyPDF2

sys.path.append(os.pardir)

import dearpygui.dearpygui as dpg
from dearpygui.demo import _hsv_to_rgb
from bates import bates
from error_box import show_info, on_selection

scriptdir, script = os.path.split(os.path.abspath(__file__))
pkgdir = os.path.join(scriptdir, 'pkgs')
# Ensure .pth files in pkgdir are handled properly
site.addsitedir(pkgdir)
sys.path.insert(0, pkgdir)

dpg.create_context()

APP_DATA = {}


def check_dir(sender, app_data):
    if dpg.is_item_visible('finished'):
        dpg.hide_item('finished')
    dirname = app_data['file_path_name']
    dpg.set_value("dirtext", f"{dirname} has been selected")
    APP_DATA['file_path_name'] = dirname


def stamp_files(sender, app_data):
    if dpg.is_item_visible('finished'):
        dpg.hide_item('finished')
    dpg.show_item('loading')
    prefix = dpg.get_value("prefix")
    xpos = dpg.get_value('xpos') if dpg.does_item_exist('xpos') else 300
    ypos = dpg.get_value('ypos') if dpg.does_item_exist('ypos') else 30
    rotation = (dpg.get_value('rotation')
                if dpg.does_item_exist('rotation') else 0)
    try:
        dirname = APP_DATA['file_path_name']
    except KeyError:
        dpg.hide_item('loading')
        show_info('Error', 'No directory selected. Please select a directory',
                  on_selection)
        return

    try:
        bates(prefix=prefix, dirname=dirname, x=xpos, y=ypos,
              rotation=rotation)
    except PyPDF2.utils.PdfReadError as re:
        msg = str(re)
        dpg.hide_item('loading')
        show_info('Error', msg, on_selection)
        return

    dpg.hide_item('loading')
    dpg.show_item('finished')
    dpg.set_value('dirtext', '')


def show_group(sender, app_data, user_data):
    if dpg.get_value(sender):
        dpg.show_item(user_data)
    else:
        dpg.hide_item(user_data)


with dpg.font_registry(label='font size'):
    default_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 18)


with dpg.window(label="Bates Stamp", width=600, height=400, tag="Bates Stamp"):
    dpg.bind_font(default_font)

    dpg.add_file_dialog(directory_selector=True, show=False,
                        callback=check_dir,
                        tag="file_dialog_id",
                        width=500, height=400)

    dpg.add_button(label="Choose a Directory",
                   callback=lambda: dpg.show_item("file_dialog_id"))

    dpg.add_text('', tag="dirtext", color=(255, 255, 0))

    dpg.add_input_text(label="Bates Prefix", tag="prefix")

    with dpg.group(tag="position", show=False):
        xpos = dpg.add_input_int(label='x (int)', default_value=300,
                                 tag='xpos')
        ypos = dpg.add_input_int(label='y (int)', default_value=30, tag='ypos')
        rotation = dpg.add_input_int(label='rotation', default_value=0,
                                     max_value=360, tag='rotation')

    dpg.add_checkbox(label="Set text position manually", tag="checkbox",
                     before="position",
                     callback=show_group, user_data="position")

    with dpg.theme(tag='rounded'):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,
                                _hsv_to_rgb(3/7.0, 0.7, 0.7))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3*5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3*3, 3*3)

    dpg.add_loading_indicator(tag="loading", parent="Bates Stamp",
                              show=False, pos=(150, 300))

    dpg.add_text('All finished!', tag='finished', pos=(150, 350), show=False,
                 parent="Bates Stamp")

    dpg.add_button(label='Stamp!', callback=stamp_files, pos=(150, 250),
                   tag='stamp')
    dpg.bind_item_theme('stamp', 'rounded')

dpg.create_viewport(title='Bates Stamp', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()
