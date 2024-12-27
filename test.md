
```python
import os, datetime, subprocess, json
p = subprocess.Popen(['java','-classpath','jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar','swisseph.Vedic','1','10','1963','10','10','10','1'],
                      stdout=subprocess.PIPE)
res = p.stdout.read().decode().strip()
res = res.replace("'",'"')
res = json.loads(res)
print ( res['Ketu (true)'] )
print ( res['true Node'] )
```

```text
['Sagittarius', 2]
['Gemini', 8]
```
