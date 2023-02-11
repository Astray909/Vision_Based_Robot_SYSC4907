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

// Sensor connection defined below. Uncomment when testing.
// int sensor_Left_pin=12;
// int sensor_Right_pin=13;
// int sensor_Mid_pin=0;



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
  
  // sensor setup begings here: uncomment when testing
  // pinMode(sensor_Left, INPUT); // pin12 set as digital input from left sensor
  // pinMode(sensor_Right, INPUT); // pin13 set as digital input from right sensor
  // pinMode(sensor_Mid, INPUT); // pin0 set as digital input from mid sensor
}


void loop() {
  //int cmd = 1; // Arduino only takes user commands when cmd = 1;
  
  // put your main code here, to run repeatedly:
  //senor condition code below: uncomment when testing
  // if (digitalRead{sensor_Mid}) // if middle sensor detect collision
  //{
  //  cmd = 0;
  //  stop(); // First, robot stop and enter collision avoidance
  //  if (!digitalRead{sensor_Left}) // if left sensor is clear,
  //    {
  //      do
  //       {
  //          turnLeft(); // turn left
  //       }while(digitalRead{sensor_Mid}) // while mid sensor still trigered
  //    }
  //  else if (!digitalRead{sensor_Left}) // if right sensor is clear,
  //    {
  //      do
  //       {
  //          turnRight(); // turn right
  //       }while(digitalRead{sensor_Mid}) // while mid still blocked
  //    }
  //  else // all sensors blocked
  //  {
  //    do
  //     {
  //        turnLeft(); // turn left BY DEFAULT, as target tracking hovering is turn right
  //     }while(digitalRead{sensor_Mid}) // while mid sensor still trigered
  //  }
  //}
  

                 
  //while (cmd == 1)
  //{
  // motion control code from rpi to arduino below:
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
  //}
  
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

