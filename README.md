# Bates Numbering

This is based on the `Marisol` project on PyPI. A few tweaks were made to change the position and rotation of the text. These can be found in `marisol.py`. 

Create a virtual environment with `virtualenv -p python3.8 .venv`. Install the required packages with `pip install -r requirements.txt`, and copy `marisol.py` to the folder `.venv/lib/python3.8/site-packages/marisol/` to get the relevant changes. The version number should be >= 3.5.

## Changing position of Bates Number

The return value of the `position` method in the `GenericTextOverlay` class is a tuple of the form `(x, y)`. As `x` increases, the text moves to the right of the page. As `y` increases, the text moves to the top of the page. Note that this has only been tested with `area=Area.BOTTOM_RIGHT` in the `Marisol` constructor. If you decide to change the position, remember to copy `marisol.py` again to `.venv/lib/python3.8/site-packages/marisol/`. 

To change the rotation of the Bates number, change the `c.rotate(angle)` function in the `apply` method in the `GenericTextOverlay` class. 
