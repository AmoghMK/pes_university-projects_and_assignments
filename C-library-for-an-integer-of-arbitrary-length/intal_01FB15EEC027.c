//Minor DAA assignment (UE15CS280)
//AMOGH M K
//01FB15EEC027

#include "intal.h"
#include<string.h>
#include<stdlib.h>
#include<stdio.h>

void* rem_zero(void* intal1);

long max(long a, long b)
{
	if(a > b)
		return a;
	else
		return b;
}

char* compute_multiplier(char* rem,void* intal,int* cnt)
{
	int flag=intal_compare((void*)(rem),intal);
    	*cnt=0;
    	while(flag==1)
    	{
       		(*cnt)++;
       		rem=intal_diff((void*)(rem),intal);
       		flag=intal_compare((void*)(rem),intal);
    	}
    	if(flag==0)
    	{	
        	(*cnt)++;
        	rem=intal_diff((void*)(rem),intal);
    	}
    	return rem;
}

void* intal_create(const char *str)
{
	if(str==NULL)
		return NULL;
	char *string;
  	int length=strlen(str);
  	int i;
  	int count=0;
  	for(i=0;i<length;i++)
  	{
    		if(str[i]!='0')
     		break;
    		count++;
  	}
  	int length_new_string;
  	int j=0;
  	if(count==length)
   		length_new_string=1;
  	else
  		length_new_string=length-count;
  	string=(char *)malloc((length_new_string+1)*sizeof(char));
  	if(length_new_string==1 && str[0]=='0')
  	{
    		string[0]=str[length-1];
    		string[1]='\0';
  	}
  	else
  	{
     		if(str[0]<'0' || str[0]>'9')
     		{
       			string=(char *)malloc((2)*sizeof(char));
       			string[0]='0';
       			string[1]='\0';
       			return (void *)string;
     		}
		for(i=count;str[i]!='\0';i++)
		{
     			if(str[i]>='0' && str[i]<='9')
     				string[j++]=str[i];
     			else
     				break;
   		}
    		string[j]='\0';
  	}
  	return (void *)string;
}

char* intal2str(void* intal)
{
  	if(intal==NULL)
   	{
     		char *null=(char *)malloc(4*sizeof(char));
     		null[0]='N';
     		null[1]='a';
     		null[2]='N';
     		null[3]='\0';
     		return null;
   	}
  	return (char*)intal_create((char*)intal);
}

void intal_destroy(void* intal)
{
  	if(intal==NULL)
		return;
	if(intal!=NULL)
	{
    		free(intal);
  	}
}

int intal_compare(void* intal1, void* intal2)
{
  	//Returns -1, 0, +1
  	//Returns 0 when both are equal.
  	//Returns +1 when intal1 is greater, and -1 when intal2 is greater.
  	if(intal1==NULL || intal2==NULL)
   		return -2;
  	char *string1,*string2;
  	string1=(char *)intal1;
  	string2=(char *)intal2;
  	int string1_len=strlen(string1);
  	int string2_len=strlen(string2);
  	int string1_digit,string2_digit;
  	int i;
  	if(string1_len>string2_len)
   		return 1;
  	else if(string2_len>string1_len)
   		return -1;
  	else
  	{
   		for(i=0;i<string1_len;i++)
   		{
    			 string1_digit=string1[i]-'0';
    			 string2_digit=string2[i]-'0';
    			 if(string1_digit!=string2_digit)
    			{
    				if(string1_digit>string2_digit)
       					return 1;
      				else
       					return -1;
    			}
  		}
   		return 0;
	}
}

