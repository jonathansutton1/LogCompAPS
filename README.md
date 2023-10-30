# LogCompAPS
APS de Lógica da Computação

## EBNF
```
PROGRAMA = { DECLARACION };
DECLARACION = ( λ | ASIGNACION | IMPRIMIR | CONTROL ), "\n" ;
ASIGNACION = IDENTIFICADOR, "=", EXPRESION ;
IMPRIMIR = "Imprimir", "(", EXPRESION, ")" ;
CONTROL = SI | BUCLE ;
SI = "si", "(", EXPRESION, ")", "{", { DECLARACION }, "}", [ "sino", "{", { DECLARACION }, "}" ];
BUCLE = "mientras", "(", EXPRESION, ")", "{", { DECLARACION }, "}" ;
EXPRESION = TERMINO, { ("+" | "-"), TERMINO } ;
TERMINO = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMERO | "(", EXPRESION, ")" | IDENTIFICADOR ;
IDENTIFICADOR = LETRA, { LETRA | DIGITO | "_" } ;
NUMERO = DIGITO, { DIGITO } ;
LETRA = ( a | ... | z | A | ... | Z  ) ;
DIGITO = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

```
