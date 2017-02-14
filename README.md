Databaker Jupyter notebook tool for converting data that is laid out in a formatted excel 
spreadsheet into a normalized form for use by databases.  
It depends on [okfn/messytables](https://github.com/okfn/messytables) and 
[sensiblecodeio/xypath](https://github.com/sensiblecodeio/xypath)

See the documentation is in the Jupyter notebooks in
**[tutorial](databaker/tutorial)**.

## Starting up

To install for development, go into the virtualenv with 

`source bin/activate`

and then type

`pip install -e git+https://github.com/sensiblecodeio/databaker.git#egg=databaker`

This will install the code into src/databaker where you can edit and commit it.  
Then type:

`jupyter notebook` 

to start it up.  

## Authors

Made by the [Sensible Code Company](http://sensiblecode.io) on behalf of the 
[Office of National Statistics](https://www.ons.gov.uk/) (UK).

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
