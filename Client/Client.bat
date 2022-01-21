set url="http://localhost:5000"
start "chrome" %url%

python main.py %1
