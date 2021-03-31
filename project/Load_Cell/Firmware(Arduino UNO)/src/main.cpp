#include "HX711.h"
#include <Wire.h>
#include "Seeed_BME280.h"

//#define calibration_factor 7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketch
#define calibration_factor 6560

#define LOADCELL_DOUT_PIN 3
#define LOADCELL_SCK_PIN 2

#define lbstokg(lbs) (lbs / 2.2046)

HX711 scale;
BME280 bme280;

void setup()
{
	Serial.begin(9600);
	scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
	scale.set_scale(calibration_factor); //This value is obtained by using the SparkFun_HX711_Calibration sketch
	scale.tare();						 //Assuming there is no weight on the scale at start up, reset the scale to 0
    if (!bme280.init())
	{
        Serial.println("Device error!");
	}
}

void loop()
{
	float M=lbstokg(scale.get_units());
    float Temp=bme280.getTemperature();
    float press=bme280.getPressure();
    float Hum=bme280.getHumidity();
	if(Serial.available())
	{
		Serial.println(String(M,3)+","+String(Temp,3)+","+String(Hum,3)+","+String(press/100,3));
		Serial.read();
	}
	delay(10);
}