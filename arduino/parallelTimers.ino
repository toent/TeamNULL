// // including display library
// #include "Display.h"

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

// current timer variable, used to index switches and maintained between 1 and 4. There probably is a better method to do this that I don't yet know of, feedback is appreciatd c:
int currentTimer = 1;

// per timer start time variables
unsigned long redStartTime = 0;
unsigned long blueStartTime = 0;
unsigned long greenStartTime = 0;
unsigned long yellowStartTime = 0;

// variable for cycle time management (used to check and update timers once per second)
unsigned long lastCycleTime = millis() + 1100;

// previous input management
int previousLeftInput = 1;
int previousRightInput = 1;

void setup() {
  pinMode(redLed,OUTPUT);
  pinMode(greenLed,OUTPUT);
  pinMode(blueLed,OUTPUT);
  pinMode(yellowLed,OUTPUT);
  pinMode(leftButton,INPUT_PULLUP);
  pinMode(rightButton,INPUT_PULLUP);
  pinMode(buzzer,OUTPUT);

  Serial.begin(9600);
};

// function to start red timer
unsigned long redTimer() {
  // turning on red timer light and returning the start time
  digitalWrite(redLed, HIGH);
  return millis();
};

// function to start green timer, same code as redTimer
unsigned long greenTimer() {
  digitalWrite(greenLed, HIGH);
  return millis();
};

// function to start blue timer, same code as redTimer
unsigned long blueTimer() {
  digitalWrite(blueLed, HIGH);
  return millis();
};

// function to start yellow timer, same code as redTimer
unsigned long yellowTimer() {
  digitalWrite(yellowLed, HIGH);
  return millis();
};

// the completed timer state
unsigned long timerComplete(int timerLed, int timerTone) {
  // cycling the LED and buzzer on and off each check
  digitalWrite(timerLed, !digitalRead(timerLed));
  tone(buzzer,timerTone, toneLength);

  // resetting the timer if the right button is pressed
  if (digitalRead(rightButton) == 0) {
    digitalWrite(timerLed, LOW);
    // decrementing current timer only if it will remain within the allowed range
    if (currentTimer > 1) {--currentTimer;};
    return 0;
  };
};

void loop() {
  // updating previous input to stop continous input on button hold
  if (digitalRead(leftButton) == 1) {
    previousLeftInput = 1;
    // TEMP DEBOUNCE WITH DELAY ---------------------------------------------------------
    delay(30);
  }

  // updating previous input to stop continous input on button hold
  if (digitalRead(rightButton) == 1) {
    previousRightInput = 1;
    // TEMP DEBOUNCE WITH DELAY ---------------------------------------------------------
    delay(30);
  }

  // checking for left button press
  if (digitalRead(leftButton) == 0 && previousLeftInput != digitalRead(leftButton))
  {
    // using a switch to select which timer to start. Starting it only if it was previously disabled
    switch (currentTimer) {
    case 1:
        // checking to make sure the timer isn't already started
        if (redStartTime != 0) {break;}
        redStartTime = redTimer();   
        break;
    case 2:
        if (greenStartTime != 0) {break;}
        greenStartTime = greenTimer();
        break;
    case 3:
        if (blueStartTime != 0) {break;}
        blueStartTime = blueTimer();
        break;
    case 4:
        if (yellowStartTime != 0) {break;}
        yellowStartTime = yellowTimer();
        break;
    }
    
    // checking if current timer is at limit of or beyond allowed range
    if (currentTimer < 1 || currentTimer >= 4) {
      // returning it to the range in such a case
      currentTimer = 1;
    } else {
      // otherwise incrementing current timer normally
      ++currentTimer;
    };

    previousLeftInput = 0;
    // TEMP DEBOUNCE WITH DELAY ---------------------------------------------------------
    delay(30);
  }
    
  // checking for combined left and right button press
  if (digitalRead(leftButton) == 0 && digitalRead(rightButton) == 0)
  {
    // selecting the previous timer (with a min value of 1) and resetting it
    if (currentTimer > 1) {--currentTimer;};

    switch (currentTimer)
    {
      case 1:
          redStartTime = 0;
          digitalWrite(redLed, LOW);
          break;
      case 2:
          greenStartTime = 0;
          digitalWrite(greenLed, LOW);
          break;
      case 3:
          blueStartTime = 0;
          digitalWrite(blueLed, LOW);
          break;
      case 4:
          yellowStartTime = 0;
          digitalWrite(yellowLed, LOW);
          break;
      default:
          break;
    }
      
    previousLeftInput = 0;
    previousRightInput = 0;
  };

  // checking and updating timers once every second
  if (millis() - lastCycleTime > 1000) {
    // elapsed time check for red timer
    if (millis() - redStartTime > timerDuration && redStartTime != 0) {
      // setting timer to complete if time is elapsed
      redStartTime = timerComplete(redLed,redTone);
    };

    // elapsed time check for green timer (same as red timer)
    if (millis() - greenStartTime > timerDuration && greenStartTime != 0) {
      greenStartTime = timerComplete(greenLed,greenTone);
    };

    // elapsed time check for blue timer (same as red timer)
    if (millis() - blueStartTime > timerDuration && blueStartTime != 0) {
      blueStartTime = timerComplete(blueLed,blueTone);
    };

    // elapsed time check for yellow timer (same as red timer)
    if (millis() - yellowStartTime > timerDuration && yellowStartTime != 0) {
      yellowStartTime = timerComplete(yellowLed,yellowTone);
    };
  };
}