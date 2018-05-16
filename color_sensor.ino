/* HEADER 
 * MacRobotics Color Sensing Code      
 * Created May 9th, 2018 
 * Written by Genevieve & Samy Coulombe      
 */

/* --- Variable Definition  --- */
// Sensor pins
#define S0 8 
#define S1 9
#define S2 10
#define S3 11
#define led 7
#define sensorOut 12

// Color readings 
int red_frequency = 0;
int blue_frequency = 0;
int green_frequency =0;
char col; 
int color = 0; 

/* --- Setup Code  --- */
void setup() {
  // Set output pins   
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(led, OUTPUT);
  // Set sensor input pin  
  pinMode(sensorOut, INPUT);
  
  // Setting frequency-scaling to 20%
  digitalWrite(S0, HIGH);
  digitalWrite(S1, HIGH);
  Serial.begin(9600);
}

/* --- Loop - Read Color value from the sensor & record it --- */
void loop() {
  color = readColor();
  delay(500);  
  Serial.print("Color = ");
  Serial.println(color);
}

// Custom Function - readColor()
int readColor() { 
  // Setting red filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  digitalWrite(led, HIGH); 
  
  // Reading the output frequency
  red_frequency = pulseIn(sensorOut, LOW);
  /* Printing the value on the serial monitor
   * Serial.print("R= ");//printing name
   * Serial.print(red_frequency);//printing RED color frequency
   * Serial.print("  "); */
  delay(100);

  // Setting Green filtered photodiodes to be read
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  // Reading the output frequency
  green_frequency = pulseIn(sensorOut, LOW);
   /* Printing the value on the serial monitor
   * Serial.print("B= ");//printing name
   * Serial.print(green_frequency);//printing GREEN color frequency
   * Serial.print("  "); */
  delay(100);

  // Setting Blue filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  // Reading the output frequency
  blue_frequency = pulseIn(sensorOut, LOW);
   /* Printing the value on the serial monitor
   * Serial.print("B= ");//printing name
   * Serial.print(blue_frequency);//printing BLUE color frequency
   * Serial.print("  "); */ 
  delay(100);
  digitalWrite(led, LOW); 

  if(green_frequency >red_frequency & blue_frequency > red_frequency & red_frequency < 30){
    color = 1; // Red
  }
 else if(red_frequency<blue_frequency & green_frequency<blue_frequency & green_frequency < red_frequency){
    color = 2; // Green
  }
  else if(red_frequency > blue_frequency & green_frequency>blue_frequency){
    color = 3; // Blue
  }
  else {
   color = 0;
  }
  
  return color;  
}
