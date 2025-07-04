from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import itertools, os, sys, subprocess, json
from pytz import timezone, utc
import pandas as pd
import numpy as np

fdir = os.path.dirname(os.path.realpath(__file__))
planets = ['sun','mo','mer','ven','mar','ju','sa','ur','ne','pl']

sun_moon_table = np.array(range(144)).reshape((12,12)) + 1

mbti = {'estp':['se','ti','fe','ni'],'esfp':['se','fi','te','ni'],
        'istj': ['si','te','fi','ne'],'isfj':['si','fe','ti','ne'],
        'entp': ['ne','ti','fe','si'], 'enfp': ['ne','fi','te','si'],
        'intj': ['ni','te','fi','se'], 'infj': ['ni','fe','ti','se'],
        'estj': ['te','si','ne','fi'], 'entj': ['te','ni','se','fi'],
        'istp': ['ti','se','ni','fe'], 'intp': ['ti','ne','si','fe'],
        'esfj': ['fe','si','ne','ti'], 'enfj': ['fe','ni','se','ti'],
        'isfp': ['fi','se','ni','te'], 'infp': ['fi','ne','si','te']}

def lewimap_init():
    import pandas as pd
    mapping = pd.DataFrame(index=planets,columns=['tick','*','sq','tri','opp'])
    mapping.loc['mo']['tick'] = {'sun':245,'mer':145,'ven':146,'mar':147,'ju':148,'sa':149,'ur':150,'ne':151,'pl':254}
    mapping.loc['mo']['tri'] = {'sun':246,'mer':152,'ven':153,'mar':154,'ju':155,'sa':156,'ur':157,'ne':158,'pl':255}
    mapping.loc['mo']['*'] = {'sun':246,'mer':152,'ven':153,'mar':154,'ju':155,'sa':156,'ur':157,'ne':158,'pl':255}
    mapping.loc['mo']['sq'] = {'sun':247,'mer':159,'ven':160,'mar':161,'ju':162,'sa':163,'ur':164,'ne':165,'pl':256}
    mapping.loc['mo']['opp'] = {'sun':247,'mer':159,'ven':160,'mar':161,'ju':162,'sa':163,'ur':164,'ne':165,'pl':256}
    mapping.loc['ur']['tick'] = {'ne':242,'pl':272}
    mapping.loc['ur']['tri'] = {'ne':243,'pl':273}
    mapping.loc['ur']['*'] = {'ne':243,'pl':273}
    mapping.loc['ur']['sq'] = {'ne':244,'pl':274}
    mapping.loc['ur']['opp'] = {'ne':244,'pl':274}
    mapping.loc['sun']['tick'] = {'mer':166,'ven':167,'mar':168,'ju':169,'sa':170,'ur':171,'ne':172,'pl':251}
    mapping.loc['sun']['tri'] = {'ven':248,'mar':173,'ju':174,'sa':175,'ur':176,'ne':177,'pl':252}
    mapping.loc['sun']['*'] = {'ven':248,'mar':173,'ju':174,'sa':175,'ur':176,'ne':177,'pl':252}
    mapping.loc['sun']['sq'] = {'mar':178,'ju':179,'sa':180,'ur':181,'ne':182,'pl':253}
    mapping.loc['sun']['opp'] = {'mar':178,'ju':179,'sa':180,'ur':181,'ne':182,'pl':253}
    mapping.loc['sa']['tick'] = {'ur':236,'ne':237,'pl':269}
    mapping.loc['sa']['tri'] = {'ur':238,'ne':239,'pl':270}
    mapping.loc['sa']['*'] = {'ur':238,'ne':239,'pl':270}
    mapping.loc['sa']['sq'] = {'ur':240,'ne':241,'pl':271}
    mapping.loc['sa']['opp'] = {'ur':240,'ne':241,'pl':271}
    mapping.loc['mer']['tick'] = {'ven':183,'mar':184,'ju':185,'sa':186,'ur':187,'ne':188,'pl':257}
    mapping.loc['mer']['tri'] = {'ven':189,'mar':190,'ju':191,'sa':192,'ur':193,'ne':194,'pl':258}
    mapping.loc['mer']['*'] = {'ven':189,'mar':190,'ju':191,'sa':192,'ur':193,'ne':194,'pl':258}
    mapping.loc['mer']['sq'] = {'mar':195,'ju':196,'sa':197,'ur':198,'ne':199,'pl':259}
    mapping.loc['mer']['opp'] = {'mar':195,'ju':196,'sa':197,'ur':198,'ne':199,'pl':259}
    mapping.loc['ju']['tick'] = {'sa':227,'ur':228,'ne':229,'pl':266}
    mapping.loc['ju']['tri'] = {'sa':230,'ur':231,'ne':232,'pl':267}
    mapping.loc['ju']['*'] = {'sa':230,'ur':231,'ne':232,'pl':267}
    mapping.loc['ju']['sq'] = {'sa':233,'ur':234,'ne':235,'pl':268}
    mapping.loc['ju']['opp'] = {'sa':233,'ur':234,'ne':235,'pl':268}
    mapping.loc['ven']['tick'] = {'mar':200,'ju':201,'sa':202,'ur':203,'ne':204,'pl':260}
    mapping.loc['ven']['tri'] = {'mar':205,'ju':206,'sa':207,'ur':208,'ne':209,'pl':261}
    mapping.loc['ven']['*'] = {'mar':205,'ju':206,'sa':207,'ur':208,'ne':209,'pl':261}
    mapping.loc['ven']['sq'] = {'mar':210,'ju':211,'sa':212,'ur':213,'ne':214,'pl':262}
    mapping.loc['ven']['opp'] = {'mar':210,'ju':211,'sa':212,'ur':213,'ne':214,'pl':262}
    mapping.loc['mar']['tick'] = {'ju':215,'sa':216,'ur':217,'ne':218,'pl':263}
    mapping.loc['mar']['tri'] = {'ju':219,'sa':220,'ur':221,'ne':222,'pl':264}
    mapping.loc['mar']['*'] = {'ju':219,'sa':220,'ur':221,'ne':222,'pl':264}
    mapping.loc['mar']['sq'] = {'ju':223,'sa':224,'ur':225,'ne':226,'pl':265}
    mapping.loc['mar']['opp'] = {'ju':223,'sa':224,'ur':225,'ne':226,'pl':265}
    mapping.loc['ne']['tick'] = {'pl':275}
    mapping.loc['ne']['tri'] = {'pl':276}
    mapping.loc['ne']['*'] = {'pl':276}
    mapping.loc['ne']['sq'] = {'pl':277}
    mapping.loc['ne']['opp'] = {'pl':277}    
    return mapping

