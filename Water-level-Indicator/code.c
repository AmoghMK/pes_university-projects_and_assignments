#include<reg51.h>
sbit rs=P1^0;
sbit rw=P1^1;
sbit e=P1^2;
sbit quarter=P3^0;
sbit half=P3^1;
sbit threefourth=P3^2;
sbit full=P3^3;

void delay(unsigned int x)
{
	unsigned int i,j;
	for (i=x;i>0;i--)
	{
		for (j=0;j<1000;j++);
	}
}

void write(int j)
{
	rs=1;
	rw=0;
	P2=j;
	e=1;
	delay(1);
	e=0;
}

void cmd(int j)
{
	P2=j;
	rs=0;
	rw=0;
	e=1;
	delay(1);
	e=0;
}

void puts(char *a)
{
	unsigned int p=0;
	for (;a[p]!=0;p++)
		write(a[p]);
}

void lcd_init()
{
	cmd(0x38);
	delay(1);
	cmd(0x0e);
	delay(1);
	cmd(0x01);
	cmd(0x80);
}

void main()
{
	quarter=half=threefourth=full=1;
	while(1)
	{
		quarter=half=threefourth=full=0;
		if((quarter==0)&&(half==0)&&(threefourth==0)&&(full==0))   
  		{
   			lcd_init();
			puts("empty");
			delay(500);       
		}
		quarter=1;
		if((quarter==1)&&(half==0)&&(threefourth==0)&&(full==0))   
  		{
   			lcd_init();
			puts("quarter");
			delay(500);      
		}
		half=1;
		if((quarter==1)&&(half==1)&&(threefourth==0)&&(full==0))   
  		{
   			lcd_init();
			puts("half");
			delay(500);     
		}
		threefourth=1;
		if((quarter==1)&&(half==1)&&(threefourth==1)&&(full==0))   
  		{
   			lcd_init();
			puts("three-fourth");
			delay(500);       
		}
		full=1;
		if((quarter==1)&&(half==1)&&(threefourth==1)&&(full==1))   
  		{											  	
   			lcd_init();
			puts("full");
			delay(500);      
		}
	}
}  