/* HEADER 

 * MacRobotics Color Sensing Code      

 * Created May 9th, 2018 

 * Written by Genevieve & Samy Coulombe      

 */

#include <Wire.h>

#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(); // called this way, it uses the default address 0x40

/* --- Variable Definition  --- */

// Sensor pins

#define S0 8 

#define S1 9

#define S2 10

#define S3 11

#define led 7

#define sensorOut 12

const int motor_servo = 0;

//PWM Constants

const int servo_off = 335;

const int pwm_freq = 60;

// Color readings 

int red_frequency = 0;

int blue_frequency = 0;

int green_frequency =0;

int color = 0; 

char color_char;

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

//Servo functions//

pwm.begin();

pwm.setPWMFreq(pwm_freq);

pwm.setPWM(motor_servo, 0, servo_off);

}

void loop() {

  color = readColor(12);

  delay(1000);  

  Serial.print("Color = ");

  Serial.println(color);

  pwm.setPWM(motor_servo, 0, 600);

  delay (1000);

  pwm.setPWM(motor_servo, 0, servo_off);

  delay (1000);

  

}

// Custom Function - readColor()
// readColor() 
// input: int number_of_reads, the number of individual readings to make before finding their median
// output: int 0, 1, 2, or 3, which corresponds to a reading of "unknown", "red", "green", or "blue"
// description: takes 3 sets of readings, one for each primary colour (red, green, blue).
// each set of readings is made up of $number_of_reads individual readings, and the median
// of those readings is considered the final reading (the median is obtained by sorting 
// the readings in the set from lowest->highest using the quickSort() function). 
// the three medians (red median as red_frequency, green median as green_frequency, blue median as 
// blue_frequency) are then considered in an if/else if/else block.
// NOTE: there are a few "delay()" statements that could maybe be removed to speed things up.

int readColor(number_of_reads) { 

  // Setting red filtered photodiodes to be read

  digitalWrite(S2,LOW);

  digitalWrite(S3,LOW);

  digitalWrite(led, HIGH); 

  // Initializing the read-frequency, array length can be changed.
  int array_length = number_of_reads;
  int red_freqs[array_length];
  int blue_freqs[array_length];
  int green_freqs[array_length];
  int midpoint = (array_length+1)/2; // arduino uses integer division
  
  int i = 0; // index for arrays
  // Reading the output frequency

  //red_frequency = pulseIn(sensorOut, LOW);
  while (i < 7) {
    red_freqs[i] = pulseIn(sensorOut, LOW);
    i++;
    delay(10);
  }
  quickSort(red_freqs, 0, array_length);
  red_frequency = red_freqs[midpoint]; // sets red_frequency to the median value
  i = 0; // resetting i
  Serial.print("Median red freq: ");
  Serial.println(red_frequency);
  // delay(100);

  // Setting Green filtered photodiodes to be read

  digitalWrite(S2,HIGH);

  digitalWrite(S3,HIGH);

  // Reading the output frequency

  //green_frequency = pulseIn(sensorOut, LOW);
  
  while (i < 7) {
    green_freqs[i] = pulseIn(sensorOut, LOW);
    i++;
    delay(10);
  }
  quickSort(green_freqs, 0, array_length);
  green_frequency = green_freqs[midpoint]; // sets green_frequency to the median value
  i = 0; // resetting i
  Serial.print("Median green freq: ");
  Serial.println(green_frequency);
  // delay(100);

  // Setting Blue filtered photodiodes to be read

  digitalWrite(S2,LOW);

  digitalWrite(S3,HIGH);

  // Reading the output frequency
  while (i < 7) {
    blue_freqs[i] = pulseIn(sensorOut, LOW);
    i++;
    delay(10);
  }
  quickSort(blue_freqs, 0, array_length);
  blue_frequency = blue_freqs[midpoint]; // sets blue_frequency to the median value
  i = 0; // resets i
  Serial.print("Median blue freq: ");
  Serial.println(blue_frequency);
  //blue_frequency = pulseIn(sensorOut, LOW);
  
  delay(10);

  digitalWrite(led, LOW); 

  if(green_frequency >red_frequency & blue_frequency > red_frequency & red_frequency < 30){

    color = 1; // Red

    color_char = 'R'; // Added for compatibility with the BallPicker2 code
  }

 //else if(red_frequency<blue_frequency & green_frequency<blue_frequency & green_frequency < red_frequency){
 else if(green_frequency<blue_frequency & green_frequency < red_frequency){

    color = 2; // Green

    color_char = 'G'; // Added for compatibility with the BallPicker2 code
  }

  else if(red_frequency > blue_frequency & green_frequency>blue_frequency){

    color = 3; // Blue

    color_char = 'B'; // Added for compatibility with the BallPicker2 code
  } 

 else {

  color = 0;

  color_char = 'N'; // Added for compatibility with the BallPicker2 code
 }

 return color_char;  

}

// quickSort recursively sorts (from low -> high) the input array arr
void quickSort(int arr[], int left, int right) {
  int i = left;
  int j = right;
  int tmp;
  int pivot = arr[(left + right)/2];

  /*partitioning block*/
  while (i <= j) {
    while (arr[i] < pivot) {
      i++;
    } while (arr[j] > pivot) {
      j--;
    }

    if (i <= j) {
      tmp = arr[i];
      arr[i] = arr[j];
      arr[j] = tmp;
      i++;
      j--;
    }
    
  };

  /* recursive block */
  if (left < j) {
    quickSort(arr, left, j);
  }
  if (i < right) {
    quickSort(arr, i, right);
  } 
} // end of quickSort


int red_grab (void) {

  // make arm turn 360 degrees and stop --> door stays closed//

  

}

int blue_grab (void) {

  //make arm turn 360 degrees and stop --> door opens for 10 seconds and then closes//

}

int green_grab (void) {

  

}