void* intal_increment(void* intal)
{
   	if(intal==NULL)
    		return NULL;
  	char *string=(char *)intal;
  	int string_len=strlen(string);
  	int i;
  	int digit;
  	int temp;
  	int carry=0;
  	if(string_len==1)
  	{
    		digit=string[0]-'0';
    		digit=digit+1;
    		if(digit<=9)
     			string[0]=digit+'0';
    		else
    		{
      			string=(char *)malloc((string_len+2)*sizeof(char));
      			string[0]='1';
      			string[1]='0';
      			string[2]='\0';
    		}
  	}
 	else
 	{
  		for(i=string_len-1;i>0;i--)
  		{
    			digit=string[i]-'0';
    			if(i==string_len-1)
     				temp=digit+carry+1;
    			else
     				temp=digit+carry;
    			if(temp==10)
    			{
      				carry=1;
      				string[i]='0';
    			}
    			else
    			{
      				carry=0;
      				string[i]=temp+'0';
  			}
		}
		char *temp_string=(char *)malloc((string_len+1)*sizeof(char));
		digit=string[0]-'0';
		temp=digit+carry;
		int j;
		if(temp<=9)
 			string[0]=temp+'0';
		else
		{
  			for(i=0;i<string_len;i++)
    				temp_string[i]=string[i];
  			temp_string[i]='\0';
  			string=(char *)malloc((string_len+2)*sizeof(char));
 			string[0]='1';
  			string[1]='0';
  			j=2;
  			for(i=1;i<string_len;i++)
   				string[j++]=temp_string[i];
  			string[j]='\0';
		}
		free(temp_string);
	}
 	return (void *)string;
}

void* intal_add(void* intal1, void* intal2)
{
  	if(intal1==NULL || intal2==NULL)
   		return NULL;
  	char *string1=(char *)intal1;
  	char *string2=(char *)intal2;
  	int string1_len=strlen(string1);
  	int string2_len=strlen(string2);
  	int string3_len;
  	int flag=0;
  	if(string1_len>=string2_len)
   		string3_len=string1_len+1;
  	else
  	{
   		string3_len=string2_len+1;
   		flag=1;
 	}
  	char *add_string=(char *)malloc(string3_len*sizeof(char));
  	int carry=0;
  	int i,j,k;
  	int str1digit,str2digit,digit;
  	char *temp_string=(char *)malloc((string3_len)*sizeof(char));
  	if(string1_len==string2_len)
  	{
    		j=string1_len-1;
    		for(i=string1_len-1;i>0;i--)
    		{
      			str1digit=string1[i]-'0';
      			str2digit=string2[i]-'0';
      			digit=str1digit+str2digit+carry;
      			if(digit<=9)
      			{
        			add_string[j--]=digit+'0';
        			carry=0;
      			}
      			else
      			{
        			add_string[j--]=(digit%10)+'0';
        			carry=1;
      			}
    		}
    		digit=(string1[0]-'0')+(string2[0]-'0')+carry;
    		if(digit<=9)
    		{
      			add_string[0]=digit+'0';
      			add_string[string3_len]='\0';
    		}
    		else
    		{
      			for(i=0;i<string3_len;i++)
        			temp_string[i]=add_string[i];
      			temp_string[i]='\0';
      			add_string=(char *)malloc((string3_len+1)*sizeof(char));
      			add_string[0]='1';
      			add_string[1]=(((string1[0]-'0')+(string2[0]-'0')+carry)%10)+'0';
      			j=2;
      			for(i=1;i<string3_len;i++)
       				add_string[j++]=temp_string[i];
      			add_string[j]='\0';
    		}
  	}
  	else
  	{
    		if(flag==0)
    		{
      			j=string1_len-1;
      			char *temp=(char *)malloc((string1_len+1)*sizeof(char));
      			for(i=0;i<(string1_len-string2_len);i++)
        			temp[i]='0';
      			for(k=0;k<string2_len;k++)
       				temp[i++]=string2[k];
      			for(i=string1_len-1;i>0;i--)
      			{
        			str1digit=string1[i]-'0';
        			str2digit=temp[i]-'0';
        			digit=str1digit+str2digit+carry;
        			if(digit<=9)
        			{
          				add_string[j--]=digit+'0';
          				carry=0;
        			}
        			else
        			{
          				add_string[j--]=(digit%10)+'0';
          				carry=1;
        			}
      			}
      			digit=(string1[0]-'0')+(temp[0]-'0')+carry;
      			if(digit<=9)
      			{
        			add_string[0]=digit+'0';
        			add_string[string3_len]='\0';
      			}
      			else
      			{
        			for(i=0;i<string3_len;i++)
          				temp_string[i]=add_string[i];
        			temp_string[i]='\0';
        			add_string=(char *)malloc((string3_len+1)*sizeof(char));
        			add_string[0]='1';
        			add_string[1]=(((string1[0]-'0')+(temp[0]-'0')+carry)%10)+'0';
        			j=2;
        			for(i=1;i<string3_len;i++)
         				add_string[j++]=temp_string[i];
        			add_string[j]='\0';
      			}
        		free(temp);
    		}
    		else
    		{
            		j=string2_len-1;
            		char *temp=(char *)malloc((string2_len+1)*sizeof(char));
            		for(i=0;i<(string2_len-string1_len);i++)
            	 		temp[i]='0';
            		for(k=0;k<string1_len;k++)
             			temp[i++]=string1[k];
            		for(i=string2_len-1;i>0;i--)
            		{
              			str2digit=string2[i]-'0';
              			str1digit=temp[i]-'0';
              			digit=str1digit+str2digit+carry;
              			if(digit<=9)
              			{
                			add_string[j--]=digit+'0';
                			carry=0;
              			}
              			else
              			{
                			add_string[j--]=(digit%10)+'0';
                			carry=1;
              			}
            		}
            		digit=(string2[0]-'0')+(temp[0]-'0')+carry;
            		if(digit<=9)
            		{
              			add_string[0]=digit+'0';
              			add_string[string3_len]='\0';
            		}
            		else
            		{
              			for(i=0;i<string3_len;i++)
                			temp_string[i]=add_string[i];
              			temp_string[i]='\0';
              			add_string=(char *)malloc((string3_len+1)*sizeof(char));
              			add_string[0]='1';
              			add_string[1]=(((string2[0]-'0')+(temp[0]-'0')+carry)%10)+'0';
              			j=2;
              			for(i=1;i<string3_len;i++)
               				add_string[j++]=temp_string[i];
              			add_string[j]='\0';
            		}
         		free(temp);
    		}
  	}
	return (void *)add_string;
}

