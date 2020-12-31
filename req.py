import requests
res = requests.post('http://185.8.174.140:8556/filter/aa', json={"code":"(pl)>(pf) && ((pf)-(pmin)) > 2.5* ((pl)-(pf)) && ((pmax)-(pl)) <= 0.5*((pl)-(pf))"})

print(res.json())