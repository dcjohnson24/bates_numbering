import enum
import os
from marisol import Marisol, Area
from tqdm import tqdm
import PyPDF4
import logging

logging.basicConfig(filename='./error.log', level=logging.ERROR, filemode='w')
logger = logging.getLogger(__name__)

def bates(prefix: str, file_list: list, zero_pad_length: int=6, start: int=1, save: bool=True) -> None:
    """ Stamp Bates Numbers on Bottom of Document

    Args:
        prefix (str): The prefix of the bates number
        file_list (list): list of files files to be stamped
        zero_pad_length (int, optional): Number of zeros preceding the Bates number. Defaults to 6.
        start (int, optional): Start of the bates numbering. Defaults to 1.
        save (bool, optional): Whether to save files. Defaults to True.

    Returns:
        None
    """
    m = Marisol(prefix, zero_pad_length, start, area=Area.BOTTOM_RIGHT)
    pbar = tqdm(file_list)
    for i, f in enumerate(pbar):
        pbar.set_description(f'Processing {f}')
        # m.append(f)
        try:
            m.append(f)
        except ValueError as ve:
            logger.error(f'{i}: File {f} has thrown {ve}')
            os.system(f"cp '{f}' ../badfiles")
            break
        except PyPDF4.utils.PdfReadError as pe:
            logger.error(f'{i}: File {f} has thrown {pe}') 
            os.system(f"cp '{f}' ../badfiles")
            break
    if save:
        m.save(overwrite=True)
    return m.number


def retrieve_files(dirname: str, file_ext: str='.pdf') -> list:
    file_list = []
    for root, dirs, files in os.walk(dirname):
        for file in files:
            if file.endswith(".pdf"):
                file_list.append(os.path.join(root, file))
    return file_list


if __name__ == '__main__':
    os.chdir('SEC Production')
    order_list = [f for f in os.listdir('.') if os.path.isdir(f) or f.endswith('.pdf')]
    order_dict = {
        'Account Forms': 0,
        'Misc Account Documents': 1,
        'GWG Holdings Purchases Excel Spreadsheet.pdf': 2,
        'Due Diligence': 3,
        'GWG': 4,
        'GWG LB3 Due Diligence': 5,
        'Subscription Agreements': 6,
        'CRM': 7,
        'Paulson Response to Attachment A.pdf': 8,
        'FOIA Confidential Treatment Request.pdf': 9
    }
    sorted_list = sorted(order_list, key=order_dict.get)
    sorted_dict = {}

    for f in sorted_list:
        if os.path.isdir(f):
            sorted_dict[f] = retrieve_files(f)
        else:
            sorted_dict[f] = f

    val_list = list(sorted_dict.values())
    flat_list = []
    for sublist in val_list:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
        else:
            flat_list.append(sublist)
    
    stamp = 'Confidential Treatment Requested by Paulson Investment Company, LLC    PIC'
    
    troubled_indices = [5, 6, 19, 24, 27, 29, 30, 31, 33, 85, 94]
    page_lens = [26, 30, 0, 1, 6, 2, 5, 133, 1, 1, 6, 6]
    bates_starts = [1, 126, 156, 362, 390, 403, 406, 411, 544, 604, 1618, 1806]
    
    # You must change 'break' to 'continue' to run this all the way through.
    # Uncomment the first 'm.append'
    # bates(stamp, file_list=flat_list, save=False)

    
    # Final numbering
    bates(stamp, file_list=flat_list, start=bates_starts[0])
    bates(stamp, file_list=flat_list[troubled_indices[0] + 1:], start=bates_starts[1])
    bates(stamp, file_list=flat_list[troubled_indices[1] + 1: ], start=bates_starts[2])
    bates(stamp, file_list=flat_list[troubled_indices[2] + 1: ], start=bates_starts[3])
    bates(stamp, file_list=flat_list[troubled_indices[3] + 1: ], start=bates_starts[4])
    bates(stamp, file_list=flat_list[troubled_indices[4] + 1: ], start=bates_starts[5])
    bates(stamp, file_list=flat_list[troubled_indices[5] + 1: ], start=bates_starts[6])
    bates(stamp, file_list=flat_list[troubled_indices[6] + 1: ], start=bates_starts[7])
    bates(stamp, file_list=flat_list[troubled_indices[7] + 1: ], start=bates_starts[8])
    bates(stamp, file_list=flat_list[troubled_indices[8] + 1: ], start=bates_starts[9])
    bates(stamp, file_list=flat_list[troubled_indices[9] + 1: ], start=bates_starts[10])
    bates(stamp, file_list=flat_list[troubled_indices[10] + 1: ], start=bates_starts[11])
