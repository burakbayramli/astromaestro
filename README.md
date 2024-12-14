# Astro Maestro

This project aims to combine numerology, psychology, and
astrology. Most people know about sun signs (Capricorn, Taurus, etc)
which gives 1 out of 12 possibilities. One method we show here uses
(by G. Lewi) all sun and moon combinations, 12x12 = 144 character
possibilities. Grant Lewi method also looks at other planetary
combinations that can supply more in-depth information. Jan Spiller
looks at moon readings differently; the result is another even more
detailed informatio. The accuracy of this reading can be quite
shocking. Lastly Millman numerology, another detailed method that can
reveal character is shared. Chinese astrology is the bonus.

Usage:

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

Refer to the book on the details of these readings. 

### Millman

This is numerology, can be quite predictive for certain things. It can
also report a cycle number which is the period your life path is on;
according to his method life proceeds in 9 year cycles, 1 is time to
start something 9 to enjoy its fruits (and not start something
new). An interesting exercise; starting from the cycle you are at
today, go back in time, year by year; i.e. if current cycle point says
4, and the current year is 2015,

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

### Features

All data required for Spiller and Chinese astrology are already under `data`.
Lewi data needs decans, which are already under `data`, if there is need to
regenerate it, see under `jlewi`.

### Summary

In sum, `mindmeld` calculates the following:

* Grant Lewi Numbers (based on decans)

* Dan Millman Numerology

* Jan Spiller Moon North Node Astrology

* Chinese Astrology

* Myers-Briggs Test

References

[1] Grant Lewi, *Heaven Knows What*

[2] Jan Spiller, Astrology for the Soul

[3] Dan Millman, Live the Life You Were Meant to Live

