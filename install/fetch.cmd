@echo OFF
if [%3] == [] goto :needmoreargs

echo okfn/messytables@%1
echo scraperwiki/xypath@%2
echo scraperwiki/databaker@%3
pause

pip uninstall -y xypath
pip uninstall -y messytables
rmdir /s /q databaker

pip install --user https://github.com/okfn/messytables/archive/%1.zip || goto :error
pip install --user https://github.com/scraperwiki/xypath/archive/%2.zip || goto :error
python unzip_from_web.py %3 || goto :error

echo Success!
exit /b 0

:needmoreargs
echo "Usage: fetch <messytables-branch> <xypath-branch> <databaker-branch>"
exit /b 1

:error
echo Stopped. Either pip or unzip failed.
exit /b 2
