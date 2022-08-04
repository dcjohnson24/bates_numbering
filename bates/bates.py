import os

import PyPDF4
from marisol import Marisol, Area
from tqdm import tqdm
from pathlib import Path
from datetime import datetime


def bates(dirname: str, prefix: str = '', zero_pad_length: int = 6,
          start: int = 1, x: int = 300, y: int = 30, rotation: int = 0,
          manual: bool = True, output_dir: str = None) -> None:

    """ Stamp bates numbers on bottom of document

    Args:
        dirname (str): directory of the files to be stamped
        prefix (str): The prefix of the bates number. Default is no prefix.
        zero_pad_length (int, optional): Number of zeros to left
        pad bates number. Defaults to 6.
        start (int, optional): Where to start numbering from.
            Defaults to 1.
        x (int, optional): Horizontal position of text.
            Text moves to the right as x increases.
        y (int, optional): Vertical position of text.
            Text moves up as y increases.
        rotation (int, optional): angle of rotation of text.
        manual (bool, optional): whether to manually position text.
        output_dir (str, optional): Where to save the stamped files.
            Defaults to a directory called 'output'
    """
    if output_dir is None:
        now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        output_dir = Path.home() / 'Documents' / f'stamped_docs_{now}'
        output_dir.mkdir(parents=True, exist_ok=True)

    m = Marisol(prefix, zero_pad_length, start, area=Area.BOTTOM_RIGHT, x=x,
                y=y, rotation=rotation, manual=manual, output_dir=output_dir)

    file_list = [os.path.join(dirname, f) for f in os.listdir(dirname)
                 if os.path.isfile(os.path.join(dirname, f))
                 if f.endswith('.pdf')]

    if not file_list:
        raise PyPDF4.utils.PdfReadError(
            "Please select a directory containing PDF files."
        )
    pbar = tqdm(file_list)
    for f in pbar:
        pbar.set_description(f'Processing {f}')
        try:
            m.append(f)
        except PyPDF4.utils.PdfReadError as re:
            if 'malformed' in str(re).lower():
                raise PyPDF4.utils.PdfReadError(
                    f"{f} is malformed and cannot be processed.\n"
                    "Remove this file from the directory and try again."
                )

    m.save(overwrite=True)
