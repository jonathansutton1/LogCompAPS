# LogCompAPS
APS de Lógica da Computação

## EBNF
```
PROGRAMA = { DECLARAÇÃO };
DECLARAÇÃO = ( λ | ATRIBUIÇÃO | IMPRIMIR | CONTROLE ), "\n" ;
ATRIBUIÇÃO = IDENTIFICADOR, "=", EXPRESSÃO ;
IMPRIMIR = "Imprimir", "(", EXPRESSÃO, ")" ;
CONTROLE = SE | LAÇO ;
SE = "se", "(", EXPRESSÃO, ")", "{", { DECLARAÇÃO }, "}", [ "senao", "{", { DECLARAÇÃO }, "}" ];
LAÇO = "enquanto", "(", EXPRESSÃO, ")", "{", { DECLARAÇÃO }, "}" ;
EXPRESSÃO = TERMO, { ("+" | "-"), TERMO } ;
TERMO = FATOR, { ("*" | "/"), FATOR } ;
FATOR = (("+" | "-"), FATOR) | NÚMERO | "(", EXPRESSÃO, ")" | IDENTIFICADOR ;
IDENTIFICADOR = LETRA, { LETRA | DÍGITO | "_" } ;
NÚMERO = DÍGITO, { DÍGITO } ;
LETRA = ( a | ... | z | A | ... | Z | á | é | í | ó | ú | ç | ã | õ ) ;
DÍGITO = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```
