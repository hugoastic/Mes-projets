/*
    Grove_Air_Quality_Sensor.ino
*/

#include "Air_Quality_Sensor.h"
#include <SoftwareSerial.h>

//Bluetooth
#define rxPin 11 // Broche 11 en tant que RX, à raccorder sur TX du HC-05
#define txPin 13 // Broche 10 en tant que TX, à raccorder sur RX du HC-05
SoftwareSerial mySerial =  SoftwareSerial(rxPin, txPin); // Bluetooth

//LED couleur
#define rouge 5
#define jaune 7
#define vert 9

AirQualitySensor sensor(A0);//capteur Arduino
#define  sensor_non_arduino_home A1//capteur TGS2600
#define sensor_non_arduino_industry A2//capteur TGS822

/*Variable utilisées pour les calculs de qualité d'air*/
int Vrl0; //tension en mV dans l'air pur
float R0; //resistance du capteur dans air pur
float Rs; // resistance lors de la mesure de la quélité d'air
float ratio; // raport Rs/R0
float concentration;
int analog_value; // valeur analogique entre 0 et 1024 (10bits) retournée par le capteur
int mV_value; // valeur convertit en mV retournée par le capteur


//choice of the non Arduino sensor to use
String choix_sensor = "arduino";

void setup(void) {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);

  pinMode(rouge, OUTPUT);
  pinMode(jaune, OUTPUT);
  pinMode(vert, OUTPUT);

  pinMode(sensor_non_arduino_home, INPUT);
  pinMode(sensor_non_arduino_industry, INPUT);

  mySerial.begin(9600);

  while ((!mySerial)and(mySerial.available() <= 0)) ;
  mySerial.println("Waiting sensor to init and choice sensor...");
  delay(3000);

  if (sensor.init()) {
    mySerial.println("Sensor ready.");
  } else {
    mySerial.println("Sensor ERROR!");
  }
}

void loop(void) {

  if (mySerial.available() > 0) {
    choix_sensor = mySerial.readStringUntil('\n');//on lit tous les caractères envoyés jusqu'au caractère sentinelle
    choix_sensor.trim();//'netoie' la chaine de caractères des caractères parasites
  }

  delay(500);

  if (choix_sensor == "arduino") { /*Arduino Sensor*/

    Vrl0 = 140.0;  //reference value in fresh air in mV for arduino groove sensor

    int quality = sensor.slope();
    analog_value = sensor.getValue();
    mV_value = (float) map(analog_value, 0, 1024, 150, 4400);

    R0 = ((5000.0 / Vrl0) - 1.0) * 10000.0;
    Rs = (((5000.0 / mV_value) - 1.0) * 10000.0);
    ratio = (Rs / R0);

    mySerial.println("arduino");
    mySerial.println("Sensor value in mV: ");
    mySerial.print(mV_value);
    mySerial.println("");
    mySerial.print("Value Rs on R0: ");
    mySerial.print(ratio);
    mySerial.println("");

    //The arduino gaz sensor module provides a method that send a message wether the pollution is high or low
    if (quality == AirQualitySensor::HIGH_POLLUTION) {
      mySerial.println("High pollution!");
      digitalWrite(vert, LOW);
      digitalWrite(jaune, LOW);
      digitalWrite(rouge, HIGH);
    } else if (quality == AirQualitySensor::LOW_POLLUTION) {
      mySerial.println("Low pollution!");
      digitalWrite(vert, LOW);
      digitalWrite(jaune, HIGH);
      digitalWrite(rouge, LOW);
    } else if (quality == AirQualitySensor::FRESH_AIR) {
      mySerial.println("Fresh air.");
      digitalWrite(vert, HIGH);
      digitalWrite(jaune, LOW);
      digitalWrite(rouge, LOW);
    }

  }

  else if (choix_sensor == "TGS822") { /* Non -arduino sensor for home*/

    R0 = 37654.3;  //reference value in fresh air in mV for TGS822 calculated with Rs,air/R0=10.8

    analog_value = analogRead(sensor_non_arduino_industry);
    mV_value = (float) map(analog_value, 0, 1024, 70, 4000); //Value in mV
    
    Rs = (((5000.0 / mV_value) - 1.0) * 10000.0);
    ratio = (Rs / R0);

    concentration = log(ratio/3.7338) / 0.002; // modèle déduit lors de la calibration


    mySerial.println("TGS822");
    mySerial.println("Sensor value in mV: ");
    mySerial.print(mV_value);
    mySerial.println("");
    mySerial.print("Value Rs on R0: ");
    mySerial.print(ratio);
    mySerial.println("");
    mySerial.print("Concentration (ppm) : ");
    mySerial.print(concentration);
    mySerial.println("");

    if (ratio > 2) {
      digitalWrite(vert, HIGH);
      digitalWrite(jaune, LOW);
      digitalWrite(rouge, LOW);
    }
    else if (ratio<2 and ratio>0.7) {
      digitalWrite(jaune, HIGH);
      digitalWrite(vert, LOW);
      digitalWrite(rouge, LOW);
    }
    else if (ratio < 0.7) {
      digitalWrite(rouge, HIGH);
      digitalWrite(jaune, LOW);
      digitalWrite(vert, LOW);
    }

  }


  else if  (choix_sensor == "TGS2600") { /* Non -arduino sensor for industries*/

    Vrl0 = 100.0;  //reference value in fresh air in mV for TS2600

    analog_value = analogRead(sensor_non_arduino_home);
    mV_value = (float) map(analog_value, 0, 1024, 100, 5000); //Value in mV

    R0 = ((5000.0 / Vrl0) - 1.0) * 10000.0;
    Rs = (((5000.0 / mV_value) - 1.0) * 10000.0);
    ratio = (Rs / R0);


    mySerial.println("TGS2600");
    mySerial.println("Sensor value in mV: ");
    mySerial.print(mV_value);
    mySerial.println("");
    mySerial.print("Value Rs on R0: ");
    mySerial.print(ratio);
    mySerial.println("");

    if (ratio > 0.4) {
      digitalWrite(vert, HIGH);
      digitalWrite(jaune, LOW);
      digitalWrite(rouge, LOW);
    }
    else if (ratio<0.4 and ratio>0.1) {
      digitalWrite(jaune, HIGH);
      digitalWrite(vert, LOW);
      digitalWrite(rouge, LOW);
    }
    else if (ratio < 0.1) {
      digitalWrite(rouge, HIGH);
      digitalWrite(jaune, LOW);
      digitalWrite(vert, LOW);
    }

  }

  else {
    mySerial.println("Waiting for sensor choice...");
  }

  delay(1000);

}