void* intal_decrement(void* intal)
{
  	if(intal==NULL)
   		return NULL;
  	char *string=(char *)intal;
  	int string_len=strlen(string);
  	if(string[0]=='0' && strlen(string)==1)
  	{
    		string=(char *)malloc(2*sizeof(char));
    		string[0]='0';
    		string[1]='\0';
  	}
  	else
 	{
  		int i,j;
  		int borrow=0;
  		int digit=string[string_len-1]-'0';
  		if(digit>0)
  		{
    			digit=digit-1;
    			string[string_len-1]=digit+'0';
  		}
  		else
  		{
    			borrow=1;
    			digit=9;
    			string[string_len-1]=digit+'0';
    			for(i=string_len-2;i>0;i--)
    			{
      				digit=string[i]-'0';
      				if(borrow==1)
    				{
      					if(digit!=0)
      					{
        					digit=digit-1;
        					string[i]=digit+'0';
        					borrow=0;
      					}
      					else
      					{
        					string[i]='9';
        					borrow=1;
      					}
    				}
  			}
    			if(string[0]=='1' &&  borrow==1)
    			{
      				char *temp=(char *)malloc(string_len*sizeof(char));
      				for(i=0;i<string_len;i++)
       					temp[i]=string[i];
      				char *string=(char *)malloc(string_len*sizeof(char));
       				string[0]='9';
       				j=1;
      				for(i=2;i<string_len;i++)
        				string[j++]=temp[i];
     	 			string[j]='\0';
     			 	return (void *)string;
    			}
    			else if(borrow==1 && string[0]!='1')
    			{
      				digit=string[0]-'0';
      				digit=digit-1;
      				string[0]=digit+'0';
    			}
  		}
	}
  	return (void *)string;
}

