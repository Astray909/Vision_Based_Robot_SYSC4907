//Motor Connections
//Change this if you wish to use another diagram
#define EnA 10
#define EnB 5
#define In1 9
#define In2 8
#define In3 7
#define In4 6

#define mov0 2
#define mov1 3
#define mov2 4
#define mov3 11

// #define debug1 3
// #define debug2 11

void setup() {
  // put your setup code here, to run once:
  // All motor control pins are outputs
  pinMode(EnA, OUTPUT);
  pinMode(EnB, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);

  //0000STOP
  //0001STRAIGHT
  //0010BACK
  //0011LEFT
  //0100RIGHT
  //0101LEFTC
  //0110RIGHTC
  //0111LEFTB
  //1000RIGHTB
  pinMode(mov0, INPUT);
  pinMode(mov1, INPUT);
  pinMode(mov2, INPUT);
  pinMode(mov3, INPUT);
  // pinMode(debug1, INPUT);
  // pinMode(debug2, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(mov0) == 0 && digitalRead(mov1) == 0 && digitalRead(mov2) == 0 && digitalRead(mov3) == 1)
  {
    Serial.println("goStraight");
    goStraight();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 0 && digitalRead(mov2) == 1 && digitalRead(mov3) == 0)
  {
    Serial.println("goBack");
    goBack();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 0 && digitalRead(mov2) == 1 && digitalRead(mov3) == 1)
  {
    Serial.println("turnLeft");
    turnLeft();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 1 && digitalRead(mov2) == 0 && digitalRead(mov3) == 0)
  {
    Serial.println("turnRight");
    turnRight();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 1 && digitalRead(mov2) == 0 && digitalRead(mov3) == 1)
  {
    Serial.println("curveLeft");
    curveLeft();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 1 && digitalRead(mov2) == 1 && digitalRead(mov3) == 0)
  {
    Serial.println("curveRight");
    curveRight();
  }
  else if (digitalRead(mov0) == 0 && digitalRead(mov1) == 1 && digitalRead(mov2) == 1 && digitalRead(mov3) == 1)
  {
    Serial.println("backLeft");
    backLeft();
  }
  else if (digitalRead(mov0) == 1 && digitalRead(mov1) == 0 && digitalRead(mov2) == 0 && digitalRead(mov3) == 0)
  {
    Serial.println("backRight");
    backRight();
  }
  else
  {
    Serial.println("stop");
    stop();
  }
}

void stop()
{
  analogWrite(EnA, 0);
  analogWrite(EnB, 0);
}

void goStraight()   //run both motors in the same direction
{
  analogWrite(EnA, 200);
  analogWrite(EnB, 200);
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void goBack()   //run both motors in the same direction
{
  analogWrite(EnA, 200);
  analogWrite(EnB, 200);
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

void turnLeft()
{
  analogWrite(EnA, 100);
  analogWrite(EnB, 100);
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

void turnRight()
{
  analogWrite(EnA, 100);
  analogWrite(EnB, 100);
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void curveLeft()   //run both motors in the same direction
{
  analogWrite(EnA, 200);
  analogWrite(EnB, 100);
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void curveRight()   //run both motors in the same direction
{
  analogWrite(EnA, 100);
  analogWrite(EnB, 200);
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void backLeft()   //run both motors in the same direction
{
  analogWrite(EnA, 200);
  analogWrite(EnB, 100);
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

void backRight()   //run both motors in the same direction
{
  analogWrite(EnA, 100);
  analogWrite(EnB, 200);
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
