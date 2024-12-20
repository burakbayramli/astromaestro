package swisseph;

import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Arrays;

/**
 * This class is an example of how to calculate planets and houses in the indian
 * vedic style of astrology (jyotish).
 */
public class VedicTest {

    /**
     * The method to determine ayanamsha value:
     */
    private static final int SID_METHOD = SweConst.SE_SIDM_LAHIRI;
    private static final String[] signNames = { "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
						"Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"};
    
    public static void main(String[] args) {
	System.out.println((int)'P');
				
	int year = 1973;
	int month = 4;
	int day = 24;
	double longitude = 32.85646943314241;
	double latitude = 39.941139297390365;
	double hour = 10 + (0. / 60.) - 3; // IST
				
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

	// Print input details:
	System.out.println("Date (YYYY/MM/DD): " + sd.getYear() + "/" + sd.getMonth() + "/" + sd.getDay() + ", "
			   + toHMS(sd.getHour()));
	System.out.println("Jul. day:  " + sd.getJulDay());
	System.out.println("DeltaT:    " + sd.getDeltaT() * 24 * 3600 + " sec.");
	System.out.println("Location:  " + toDMS(Math.abs(longitude)) + (longitude > 0 ? "E" : "W") + " / "
			   + toDMS(Math.abs(latitude)) + (latitude > 0 ? "N" : "S"));

	// Get and print ayanamsa value for info:
	double ayanamsa = sw.swe_get_ayanamsa_ut(sd.getJulDay());
	System.out.println("Ayanamsa:  " + toDMS(ayanamsa) + " (" + sw.swe_get_ayanamsa_name(SID_METHOD) + ")");

	// Get and print lagna:
	int flags = SweConst.SEFLG_SIDEREAL;
	int result = sw.swe_houses(sd.getJulDay(), flags, latitude, longitude, 'P', cusps, acsc);
	System.out.println("Ascendant: " + toDMS(acsc[0]) + "\n");

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

	for (int p = 0; p < planets.length; p++) {
	    int planet = planets[p];
	    String planetName = sw.swe_get_planet_name(planet);
	    int ret = sw.swe_calc_ut(sd.getJulDay(), planet, flags, xp, serr);

	    if (ret != flags) {
		if (serr.length() > 0) {
		    System.err.println("Warning: " + serr);
		} else {
		    System.err.println(String.format("Warning, different flags used (0x%x)", ret));
		}
	    }

	    sign = (int) (xp[0] / 30) + 1;
	    System.out.println(planetName);
	    System.out.println(signNames[sign-1]);
	    house = (sign + 12 - ascSign) % 12 + 1;
	    retrograde = (xp[3] < 0);

	    System.out.printf("%-12s: %s %c; sign: %2d; %s in house %2d\n", planetName, toDMS(xp[0]),
			      (retrograde ? 'R' : 'D'), sign, toDMS(xp[0] % 30), house);
	}
	// KETU
	xp[0] = (xp[0] + 180.0) % 360;
	String planetName = "Ketu (true)";

	sign = (int) (xp[0] / 30) + 1;
	house = (sign + 12 - ascSign) % 12 + 1;

	System.out.printf("%-12s: %s %c; sign: %2d; %s in house %2d\n", planetName, toDMS(xp[0]),
			  (retrograde ? 'R' : 'D'), sign, toDMS(xp[0] % 30), house);
    }

    static String toHMS(double d) {
	d += 0.5 / 3600.; // round to one second
	int h = (int) d;
	d = (d - h) * 60;
	int min = (int) d;
	int sec = (int) ((d - min) * 60);


		
	return String.format("%2d:%02d:%02d", h, min, sec);
    }

    static String toDMS(double d) {
	d += 0.5 / 3600. / 10000.; // round to 1/1000 of a second
	int deg = (int) d;
	d = (d - deg) * 60;
	int min = (int) d;
	d = (d - min) * 60;
	double sec = d;

	return String.format("%3d°%02d'%07.4f\"", deg, min, sec);
    }
	
}
