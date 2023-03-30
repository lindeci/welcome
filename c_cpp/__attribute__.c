
#include <stdio.h>


struct my_packed_struct
{
     char c;
     int i;
}__attribute__ ((__packed__));

struct my_packed_struct_2
{
     char c;
     int i;
};

struct student
{
    char name[7];       //8个字节
    int id;     //4个字节
    char subject[5];       //8个字节
} __attribute__ ((aligned(4))); 

int main()
{
    printf("sizeof my_packed_struct   :  %ld\n",sizeof(struct my_packed_struct));
    printf("sizeof my_packed_struct_2 :  %ld\n",sizeof(struct my_packed_struct_2));
    printf("sizeof student            :  %ld\n",sizeof(struct student));
    return 0;
}