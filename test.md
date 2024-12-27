

```python
import os, datetime, subprocess, json
cp = 'jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar'
```

```python
p = subprocess.Popen(['java','-classpath',cp,'swisseph.Vedic','1','10','1963','10','10','10','1'],
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

https://astrolinked.com/native/792/donald-trump/charts/birth/
Trump
Friday, June 14, 1946, 10:54 AM
Jamaica, Queens, NY, United States
Asc Leo
Sun Taurus
Moon Scorpio

```python
p = subprocess.Popen(['java','-classpath',cp,'swisseph.Vedic','14','6','1946','11','40.70','-73.79','-5'],
                      stdout=subprocess.PIPE)
res = p.stdout.read().decode().strip()
res = res.replace("'",'"')
res = json.loads(res)
print (res)
```

```text
{'Ascending': ['Leo'], 'Sun': ['Taurus', 10], 'Moon': ['Scorpio', 4], 'Mars': ['Leo', 1], 'Mercury': ['Gemini', 11], 'Jupiter': ['Virgo', 2], 'Venus': ['Cancer', 12], 'Saturn': ['Cancer', 12], 'true Node': ['Taurus', 10], 'Ketu (true)': ['Scorpio', 4]}
```











