
%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex();
extern char *yytext;
void yyerror(const char *s) { fprintf(stderr, "Error de análisis: %s\n", s); }
%}

%token VAR FUNCION RETORNAR IMPRIMIR SI SINO PARA ENT FLO TEXTO BOOLEANO VERDADERO FALSO 
%token IDENTIFICADOR LITERAL_NUMERICO LITERAL_TEXTO LITERAL_FLUTUANTE
%token SUMA SUBTRACION MULTIPLICACION DIVISON IGUAL COMA ABRE_PARENTESES FECHA_PARENTESES ABRE_CHAVES FECHA_CHAVES PUNTO_Y_COMA
%token MAJOR_QUE MINOR_QUE

%%

programa:
          /* vacío */
        | programa declaracion
        ;

declaracion:
          VAR IDENTIFICADOR tipo IGUAL expresion 
        | FUNCION IDENTIFICADOR ABRE_PARENTESES lista_params FECHA_PARENTESES tipo ABRE_CHAVES programa FECHA_CHAVES
        | RETORNAR IDENTIFICADOR
        | IMPRIMIR expresion
        | SI ABRE_PARENTESES expresion FECHA_PARENTESES ABRE_CHAVES programa FECHA_CHAVES
        | SI ABRE_PARENTESES expresion FECHA_PARENTESES ABRE_CHAVES programa FECHA_CHAVES SINO ABRE_CHAVES programa FECHA_CHAVES
        | PARA expresion PUNTO_Y_COMA expresion PUNTO_Y_COMA expresion ABRE_CHAVES programa FECHA_CHAVES
        | expresion
        ;

expresion:
          expresion SUMA expresion
        | expresion SUBTRACION expresion
        | expresion MULTIPLICACION expresion
        | expresion DIVISON expresion
        | expresion MAJOR_QUE expresion
        | expresion MINOR_QUE expresion
        | VAR IDENTIFICADOR tipo IGUAL LITERAL_NUMERICO
        | IDENTIFICADOR IGUAL IDENTIFICADOR SUMA LITERAL_NUMERICO ABRE_CHAVES
        | IDENTIFICADOR IGUAL IDENTIFICADOR MULTIPLICACION LITERAL_NUMERICO 
        | IDENTIFICADOR
        | LITERAL_NUMERICO
        | LITERAL_TEXTO
        | LITERAL_FLUTUANTE
        | VERDADERO
        | FALSO
        | ABRE_PARENTESES expresion FECHA_PARENTESES
        ;

tipo:
    ENT
    |FLO
    |TEXTO
    |BOOLEANO
    |
    ;

lista_params: /* vazio */
            | lista_params COMA param
            | param
            ;

param: IDENTIFICADOR tipo
     ;

%%

int main() {
    if (yyparse()) {
        fprintf(stderr, "Análisis falló\n");
        return 1;
    }
    return 0;
}