def get_decans(date):
   # Decans values are between 1 and 24, there are 10 of them in an
   # array per birthday. This data comes from SwissEph. Array cells
   # represent sun, moon, mercury, etc.  First one is sun, second is
   # the moon, the order is the same as the array shown in
   # mapping.planets. 
   decans = pd.read_csv('data/decans.dat',names=['date','decans'],sep=' ')
   tmp=np.array(decans[decans['date']==int(date)]['decans'])
   res = tmp[0].split(':')   
   res = res[:-1]
   res = list(map(int, res))
   return res

def calculate_millman(date):
    millman = []
    sum1 = 0; sum2 = 0
    for s in date: sum1+=int(s)
    for s in str(sum1): sum2+=int(s)
    millman.append(sum1)
    millman.append(sum2)
    for s in str(sum1)+str(sum2): millman.append(int(s))
    res = []
    res = [x for x in millman[2:] if x not in res]
    res.insert(0,millman[0])
    res.insert(1,millman[1])    
    return res

def get_spiller(date):
   spiller = pd.read_csv(fdir + "/" + "data/spiller",names=['from','to','sign'])
   res = spiller.apply(lambda x: int(date) >=int(x['from']) and int(date) <= int(x['to']),axis=1)
   if not np.any(res): return None
   return np.array(spiller[res])[0][2]
   
def get_chinese(date):
   chinese = pd.read_csv(fdir + "/" + "data/chinese",names=['from','to','sign'])
   res = chinese.apply(lambda x: int(date) >=int(x['from']) and int(date) <= int(x['to']),axis=1)
   if not np.any(res): return None
   return np.array(chinese[res])[0][2]
      
