#include <stdlib.h>
#include <dlfcn.h>
typedef void function_t(int i);
int main(int argc, char const *argv[])
{
        void *libfunctions;
        function_t *func1;
        libfunctions = dlopen("/tmp/libfunctions.so", RTLD_NOW);
        func1 = dlsym(libfunctions, "ICQ_Process_1");
        func1(999); // I am ICQ_Process_1
        dlclose(libfunctions);
        return EXIT_SUCCESS;
}
