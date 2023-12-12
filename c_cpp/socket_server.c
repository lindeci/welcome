#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>

#include <errno.h>


int
main(void){
        char send_message[255] = "hello i am server";
        int server_sock = socket(AF_INET, SOCK_STREAM, 0);

        // address
        struct sockaddr_in server_addr;
        server_addr.sin_addr.s_addr = INADDR_ANY;
        server_addr.sin_port = htons(9001);
        server_addr.sin_family = AF_INET; 

        //bind
        if ( (bind(server_sock, (struct sockaddr*) &server_addr, sizeof(server_addr))) != 0 ){
                fprintf(stderr, "couldn't bind: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
        }

        //listen
        if ((listen(server_sock, 10)) != 0){
                fprintf(stderr, "couldn't listen: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
        }

        int client_sock;
        //accept
        if( (client_sock = accept(server_sock, NULL, NULL)) == -1 ){
                fprintf(stderr, "couldn't accept: %s\n", strerror(errno));
                exit(EXIT_FAILURE);
        }

        send(client_sock, send_message, sizeof(send_message), 0);

        close(server_sock);
        close(client_sock);
}