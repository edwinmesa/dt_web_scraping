echo.
echo PROCESO DE SCRAPING EXITO

rem init extracting data for EXITO
"C:\envPython\venv4\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_carulla_v1.py
"C:\envPython\venv4\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_cava_carulla_v1.py
"C:\envPython\venv4\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_exito_v3.py
rem finish extracting data for EXITO

echo.

exit

