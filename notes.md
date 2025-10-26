request-headers

https://code.tutsplus.com/tutorials/how-to-write-your-own-python-packages--cms-26076
https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693

www.github.com	homedrms@gmail.com	Hyr65sd43hey2U93	ipicspro

> make new env
python -m venv env

> collect dependencies
pip freeze > requirements.txt

pip install -r requirements.txt

>Make package distribution

> test
python setup.py test




> create distribution:

> * create a source distribution - (wheel)
python setup.py bdist_wheel

> or - older method
> create a source distribution - (eggs)
python setup.py sdist




> install package from github
pip3 install --no-cache-dir https://github.com/ipicspro/request-headers/raw/main/dist/request_headers-0.1-py3-none-any.whl
?pip3 install --no-cache-dir https://raw.githubusercontent.com/ipicspro/request-headers/master/dist/request_headers-0.1-py3-none-any.whl

git clone https://ipicspro@github.com/ipicspro/request-headers.git
pip install request-headers/dist/request_headers-0.1-py3-none-any.whl
or
sudo python setup.py install
or 
pip install git+https://github.com/ipicspro/request-headers.git#egg=request-headers
pip install --upgrade git+https://github.com/ipicspro/request-headers.git#egg=request-headers



> reinstall
pip install--force-reinstall dist/request_headers-0.1-py3-none-any.whl
or
pip uninstall -y request-headers && pip install request_headers-0.1-py3-none-any.whl
or
pip uninstall -y request-headers
pip install request_headers-0.1-py3-none-any.whl


# git clone https://github.com/ipicspro/request-headers.git
# git clone https://ipicspro:password@github.com/ipicspro/request-headers.git

> install package from local
pip install--force-reinstall dist/request_headers-0.1-py3-none-any.whl

pip install --upgrade https://github.com/ipicspro/request-headers/master
pip install --upgrade https://github.com/ipicspro/request-headers.git





> uninstall package
pip uninstall request-headers













bad ua:
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0
