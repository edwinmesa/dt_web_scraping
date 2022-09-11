echo.
echo PROCESO DE SCRAPING LA LICORERA

rem init extracting data for LA LICORERA
"D:\PyEnv\venv6\Scripts\python.exe" D:\workflow\dt_web_scraping\prod\lalicorera\web_scraping_la_licorera_v2.py
rem finish extracting data for LA LICORERA

@REM xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y


echo.

exit