void* intal_diff(void *intal1,void *intal2)
{
	if(intal1==NULL || intal2==NULL)
   		return NULL;
  	char *max_string;
  	int l;
  	char *string1=(char *)intal1;
  	char *string2=(char *)intal2;
  	char *temp;
  	max_string=(intal_compare(intal1, intal2) > 0) ? intal2str(intal1) : intal2str(intal2);
  	if(strcmp(max_string,string1))
  	{
    		temp=string1;
    		string1=string2;
    		string2=temp;
  	}
  	char *string2_new;
  	int i,j;
  	j=strlen(string2)-1;
  	if(strlen(string1)!=strlen(string2))
  	{
    		string2_new=(char *)malloc((strlen(string1)+1)*sizeof(char));
    		string2_new[strlen(string1)+1]='\0';
    		for(i=strlen(string1)-1;i>=strlen(string1)-strlen(string2);i--)
    		{
      			string2_new[i]=string2[j];
      			j--;
    		}
    		for(;i>=0;i--)
    		{
      			string2_new[i]='0';
    		}
  	}
  	else
  	{
   		string2_new=(char *)malloc((strlen(string1)+1)*sizeof(char));
   		for(l=0;string2[l]!='\0';l++)
    			string2_new[l]=string2[l];
   		string2_new[l]='\0';
 	}
 	int digit1,digit2;
  	char *diff=(char *)malloc((strlen(string1)+1)*sizeof(char));
  	diff[strlen(string1)]='\0';
  	int borrow=0;
  	for(i=strlen(string1)-1;i>=0;i--)
  	{
    		digit1=string1[i]-'0';
    		digit2=string2_new[i]-'0';
    		if(digit1>=digit2)
    		{
      			digit1=digit1-borrow;
      			if(digit1>=digit2)
      			{
       				diff[i]=(digit1-digit2)+'0';
       				borrow=0;
      			}
      			else
      			{
        			digit1=digit1+borrow;
        			digit1=digit1+10-borrow;
        			diff[i]=(digit1-digit2)+'0';
        			borrow=1;
      			}
   		}
    		else
    		{
      			digit1=digit1+10-borrow;
      			diff[i]=(digit1-digit2)+'0';
      			borrow=1;
    		}
  	}
  	int len=strlen(diff);
  	if(diff[0]=='0' && len!=1)
  	{
    		for(i=1;i<len+1;i++)
     		diff[i-1]=diff[i];
  	}
  	free(string2_new);
  	return (void *)diff;
}

void* intal_multiply(void* intal1, void* intal2)
{
  	if(intal1==NULL || intal2==NULL)
   		return NULL;
  	char *string1=(char *)intal1;
  	char *string2=(char *)intal2;
  	int string1_len=strlen(string1);
  	int string2_len=strlen(string2);
  	int i;
  	int flag=0;
  	char *temp=(char *)malloc(sizeof(char)*(string1_len+2));
  	for(i=0;i<=string1_len+1;i++)
   		temp[i]='0';
  	temp[string1_len+1]='\0';
  	int count=0;
  	int j;
  	int digit1,digit2;
  	int carry=0;
  	int temp_res;
  	int k;
    	carry=0;
    	digit2=string2[string2_len-1]-'0';
    	k=string1_len;
    	for(j=string1_len-1;j>0;j--)
    	{
      		digit1=string1[j]-'0';
      		temp_res=digit1*digit2+carry;
      		if(temp_res>9)
      		{
        		carry=temp_res/10;
        		temp_res=temp_res%10;
      		}
      		else
        		carry=0;
      		temp[k--]=temp_res+'0';
    	}
    	digit1=string1[0]-'0';
    	temp_res=digit1*digit2+carry;
    	if(temp_res>9)
    	{
      		carry=temp_res/10;
      		temp_res=temp_res%10;
      		temp[k--]=temp_res+'0';
      		temp[k--]=carry+'0';
    	}
    	else
    		temp[k--]=temp_res+'0';
    	char *temp2;
    	count=1;
    	char *add_char;
    	add_char=temp;
	for(i=string2_len-2;i>=0;i--)
	{
  		digit2=string2[i]-'0';
  		carry=0;
  		temp2=(char *)malloc(sizeof(char)*(string1_len+2+count));
  		for(j=0;j<=string1_len+1+count;j++)
   			temp2[j]='0';
  		temp2[string1_len+1+count]='\0';
  		k=string1_len+count;
  		j=count;
  		for(;j>0;j--)
   			temp2[k--]='0';
  		for(j=string1_len-1;j>0;j--)
  		{
    			digit1=string1[j]-'0';
    			temp_res=digit1*digit2+carry;
    			if(temp_res>9)
    			{
      				carry=temp_res/10;
      				temp_res=temp_res%10;
    			}
    			else
      				carry=0;
    			temp2[k--]=temp_res+'0';
  		}
  		digit1=string1[0]-'0';
  		temp_res=digit1*digit2+carry;
  		if(temp_res>9)
  		{
    			carry=temp_res/10;
    			temp_res=temp_res%10;
    			temp2[k--]=temp_res+'0';
    			temp2[k--]=carry+'0';
  		}
  		else
    			temp2[k--]=temp_res+'0';
  		count++;
  		if(flag==0)
  		{
    			add_char=(char *)intal_add((void *)temp,(void *)temp2);
    			flag=1;
  		}
  		else
    			add_char=(char *)intal_add((void *)add_char,(void *)temp2);
	}
	if(add_char[0]=='0' && strlen(add_char)!=1)
	{
  		for(i=1;i<strlen(add_char)+1;i++)
   			add_char[i-1]=add_char[i];
	}
	free(temp);
	free(temp2);
	return (void *)add_char;
}

