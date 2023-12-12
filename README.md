# LogCompAPS
APS de Lógica da Computação

## Origem
A motivação para a criação dessa linguagem é ampliar o acesso e facilitar o aprendizado da população da América Latina. A linguagem é bastante similar a Golang, mas com a sintaxe alterada para espanhol, com o principal objetivo de ser uma opção para pessoas que querem programar mas não falam muito bem em inglês.

## EBNF
```
PROGRAMA = { DECLARACION | FUNCION };
DECLARACION = ( λ | ASIGNACION | IMPRIMIR | CONTROL | COMENTARIO ), "\n" ;
ASIGNACION = ["var"], IDENTIFICADOR, ["=", EXPRESION] ;
IMPRIMIR = "Imprimir", "(", EXPRESION, ")" ;
CONTROL = SI | BUCLE ;
SI = "si", "(", EXPRESION, ")", BLOQUE, [ "sino", BLOQUE ];
BUCLE = "mientras", "(", CONDICION_BUCLE, ")", BLOQUE ;
FUNCION = "func", IDENTIFICADOR, "(", [PARAMETROS], ")", [TIPO_RETORNO], BLOQUE ;
PARAMETROS = IDENTIFICADOR, TIPO, { ",", IDENTIFICADOR, TIPO } ;
BLOQUE = "{", { DECLARACION }, "}" ;
EXPRESION = TERMINO, { ("+" | "-" | "&&" | "||" | "==" | "<" | ">" | "!"), TERMINO } ;
TERMINO = FACTOR, { ("*" | "/" | "." | "!"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMERO | "(", EXPRESION, ")" | IDENTIFICADOR | CADENA ;
IDENTIFICADOR = LETRA, { LETRA | DIGITO | "_" } ;
NUMERO = DIGITO, { DIGITO } ;
CADENA = "\"", { TODOS_EXCETO_COMILLA }, "\"" ;
TIPO_RETORNO = "->", TIPO ;
TIPO = "ent" | "cadena" ;
CONDICION_BUCLE = EXPRESION, ";", EXPRESION, ";", EXPRESION ;
COMENTARIO = "//", { TODOS_EXCETO_SALTO_LINEA } ;
LETRA = ( a | ... | z | A | ... | Z ) ;
DIGITO = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

```

## Dicionário
```
Println -> Imprimir
if -> si
else -> sino
for -> mientras
func -> func
return -> devolver
int -> ent
string -> cadena
Scanln -> LeerLinea
```

