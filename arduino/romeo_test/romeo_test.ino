/*
   Romeo Board Test

   Reads keys and drives both motor outputs based on the key pressed
   S1 = Forward
   S2 = Stop
   S3 = Reverse
   S4 = 50% Speed
   S5 = 100% Speed
*/
const int BTN_NONE = 0;
const int BTN_FORWARD = 1;
const int BTN_STOP = 2;
const int BTN_REVERSE = 3;
const int BTN_HALF_SPEED = 4;
const int BTN_FULL_SPEED = 5;

//  Motor A
int const M1_DIR = 4;  
int const M1_EN = 5;
//  Motor B
int const M2_EN = 6;  
int const M2_DIR = 7;

int key_Pressed = BTN_NONE;

void setup() {
  pinMode(13, OUTPUT);  //we'll use the debug LED to output a heartbeat
  Serial.begin(9600);
  //while (!Serial);    // Pause until serial link is established. 
                      // Comment out if not using USB connection
 delay(1000);

  // Print instructions one time
 Serial.println("Press S1 = Forward");
 Serial.println("Press S2 = Stop");
 Serial.println("Press S3 = Reverse");
 Serial.println("Press S4 = 50% Speed");
 Serial.println("Press S5 = 100% Speed");
}

void loop()
{
  key_Pressed = Read_Buttons();  // read the buttons

  switch (key_Pressed)           // Do something based on the button pressed
  { 
    case BTN_FORWARD:
      {
        digitalWrite(M1_DIR, HIGH);
        digitalWrite(M2_DIR, HIGH);
        Serial.println("Motors = Forward"); // Print the key that was pressed
        break;
      }
    case BTN_STOP:
      {
        digitalWrite(M1_EN,LOW);  
        digitalWrite(M2_EN,LOW); 
        Serial.println("Motors = Stop");
        break;
      }
    case BTN_REVERSE:
      {
        digitalWrite(M1_DIR, LOW); 
        digitalWrite(M2_DIR, LOW); 
        Serial.println("Motors = Reverse");
        break;
      }
    case BTN_HALF_SPEED:
      {
        analogWrite(M1_EN, 128);
        analogWrite(M2_EN, 128);
        Serial.println("Motors = 50% Speed");
        break;
      }
    case BTN_FULL_SPEED:
      {
        digitalWrite(M1_EN, HIGH);
        digitalWrite(M2_EN, HIGH);
        Serial.println("Motors = Full Speed");
      }
    case BTN_NONE:
      {
        break;
      }
  }
  if(key_Pressed != BTN_NONE)   // Blink LED and debounce switch
  {
  digitalWrite(13, HIGH);  // Turn LED on
  delay(500);              // Delay for switch debounce & LED blink
  digitalWrite(13, LOW);   // Turn LED off
  }
}
//===============================================================================
//  Read Buttons - Subroutine to read the ADC and return the button value
//===============================================================================
int Read_Buttons()
{
  int adc_key_in = analogRead(A0);      // read the value of the key resistor divider
  // The buttons are connected to a voltage divider that feeds into analog input A0.
  // By looking at the voltage level, we can tell which button has been pressed if any.
  // With no button pressed, the voltage will be pulled up to Vcc.
    //Serial.println (adc_key_in);
  if (adc_key_in >= 1000) return BTN_NONE; // Most likely result, so it is the first option.
  if (adc_key_in < 30)   return BTN_FORWARD; // Work our way up the voltage ladder and return 1st valid result
  if (adc_key_in < 200)  return BTN_STOP;
  if (adc_key_in < 500)  return BTN_REVERSE;
  if (adc_key_in < 700)  return BTN_HALF_SPEED;
  if (adc_key_in < 990)  return BTN_FULL_SPEED;

  return BTN_NONE;  // when all others fail, return this...
}
