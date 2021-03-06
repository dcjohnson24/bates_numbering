# Bates Numbering

This is based on the `Marisol` project on [PyPI](https://pypi.org/project/Marisol/). A few tweaks were made to change the position and rotation of the text. These can be found in `marisol.py`. 

Create a virtual environment with `virtualenv -p python3.8 .venv`. Install the required packages with `pip install -r requirements.txt`, and copy `marisol.py` to the folder `.venv/lib/python3.8/site-packages/marisol/` to get the relevant changes. The python version number should be >= 3.5.

## Usage
```bash

user@desktop:~/bates_numbering$ python bates.py -h
usage: bates.py [-h] [--prefix PREFIX] [--x X] [--y Y] [--rotation ROTATION] [--no-manual] dirname

Change string prefix of Bates number

positional arguments:
  dirname              directory with the unstamped files

optional arguments:
  -h, --help           show this help message and exit
  --prefix PREFIX      string prefix for the Bates number
  --x X                horizontal position of text
  --y Y                vertical position of text
  --rotation ROTATION  rotation of the text
  --no-manual          whether to manually set the text position.True if called, false otherwise
```

The default position of the text is at the bottom center of the page, where `x` is 300 and `y` is 30.
As `x` increases, the text moves to the right of the page. As `y` increases, the text moves to the top of the page.

### Example
Generate a few sample PDFs with 
```python
import os
from reportlab.pdfgen import canvas

os.makedirs('mydocs', exist_ok=True)
for i in range(3):
  pdf = canvas.Canvas(f'mydocs/some_file{i}.pdf')
  text = pdf.beginText(40, 680)
  text.textLine('Hello there!')
  pdf.drawText(text)
  pdf.save()
```

Then stamp the documents using `python bates.py mydocs --prefix Important_`

## GUI 
Run the GUI with `cd gui && python gui.py`. Note that the GUI must be run from the `gui` directory.