def calculate_lewi_decans(decans):
   import pandas as pd
   smap = lewimap_init()
   res = []
   # In order to map the 1-24 decan value to a sign, a little division
   # magic is used. Each sign has 3 decan values, 1-3 is Aries, 4-6 is
   # Taurus, etc. Below this mapping is done for sun and moon only.
   sun = np.ceil(float(decans[0])/3)-1
   moon = np.ceil(float(decans[1])/3)-1
   res.append(sun_moon_table[int(sun),int(moon)])

   # now calculate all the angles
   step_signs = ['*', 'sq', 'tri', 'opp', 'tri', 'sq', '*']
   steps = np.array([6,9,12,18,24,27,30])
   decans = np.array(decans)
   for planet in planets:
      decan = decans[planets.index(planet)]
      relpos = steps + decan; relpos = map(lambda x: x % 36,relpos)
      for pos,step_sign in zip(relpos,step_signs):
         matches = np.array(range(10))[decans == pos]
         pls = np.array(planets)[decans == pos]
         if len(matches)>0:
            for match,p in zip(matches,pls):
               if not pd.isnull(smap.loc[planet,step_sign]) and (p in smap.loc[planet,step_sign]):
                  res.append(smap.loc[planet,step_sign][p])

   # this part is for planet alignments, i.e. detecting same decans
   # that are for multiple planets.
   for i,dec in enumerate(decans):
      matches = np.array(range(10))[decans==dec]
      if len(matches) > 1:
         for x in matches:
            if i<x:
               if not pd.isnull(smap.loc[planets[i],'tick']) and (planets[x] in smap.loc[planets[i],'tick']):
                  res.append(smap.loc[planets[i],'tick'][planets[x]])
            
   return sorted(res)

def calculate_lewi(date):
    decs = get_decans(date)
    print (decs)
    return calculate_lewi_decans(decs)

def conv(s):
    return datetime.strptime(s, '%d/%m/%Y').date().strftime('%Y%m%d')

def calculate_cycle(d):
   try: 
       birth_date = datetime.strptime(d, '%Y%m%d').date()
       str_d = birth_date.strftime('%d %B %Y')
       now_year = datetime.now().year      
       cs = str(birth_date.day)+"/"+str(birth_date.month)+"/"+str(now_year)
       cycle_date = datetime.strptime(cs, '%d/%m/%Y').date()  
       str_cycle_date = cycle_date.strftime('%Y%m%d')
       millman = calculate_millman(str_cycle_date)
       res = str(millman[0])
       res = res[0:2]
       if len (res) > 1:
          total = int(res[0]) + int(res[1])
       else:
          total = int(res[0])
       if total > 9: 
           res = str(total)
           total = int(res[0]) + int(res[1])
       return total
   except: return None

def get_vedic(date):
    d =  datetime.strptime(date, "%Y%m%d")
    day = "%02d" % d.day
    mon = "%02d" % d.month
    year = "%04d" % d.year
    tf = TimezoneFinder() 
    today = datetime.now()
    tz_target = timezone(tf.certain_timezone_at(lng=10, lat=10))
    today_target = tz_target.localize(today)
    today_utc = utc.localize(today)
    offset = (today_utc - today_target).total_seconds() / 3600
    offset = str(offset)
    print ('offset',offset)
    pydir = os.path.dirname(os.path.abspath(__file__))    
    # these two jars are needed for Vedic Java call
    os.environ['CLASSPATH'] = pydir + "/astromaestro.jar:" + \
                              pydir + "/jlewi/lib/commons-lang3-3.13.0.jar"
    p = subprocess.Popen(['java','swisseph.Vedic',day,mon,year,"10","10","10","0"],
                          stdout=subprocess.PIPE)
    res = p.stdout.read().decode().strip()
    res = json.loads(res.replace("'",'"'))
    return res['true Node'][0]

   
def gen_combined():

   s = "19000101"
   fout = open("/tmp/data-19000101.json","w")
   fout.write("[\n")
   for i in range(54790):
   #for i in range(3):
       d =  datetime.strptime(s, "%Y%m%d")
       curr = d + timedelta(days=i)
       d2 = conv(curr.strftime('%d/%m/%Y'))
       print (d2)
       res1 = calculate_millman(d2)
       res2 = get_spiller(d2)
       res3 = get_chinese(d2)
       res4 = calculate_lewi(d2)
       res5 = get_vedic(d2)
       line = str([res2, res3, res5, res1, res4])
       line = line.replace("'",'"')
       fout.write(line)
       fout.write(',\n')
       fout.flush()

   fout.write("[]]")


if __name__ == "__main__":
    if sys.argv[1] == "test1":
        res = calculate_lewi_decans([4,29,1,4,32,32,8,21,25,19])
        print (res)    
    if sys.argv[1] == "test2":
        res = calculate_lewi("19730424")
        print (res)
    if sys.argv[1] == "gen-combined":
        gen_combined()
