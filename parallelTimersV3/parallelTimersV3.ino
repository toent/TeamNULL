#include "Display.h"

// pin naming
const int redLed = 4;
const int greenLed = 5;
const int blueLed = 6;
const int yellowLed = 7;
const int leftButton = 9;
const int rightButton = 8;
const int buzzer = 3;

// tone frequencies and buzzer duration
const int redTone = 200;
const int greenTone = 225;
const int blueTone = 250;
const int yellowTone = 275;
const int toneLength = 500;

// timer duration (TEMP, 600000 = 10 min, 5000 = 5 s)
const unsigned long timerDuration = 5000;

// per timer start time variables
unsigned long redStartTime = 0;
unsigned long blueStartTime = 0;
unsigned long greenStartTime = 0;
unsigned long yellowStartTime = 0;

// variable for cycle time management (used to check and update timers once per second)
unsigned long lastCycleTime = millis() + 1100;

// variable for knowing which was the most recently activated timer
// int previouslyActivatedTimer = 0;

void setup() {
  pinMode(redLed,OUTPUT);
  pinMode(greenLed,OUTPUT);
  pinMode(blueLed,OUTPUT);
  pinMode(yellowLed,OUTPUT);
  pinMode(leftButton,INPUT_PULLUP);
  pinMode(rightButton,INPUT_PULLUP);
  pinMode(buzzer,OUTPUT);
  Serial.begin(115200);
  Display.show("");
};

// red timer start
unsigned long redTimer() {
  // turning on red timer light and returning the start time
  digitalWrite(redLed, HIGH);
  return millis();
};

// green timer start, same code as redTimer
unsigned long greenTimer() {
  digitalWrite(greenLed, HIGH);
  return millis();
};

// blue timer start, same code as redTimer
unsigned long blueTimer() {
  digitalWrite(blueLed, HIGH);
  return millis();
};

// yellow timer start, same code as redTimer
unsigned long yellowTimer() {
  digitalWrite(yellowLed, HIGH);
  return millis();
};

// timer complete state
unsigned long timerComplete(int timerLed, int timerTone, int timerId) {
  // cycling the LED and buzzer on and off each check
  digitalWrite(timerLed, !digitalRead(timerLed));
  tone(buzzer,timerTone, toneLength);

  // timer reset once complete (pressing right button)
  if (digitalRead(rightButton) == 0 && digitalRead(leftButton) == 1) {
    digitalWrite(timerLed, LOW);
    Serial.println(timerId);
    return 0;
  };
};

void loop() {
  // start timer (pressing left button)
  if (digitalRead(leftButton) == 0)
  {
    // finding a pre-selected tiemr (1)
    if (redStartTime == 1) {
      // starting the timer
      redStartTime = redTimer();
      // setting it as the most recently activated timer (used for timer resets)
      // previouslyActivatedTimer = 0;
    };
    if (greenStartTime == 1) {
      greenStartTime = greenTimer();
      // previouslyActivatedTimer = 1;
    };
    if (blueStartTime == 1) {
      blueStartTime = blueTimer();
      // previouslyActivatedTimer = 2;
    };
    if (yellowStartTime == 1) {
      yellowStartTime = yellowTimer();
      // previouslyActivatedTimer = 3;
    };
  };
    
  // // reset timer (pressing left and right buttons together)
  // if (digitalRead(leftButton) == 0 && digitalRead(rightButton) == 0)
  // {
  //   // switch resets ONLY THE MOST RECENTLY ACTIVATED TIMER
  //   switch (previouslyActivatedTimer)
  //   {
  //     case 0:
  //         redStartTime = 1;
  //         digitalWrite(redLed, LOW);
  //         break;
  //     case 1:
  //         greenStartTime = 1;
  //         digitalWrite(greenLed, LOW);
  //         break;
  //     case 2:
  //         blueStartTime = 1;
  //         digitalWrite(blueLed, LOW);
  //         break;
  //     case 3:
  //         yellowStartTime = 1;
  //         digitalWrite(yellowLed, LOW);
  //         break;
  //     default:
  //         break;
  //   }
  // };

  // timer updates (1 time per second)
  if (millis() - lastCycleTime > 1000) {
    // elapsed time check for red timer
    if (millis() - redStartTime > timerDuration && redStartTime > 1) {
      // setting timer to complete if time is elapsed
      redStartTime = timerComplete(redLed,redTone,1);
    }
    // elapsed time check for green timer (same as red timer)
    if (millis() - greenStartTime > timerDuration && greenStartTime > 1) {
      greenStartTime = timerComplete(greenLed,greenTone,2);
    }
    // elapsed time check for blue timer (same as red timer)
    if (millis() - blueStartTime > timerDuration && blueStartTime > 1) {
      blueStartTime = timerComplete(blueLed,blueTone,3);
    }
    // elapsed time check for yellow timer (same as red timer)
    if (millis() - yellowStartTime > timerDuration && yellowStartTime > 1) {
      yellowStartTime = timerComplete(yellowLed,yellowTone,4);
    }
    lastCycleTime = millis();
  };

  // setting a timer to the preassigned state based on serial input
  if (Serial.available() > 0) {
    int serialInput = Serial.parseInt();
    Display.show(serialInput);
    if (serialInput == 1 && redStartTime == 0) {
      redStartTime = 1;
      Serial.println(5);
    };
    if (serialInput == 2 && greenStartTime == 0) {
      greenStartTime = 1;
      Serial.println(6);
    };
    if (serialInput == 3 && blueStartTime == 0) {
      blueStartTime = 1;
      Serial.println(7);
    };
    if (serialInput == 4 && yellowStartTime == 0) {
      yellowStartTime = 1;
      Serial.println(8);
    };
  };
}