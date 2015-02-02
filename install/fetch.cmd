@echo OFF
echo okfn/messytables@%1
echo scraperwiki/xypath@%2
echo scraperwiki/databaker@%3

if [%3] == [] exit /b

pause
pip uninstall -y xypath
pip uninstall -y messytables
rmdir /s /q databaker

pip install --user https://github.com/okfn/messytables/archive/%1.zip || goto :error
pip install --user https://github.com/scraperwiki/xypath/archive/%2.zip || goto :error
python unzip_from_web.py %3 || goto :error

echo Success!
exit /b 0

:error
echo Stopped. Either pip or unzip failed.
