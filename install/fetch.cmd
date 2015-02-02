@echo OFF
if [%3] == [] goto :needmoreargs

echo okfn/messytables@%1
echo scraperwiki/xypath@%2
echo scraperwiki/databaker@%3
pause

pip uninstall -y xypath
pip uninstall -y messytables
pip uninstall -y databaker

pip install https://github.com/okfn/messytables/archive/%1.zip || goto :error
pip install https://github.com/scraperwiki/xypath/archive/%2.zip || goto :error
pip install https://github.com/scraperwiki/databaker/archive/%3.zip || goto :error
echo Success!
exit /b 0

:needmoreargs
echo "Usage: fetch <messytables-branch> <xypath-branch> <databaker-branch>"
exit /b 1

:error
echo Stopped. Either pip or unzip failed.
exit /b 2
