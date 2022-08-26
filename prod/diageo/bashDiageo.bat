echo.
echo PROCESO DE SCRAPING DIAGEO

rem init extracting data for DIAGEO
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\diageo\web_scraping_diageo_v1.py
rem finish extracting data for DIAGEO

xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y

echo.

exit

