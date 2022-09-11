echo.
echo PROCESO DE SCRAPING EXITO

rem init extracting data for EXITO
@REM "C:\envPython\venv4\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_carulla_v1.py
@REM "C:\envPython\venv4\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_cava_carulla_v1.py
"D:\PyEnv\venv7\Scripts\python.exe" D:\workflow\dt_web_scraping\prod\exito\web_scraping_exito_v4.py
rem finish extracting data for EXITO

@REM xcopy C:\workflow\dt_web_scraping\prod\data\ \\wsl.localhost\Ubuntu\home\developer\dislicores\dt_web_scraping_classification\dataScraping\ /K /D /H /Y


echo.

exit

