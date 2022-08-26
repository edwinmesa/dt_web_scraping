echo.
echo PROCESO DE SCRAPING OLIMPICA

rem init extracting data for OLIMPICA 
"C:\envPython\venv7\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\olimpica\web_scraping_olimpica_v1.py
rem finish extracting data for OLIMPICA

xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y


echo.

exit

