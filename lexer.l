%{
#include <stdio.h>
%}

%option noyywrap

/* Definitions */
DIGIT   [0-9]+
ID      [a-zA-Z_][a-zA-Z0-9_]*

%%

"if"               { printf("TOKEN_IF\n"); }
"else"             { printf("TOKEN_ELSE\n"); }
"while"            { printf("TOKEN_WHILE\n"); }
"return"           { printf("TOKEN_RETURN\n"); }

{ID}               { printf("TOKEN_ID %s\n", yytext); }
{DIGIT}            { printf("TOKEN_NUM %s\n", yytext); }
[+\-*/=<>!]+       { printf("TOKEN_OP %s\n", yytext); }
[(){};,]           { printf("TOKEN_DELIM %s\n", yytext); }
[ \t\r\n]+         { /* ignore whitespace */ }
.                  { printf("TOKEN_UNKNOWN %s\n", yytext); }

%%

int main(int argc, char **argv) {
    yylex();
    return 0;
}
