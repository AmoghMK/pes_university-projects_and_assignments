#include<Servo.h>
Servo servobase,servotop,servoclaw;
int pos,pos2,basepin=7,toppin=12,clawpin=8,trigpin=2,echopin=4;
float dist,A,B,C,D,pheight=38,oheight=9,x,vdist;
int turned,turned2;
float trigger()
{
  float duration,dist;
  pinMode(trigpin,OUTPUT);
  digitalWrite(trigpin,LOW);
  delayMicroseconds(2);
  digitalWrite(trigpin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin,LOW);
  pinMode(echopin,INPUT);
  duration=pulseIn(echopin,HIGH);
  dist=(duration/29.0/2.0);
  return(dist);
}

void setup()
{
  servobase.attach(basepin);
  servotop.attach(toppin);
  servoclaw.attach(clawpin);
  Serial.begin(9600);
}

void loop()
{
  servobase.write(0);
  servotop.write(0);
  servoclaw.write(90);
  for (pos=0;pos<=180;pos++)
  {
    servobase.write(pos);
    dist=trigger();
    if (dist<=50)
    {
      turned=pos;
      vdist=pheight-oheight;
      //x=sqrt((dist*dist)+(vdist*vdist));
      A=(atan(vdist/dist))*(3.14/180.0);
      //C=2*A;
      //B=(atan(vdist/dist))*(3.14/180.0);
      //D=A-B;
      for (pos2=turned;pos2=(turned+10);pos++)
      {
        servotop.write(90);
        servobase.write(pos2);
        delay(100);
      }
      for (pos2=0;pos2<=A+40;pos2++)
      {
        servotop.write(85);
        delay(29);
        servotop.write(90);
        delay(29);
        turned2=pos2;
      }
      /*for (pos2=0;pos2<=C;pos2++)
      {
       servomid.write(pos2);
       delay(100);
      }*/
      for (pos2=90;pos2>=5;pos2--)
      {
        servoclaw.write(pos2);
        delay(50);
      }
      for (pos2=turned2;pos2>=20;pos2--)
      {
        servotop.write(110);
        delay(10);
        servotop.write(90);
        delay(10);
      }
      break;
    }
    delay (100);
  }
  for(pos=turned+10;pos>=0;pos--)
  {
    servobase.write(pos);
    delay(100);
  }
  for (pos=5;pos<=90;pos++)
  {
    servoclaw.write(pos);
    delay(50);
  }
  /*for (pos=176;pos>=0;pos--)
  {
    servobase.write(pos);
    delay(100);  
  }
  for (pos=D;pos>=0;pos--)
  {
    servotop.write(pos);
    delay(100);
  }*/
  delay(3600000);
}
