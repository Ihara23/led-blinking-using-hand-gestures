char l;
//char il = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
int pwm_val;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    l = Serial.read();
    
    pwm_val = map(l,97,122,0,255);
    analogWrite(3,pwm_val);
     
    
  }

}
