import os
from marisol import Marisol, Area
from tqdm import tqdm


def bates(prefix: str, dirname: str, zero_pad_length: int=6, start: int=1) -> None:
    """ Stamp bates numbers on bottom of document

    Args:
        prefix (str): The prefix of the bates number
        dirname (str): directory of the files to be stamped
        zero_pad_length (int, optional): Number of zeros to left pad bates number. Defaults to 6.
        start (int, optional): Where to start numbering from. Defaults to 1.
    """
    m = Marisol(prefix, zero_pad_length, start, area=Area.BOTTOM_RIGHT)
    file_list = [os.path.join(dirname, f) for f in os.listdir(dirname) 
                 if os.path.isfile(os.path.join(dirname, f))]
    pbar = tqdm(file_list)
    for f in pbar:
        pbar.set_description(f'Processing {f}')
        m.append(f)
    m.save(overwrite=True)


if __name__ == '__main__':
    bates('Mallon&Johnson', 'docs')
