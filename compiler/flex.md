- [官网](#官网)
- [代码文件格式](#代码文件格式)
  - [Format of the Definitions Section](#format-of-the-definitions-section)
  - [Format of the Rules Section](#format-of-the-rules-section)
  - [Format of the User Code Section](#format-of-the-user-code-section)
  - [Comments in the Input](#comments-in-the-input)
- [Patterns 介绍](#patterns-介绍)
- [How the Input Is Matched](#how-the-input-is-matched)
- [Actions](#actions)
- [The Generated Scanner](#the-generated-scanner)
- [Start Conditions](#start-conditions)
- [Multiple Input Buffers](#multiple-input-buffers)
- [Miscellaneous Macros](#miscellaneous-macros)
- [Values Available To the User](#values-available-to-the-user)
- [Interfacing with Yacc](#interfacing-with-yacc)
- [Scanner Options](#scanner-options)
- [Performance Considerations](#performance-considerations)
- [Generating C++ Scanners](#generating-c-scanners)
- [Reentrant C Scanners](#reentrant-c-scanners)
  - [Reentrant Example](#reentrant-example)
- [Incompatibilities with Lex and Posix](#incompatibilities-with-lex-and-posix)
- [Memory Management](#memory-management)
- [Serialized Tables](#serialized-tables)
- [Diagnostics](#diagnostics)
- [Limitations](#limitations)
- [Additional Reading](#additional-reading)
- [正则表达式](#正则表达式)
  - [转义符](#转义符)
  - [贪婪、懒惰匹配](#贪婪懒惰匹配)
  - [最后一行的约束](#最后一行的约束)
- [token 编写顺序](#token-编写顺序)
- [yytext 和 yylval 结构体](#yytext-和-yylval-结构体)
- [关键字](#关键字)

# 官网
https://github.com/westes/flex

其它格式：https://westes.github.io/flex/manual/index.html#SEC_Contents
# 代码文件格式
```
definitions
%%
rules
%%
user code
```
## Format of the Definitions Section
name definition:  
The ‘name’ is a word beginning with a letter or an underscore (‘_’) followed by zero or more letters, digits, ‘_’, or ‘-’ (dash). The definition is taken to begin at the first non-whitespace character following the name and continuing to the end of the line. The definition can subsequently be referred to using ‘{name}’, which will expand to ‘(definition)’.

Any indented text or text enclosed in ‘%{’ and ‘%}’ is also copied verbatim to the output (with the %{ and %} symbols removed). The %{ and %} symbols must appear unindented on lines by themselves. 
## Format of the Rules Section
```
pattern   action
```
the pattern must be `unindented` and the action must begin on the same line.
## Format of the User Code Section
The user code section is simply copied to lex.yy.c verbatim.
## Comments in the Input
All the comments in the following example are valid:
```c
%{
/* code block */
%}

/* Definitions Section */
%x STATE_X

%%
    /* Rules Section */
ruleA   /* after regex */ { /* code block */ } /* after code block */
        /* Rules Section (indented) */
<STATE_X>{
ruleC   ECHO;
ruleD   ECHO;
%{
/* code block */
%}
}
%%
/* User Code Section */
```
# Patterns 介绍
The patterns in the input (see Rules Section) are written using an extended set of regular expressions. These are:
- ‘x’

    match the character ’x’
-  ‘.’

    any character (byte) except newline
- ‘[xyz]’

    a character class; in this case, the pattern matches either an ’x’, a ’y’, or a ’z’
- ‘[abj-oZ]’

    a "character class" with a range in it; matches an ’a’, a ’b’, any letter from ’j’ through ’o’, or a ’Z’
- ‘[^A-Z]’

    a "negated character class", i.e., any character but those in the class. In this case, any character EXCEPT an uppercase letter.
- ‘[^A-Z\n]’

    any character EXCEPT an uppercase letter or a newline
- ‘[a-z]{-}[aeiou]’

    the lowercase consonants
- ‘r*’

    zero or more r’s, where r is any regular expression
- ‘r+’

    one or more r’s
- ‘r?’

    zero or one r’s (that is, “an optional r”)
- ‘r{2,5}’

    anywhere from two to five r’s
- ‘r{2,}’

    two or more r’s
- ‘r{4}’

    exactly 4 r’s
- ‘{name}’

    the expansion of the ‘name’ definition (see Format).
- ‘"[xyz]\"foo"’

    the literal string: ‘[xyz]"foo’
- **`‘\X’`**

    if X is ‘a’, ‘b’, ‘f’, ‘n’, ‘r’, ‘t’, or ‘v’, then the ANSI-C interpretation of ‘\x’. Otherwise, a literal ‘X’ (used to escape operators such as ‘*’)
- ‘\0’

    a NUL character (ASCII code 0)
- ‘\123’

    the character with octal value 123
- ‘\x2a’

    the character with hexadecimal value 2a
- ‘(r)’

    match an ‘r’; parentheses are used to override precedence (see below)
- ‘(?r-s:pattern)’

    apply option ‘r’ and omit option ‘s’ while interpreting pattern. Options may be zero or more of the characters ‘i’, ‘s’, or ‘x’.

    ‘i’ means case-insensitive. ‘-i’ means case-sensitive.

    ‘s’ alters the meaning of the ‘.’ syntax to match any single byte whatsoever. ‘-s’ alters the meaning of ‘.’ to match any byte except ‘\n’.

    ‘x’ ignores comments and whitespace in patterns. Whitespace is ignored unless it is backslash-escaped, contained within ‘""’s, or appears inside a character class.

    The following are all valid:

    (?:foo)         same as  (foo)
    (?i:ab7)        same as  ([aA][bB]7)
    (?-i:ab)        same as  (ab)
    (?s:.)          same as  [\x00-\xFF]
    (?-s:.)         same as  [^\n]
    (?ix-s: a . b)  same as  ([Aa][^\n][bB])
    (?x:a  b)       same as  ("ab")
    (?x:a\ b)       same as  ("a b")
    (?x:a" "b)      same as  ("a b")
    (?x:a[ ]b)      same as  ("a b")
    (?x:a
        /* comment */
        b
        c)          same as  (abc)

- ‘(?# comment )’

    omit everything within ‘()’. The first ‘)’ character encountered ends the pattern. It is not possible to for the comment to contain a ‘)’ character. The comment may span lines.
- ‘rs’

    the regular expression ‘r’ followed by the regular expression ‘s’; called concatenation
- ‘r|s’

    either an ‘r’ or an ‘s’
- ‘r/s’

    an ‘r’ but only if it is followed by an ‘s’. The text matched by ‘s’ is included when determining whether this rule is the longest match, but is then returned to the input before the action is executed. So the action only sees the text matched by ‘r’. This type of pattern is called trailing context. (There are some combinations of ‘r/s’ that flex cannot match correctly. See Limitations, regarding dangerous trailing context.)
- ‘^r’

    an ‘r’, but only at the beginning of a line (i.e., when just starting to scan, or right after a newline has been scanned).
- ‘r$’

    an ‘r’, but only at the end of a line (i.e., just before a newline). Equivalent to ‘r/\n’.

    Note that flex’s notion of “newline” is exactly whatever the C compiler used to compile flex interprets ‘\n’ as; in particular, on some DOS systems you must either filter out ‘\r’s in the input yourself, or explicitly use ‘r/\r\n’ for ‘r$’.
- `‘<s>r’**`

    an ‘r’, but only in start condition s (see Start Conditions for discussion of start conditions).
- ‘<s1,s2,s3>r’

    same, but in any of start conditions s1, s2, or s3.
- ‘<*>r’

    an ‘r’ in any start condition, even an exclusive one.
- `‘<<EOF>>’`

    an end-of-file.
- `‘<s1,s2><<EOF>>’`

    an end-of-file when in start condition s1 or s2 

**`Note that inside of a character class, all regular expression operators lose their special meaning except escape (‘\’) and the character class operators, ‘-’, ‘]]’, and, at the beginning of the class, ‘^’. `**

The regular expressions listed above are grouped according to precedence, from highest precedence at the top to lowest at the bottom. Those grouped together have equal precedence (see special note on the precedence of the repeat operator, ‘{}’, under the documentation for the ‘--posix’ POSIX compliance option). For example,
```
    foo|bar*
```
is the same as
```
    (foo)|(ba(r*))
```
**`since the ‘*’ operator has higher precedence than concatenation, and concatenation higher than alternation (‘|’).`** This pattern therefore matches either the string ‘foo’ or the string ‘ba’ followed by zero-or-more ‘r’’s. To match ‘foo’ or zero-or-more repetitions of the string ‘bar’, use:
```
    foo|(bar)*
```
In addition to characters and ranges of characters, character classes can also contain character class expressions. These are expressions enclosed inside ‘[:’ and ‘:]’ delimiters (which themselves must appear between the ‘[’ and ‘]’ of the character class. Other elements may occur inside the character class, too). The valid expressions are:
```
    [:alnum:] [:alpha:] [:blank:]
    [:cntrl:] [:digit:] [:graph:]
    [:lower:] [:print:] [:punct:]
    [:space:] [:upper:] [:xdigit:]
```
These expressions all designate a set of characters equivalent to the corresponding standard C isXXX function. For example, ‘[:alnum:]’ designates those characters for which isalnum() returns true - i.e., any alphabetic or numeric character. Some systems don’t provide isblank(), so flex defines ‘[:blank:]’ as a blank or a tab.

For example, the following character classes are all equivalent:
```
    [[:alnum:]]
    [[:alpha:][:digit:]]
    [[:alpha:][0-9]]
    [a-zA-Z0-9]
```
A word of caution. Character classes are expanded immediately when seen in the flex input. This means the character classes are sensitive to the locale in which flex is executed, and the resulting scanner will not be sensitive to the runtime locale. This may or may not be desirable.
```
1.    If your scanner is case-insensitive (the ‘-i’ flag), then ‘[:upper:]’ and ‘[:lower:]’ are equivalent to ‘[:alpha:]’.
2.    Character classes with ranges, such as ‘[a-Z]’, should be used with caution in a case-insensitive scanner if the range spans upper or lowercase characters. Flex does not know if you want to fold all upper and lowercase characters together, or if you want the literal numeric range specified (with no case folding). When in doubt, flex will assume that you meant the literal numeric range, and will issue a warning. The exception to this rule is a character range such as ‘[a-z]’ or ‘[S-W]’ where it is obvious that you want case-folding to occur. Here are some examples with the ‘-i’ flag enabled:
    Range	Result	Literal Range	Alternate Range
    ‘[a-t]’	ok	‘[a-tA-T]’	
    ‘[A-T]’	ok	‘[a-tA-T]’	
    ‘[A-t]’	ambiguous	‘[A-Z\[\\\]_`a-t]’	‘[a-tA-T]’
    ‘[_-{]’	ambiguous	‘[_`a-z{]’	‘[_`a-zA-Z{]’
    ‘[@-C]’	ambiguous	‘[@ABC]’	‘[@A-Z\[\\\]_`abc]’
3.    A negated character class such as the example ‘[^A-Z]’ above will match a newline unless ‘\n’ (or an equivalent escape sequence) is one of the characters explicitly present in the negated character class (e.g., ‘[^A-Z\n]’). This is unlike how many other regular expression tools treat negated character classes, but unfortunately the inconsistency is historically entrenched. Matching newlines means that a pattern like ‘[^"]*’ can match the entire input unless there’s another quote in the input.

    Flex allows negation of character class expressions by prepending ‘^’ to the POSIX character class name.

        [:^alnum:] [:^alpha:] [:^blank:]
        [:^cntrl:] [:^digit:] [:^graph:]
        [:^lower:] [:^print:] [:^punct:]
        [:^space:] [:^upper:] [:^xdigit:]

    Flex will issue a warning if the expressions ‘[:^upper:]’ and ‘[:^lower:]’ appear in a case-insensitive scanner, since their meaning is unclear. The current behavior is to skip them entirely, but this may change without notice in future revisions of flex.
4.    The ‘{-}’ operator computes the difference of two character classes. For example, ‘[a-c]{-}[b-z]’ represents all the characters in the class ‘[a-c]’ that are not in the class ‘[b-z]’ (which in this case, is just the single character ‘a’). The ‘{-}’ operator is left associative, so ‘[abc]{-}[b]{-}[c]’ is the same as ‘[a]’. Be careful not to accidentally create an empty set, which will never match.
5.    The ‘{+}’ operator computes the union of two character classes. For example, ‘[a-z]{+}[0-9]’ is the same as ‘[a-z0-9]’. This operator is useful when preceded by the result of a difference operation, as in, ‘[[:alpha:]]{-}[[:lower:]]{+}[q]’, which is equivalent to ‘[A-Zq]’ in the "C" locale.
6.    A rule can have at most one instance of trailing context (the ‘/’ operator or the ‘$’ operator). The start condition, ‘^’, and ‘<<EOF>>’ patterns can only occur at the beginning of a pattern, and, as well as with ‘/’ and ‘$’, cannot be grouped inside parentheses. A ‘^’ which does not occur at the beginning of a rule or a ‘$’ which does not occur at the end of a rule loses its special properties and is treated as a normal character.
7.    The following are invalid:

        foo/bar$
        <sc1>foo<sc2>bar

    Note that the first of these can be written ‘foo/bar\n’.
8.    The following will result in ‘$’ or ‘^’ being treated as a normal character:

        foo|(bar$)
        foo|^bar

    If the desired meaning is a ‘foo’ or a ‘bar’-followed-by-a-newline, the following could be used (the special | action is explained below, see Actions):

        foo      |
        bar$     /* action goes here */

    A similar trick will work for matching a ‘foo’ or a ‘bar’-at-the-beginning-of-a-line. 
```

# How the Input Is Matched
Once the match is determined, the text corresponding to the match (called the token) is made available in the global character pointer `yytext`, and its length in the global integer `yyleng`. The action corresponding to the matched pattern is then executed (see Actions), and then the remaining input is scanned for another match. 

# Actions
If the action contains a ‘{’, then the action spans till the balancing ‘}’ is found, and the action may cross multiple lines. 

An action consisting solely of a vertical bar (‘|’) means “same as the action for the next rule”.

Actions can include arbitrary C code, including return statements to return a value to whatever routine called yylex(). Each time yylex() is called it continues processing tokens from where it last left off until it either reaches the end of the file or executes a return. 

There are a number of special directives which can be included within an action:

- ECHO

    copies yytext to the scanner’s output.
- BEGIN

    followed by the name of a start condition places the scanner in the corresponding start condition (see below).
- REJECT
- 
    Without the REJECT, any occurrences of ‘frob’ in the input would not be counted as words, since the scanner normally executes only one action per token. Multiple uses of REJECT are allowed, each one finding the next best choice to the currently active rule. For example, when the following scanner scans the token ‘abcd’, it will write ‘abcdabcaba’ to the output:
```
    %%
    a        |
    ab       |
    abc      |
    abcd     ECHO; REJECT;
    .|\n     /* eat up any unmatched character */
```
- yymore()

    tells the scanner that the next time it matches a rule, the corresponding token should be appended onto the current value of yytext rather than replacing it. For example, given the input ‘mega-kludge’ the following will write ‘mega-mega-kludge’ to the output:
```
        %%
        mega-    ECHO; yymore();
        kludge   ECHO;
```
First ‘mega-’ is matched and echoed to the output. Then ‘kludge’ is matched, but the previous ‘mega-’ is still hanging around at the beginning of yytext so the ECHO for the ‘kludge’ rule will actually write ‘mega-kludge’. 

Two notes regarding use of yymore(). First, yymore() depends on the value of yyleng correctly reflecting the size of the current token, so you must not modify yyleng if you are using yymore(). Second, the presence of yymore() in the scanner’s action entails a minor performance penalty in the scanner’s matching speed. 

- yyless(n) 

returns all but the first n characters of the current token back to the input stream, where they will be rescanned when the scanner looks for the next match. yytext and yyleng are adjusted appropriately (e.g., yyleng will now be equal to n). For example, on the input ‘foobar’ the following will write out ‘foobarbar’:
```
    %%
    foobar    ECHO; yyless(3);
    [a-z]+    ECHO;
```
- unput(c)

puts the character c back onto the input stream. It will be the next character scanned. The following action will take the current token and cause it to be rescanned enclosed in parentheses.

    {
    int i;
    /* Copy yytext because unput() trashes yytext */
    char *yycopy = strdup( yytext );
    unput( ')' );
    for ( i = yyleng - 1; i >= 0; --i )
        unput( yycopy[i] );
    unput( '(' );
    free( yycopy );
    }
- input()

reads the next character from the input stream. 
- YY_FLUSH_BUFFER; 

flushes the scanner’s internal buffer so that the next time the scanner attempts to match a token, it will first refill the buffer using YY_INPUT() (see Generated Scanner). 
- yyterminate()

can be used in lieu of a return statement in an action. It terminates the scanner and returns a 0 to the scanner’s caller, indicating “all done”. By default, yyterminate() is also called when an end-of-file is encountered. It is a macro and may be redefined. 

# The Generated Scanner
Whenever yylex() is called, it scans tokens from the global input file yyin (which defaults to stdin). It continues until it either reaches an end-of-file (at which point it returns the value 0) or one of its actions executes a return statement. 

If the scanner reaches an end-of-file, subsequent calls are undefined unless either yyin is pointed at a new input file (in which case scanning continues from that file), or yyrestart() is called. yyrestart() takes one argument, a FILE * pointer (which can be NULL, if you’ve set up YY_INPUT to scan from a source other than yyin), and initializes yyin for scanning from that file. Essentially there is no difference between just assigning yyin to a new input file or using yyrestart() to do so; the latter is available for compatibility with previous versions of flex, and because it can be used to switch input files in the middle of scanning. It can also be used to throw away the current input buffer, by calling it with an argument of yyin; but it would be better to use YY_FLUSH_BUFFER (see Actions). Note that yyrestart() does not reset the start condition to INITIAL (see Start Conditions). 

By default (and for purposes of efficiency), the scanner uses block-reads rather than simple getc() calls to read characters from yyin. The nature of how it gets its input can be controlled by defining the YY_INPUT macro. The calling sequence for YY_INPUT() is YY_INPUT(buf,result,max_size). Its action is to place up to max_size characters in the character array buf and return in the integer variable result either the number of characters read or the constant YY_NULL (0 on Unix systems) to indicate ‘EOF’. The default YY_INPUT reads from the global file-pointer yyin. 
```c
    %{
    #define YY_INPUT(buf,result,max_size) \
        { \
        int c = getchar(); \
        result = (c == EOF) ? YY_NULL : (buf[0] = c, 1); \
        }
    %}
```
This definition will change the input processing to occur one character at a time.

When the scanner receives an end-of-file indication from YY_INPUT, it then checks the yywrap() function. If yywrap() returns false (zero), then it is assumed that the function has gone ahead and set up yyin to point to another input file, and scanning continues. If it returns true (non-zero), then the scanner terminates, returning 0 to its caller. Note that in either case, the start condition remains unchanged; it does not revert to INITIAL.

If you do not supply your own version of yywrap(), then you must either use %option noyywrap (in which case the scanner behaves as though yywrap() returned 1), or you must link with ‘-lfl’ to obtain the default version of the routine, which always returns 1. 

# Start Conditions
Start conditions are declared in the definitions (first) section of the input using unindented lines beginning with either ‘%s’ or ‘%x’ followed by a list of names.

The default rule (to ECHO any unmatched character) remains active in start conditions. It is equivalent to:
```
    <*>.|\n     ECHO;
```
BEGIN(0) returns to the original state where only the rules with no start conditions are active. This state can also be referred to as the start-condition INITIAL, so BEGIN(INITIAL) is equivalent to BEGIN(0). 

Here is a scanner which recognizes (and discards) C comments while maintaining a count of the current input line.
```
    %x comment
    %%
            int line_num = 1;

    "/*"         BEGIN(comment);

    <comment>[^*\n]*        /* eat anything that's not a '*' */
    <comment>"*"+[^*/\n]*   /* eat up '*'s not followed by '/'s */
    <comment>\n             ++line_num;
    <comment>"*"+"/"        BEGIN(INITIAL);
```

```
    <ESC>{
        "\\n"   return '\n';
        "\\r"   return '\r';
        "\\f"   return '\f';
        "\\0"   return '\0';
    }
```
is equivalent to:
```
    <ESC>"\\n"  return '\n';
    <ESC>"\\r"  return '\r';
    <ESC>"\\f"  return '\f';
    <ESC>"\\0"  return '\0';
```

# Multiple Input Buffers
flex provides a mechanism for creating and switching between multiple input buffers. An input buffer is created by using:

Function: `YY_BUFFER_STATE yy_create_buffer ( FILE *file, int size )`

which takes a FILE pointer and a size and creates a buffer associated with the given file and large enough to hold size characters (when in doubt, use YY_BUF_SIZE for the size). It returns a YY_BUFFER_STATE handle, which may then be passed to other routines (see below). The YY_BUFFER_STATE type is a pointer to an opaque struct yy_buffer_state structure, so you may safely initialize YY_BUFFER_STATE variables to ((YY_BUFFER_STATE) 0) if you wish, and also refer to the opaque structure in order to correctly declare input buffers in source files other than that of your scanner. Note that the FILE pointer in the call to yy_create_buffer is only used as the value of yyin seen by YY_INPUT. If you redefine YY_INPUT() so it no longer uses yyin, then you can safely pass a NULL FILE pointer to yy_create_buffer. You select a particular buffer to scan from using: 

Function: `void yy_switch_to_buffer ( YY_BUFFER_STATE new_buffer )`

The above function switches the scanner’s input buffer so subsequent tokens will come from new_buffer. Note that yy_switch_to_buffer() may be used by yywrap() to set things up for continued scanning, instead of opening a new file and pointing yyin at it. If you are looking for a stack of input buffers, then you want to use yypush_buffer_state() instead of this function. Note also that switching input sources via either yy_switch_to_buffer() or yywrap() does not change the start condition.

Function: `void yy_delete_buffer ( YY_BUFFER_STATE buffer )`

is used to reclaim the storage associated with a buffer. (buffer can be NULL, in which case the routine does nothing.) You can also clear the current contents of a buffer using:

Function: `void yypush_buffer_state ( YY_BUFFER_STATE buffer )`

This function pushes the new buffer state onto an internal stack. The pushed state becomes the new current state. The stack is maintained by flex and will grow as required. This function is intended to be used instead of yy_switch_to_buffer, when you want to change states, but preserve the current state for later use.

Function: `void yypop_buffer_state ( )`

This function removes the current state from the top of the stack, and deletes it by calling yy_delete_buffer. The next state on the stack, if any, becomes the new current state.

Function: `void yy_flush_buffer ( YY_BUFFER_STATE buffer )`

This function discards the buffer’s contents, so the next time the scanner attempts to match a token from the buffer, it will first fill the buffer anew using YY_INPUT().

Function: `YY_BUFFER_STATE yy_new_buffer ( FILE *file, int size )`

is an alias for yy_create_buffer(), provided for compatibility with the C++ use of new and delete for creating and destroying dynamic objects. 
```c
/* the "incl" state is used for picking up the name
     * of an include file
     */
    %x incl

    %{
    #define MAX_INCLUDE_DEPTH 10
    YY_BUFFER_STATE include_stack[MAX_INCLUDE_DEPTH];
    int include_stack_ptr = 0;
    %}

    %%
    include             BEGIN(incl);

    [a-z]+              ECHO;
    [^a-z\n]*\n?        ECHO;

    <incl>[ \t]*      /* eat the whitespace */
    <incl>[^ \t\n]+   { /* got the include file name */
            if ( include_stack_ptr >= MAX_INCLUDE_DEPTH )
                {
                fprintf( stderr, "Includes nested too deeply" );
                exit( 1 );
                }

            include_stack[include_stack_ptr++] =
                YY_CURRENT_BUFFER;

            yyin = fopen( yytext, "r" );

            if ( ! yyin )
                error( ... );

            yy_switch_to_buffer(
                yy_create_buffer( yyin, YY_BUF_SIZE ) );

            BEGIN(INITIAL);
            }

    <<EOF>> {
            if ( --include_stack_ptr  0 )
                {
                yyterminate();
                }

            else
                {
                yy_delete_buffer( YY_CURRENT_BUFFER );
                yy_switch_to_buffer(
                     include_stack[include_stack_ptr] );
                }
            }
```
Function: `YY_BUFFER_STATE yy_scan_string ( const char *str )`

    scans a NUL-terminated string. 

Function: `YY_BUFFER_STATE yy_scan_bytes ( const char *bytes, int len )`

    scans len bytes (including possibly NULs) starting at location bytes. 

Note that both of these functions create and scan a copy of the string or bytes. (This may be desirable, since yylex() modifies the contents of the buffer it is scanning.) You can avoid the copy by using:

Function: `YY_BUFFER_STATE yy_scan_buffer (char *base, yy_size_t size)`

    which scans in place the buffer starting at base, consisting of size bytes, the last two bytes of which must be YY_END_OF_BUFFER_CHAR (ASCII NUL). These last two bytes are not scanned; thus, scanning consists of base[0] through base[size-2], inclusive. 

If you fail to set up base in this manner (i.e., forget the final two YY_END_OF_BUFFER_CHAR bytes), then yy_scan_buffer() returns a NULL pointer instead of creating a new input buffer.

Data type: `yy_size_t`

    is an integral type to which you can cast an integer expression reflecting the size of the buffer. 

# Miscellaneous Macros

# Values Available To the User
This chapter summarizes the various values available to the user in the rule actions.

`char *yytext`

    holds the text of the current token. It may be modified but not lengthened (you cannot append characters to the end).

    If the special directive %array appears in the first section of the scanner description, then yytext is instead declared char yytext[YYLMAX], where YYLMAX is a macro definition that you can redefine in the first section if you don’t like the default value (generally 8KB). Using %array results in somewhat slower scanners, but the value of yytext becomes immune to calls to unput(), which potentially destroy its value when yytext is a character pointer. The opposite of %array is %pointer, which is the default.

    You cannot use %array when generating C++ scanner classes (the ‘-+’ flag).
`int yyleng`

    holds the length of the current token.
`FILE *yyin`

    is the file which by default flex reads from. It may be redefined but doing so only makes sense before scanning begins or after an EOF has been encountered. Changing it in the midst of scanning will have unexpected results since flex buffers its input; use yyrestart() instead. Once scanning terminates because an end-of-file has been seen, you can assign yyin at the new input file and then call the scanner again to continue scanning.
`void yyrestart( FILE *new_file )`

    may be called to point yyin at the new input file. The switch-over to the new file is immediate (any previously buffered-up input is lost). Note that calling yyrestart() with yyin as an argument thus throws away the current input buffer and continues scanning the same input file.
`FILE *yyout`

    is the file to which ECHO actions are done. It can be reassigned by the user.
`YY_CURRENT_BUFFER`

    returns a YY_BUFFER_STATE handle to the current buffer.
`YY_START`

    returns an integer value corresponding to the current start condition. You can subsequently use this value with BEGIN to return to that start condition. 

# Interfacing with Yacc
One of the main uses of flex is as a companion to the yacc parser-generator. yacc parsers expect to call a routine named yylex() to find the next input token. The routine is supposed to return the type of the next token as well as putting any associated value in the global yylval. To use flex with yacc, one specifies the ‘-d’ option to yacc to instruct it to generate the file y.tab.h containing definitions of all the %tokens appearing in the yacc input. This file is then included in the flex scanner. For example, if one of the tokens is TOK_NUMBER, part of the scanner might look like:

    %{
    #include "y.tab.h"
    %}

    %%

    [0-9]+        yylval = atoi( yytext ); return TOK_NUMBER;

# Scanner Options
The various flex options are categorized by function in the following menu. If you want to lookup a particular option by name, See Index of Scanner Options.
```
• Options for Specifying Filenames:	  	
• Options Affecting Scanner Behavior:	  	
• Code-Level And API Options:	  	
• Options for Scanner Speed and Size:	  	
• Debugging Options:	  	
• Miscellaneous Options:	  	
```
Even though there are many scanner options, a typical scanner might only specify the following options:
```
%option   8bit reentrant bison-bridge
%option   warn nodefault
%option   yylineno
%option   outfile="scanner.c" header-file="scanner.h"
```
The first line specifies the general type of scanner we want. The second line specifies that we are being careful. The third line asks flex to track line numbers. The last line tells flex what to name the files. (The options can be specified in any order. We just divided them.)

flex also provides a mechanism for controlling options within the scanner specification itself, rather than from the flex command-line. This is done by including %option directives in the first section of the scanner specification. You can specify multiple options with a single %option directive, and multiple directives in the first section of your flex input file.

Most options are given simply as names, optionally preceded by the word ‘no’ (with no intervening whitespace) to negate their meaning. The names are the same as their long-option equivalents (but without the leading ‘--’ ).

flex scans your rule actions to determine whether you use the REJECT or yymore() features. The REJECT and yymore options are available to override its decision as to whether you use the options, either by setting them (e.g., %option reject) to indicate the feature is indeed used, or unsetting them to indicate it actually is not used (e.g., %option noyymore).

A number of options are available for lint purists who want to suppress the appearance of unneeded routines in the generated scanner. Each of the following, if unset (e.g., %option nounput), results in the corresponding routine not appearing in the generated scanner:

    input, unput
    yy_push_state, yy_pop_state, yy_top_state
    yy_scan_buffer, yy_scan_bytes, yy_scan_string

    yyget_extra, yyset_extra, yyget_leng, yyget_text,
    yyget_lineno, yyset_lineno, yyget_in, yyset_in,
    yyget_out, yyset_out, yyget_lval, yyset_lval,
    yyget_lloc, yyset_lloc, yyget_debug, yyset_debug

(though yy_push_state() and friends won’t appear anyway unless you use %option stack). 

# Performance Considerations

# Generating C++ Scanners
**`IMPORTANT: the present form of the scanning class is experimental and may change considerably between major releases. `**

Here is an example of a simple C++ scanner:
```cpp
     // An example of using the flex C++ scanner class.

    %{
    #include <iostream>
    using namespace std;
    int mylineno = 0;
    %}

    %option noyywrap c++

    string  \"[^\n"]+\"

    ws      [ \t]+

    alpha   [A-Za-z]
    dig     [0-9]
    name    ({alpha}|{dig}|\$)({alpha}|{dig}|[_.\-/$])*
    num1    [-+]?{dig}+\.?([eE][-+]?{dig}+)?
    num2    [-+]?{dig}*\.{dig}+([eE][-+]?{dig}+)?
    number  {num1}|{num2}

    %%

    {ws}    /* skip blanks and tabs */

    "/*"    {
            int c;

            while((c = yyinput()) != 0)
                {
                if(c == '\n')
                    ++mylineno;

                else if(c == '*')
                    {
                    if((c = yyinput()) == '/')
                        break;
                    else
                        unput(c);
                    }
                }
            }

    {number}  cout << "number " << YYText() << '\n';

    \n        mylineno++;

    {name}    cout << "name " << YYText() << '\n';

    {string}  cout << "string " << YYText() << '\n';

    %%

	// This include is required if main() is an another source file.
	//#include <FlexLexer.h>

    int main( int /* argc */, char** /* argv */ )
    {
        FlexLexer* lexer = new yyFlexLexer;
        while(lexer->yylex() != 0)
            ;
        return 0;
    }
```
If you want to create multiple (different) lexer classes, you use the ‘-P’ flag (or the prefix= option) to rename each yyFlexLexer to some other ‘xxFlexLexer’. You then can include <FlexLexer.h> in your other sources once per lexer class, first renaming yyFlexLexer as follows:
```cpp
    #undef yyFlexLexer
    #define yyFlexLexer xxFlexLexer
    #include <FlexLexer.h>

    #undef yyFlexLexer
    #define yyFlexLexer zzFlexLexer
    #include <FlexLexer.h>
```
if, for example, you used %option prefix="xx" for one of your scanners and %option prefix="zz" for the other. 

# Reentrant C Scanners
flex has the ability to generate a reentrant C scanner. This is accomplished by specifying %option reentrant (‘-R’) The generated scanner is both portable, and safe to use in one or more separate threads of control. The most common use for reentrant scanners is from within multi-threaded applications. Any thread may create and execute a reentrant flex scanner without the need for synchronization with other threads. 

## Reentrant Example
First, an example of a reentrant scanner:
```c
    /* This scanner prints "//" comments. */

    %option reentrant stack noyywrap
    %x COMMENT

    %%

    "//"                 yy_push_state( COMMENT, yyscanner);
    .|\n

    <COMMENT>\n          yy_pop_state( yyscanner );
    <COMMENT>[^\n]+      fprintf( yyout, "%s\n", yytext);

    %%

    int main ( int argc, char * argv[] )
    {
        yyscan_t scanner;

        yylex_init ( &scanner );
        yylex ( scanner );
        yylex_destroy ( scanner );
    return 0;
   }
```

# Incompatibilities with Lex and Posix

# Memory Management

# Serialized Tables

# Diagnostics

# Limitations

# Additional Reading
You may wish to read more about the following programs:

- lex
- yacc
- sed
- awk 

The following books may contain material of interest:

John Levine, Tony Mason, and Doug Brown, Lex & Yacc, O’Reilly and Associates. Be sure to get the 2nd edition.

M. E. Lesk and E. Schmidt, LEX – Lexical Analyzer Generator

Alfred Aho, Ravi Sethi and Jeffrey Ullman, Compilers: Principles, Techniques and Tools, Addison-Wesley (1986). Describes the pattern-matching techniques used by flex (deterministic finite automata). 

# 正则表达式
Flex正则表达式是一种通用的标准。
- `.`：匹配除换行符"\n"外的任意单个字符。
- `*`：匹配前面的正则表达式零次或多次出现。
- `+`：匹配前面的正则表达式一次或多次出现。
- `?`：匹配前面的正则表达式零次或一次出现。
- `|`：匹配紧接在前面的表达式，或者紧跟在后面的表达式。
- `()`：把一系列的正则表达式组成一个新的正则表达式。
- `^`：非
- (?i:word) 表示word不区分大小写

在Flex正则表达式中，有一些特殊字符需要添加"\"才能匹配该字符本身，包括"^", "$", "()", "[]", "{}", ".", "?", "+", "*", "|"等。

此外，Flex正则表达式还有一些常用属性设置，如Ignorecase（使匹配时不区分大小写）、Singleline（使小数点可匹配包括换行符在内的所有字符）、Multiline（使"^"和"$"可以匹配每一行的开始和结束位置）和Global（替换所有的匹配）。
## 转义符
- `\\`：表示一个反斜线（`\`）。
- `\"`：表示一个双引号（`"`）。
- `\n`：表示一个换行符。
- `\t`：表示一个制表符（tab）。
- `\r`：表示一个回车符（carriage return）。
- `\b`：表示一个退格符（backspace）。
- \f：表示一个换页符（form feed）。
- \v：表示一个垂直制表符（vertical tab）。
- \a：表示一个响铃符（bell）。

你还可以使用八进制和十六进制来表示字符：

- \0：表示一个NUL字符（ASCII码为0）。
- \123：表示八进制值为123的字符。
- \x2a：表示十六进制值为2a的字符。

## 贪婪、懒惰匹配
在FLEX中，正则表达式默认是贪婪匹配的，也就是说它会尽可能多地匹配字符12。例如，如果你有一个模式.*，它会匹配尽可能多的任何字符。

然而，FLEX并不直接支持懒惰匹配（也称为非贪婪匹配），这意味着它会尽可能少地匹配字符1。在其他正则表达式引擎中，你可以通过在量词后面添加一个问号（?）来实现懒惰匹配，例如.*?2。但是在FLEX中，这种语法并不适用。

如果你需要在FLEX中实现类似懒惰匹配的效果，你可能需要使用更复杂的方法。例如，你可以使用开始条件（start conditions）来显式地指定状态机1，或者直接读取字符来手动输入1。
```c
%x COMMENT
%%
"/*"          { BEGIN(COMMENT); }
<COMMENT>"*/" { BEGIN(INITIAL); }
<COMMENT>.    { /* 忽略注释中的字符 */ }
```
## 最后一行的约束
需要这么写
```
<REPLACE,NO_REPLACE>. {
    strcat(abs_sql,yytext);
    }
```
不能这么写,因为这里的贪婪会忽视前面的匹配规则
```
<REPLACE,NO_REPLACE>.* {
    strcat(abs_sql,yytext);
    }
```
# token 编写顺序
在FLEX的.l文件中，对TOKEN的编写顺序确实有一些要求。FLEX在匹配输入时，会按照以下规则进行：

1. **最长匹配规则**：FLEX总是尝试找到能够匹配最长字符串的规则。例如，如果你有两个规则，一个是`"abc"`，另一个是`"abcd"`，那么对于输入`"abcd"`，FLEX会选择`"abcd"`这个规则。

2. **先定义优先规则**：如果有两个或更多的规则可以匹配相同长度的字符串，那么FLEX会选择在.l文件中最先定义的那个规则。例如，如果你有两个规则，一个是`"abc"`，另一个是`"a[bc]*"`，那么对于输入`"abc"`，尽管这两个规则都可以匹配，但FLEX会选择`"abc"`这个规则，因为它在文件中出现得更早。

# yytext 和 yylval 结构体
在Flex中，`yytext`和`yylval`是两个非常重要的变量。

- `yytext`：这是一个C风格的字符串（char *），包含当前匹配的字符。例如，如果`yylex()`读取到的标记是一个整数，那么`yytext`就包含组成该整数的数字字符串。

- `yylval`：这是一个联合体（union），用于存储语义值。在默认情况下，`yylval`被声明为int类型，但可以通过某些方式更改此默认设置。例如，如果你在.y文件中想要为int、float和string类型提供基本支持，你可以这样定义联合体：
  ```c
  %union  
  {  
    int intValue;  
    float floatValue;  
    char *stringValue;  
  }
  ```
# 关键字

- `INITIAL`：这是FLEX中的默认开始状态。当你的词法分析器开始运行时，它会处于`INITIAL`状态。在你的规则中，你可以使用`<INITIAL>`来指定当FLEX处于`INITIAL`状态时应该匹配哪些规则。

- `BEGIN`：这个关键字用于改变当前的开始状态。例如，如果你想在匹配到某个特定的模式后改变开始状态，你可以使用`BEGIN`关键字。在你给出的代码中，当匹配到"A"时，使用了`BEGIN A_START;`来将开始状态切换到`A_START`。

所以，在你给出的代码中，`<INITIAL,A_START>"A"`表示当FLEX处于`INITIAL`或者`A_START`状态时，如果输入流中的下一个字符是"A"，那么就会执行后面的动作——切换到`A_START`状态，并且如果这是输入流的第一个字符（即`first_char == 1`），就打印出"输入流以A开头"并将`first_char`设置为0。

其它关键字
-  ECHO：这个关键字用于将当前匹配的文本输出到标准输出1。

-  yymore()：这个函数用于将下一次匹配的文本附加到当前匹配的文本上1。

-  yyless(n)：这个函数用于将输入流回退n个字符1。

-  REJECT：这个关键字用于放弃当前的匹配规则，并尝试下一个匹配规则1。

-  YYSTATE：这个宏用于获取当前的开始状态1。
