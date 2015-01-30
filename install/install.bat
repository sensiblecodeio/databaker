echo OFF
echo okfn/messytables@%1
echo scraperwiki/xypath@%2
echo scraperwiki/databaker@%3
 
pause
pip uninstall -y xypath
pip uninstall -y messytables
rmdir /s databaker
 
pip install --user https://github.com/okfn/messytables/archive/%1.zip
pip install --user https://github.com/scraperwiki/xypath/archive/%2.zip
python unzip_from_web.py %3
