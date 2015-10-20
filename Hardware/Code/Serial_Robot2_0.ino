/**** Created by: Hamza Boughraira****/
#include<Servo.h> 
#include"DHT.h"

#define DRM 4 
#define IRM 7
#define DLM 8
#define ILM 12
#define DHTPIN 3
#define DHTTYPE DHT11

unsigned long time = 0;
int l;
int data;
int h;
int t;
Servo cam;
DHT dht(DHTPIN, DHTTYPE);

void setup(){
  cam.attach(9);
  cam.write(90);
  pinMode(DRM, OUTPUT);
  pinMode(IRM, OUTPUT);
  pinMode(DLM, OUTPUT);
  pinMode(ILM, OUTPUT);
  Serial.begin(9600);
  dht.begin();
}
void loop(){
    h = dht.readHumidity();
    t = dht.readTemperature();
    l = map(analogRead(A5), 0, 1023, 0, 100);
      data = Serial.read();
      switch(data){
        case 'f': Forward();
        break;
        case 'b': Backward();
        break;
        case 's': Stop();
        break;
        case 'l': Left();
        break;
        case 'r': Right();
        break;
        case '1': camRight();
        break;
        case '2': camLeft();
        break;
        case '0': camMiddle();
        break;
      }
      if ((millis() - time) > 1000){
        Serial.print(h);
        Serial.print(';');
        Serial.print(t);
        Serial.print(';');
        Serial.print(l);
        Serial.println(';');
        time = millis();
      }
  
}

void Forward(){
     digitalWrite(DRM, 1);
      digitalWrite(DLM, 1);
      digitalWrite(IRM, 0);
      digitalWrite(ILM, 0);
}

void Backward(){
     digitalWrite(DRM, 0);
      digitalWrite(DLM, 0);
      digitalWrite(IRM, 1);
      digitalWrite(ILM, 1);
}

void Stop(){
     digitalWrite(DRM, 0);
      digitalWrite(DLM, 0);
      digitalWrite(IRM, 0);
      digitalWrite(ILM, 0);
}

void Left(){
     digitalWrite(DRM, 1);
      digitalWrite(DLM, 0);
      digitalWrite(IRM, 0);
      digitalWrite(ILM, 0);
}

void Right(){
     digitalWrite(DRM, 0);
      digitalWrite(DLM, 1);
      digitalWrite(IRM, 0);
      digitalWrite(ILM, 0);
}

void camRight(){
  cam.write(0);
}

void camLeft(){
    cam.write(180);
}

void camMiddle(){
  cam.write(90);
}
  
