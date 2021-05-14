import os
from marisol import Marisol, Area
from tqdm import tqdm
import PyPDF2

def bates(prefix: str, file_list: str, zero_pad_length: int=6, start: int=1) -> None:
    """ Stamp bates numbers on bottom of document

    Args:
        prefix (str): The prefix of the bates number
        dirname (str): list of files to be stamped
        zero_pad_length (int, optional): Number of zeros to left pad bates number. Defaults to 6.
        start (int, optional): Where to start numbering from. Defaults to 1.
    """
    m = Marisol(prefix, zero_pad_length, start, area=Area.BOTTOM_RIGHT)
    # file_list = [os.path.join(dirname, f) for f in os.listdir(dirname) 
    #              if os.path.isfile(os.path.join(dirname, f))]
    pbar = tqdm(file_list)
    for f in pbar:
        pbar.set_description(f'Processing {f}')
        try:
            m.append(f)
        except ValueError as ve:
            print(f'{f} is a bad file {ve}')
            continue
        except PyPDF2.utils.PdfReadError as pe:
            print(f'{f} has the problem {pe}') 
            continue
    m.save(overwrite=True)


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
        'Paulson  Response to Attachment A.pdf': 8,
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
    bates(stamp, file_list=flat_list[:5])