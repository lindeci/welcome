%{
# include "calc.tab.h"
int lexerror(char *s);
%}

%%
"+" { return ADD; }
"-" { return SUB; }
"*" { return MUL; }
"/" { return DIV; }
"("     { return LP; }
")"     { return RP; }
[0-9]+  { yylval = atoi(yytext); return NUM; }

\n      { return EOL; }
[ \t]   { /* ignore white space */ }
.   { lexerror(yytext); }
%%

int lexerror(char *s)
{
  fprintf(stderr, "lexical error: %s\n", s);
}