void* intal_pow(void* intal1, void* intal2)
{
  	if(intal1==NULL || intal2==NULL)
      		return NULL;
  	char *string1=(char *)intal1;
  	char *string2=(char *)intal2;
  	char *string2_temp=(char *)malloc((strlen(string2)+1)*sizeof(char));
  	strcpy(string2_temp,string2);
  	char *product;
  	if(string1[0]=='0' && string2[0]=='0')
  	{
   		product=(char *)malloc(2*sizeof(char));
   		product[0]='0';
   		product[1]='\0';
  	}
  	else if(string2_temp[0]-'0'==0)
  	{
    		product=(char *)malloc(2*sizeof(char));
    		product[0]='1';
    		product[1]='\0';
  	}
  	else
  	{
    		product=(char *)malloc(2*sizeof(char));
    		product[0]='1';
    		product[1]='\0';
    		while(!(string2_temp[0]=='0' && strlen(string2_temp)==1))
    		{
      			product=(char *)intal_multiply((void *)product,(void *)string1);
      			string2_temp=(char *)intal_decrement((void *)string2_temp);
    		}
  	}
  	return (void *)product;
}

void* intal_divide(void* intal1,void* intal2)
{
    	if(intal1==NULL || intal2==NULL)
        	return NULL;
    	if(intal_compare(intal2,intal_create("0"))==0)
        	return NULL;
    	if(intal_compare(intal1,intal2)==-1)
        	return intal_create("0");
    	char* no1=intal2str(rem_zero(intal1));
    	char* no2=intal2str(rem_zero(intal2));
    	int l1=strlen(no1);
    	int l2=strlen(no2);
    	char* rem=(char*)malloc(sizeof(char)*(l2+1));
    	char* quo=(char*)malloc(sizeof(char)*(l1));
    	int i,k=0;
    	for(i=0;i<l2;i++)
        	rem[i]=no1[i];
    	int len,cnt;
    	while(i<=l1)
    	{
        	rem=compute_multiplier(rem,intal2,&cnt);
        	quo[k++]=cnt+48;
        	len=strlen(rem);
        	rem[len]=no1[i++];
        	rem[len+1]='\0';
     	}
     	quo[k]='\0';
     	return rem_zero((void*)(quo));
}

void* rem_zero(void* intal1)
{
    	char* str=intal2str(intal1);
    	char *p = str;
    	while (*(p+1) && (*p == '0'))
        	p++;
    	void* intal2=(void*)p;
    	return intal2;
}


