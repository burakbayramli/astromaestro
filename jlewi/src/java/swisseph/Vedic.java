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
    
    public void getReading(int day, int month, int year, double latitude, double longitude, double time, double greenwichOffset) {
	double hour = time + (0. / 60.) + greenwichOffset; // IST
				
	SwissEph sw = new SwissEph();
	SweDate sd = new SweDate(year, month, day, hour);
	System.out.println(sd.getDate(0).toString());
	// Set sidereal mode:
	sw.swe_set_sid_mode(SID_METHOD, 0, 0);

	// Some required variables:
	double[] cusps = new double[13];
	double[] acsc = new double[10];
	double[] xp = new double[6];
	StringBuffer serr = new StringBuffer();

	// Get and print ayanamsa value for info:
	double ayanamsa = sw.swe_get_ayanamsa_ut(sd.getJulDay());

	// Get and print lagna:
	int flags = SweConst.SEFLG_SIDEREAL;
	int result = sw.swe_houses(sd.getJulDay(), flags, latitude, longitude, 'P', cusps, acsc);

	int ascSign = (int) (acsc[0] / 30) + 1;
	System.out.println("Ascendant Sign: " + signNames[ascSign-1] + "\n");

	// Calculate all planets:
	int[] planets = { SweConst.SE_SUN, SweConst.SE_MOON, SweConst.SE_MARS, SweConst.SE_MERCURY, SweConst.SE_JUPITER,
			  SweConst.SE_VENUS, SweConst.SE_SATURN, SweConst.SE_TRUE_NODE }; // Some
	// systems
	// prefer
	// SE_MEAN_NODE

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
	
	planet = planets[0]; // Sun
	planetName = sw.swe_get_planet_name(planet);
	ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);
	sign = (int) (xp[0] / 30) + 1;
	System.out.println(planetName);
	System.out.println(signNames[sign-1]);

	planet = planets[1]; // Moon
	planetName = sw.swe_get_planet_name(planet);
	ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);
	sign = (int) (xp[0] / 30) + 1;
	System.out.println(planetName);
	System.out.println(signNames[sign-1]);
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
	v.getReading(day, month, year, latitude, longitude, time, greenwichOffset);
    }
	
	
    
}

