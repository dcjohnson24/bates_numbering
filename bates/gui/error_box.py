# https://github.com/hoffstadt/DearPyGui/discussions/1308

import dearpygui.dearpygui as dpg


def show_info(title, message, selection_callback):
    # guarantee these commands happen in the same frame
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label=title, modal=True, no_close=True,
                        no_collapse=True) as modal_id:
            dpg.add_text(message)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Ok", width=75,
                               user_data=(modal_id, True),
                               callback=selection_callback)
    # guarantee these commands happen in another frame
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2,
                     viewport_height // 2 - height // 2])


def on_selection(sender, unused, user_data):
    # delete window
    dpg.delete_item(user_data[0])
