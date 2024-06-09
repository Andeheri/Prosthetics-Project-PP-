
#define sampling_pin 21
#define sampling_time 10

int i = 1;

void setup() {
  // Begin serial communication at 9600 baud rate
  Serial.begin(9600);
  // Wait for serial port to connect (only needed on some boards)
  while (!Serial) {
    ; // Wait for serial port to connect. Needed for native USB
  }
}

void loop() {
  // If data is available to read
  Serial.println(String(analogRead(sampling_pin)));
  delay(sampling_time);
}
