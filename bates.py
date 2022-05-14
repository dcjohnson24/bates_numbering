import os
from marisol import Marisol, Area
from tqdm import tqdm
import argparse


def bates(dirname: str, prefix: str = '', zero_pad_length: int = 6,
          start: int = 1, x: int = 300, y: int = 30, rotation: int = 0,
          manual: bool = True) -> None:

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
    """

    m = Marisol(prefix, zero_pad_length, start, area=Area.BOTTOM_RIGHT, x=x,
                y=y, rotation=rotation, manual=manual)
    file_list = [os.path.join(dirname, f) for f in os.listdir(dirname)
                 if os.path.isfile(os.path.join(dirname, f))
                 if f.endswith('.pdf')]
    if not file_list:
        raise ValueError("Please select a directory containing pdf files")
    pbar = tqdm(file_list)
    for f in pbar:
        pbar.set_description(f'Processing {f}')
        m.append(f)
    m.save(overwrite=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Change string prefix of Bates number')
    parser.add_argument('dirname', type=str,
                        help='directory with the unstamped files')
    parser.add_argument('--prefix', type=str,
                        help='string prefix for the Bates number', default='')
    parser.add_argument('--x', help='horizontal position of text', type=int,
                        default=300)
    parser.add_argument('--y', help='vertical position of text', type=int,
                        default=30)
    parser.add_argument('--rotation', help='rotation of the text', type=int,
                        default=0)
    parser.add_argument('--no-manual',
                        help='whether to manually set the text position.'
                        'True if called, false otherwise',
                        action='store_true')
    args = parser.parse_args()
    if args.no_manual:
        manual = False
    else:
        manual = True
    bates(dirname=args.dirname, prefix=args.prefix, x=args.x, y=args.y,
          rotation=args.rotation, manual=manual)
