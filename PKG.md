# Skeleton structure for a new python project

I've developed this bare-bones new project structure after developing and distributing several python applications. 
I found it to work best for the later deployment of a python project either with local sdist or deployed to PyPi.
For other ways to create a project template, see Cookiecutter open source project: 
https://cookiecutter.readthedocs.io/en/latest/readme.html

## To use:
Just copy it, rename the obviously named keywords and start coding.

## To deploy
Create 2 distributions:
- Source Distribution or sdist (contains source code)
- Build distribution or Wheel (platform dependent build, i.e. need one for each platform if code is not platform-independent)

To upload to PyPi, will need install twine:
> pip install twine
(Also this command: python -m pip install --user --upgrade twine)

#### Create local distributions (source and wheel):
python setup.py sdist bdist_wheel

#### Install and test local source distribution
Copy app.tar.gz from created dist directory to some test directory
In testdirectory, create and source new venv, deploy your package there:

> virtualenv venv

> source venv/bin/activate

> pip install app.tar.gz

If yaml files were distributed with the app, they will be in venv/lib/python3.6/site-packages/app-package (so will be the code)

Uninstall: just delete the venv and your test directory

#### Deploy to PyPi test package manager
http://devarea.com/deploying-a-new-python-package-to-pypi/

Create and place in a home directory a .pypirc file. - This did not work for me: need to enter passwd anyways.

Upload an existing dist to PyPi
> twine upload --repository-url https://test.pypi.org/legacy/ dist/*

WARNING: PyPI does not allow for a filename to be reused, even once a project has been deleted and recreated. If things don't work, you can change the version number and re-upload, but not re-upload same project and same version.

##### Install from PyPi test
In a test venv do:

> pip install -i https://testpypi.python.org/pypi myapp

> python -m pip install --index-url https://test.pypi.org/simple/ brdm


#### Deploy to real PyPi

twine upload dist/*

###### Install from PyPi
In a test venv do:

> pip install -i https://pypi.org/pypi myapp

> pip install 'myapp'

> pip install 'myapp==0.1'


## To create and deploy Wheel