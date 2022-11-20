//Motor Connections
//Change this if you wish to use another diagram
#define EnA 10
#define EnB 5
#define In1 9
#define In2 8
#define In3 7
#define In4 6

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
  // pinMode(debug1, INPUT);
  // pinMode(debug2, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(EnA, 80);
  analogWrite(EnB, 80);
  goStraight();
  // Serial.println(analogRead(debug1));
  // Serial.println(analogRead(debug2));
  // delay(1000);
  // goBack();
  // delay(1000);
  // turnLeft();
  // delay(1000);
  // turnRight();
  // delay(1000);
}

void goStraight()   //run both motors in the same direction
{
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}

void goBack()   //run both motors in the same direction
{
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void turnLeft()
{
  // turn on motor A
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  // turn on motor B
  digitalWrite(In3, LOW);
  digitalWrite(In4, HIGH);
}

void turnRight()
{
  // turn on motor A
  digitalWrite(In1, LOW);
  digitalWrite(In2, HIGH);
  // turn on motor B
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);
}
