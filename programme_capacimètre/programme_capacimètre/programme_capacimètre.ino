#define E 8
#define Vc A0

const int r=10; //r en Kohm

void setup() {
  // Alimentation du condensateur
  pinMode(E, OUTPUT) ;
  // Decharge initiale du condensateur
  Serial.println("Preparation du condensateur") ;
  digitalWrite(E, LOW) ;
  Serial.begin(9600) ;
  
  delay(1000) ;

  Serial.println("Charge du condensateur") ;  Serial.print("Temps t (ms)") ;
  Serial.print("\t") ;
}

void loop() {
  
  // Charge du condensateur
  digitalWrite(E, HIGH) ;
  float t1 = millis() ; //fixe notre reference de temps
  while (analogRead(Vc)<int(1023*0.63)){
    //attendre que Vc soit egal à 63% de 5v
    //Serial.print("La valeur de Vc est de:") ;Serial.println(analogRead(Vc));
  }
  float t2 = millis() ; //t=to
  float to=t2-t1;
  //Serial.print("La valeur de T2 est de: ") ;Serial.println(t2, 6);
  //Serial.print("La valeur de T1 est de: ") ;Serial.println(t1, 6);
  Serial.print("La valeur de To est de: ") ;Serial.print(to, 6); Serial.println("ms");
  digitalWrite(E, LOW) ;//Arret de la charge du condensateur
  float c=to/r;//Calcul de la valeur de C
  
  Serial.print("La valeur de C est de: ") ;Serial.print(c,3); Serial.println(" microF");
  delay(10*int(to)) ;//On s'assure que le condensateur se decharge avec un temps de 10 to
}

