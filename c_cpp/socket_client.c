#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#include <netinet/in.h>

#include <errno.h>

int main(void){
        //create sock
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if(sock < 0){
                fprintf(stderr, "can't create socket because of %s\n", strerror(errno));
                exit(EXIT_FAILURE);
        }

        //create address
        struct sockaddr_in server_addr;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(9001);
        server_addr.sin_family = AF_INET;

        //connect
        if( (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr))) == -1  ){
                perror("connect error because of: ");
                close(sock);
                exit(EXIT_FAILURE);

        }

        //create recv buffer and recv
        char recv_buffer[255];
        recv(sock, recv_buffer, sizeof(recv_buffer), 0);

        //print
        printf("printf recv: %s\n", recv_buffer);

        close(sock);
        return 0;
}