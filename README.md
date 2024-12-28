# Astro Maestro

This project aims to combine numerology, psychology, astrology, and
numerology. Most people know about sun signs (Capricorn, Taurus, etc)
which gives 1 out of 12 possibilities. One method we show here uses
(by G. Lewi) all sun and moon combinations, 12x12 = 144 character
descriptions. Grant Lewi method also looks at other planetary
combinations that can supply more in-depth information. Jan Spiller
looks at moon readings differently; the result is another detailed
reading. Millman numerology, another in-depth method that can reveal
detailed character attributes is also shared. Chinese and Vedic
astrology are the bonus additions.

All data required for Spiller and Chinese astrology are in under
`data/decans.dat`.  Lewi data needs decans, which are already under
`data`, if there is need to regenerate it, see `jlewi`.

## Usage

```python
import astromaestro
astromaestro.calculate_millman(astromaestro.conv("10/3/1968"))
```

```text
Out[1]: [28, 10, 2, 8, 1, 0]
```

```python
astromaestro.calculate_lewi(astromaestro.conv("10/3/1968"))
```

```text
Out[1]: [136, 161, 163, 183, 196, 199, 211, 214, 216, 235, 243, 246, 272, 276]
```

Refer to the books in the Reference section on the details of these
readings.

The Lewi and SwissEph codes can be compiled, jarred using the
`build.py` script. Compiling is `python build.py compile`, jarring
requires calling `jar`. To generate decans use `gen-decans`, user can
also generate a combined json file containing all readings per date
via `gen-combined`.

### Millman

This is numerology. The calculation is done via straight addition on the
individual digits of the birthdate.

Millman approach can also calculate a cycle number which is the period
your life path is on; according to his method life proceeds in 9 year
cycles, 1 is time to start something 9 to enjoy its fruits (and not
start something new). An interesting exercise; starting from the cycle
you are at today, go back in time, year by year; i.e. if current cycle
point says 4, and the current year is 2015,

```
2010 8
2011 9
2012 1
2013 2
2014 3
2015 4
...
```

Get current cycle number,

```python
astromaestro.calculate_cycle(astromaestro.conv("10/3/1968"))
```

```text
Out[1]: 3
```

and try to remember the state of your life at those moments in
time, especially at year 1. The results can be revealing.

### Vedic

Using SwissEph we are able to calculate Vedic ascending, sun, moon signs
using the Java code under [swisseph](jlewi/src/java/swisseph). See the
`Vedic.java` or `VedicTest.java` codes for details. Both of these Java
programs can be run via `build.py test-vedic` and `build.py test-vedic2`
respectively. A simple test Python code for Vedic is below,

```python
import os, datetime, subprocess, json
cp = 'jlewi/lib/commons-lang3-3.13.0.jar:astromaestro.jar'

p = subprocess.Popen(['java','-classpath',cp,'swisseph.Vedic','14','6','1946','11','40.70','-73.79','-5'],
                      stdout=subprocess.PIPE)
res = p.stdout.read().decode().strip()
res = res.replace("'",'"')
res = json.loads(res)
print (res)
```

```text
{'Ascending': ['Leo'], 'Sun': ['Taurus', 10], 'Moon': ['Scorpio', 4],
'Mars': ['Leo', 1], 'Mercury': ['Gemini', 11], 'Jupiter': ['Virgo',
2], 'Venus': ['Cancer', 12], 'Saturn': ['Cancer', 12], 'true Node':
['Taurus', 10], 'Ketu (true)': ['Scorpio', 4]}
```

## Web

Vedic reading can be calculated via a simple Web application. Install
Flask

```
pip install flask
```

And a Java JDK (`javac` should be executable from the command prompt,
under any directory), on Ubuntu,

```
sudo apt install default-jdk
```

Now you could simply run Flash with

```
python app.py
```

Connect to http://localhost5000/static/index.html it will show the
main screen for Vedic input. Make sure `astromaestro.jar` exists
before starting the application.


References

[1] Grant Lewi, *Heaven Knows What*

[2] Jan Spiller, Astrology for the Soul

[3] Dan Millman, Live the Life You Were Meant to Live

