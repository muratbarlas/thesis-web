/*------------------------------------------------------------------------
  Example sketch for Adafruit Thermal Printer library for Arduino.
  Demonstrates a few text styles & layouts, bitmap printing, etc.

  IMPORTANT: DECLARATIONS DIFFER FROM PRIOR VERSIONS OF THIS LIBRARY.
  This is to support newer & more board types, especially ones that don't
  support SoftwareSerial (e.g. Arduino Due).  You can pass any Stream
  (e.g. Serial1) to the printer constructor.  See notes below.
  ------------------------------------------------------------------------*/

#include "Adafruit_Thermal.h"
#include "adalogo.h"
#include "adaqrcode.h"

// Here's the new syntax when using SoftwareSerial (e.g. Arduino Uno) ----
// If using hardware serial instead, comment out or remove these lines:
#include <Keyboard.h>

#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer


const int BUTTON_PIN = 8;
const int BUTTON_PIN2 = 9;
bool pressed = false;
bool pressed2 = false;


SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor
// Then see setup() function regarding serial & printer begin() calls.

// Here's the syntax for hardware serial (e.g. Arduino Due) --------------
// Un-comment the following line if using hardware serial:

//Adafruit_Thermal printer(&Serial1);      // Or Serial2, Serial3, etc.

// -----------------------------------------------------------------------

void setup() {
    Serial.begin(9600);

  Keyboard.begin();
  
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);

  // This line is for compatibility with the Adafruit IotP project pack,
  // which uses pin 7 as a spare grounding point.  You only need this if
  // wired up the same way (w/3-pin header into pins 5/6/7):
  pinMode(7, OUTPUT); digitalWrite(7, LOW);
  // NOTE: SOME PRINTERS NEED 9600 BAUD instead of 19200, check test page.
  mySerial.begin(19200);  // Initialize SoftwareSerial
  //Serial1.begin(19200); // Use this instead if using hardware serial
  printer.begin();        // Init printer (same regardless of serial type)


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




  if (Serial.available() > 0) {
    String data = Serial.readString();  // Read the incoming data
    Serial.print("Received: ");
    Serial.println(data);

    printer.doubleHeightOn();
    printer.println(F("Receipt of your participation"));
    printer.println(F("Your score is: "));
    printer.println((data));
    printer.println(F("Thank you for participating"));
    printer.println(F("What is real?"));
    printer.println(F(""));
    printer.println(F(""));
    printer.sleep();      // Tell printer to sleep
    delay(3000L);         // Sleep for 3 seconds
    printer.wake();       // MUST wake() before printing again, even if reset
    printer.setDefault(); // Restore printer to defaults


    // Send a response
    //Serial.println("Hello from Arduino!");
  }
}
