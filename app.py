# -*- coding: utf-8 -*-
from timezonefinder import TimezoneFinder
from pytz import timezone, utc
from flask import Flask, request
import os, datetime, subprocess

app = Flask(__name__)

@app.route('/vedic', methods=["PUT", "POST"])
def vedic():
    data = request.get_json(force=True)
    tf = TimezoneFinder() 
    today = datetime.datetime.now()
    tz_target = timezone(tf.certain_timezone_at(lng=32.94905410633718, lat=39.774503259632304))
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    offset = (today_utc - today_target).total_seconds() / 3600
    offset = str(offset)    
    pydir = os.path.dirname(os.path.abspath(__file__))    
    # these two jars are needed for Vedic Java call
    os.environ['CLASSPATH'] = pydir + "/astromaestro.jar:" + \
                              pydir + "/jlewi/lib/commons-lang3-3.13.0.jar"
    p = subprocess.Popen(['java','swisseph.Vedic',data['day'],data['mon'],data['year'],data['hour'],data['lat'],data['lon'],offset],
                          stdout=subprocess.PIPE)
    res = p.stdout.read().decode().strip()
    return res


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "secretkeyverysecret" # needed for session[] to work
    app.run(host="localhost",port=5000)

