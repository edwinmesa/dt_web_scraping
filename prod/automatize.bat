echo.
echo PROCESO DE SCRAPING 

rem Files Current Month
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_carulla_v1.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_cava_carulla_v1.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\exito\web_scraping_exito_v3.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\dislicores\web_scraping_dislicores_v2.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\jumbo\web_scraping_jumbo_v3.py
"C:\envPython\venv2\Scripts\python.exe" C:\workflow\dt_web_scraping\prod\lalicorera\web_scraping_la_licorera_v2.py

rem send files at sftp

echo.

exit

