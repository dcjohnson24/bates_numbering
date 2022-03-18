# Bates Numbering

This is based on the `Marisol` project on [PyPI](https://pypi.org/project/Marisol/). A few tweaks were made to change the position and rotation of the text. These can be found in `marisol.py`. 

Create a virtual environment with `virtualenv -p python3.8 .venv`. Install the required packages with `pip install -r requirements.txt`, and copy `marisol.py` to the folder `.venv/lib/python3.8/site-packages/marisol/` to get the relevant changes. The python version number should be >= 3.5.

## Usage
```
usage: bates.py [-h] [--x X] [--y Y] [--rotation ROTATION] [--no-manual] prefix dirname

Change string prefix of Bates number

positional arguments:
  prefix               string prefix for the Bates number
  dirname              directory with the unstamped files

optional arguments:
  -h, --help           show this help message and exit
  --x X                horizontal position of text
  --y Y                vertical position of text
  --rotation ROTATION  rotation of the text
  --no-manual          whether to manually set the text position. True if called, false otherwise
```

Run `bates.py` from the command line with `python bates.py sampleText sampleDir`.
The default position of the text is at the bottom center of the page, where `x` is 300 and `y` is 30.
As `x` increases, the text moves to the right of the page. As `y` increases, the text moves to the top of the page.