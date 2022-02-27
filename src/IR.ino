int s0 = 8;
int s1 = 9;
int s2 = 10;
int s3 = 11;

bool mode_calib;

void setup(){
  mode_calib = true;
  pinMode(s0, OUTPUT); 
  pinMode(s1, OUTPUT); 
  pinMode(s2, OUTPUT); 
  pinMode(s3, OUTPUT); 

  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
    
  Serial.begin(9600);
}


void loop(){
  //Loop through and read all 16 values
//  while(mode_calib){
//    if(Serial.available()>0){
//      char signal = Serial.read();
//      if(signal == 'R'){
//        Serial.println("Reading value...");
//        for(int i = 0; i < 5; i ++){
//          Serial.print(readMux(i));
//          Serial.print(",");
//        }
//        Serial.println();
//      }
//      else if(signal == 'X'){
//        Serial.println("Exiting calibration mode...");
//        mode_calib = false;
//      }
//    }
//  }
  
  for(int i = 0; i < 5; i ++){
//    Serial.print(4325/(readMux(i)+6.53)-4.4);
//    Serial.print(30000/(readMux(i)-1));
    Serial.print(readMux(i));
    Serial.print(",");
  }
  Serial.println();
  delay(100);
}


int readMux(int channel){
  int controlPin[] = {s0, s1, s2, s3};

  int muxChannel[16][4]={
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1}  //channel 15
  };

  //loop through the 4 sig
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }

  //read the value at the SIG pin
  int val = analogRead(A0);
  val = analogRead(A0);
  val = analogRead(A0);
  val = analogRead(A0);
  val = analogRead(A0);
  val = analogRead(A0);
  return val;
}
