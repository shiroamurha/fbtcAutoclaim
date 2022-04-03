# fbtcAutoclaim


lib needed: playwright<br>

  

<h4>Step 1:</h4> • Dump all your cookies from freebitco.in on cookies.json everyday you want to run the code (you can use editthiscookie extension for help doing this)<br>
<p align="center">• • • NOTE: remember to delete the cookie dict that has the item "name": "last_play" before running autoclaimer • • •</p> 
<h4>Step 2:</h4> • Run autoclaimer.py<br>

<h4>Commands on cmd (batch) for venv: </h4>

```
py -3 -m venv fbtcAutoclaim
cd fbtcAutoclaim
Scripts\activate
pip install playwright
set PLAYWRIGHT_BROWSERS_PATH=0
playwright install
```
then put git files inside ./fbtcAutoclaim and do `py autoclaimer.py`
