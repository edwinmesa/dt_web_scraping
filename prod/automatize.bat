echo.
echo PROCESO DE RECARGA DE DATOS

rem Files Current Month
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_carulla_v1.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_cava_carulla_v1.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_exito_v3.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\dislicores\web_scraping_dislicores_v2.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\jumbo\web_scraping_jumbo_v3.py

rem send files at sftp

echo.

exit

