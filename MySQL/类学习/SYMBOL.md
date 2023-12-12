```cpp
struct SYMBOL {
  const char *name;
  const unsigned int length;
  const unsigned int tok;
  /** group mask, see SYM_GROUP enum for bits. */
  int group;
};

static const SYMBOL symbols[] = {
    /*
     Insert new SQL keywords after that commentary (by alphabetical order):
    */
    {SYM("&&", AND_AND_SYM)},
    {SYM("<", LT)},
    {SYM("<=", LE)},
    {SYM("<>", NE)},
    ……
}
```