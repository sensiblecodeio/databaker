# Databaker

Jupyter notebook tool for converting data that is laid out in a formatted Excel 
spreadsheet into a normalized form for use by databases.

It depends on [okfn/messytables](https://github.com/okfn/messytables) and 
[sensiblecodeio/xypath](https://github.com/sensiblecodeio/xypath)

Python 3.4+ supported.

## Starting up

### For development

To install for development, the easiest way is create a virtualenv,
activate it:

`source bin/activate`

and then type

`pip install -e git+https://github.com/sensiblecodeio/databaker.git#egg=databaker`

This will install the code into `src/databaker` where you can edit and commit it.  

### For normal use

Install with `pip install databaker`

## Usage

Launch a Jupyter notebook:

`jupyter notebook` 

and then follow the tutorials as described below. 

## Documentation

The current documentation is in the form of Jupyter notebooks located
inside the [tutorial](databaker/tutorial) directory.

You can access these directly by creating a new Jupyter notebook and
running the following in a Jupyter cell:

```
from databaker.tutorial import tutorial
tutorial()
```

which will copy the tutorials to your current directory and provide
links to these copied notebooks.

## Authors

Made by the [Sensible Code Company](http://sensiblecode.io) on behalf of the 
[Office of National Statistics](https://www.ons.gov.uk/) (UK).
