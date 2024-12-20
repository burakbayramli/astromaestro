package swisseph;

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Arrays;

public class Vedic {
    
    public String getReading(int day, int month, int year, double latitude, double longitude, double time, double greenwichOffset) {

	int SID_METHOD = SweConst.SE_SIDM_LAHIRI;
	String[] signNames = { "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
			       "Libra","Scorpio","Sagittarius","Capricorn","Aquarius",
			       "Pisces"};

	
	double hour = time + (0. / 60.) + greenwichOffset; // IST				
	SwissEph sw = new SwissEph();
	SweDate sd = new SweDate(year, month, day, hour);
	sw.swe_set_sid_mode(SID_METHOD, 0, 0);

	double[] cusps = new double[13];
	double[] acsc = new double[10];
	double[] xp = new double[6];
	StringBuffer serr = new StringBuffer();

	double ayanamsa = sw.swe_get_ayanamsa_ut(sd.getJulDay());
	int flags = SweConst.SEFLG_SIDEREAL;
	int result = sw.swe_houses(sd.getJulDay(), flags, latitude, longitude, 'P', cusps, acsc);

	int ascSign = (int) (acsc[0] / 30) + 1;
	String ascOut = signNames[ascSign-1];
	
	flags = SweConst.SEFLG_SWIEPH | 
	    SweConst.SEFLG_SIDEREAL | 
	    SweConst.SEFLG_NONUT | 
	    SweConst.SEFLG_SPEED;

	int sign;
	int house;
	boolean retrograde = false;
	String output = "{";

	output += "'Ascending': ['" + ascOut + "'],";
	
	int[] planets = { SweConst.SE_SUN, SweConst.SE_MOON, SweConst.SE_MARS, SweConst.SE_MERCURY, SweConst.SE_JUPITER,
			  SweConst.SE_VENUS, SweConst.SE_SATURN, SweConst.SE_TRUE_NODE }; // Some

	for (int p = 0; p < planets.length; p++) {
	    int planet = planets[p];
	    String planetName = sw.swe_get_planet_name(planet);
	    int ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);
	    sign = (int) (xp[0] / 30) + 1;
	    house = (sign + 12 - ascSign) % 12 + 1;
	    retrograde = (xp[3] < 0);
	    output += String.format("'%s': ['%s',%d],", planetName,signNames[sign-1],house);
	}

	xp[0] = (xp[0] + 180.0) % 360;
	String planetName = "Ketu (true)";
	sign = (int) (xp[0] / 30) + 1;
	house = (sign + 12 - ascSign) % 12 + 1;
	output += String.format("'%s': ['%s',%d]", planetName,signNames[sign-1],house);

	output += "}";	
	return output;
    }

    public void test() {
	int year = 1973;
	int month = 4;
	int day = 24;
	double longitude = 32.85646943314241;
	double latitude = 39.941139297390365;
	double time = 10;
	double greenwichOffset = -3;
	String res = getReading(day, month, year, latitude, longitude, time, greenwichOffset);
	System.out.println(res);		
    }

    public String getReading(String[] args) {
	int day = Integer.valueOf(args[0]);
	int mon = Integer.valueOf(args[1]);
	int year = Integer.valueOf(args[2]);
	double time = Double.valueOf(args[3]);
	double latitude = Double.valueOf(args[4]);
	double longitude = Double.valueOf(args[5]);
	double greenwichOffset = -1 * Double.valueOf(args[6]);
	//System.out.printf("Java received %d %d %d %f %f %f %f", day,mon,year,time,latitude,longitude,offset);
	String res = getReading(day, mon, year, latitude, longitude, time, greenwichOffset);
	//System.out.println(res);		
	return res;
    }
    
    public static void main(String[] args) {
	Vedic v = new Vedic();
	v.test();
	//v.getReading(args);
    }
}
