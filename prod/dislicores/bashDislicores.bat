echo.
echo PROCESO DE SCRAPING DISLICORES

rem init extracting data for DISLICORES

"D:\PyEnv\venv3\Scripts\python.exe" D:\workflow\dt_web_scraping\prod\dislicores\web_scraping_dislicores_v2.py
rem finish extracting data for DISLICORES

@REM xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y

echo.

exit


