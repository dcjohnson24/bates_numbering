import os
from marisol import Marisol, Area


def bates(name: str, dirname: str, length: int=6, start: int=1) -> None:
    m = Marisol(name, length, start, area=Area.BOTTOM_RIGHT)
    file_list = [os.path.join(dirname, f) for f in os.listdir(dirname) 
                 if os.path.isfile(os.path.join(dirname, f))]
    for f in file_list:
        m.append(f)
    m.save(overwrite=True)


if __name__ == '__main__':
    bates('Mallon&Johnson', 'docs')
