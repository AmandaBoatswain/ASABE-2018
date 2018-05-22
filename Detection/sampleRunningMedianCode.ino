// sampleRunningMedianCode.ino
// Most of this came from Rob Tillaart's code on https://github.com/RobTillaart/Arduino/tree/master/libraries/RunningMedian
// Dependencies: RunningMedian.h (see include statement below)
// The .h and .cpp files you need to run this are RunningMedian.h and RunningMedian.cpp. These two should be saved in a 
// folder called "RunningMedian", which itself needs to be in the Adruino/libraries/ folder.
// const int windowsize = # must be provided ahead of time
// Last edit: 05-18-2018 


#include "RunningMedian.h"

const int windowsize = 15;

RunningMedian sample_data = RunningMedian(windowsize);

void setup() {
  // put your setup code here, to run once:
  while (!Serial) ;
  Serial.begin(9600);
  Serial.println("Starting....");
}

void loop() {
  // put your main code here, to run repeatedly:
  for (byte i = 0; i <= 100; i++) {
    int value = random(0, 5);
    for (byte j = 0;j < 15; j++) {
      Serial.print(sample_data.getSortedElement(j));
      Serial.print(", ");
    }
    Serial.println("");
    Serial.println("");
    float value_as_float = float(value);
    sample_data.add(value_as_float);
    float currentmedian = sample_data.getMedian();
    Serial.print("getMedian() result = ");
    Serial.println(currentmedian);
  }
  
}
