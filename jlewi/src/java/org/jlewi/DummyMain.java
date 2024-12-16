package org.jlewi;
import swisseph.Vedic;

public class DummyMain {

    public void test() {
	int year = 1973;
	int month = 4;
	int day = 24;
	double longitude = 32.85646943314241;
	double latitude = 39.941139297390365;
	double time = 10;
	double greenwichOffset = -3;
	//Vedic v = new Vedic();
	String res = Vedic.getReading(day, month, year, latitude, longitude, time, greenwichOffset);
	System.out.println(res);		
    }
    
    public String sayHello() {
	return "hello";
    }
    
    public static final void main(final String[] args) throws Exception {
	System.out.println("Welcome to AstroMeastro");
    }

}
