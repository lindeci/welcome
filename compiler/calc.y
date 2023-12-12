%{
#  include <stdio.h>

int yyerror(char *s);
int yylex();

%}

//set attribute type
%define api.value.type {int}

/* declare tokens (terminal symbols) */
%token NUM  256
%token ADD 257
%token SUB 258
%token MUL 259
%token DIV 260
%token LP 261
%token RP 262
%token EOL 263

%%

start: 
 | start expr EOL { printf("= %d\n> ", $2); };

expr: term
 | expr ADD term { $$ = $1 + $3; }
 | expr SUB term { $$ = $1 - $3; } 
 ;

term: factor { $$ = $1; }
 | term MUL factor { $$ = $1 * $3; }
 | term DIV factor { $$ = $1 / $3; } 
 ;

factor: NUM { $$ = $1; }
 | LP expr RP { $$ = $2; }
 ;

%%
int main()
{
  printf("> "); 
  yyparse();
}

int yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}
int yywrap() 
{ 
   return(1); 
}