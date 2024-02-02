#define PIN_LED_R 12
#define PIN_LED_G 11
#define PIN_LED_B 10
#define PIN_LED_R2 9
#define PIN_LED_G2 7
#define PIN_LED_B2 4
#define Micro  2
int nMicro;

void setup() {
  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_G, OUTPUT);
  pinMode(PIN_LED_B, OUTPUT); 
  pinMode(PIN_LED_R2, OUTPUT);
  pinMode(PIN_LED_G2, OUTPUT);
  pinMode(PIN_LED_B2, OUTPUT);
  pinMode(Micro, INPUT); 
  displayColor(0, 0, 0);
  displayColorn2(0, 0, 0);
  Serial.begin(9600);
}

void loop() {
  
  nMicro=analogRead (Micro);

  digitalRead(nMicro);

  displayColor(50*nMicro, nMicro*50, 50*nMicro); // trouver pour une plus grande variation de couleur
  displayColorn2(nMicro*50, nMicro*50, nMicro*50);
}

void displayColor(byte r, byte g, byte b) {

  analogWrite(PIN_LED_R, ~r);
  analogWrite(PIN_LED_G, ~g);
  analogWrite(PIN_LED_B, ~b);
}


void displayColorn2(byte r, byte g, byte b) {

  analogWrite(PIN_LED_R2, ~r);
  analogWrite(PIN_LED_G2, ~g);
  analogWrite(PIN_LED_B2, ~b);

}
