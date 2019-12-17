#include <Servo.h>

Servo myservo; 
                
int pos = 90;  // angle tracker
int angle = 20; // how much to rotate by
int led = 13;
 
void setup()
{
  Serial.begin(9600);  //Begin serial communcation
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(pos);
  pinMode(led,OUTPUT);
}
 
void loop()
{

  char var = Serial.read();
  switch (var) {
    case 'p': //rotate +
        pos = pos + angle;
        myservo.write(pos);
      break;
 
      case 'm': //rotate -
        pos = pos - angle;
        myservo.write(pos);
      break;
      
      case 'o': //ON led in pin13
        digitalWrite(led,HIGH);
      break;
      
      case 'f': //OFF led in pin13
        digitalWrite(led,LOW);
      break;
  }

}
