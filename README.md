# Bates Numbering

This is based on the `Marisol` project on PyPI. A few tweaks were made to change the position and rotation of the text. These can be found in `marisol.py`. After installing for the first time, copy `marisol.py` to the folder `.venv/lib/python3.7/site-packages/marisol/` to get the relevant changes.

## Changing position of Bates Number

The return value of the `position` method in the `GenericTextOverlay` class is a tuple of the form `(y, x)`. As `y`-> &#8734; , the text moves to the top of the page. And as`x` -> &#8734;, the text moves to the left of the page. Note that this has only been tested with `area=Area.BOTTOM_RIGHT` in the `Marisol` constructor.
