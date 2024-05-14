#include <Keyboard.h>

const int BUTTON_PIN = 8;
const int BUTTON_PIN2 = 9;
bool pressed = false;
bool pressed2 = false;

void setup() {
  Keyboard.begin();
  Serial.begin(9600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);
}

void loop() {
  bool currentState = digitalRead(BUTTON_PIN);
  bool currentState2 = digitalRead(BUTTON_PIN2);


  if (currentState != pressed) {
    // Button state changed
    pressed = currentState;

    if (pressed == LOW) {
      // Button is pressed
      Serial.println("Button pressed");
      

      // Simulate keyboard input
      Keyboard.press('a');
      Keyboard.release('a');

      while (digitalRead(BUTTON_PIN)==LOW){
        
      }
      delay(200); // Adjust delay as needed
    }
  }


  if (currentState2 != pressed2) {
    // Button state changed
    pressed2 = currentState2;

    if (pressed2 == LOW) {
      // Button is pressed
      Serial.println("Button2 pressed");
      

      // Simulate keyboard input
      Keyboard.press('b');
      Keyboard.release('b');

      while (digitalRead(BUTTON_PIN2)==LOW){
        
      }
      delay(200); // Adjust delay as needed
    }
  }
}