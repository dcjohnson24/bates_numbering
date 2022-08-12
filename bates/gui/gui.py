#!python3.8
import PyPDF4
from pathlib import Path
import dearpygui.dearpygui as dpg
from dearpygui.demo import _hsv_to_rgb

from ..bates import bates
from .error_box import show_info, on_selection

dpg.create_context()

APP_DATA = {}


def check_dir(sender, app_data):
    if dpg.is_item_visible('finished'):
        dpg.hide_item('finished')
    dirname = app_data['file_path_name']
    msg = f"{dirname} has been selected"
    if sender == 'input_dir':
        dpg.set_value("indir_text", msg)
    elif sender == 'output_dir':
        dpg.set_value('outdir_text', msg)
    APP_DATA[sender] = dirname


def stamp_files(sender, app_data):
    if dpg.is_item_visible('finished'):
        dpg.hide_item('finished')
    try:
        if dpg.is_item_visible('OutputDir'):
            dpg.delete_item('OutputDir')
    except SystemError:
        pass

    prefix = dpg.get_value("prefix")
    xpos = dpg.get_value('xpos') if dpg.does_item_exist('xpos') else 300
    ypos = dpg.get_value('ypos') if dpg.does_item_exist('ypos') else 30
    rotation = (dpg.get_value('rotation')
                if dpg.does_item_exist('rotation') else 0)
    try:
        input_dir = APP_DATA['input_dir']
    except KeyError:
        dpg.hide_item('loading')
        show_info(
            title='Error',
            message='No directory selected. Please select a directory',
            selection_callback=on_selection
        )
        return

    try:
        output_dir = APP_DATA['output_dir']
    except KeyError:
        output_dir = None
        msg = (
            f"No output directory selected.\nStamped documents "
            f"will be saved in {Path.home() / 'Documents'}"
        )
        with dpg.window(label="Note", pos=(250, 250), no_collapse=True):
            dpg.add_text(msg)

    try:
        dpg.show_item('loading')
        bates(prefix=prefix, dirname=input_dir, x=xpos, y=ypos,
              rotation=rotation, output_dir=output_dir)

    except PyPDF4.utils.PdfReadError as re:
        msg = str(re)
        dpg.hide_item('loading')
        show_info('Error', msg, on_selection)
        return

    dpg.hide_item('loading')
    dpg.show_item('finished')
    with dpg.window(tag="OutputDir", pos=(150, 450), no_collapse=True):
        if output_dir is None:
            dpg.add_text(f"Stamped files are saved in "
                         f"{Path.home() / 'Documents'}")
        else:
            dpg.add_text(f"Stamped files are saved in {output_dir}")

    dpg.remove_alias('OutputDir')
    dpg.set_value('indir_text', '')
    dpg.set_value('outdir_text', '')

    APP_DATA.clear()


def show_group(sender, app_data, user_data):
    if dpg.get_value(sender):
        dpg.show_item(user_data)
    else:
        dpg.hide_item(user_data)


def main():
    with dpg.font_registry(label='font size'):
        font_file = str(Path(__file__).parent / 'NotoSerifCJKjp-Medium.otf')
        default_font = dpg.add_font(font_file, 18)

    with dpg.window(label="Bates Stamp", width=800, height=600,
                    tag="Bates Stamp", no_close=True, no_collapse=True):
        dpg.bind_font(default_font)

        dpg.add_file_dialog(directory_selector=True, show=False,
                            callback=check_dir,
                            tag="input_dir",
                            width=500, height=400)

        dpg.add_button(label="Choose directory containing files to be stamped",
                       callback=lambda: dpg.show_item("input_dir"))

        dpg.add_text('', tag="indir_text", color=(255, 255, 0))

        dpg.add_file_dialog(directory_selector=True, show=False,
                            callback=check_dir,
                            tag='output_dir',
                            width=500, height=400)

        dpg.add_button(label="Choose output directory for stamped files",
                       callback=lambda: dpg.show_item('output_dir'))

        dpg.add_text('', tag='outdir_text', color=(255, 255, 0))

        dpg.add_input_text(label="Bates Prefix", tag="prefix")

        with dpg.group(tag="position", show=False):
            dpg.add_input_int(label='x (int)', default_value=300,
                              tag='xpos')
            dpg.add_input_int(label='y (int)', default_value=30,
                              tag='ypos')
            dpg.add_input_int(label='rotation', default_value=0,
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
                                  show=False, pos=(150, 350))

        dpg.add_text('All finished!', tag='finished', pos=(150, 400),
                     show=False, parent="Bates Stamp")

        dpg.add_button(label='Stamp!', callback=stamp_files, pos=(150, 300),
                       tag='stamp')
        dpg.bind_item_theme('stamp', 'rounded')

    dpg.create_viewport(title='Bates Stamp', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()
