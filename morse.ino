String s = String("");
bool separate_f = false;

// micro seconds
int signal_tone = 1600;

float short_rate = 0.05 * pow(10, 6) / signal_tone;
float long_rate = short_rate * 3;
float separate_rate = short_rate * 2;

int count[] = {0, 0};

void setup() {
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(8, INPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  digitalWrite(4, LOW);
}

void loop() {
  if(digitalRead(8) == HIGH){
    count[0]++;
    digitalWrite(13, HIGH);
    digitalWrite(2, HIGH);
    delayMicroseconds(signal_tone / 2);
    digitalWrite(2, LOW);
    delayMicroseconds(signal_tone / 2);
  }else{
    if (count[0] >= 1 && count[0] < long_rate){
      s = String(s + ".");
      char c[2] = {0x61, 0x62};
      Serial.write(".");
      separate_f = true;
      delay(100);
      count[1] = 0;
      count[0] = 0;
    }else if(count[0] >= long_rate){
      s = String(s + "-");
      Serial.write("-");
      separate_f = true;
      delay(100);
      count[1] = 0;
      count[0] = 0;
    }
    
    if(separate_f == true && count[1] >= separate_rate){
      s = String(s + " ");
      Serial.write("/");
      separate_f = false;
      delay(100);
    }

    
    count[1]++;
    digitalWrite(13, LOW);
    delay(5);      
  }

  if (count[0] >= short_rate && count[0] < long_rate){
    digitalWrite(4, HIGH);
  }else{
    digitalWrite(4, LOW);
  }
}
