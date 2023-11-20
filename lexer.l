
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"
%}

DIGITO [0-9]

%%

"var"                                   { printf("Token VAR\n"); return VAR; }
"funcion"                                { printf("Token FUNCION\n"); return FUNCION; }
"retornar"                               { printf("Token RETORNAR\n"); return RETORNAR; }
"Imprimir"                               { printf("Token IMPRIMIR\n"); return IMPRIMIR; }
"si"                                    { printf("Token SI\n"); return SI; }
"sino"                                 { printf("Token SINO\n"); return SINO; }
"para"                                  { printf("Token PARA\n"); return PARA; }
"ent"                               { printf("Token ENT\n"); return ENT; }
"flo"                             { printf("Token FLO\n"); return FLO; }
"texto"                                 { printf("Token TEXTO\n"); return TEXTO; }
"booleano"                              { printf("Token BOOLEANO\n"); return BOOLEANO; }
"verdadero"                            { printf("Token VERDADERO\n"); return VERDADERO; }
"falso"                                 { printf("Token FALSO\n"); return FALSO; }
"+"                                     { printf("Token SUMA\n"); return SUMA; }
"-"                                     { printf("Token SUBTRACION\n"); return SUBTRACION; }
"*"                                     { printf("Token MULTIPLICACION\n"); return MULTIPLICACION; }
"/"                                     { printf("Token DIVISON\n"); return DIVISON; }
">"                                     { printf("Token MAJOR_QUE\n"); return MAJOR_QUE;}
"<"                                     { printf("Token MINOR_QUE\n"); return MINOR_QUE;}
[a-zA-Z][a-zA-Z0-9]*                    { printf("Token IDENTIFICADOR\n"); return IDENTIFICADOR; }
{DIGITO}+"."{DIGITO}+                   { printf("Token LITERAL_FLUTUANTE\n"); return LITERAL_FLUTUANTE; }
{DIGITO}+                               { printf("Token LITERAL_NUMERICO\n"); return LITERAL_NUMERICO; }
\"([^\\\"]|\\.)*\"                      { printf("Token LITERAL_TEXTO\n"); return LITERAL_TEXTO; }
";"                                     { printf("Token PUNTO_Y_COMA\n"); return PUNTO_Y_COMA; }
"="                                     { printf("Token IGUAL\n"); return IGUAL; }
","                                     { printf("Token COMA\n"); return COMA; }
"("                                     { printf("Token ABRE_PARENTESES\n"); return ABRE_PARENTESES; }
")"                                     { printf("Token FECHA_PARENTESES\n"); return FECHA_PARENTESES; }
"{"                                     { printf("Token ABRE_CHAVES\n"); return ABRE_CHAVES; }
"}"                                     { printf("Token FECHA_CHAVES\n"); return FECHA_CHAVES; }
[ \t\n]                                 { /* Ignora espaços em branco */ }
.                                       { fprintf(stderr, "Caractere não reconhecido: %c\n", yytext[0]); }

%%
