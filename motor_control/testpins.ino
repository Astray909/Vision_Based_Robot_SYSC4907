#define mov0 2
#define mov1 3
#define mov2 4

void setup() {
  pinMode(mov0, INPUT);
  pinMode(mov1, INPUT);
  pinMode(mov2, INPUT);
  Serial.begin(9600);
}

void loop() {
    Serial.println(digitalRead("mov0"));
    Serial.print(digitalRead(mov0));
    Serial.println(digitalRead("mov1"));
    Serial.print(digitalRead(mov1));
    Serial.println(digitalRead("mov2"));
    Serial.print(digitalRead(mov2));
}