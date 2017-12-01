#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object

  // initialize serial:
  Serial.begin(9600);
}

void loop() {
  for (pos = 2; pos <= 72; pos += 10) { // goes from 2 degrees to 72 degrees. (Goes from 0 to 70 in real angle)
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    Serial.println(pos);
    delay(500);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 72; pos >= 2; pos -= 10) { // goes from 72 degrees to 2 degrees. (Goes from 0 to 70 in real angle)
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    Serial.println(ṕos);
    delay(500);                      // waits 15ms for the servo to reach the position
  }
}
