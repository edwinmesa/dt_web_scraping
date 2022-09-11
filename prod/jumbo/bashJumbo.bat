echo.
echo PROCESO DE SCRAPING JUMBO

rem init extracting data for JUMBO
"D:\PyEnv\venv5\Scripts\python.exe" D:\workflow\dt_web_scraping\prod\jumbo\web_scraping_jumbo_v3.py
rem finish extracting data for JUMBO

@REM xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y


echo.

exit

