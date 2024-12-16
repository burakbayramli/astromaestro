package swisseph;

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Arrays;

/**
 * This class is an example of how to calculate planets and houses in the indian
 * vedic style of astrology (jyotish).
 */
public class Vedic {

    /**
     * The method to determine ayanamsha value:
     */
    private static final int SID_METHOD = SweConst.SE_SIDM_LAHIRI;
    private static final String[] signNames = { "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
						"Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"};
    
    public String getReading(int day, int month, int year, double latitude, double longitude, double time, double greenwichOffset) {

	double hour = time + (0. / 60.) + greenwichOffset; // IST				
	SwissEph sw = new SwissEph();
	SweDate sd = new SweDate(year, month, day, hour);
	System.out.println(sd.getDate(0).toString());
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
	
	flags = SweConst.SEFLG_SWIEPH | // fastest method, requires data files
	    SweConst.SEFLG_SIDEREAL | // sidereal zodiac
	    SweConst.SEFLG_NONUT | // will be set automatically for sidereal
	    // calculations, if not set here
	    SweConst.SEFLG_SPEED; // to determine retrograde vs. direct
	// motion
	int sign;
	int house;
	boolean retrograde = false;
	int planet;
	String planetName;
	int ret;
	
	planet = SweConst.SE_SUN; // Sun
	planetName = sw.swe_get_planet_name(planet);
	ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);
	sign = (int) (xp[0] / 30) + 1;
	String sunOut = signNames[sign-1];

	planet = SweConst.SE_MOON; // Moon
	planetName = sw.swe_get_planet_name(planet);
	ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);
	sign = (int) (xp[0] / 30) + 1;
	String moonOut = signNames[sign-1];

	String output = String.format("{'ascending': '%s', 'sun': '%s', 'moon': '%s'}", ascOut, sunOut, moonOut);
	return output;
    }

    public static void main(String[] args) {
	int year = 1973;
	int month = 4;
	int day = 24;
	double longitude = 32.85646943314241;
	double latitude = 39.941139297390365;
	double time = 10;
	double greenwichOffset = -3;
	Vedic v = new Vedic();
	String res = v.getReading(day, month, year, latitude, longitude, time, greenwichOffset);
	System.out.println(res);	
    }
	
	
    
}

