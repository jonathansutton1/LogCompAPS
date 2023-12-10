import sys
from abc import ABC, abstractmethod



class PrePro:
    def filter(code):
        code = code.split("\n")
        for i in range(len(code)):
            if "//" in code[i]:
                code[i] = code[i].split("//")[0]
        code = "\n".join(code) + "\n"
        return code
    
    
class Node:
    def __init__(self, value,children: list):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self,st):
        pass

class SymbolTable:
    def __init__(self) -> None:
        self.st = {}

    def set(self, symbol, value):
        if value[0] == self.st[symbol][0]:
            if symbol not in self.st:
                raise TypeError("Error")
            else:
                self.st[symbol] = value
        else:
            raise TypeError("Error")

    def get(self, symbol):
        if symbol in self.st:
            return self.st[symbol]
        else:
            raise TypeError("Variable no declarada")
    
    def create(self, symbol, type):
        if symbol in self.st:
            print(f'symbol: {symbol}')
            raise TypeError("Error en el método de creación de SymbolTable")
        else:
            self.st[symbol] = (type, None)

class funcTable():
    ft = {}

    def set(symbol,value):
        if value[0] == funcTable[symbol][0]:
            if symbol not in funcTable.ft:
                raise TypeError("Error")
            else:
                funcTable.ft[symbol] = value

    def get(symbol):
        if symbol in funcTable.ft:
            return funcTable.ft[symbol]
        else:
            raise TypeError("Variable no declarada en Get del SymbolTable")
        
    def create(symbol, type, node):
        if symbol in funcTable.ft:
            raise TypeError("Error en el método de creación de SymbolTable")
        else:
            funcTable.ft[symbol] = (node, type)

class Identifier(Node):
    def Evaluate(self, st):
        return st.get(self.value)
    
class Print(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st)[1])

class If(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
        elif len(self.children) == 3:
            self.children[2].Evaluate(st)

class For(Node):
    def Evaluate(self, st):
        self.children[0].Evaluate(st)
        while self.children[1].Evaluate(st) == ("ent", 1):
            self.children[3].Evaluate(st)
            self.children[2].Evaluate(st)
    
class Scanln(Node):
    def Evaluate(self, st):
        return ("ent", int(input()))

class Assignment(Node):
    def Evaluate(self, st):
        st.set(self.children[0].value, self.children[1].Evaluate(st))

class Return(Node):
    def Evaluate(self, st):
        return self.children[0].Evaluate(st)
    
class funcDec(Node):
    def Evaluate(self, st):
        fname = self.children[0].children[0].value
        ftype = self.children[0].value
        funcTable.create(symbol = fname, type=ftype,node=self)

class funcCall(Node):
    def Evaluate(self, st):
        fname = self.value
        fnode = funcTable.get(fname)[0]
        ftype = funcTable.get(fname)[1]
        fst = SymbolTable()

        for i in range(len(self.children)):
            fnode.children[i+1].Evaluate(fst)
            fst.set(fnode.children[i+1].children[0].value, self.children[i].Evaluate(st))
        return_block = fnode.children[-1].Evaluate(fst)
        if return_block is not None:
            if ftype == return_block[0]:
                return return_block
            else:
                raise TypeError("Error en funccall")

class Block(Node):
    def Evaluate(self, st):
        for child in self.children:
            if isinstance(child, Return):
                return child.Evaluate(st)
            child.Evaluate(st)

class Program(Node):
    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)

class varDec(Node):
    def Evaluate(self, st):
        if len(self.children) == 2:
            st.create(self.children[0].value, self.value)
            st.set(self.children[0].value, self.children[1].Evaluate(st))
        else:
            st.create(self.children[0].value, self.value)

class stringVal(Node):
    def Evaluate(self, st):
        return ("cadena", self.value)

class BinOp(Node):

    def Evaluate(self, st):        
        left_op = self.children[0].Evaluate(st)
        right_op = self.children[1].Evaluate(st)
        if self.value == "+" and left_op[0] == "ent" and right_op[0] == "ent":
            return (("ent",left_op[1]+right_op[1])) 
        elif self.value == "-" and left_op[0] == right_op[0] and right_op[0] == "ent":
            return (("ent", left_op[1] - right_op[1]))
        elif self.value == "*" and left_op[0] == right_op[0] and right_op[0] == "ent":
            return (("ent", left_op[1] * right_op[1]))
        elif self.value == "/" and left_op[0] == right_op[0] and right_op[0] == "ent":
            return (("ent", left_op[1] // right_op[1]))
        elif self.value == "||" and left_op[0] == right_op[0] and right_op[0] == "ent":
            return (("ent", int(left_op[1] or right_op[1])))
        elif self.value == "&&" and left_op[0] == right_op[0] and right_op[0] == "ent":
            return (("ent", int(left_op[1] and right_op[1])))
        elif self.value == ">" and left_op[0] == right_op[0]:
            return (("ent", int(left_op[1] > right_op[1])))
        elif self.value == "<" and left_op[0] == right_op[0]:
            return (("ent", int(left_op[1] < right_op[1])))
        elif self.value == "==" and left_op[0] == right_op[0]:
            return (("ent", int(left_op[1] == right_op[1])))
        elif self.value == ".":
            return (("cadena", str(left_op[1]) + str(right_op[1])))
        else:
            raise Exception("Error - BINOP")

class UnOp(Node):
    def Evaluate(self, st):
        child = self.children[0].Evaluate(st)
        if self.value == "+" and child[0] == "ent":
            return ("ent", +child[1])
        elif self.value == "-" and child[0] == "ent":
            return ("ent", -child[1])
        elif self.value == "!" and child[0] == "ent":
            return ("ent", int(not child[1]))
        else:
            raise Exception("Sintaxis inválida")
        
class IntVal(Node):

    def Evaluate(self, st):
        return ("ent",self.value)
    
class NoOp(Node):

    def Evaluate(self, st):
        pass

class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self,source):
        self.source = source
        self.position = 0
        self.next = None            #Inicia em 0 

    def selectNext(self):
        if self.position < len(self.source):
            char = self.source[self.position]
            if char.isdigit():
                num_str = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    num_str += self.source[self.position]
                    self.position += 1
                self.next = Token("INT", int(num_str))

            elif char == "+":
                self.next = Token("PLUS", char)
                self.position += 1
                
            elif char == "-":
                self.next = Token("MINUS", char)
                self.position += 1

            elif char == "*":
                self.next = Token("MULT", char)
                self.position += 1

            elif char == "/":
                self.next = Token("DIV", char)
                self.position += 1

            elif char == "(":
                self.next = Token("OPEN_PAR", char)
                self.position += 1

            elif char == ")":
                self.next = Token("CLOSE_PAR", char)
                self.position += 1

            elif char == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("EQUAL_EQUAL", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUAL", char)
                    self.position += 1


            elif char == "\n":
                self.next = Token("NEWLINE", char)
                self.position += 1

            elif char == "|" and self.source[self.position+1] == "|":
                self.next = Token("OR", '||')
                self.position += 2

            elif char == "&" and self.source[self.position+1] == "&":
                self.next = Token("AND", "&&")
                self.position += 2

            elif char == "!":
                self.next = Token("NOT", char)
                self.position += 1

            elif char == "{":
                self.next = Token("OPEN_KEY", char)
                self.position += 1

            elif char == "}":
                self.next = Token("CLOSE_KEY", char)
                self.position += 1

            elif char == ";":
                self.next = Token("POINT_COMMA", char)
                self.position += 1

            elif char == ">":
                self.next = Token("BIGGER", char)
                self.position += 1
            
            elif char == "<":
                self.next = Token("SMALLER", char)
                self.position += 1

            elif char == ".":
                self.next = Token("CONCAT", char)
                self.position += 1

            elif char == ",":
                self.next = Token("COMMA", char)
                self.position += 1  

            elif char =='"':
                string = ""
                self.position += 1
                while self.source[self.position] != '"' and self.position < len(self.source):
                    string += self.source[self.position]
                    self.position += 1
                self.next = Token("STRING", string)
                self.position += 1

            elif char.isalpha():
                id_str = ""
                while self.position < len(self.source):
                    id_str += char
                    if self.position + 1 < len(self.source) and self.source[self.position + 1].isalpha() or self.source[self.position + 1].isdigit() or self.source[self.position + 1] == "_":
                        self.position += 1
                        char = self.source[self.position]
                    else:
                        self.position += 1
                        break
                if id_str == "Imprimir":
                    self.next = Token("PRINT", id_str)
                elif id_str == "si":
                    self.next = Token("IF", id_str)
                elif id_str == "sino":
                    self.next = Token("ELSE", id_str)
                elif id_str == "mientras":
                    self.next = Token("FOR", id_str)
                elif id_str == "LeerLinea":
                    self.next = Token("SCANLN", id_str)
                elif id_str == "ent":
                    self.next = Token("INT_DECLARE", id_str)
                elif id_str == "cadena":
                    self.next = Token("STR_DECLARE", id_str)
                elif id_str == "var":
                    self.next = Token("VAR", id_str)
                elif id_str == "func":
                    self.next = Token("FUNC", id_str)
                elif id_str == "devolver":
                    self.next = Token("RETURN", id_str)
                else:
                    self.next = Token("ID", id_str)

    
            elif char == " " or char == "\t":
                self.position += 1
                self.selectNext()
            else:
                print(f'char: {char}')
                raise ValueError("Error")
        else:
            self.next = Token("EOF", "")

class Parser:
    tokenizer = None

    def parseProgram():
        result = Block("Block", [])
        while Parser.tokenizer.next.type != "EOF":
            while Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "EOF":
                result.children.append(Parser.parseDeclaration())
        result.children.append(funcCall("main", []))
        return result
    
    def parseDeclaration():
        parameters = list()
        if Parser.tokenizer.next.type == "FUNC":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ID":
                fname = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OPEN_PAR":
                    Parser.tokenizer.selectNext()
                    while Parser.tokenizer.next.type == "ID":
                        varname = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        vartype = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        parameters.append((vartype,varname))
                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.selectNext()
                        else:
                            break
                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "INT_DECLARE" or Parser.tokenizer.next.type == "STR_DECLARE":
                            ftype = Parser.tokenizer.next.value
                            Parser.tokenizer.selectNext()
                            result = funcDec(None, [varDec(ftype, [Identifier(fname, [])])])
                            if len(parameters) > 0:
                                for i in range(len(parameters)):
                                    result.children.append(varDec(parameters[i][0], [Identifier(parameters[i][1], [])]))
                            result.children.append(Parser.parseBlock())
                            if Parser.tokenizer.next.type == "NEWLINE":
                                Parser.tokenizer.selectNext()
                            else:
                                raise Exception("Debería ser una nueva linea")
                            return result
                        else:
                            print(f'value: {Parser.tokenizer.next.value}')
                            print(f'tipo: {Parser.tokenizer.next.type}')
                            raise Exception("Debería ser una cadena o un int")
                    else:
                        raise Exception("Deberías cerrar los paréntesis.")
                else:
                    raise Exception("Deberías abrir los paréntesis.")
            else:
                raise Exception("Deberías ser un ID")
        else:
            raise Exception("Deberías ser una funcion")
        
    
    def parseBlock():
        result = Block("Block", [])
        if Parser.tokenizer.next.type == "OPEN_KEY":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "CLOSE_KEY":
                    result.children.append(Parser.parseStatement())
                if Parser.tokenizer.next.type == "CLOSE_KEY":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise Exception("Deberías cerrar las llaves")
                
    def parseAssignment():
        if Parser.tokenizer.next.type == "ID":
            id = Identifier(Parser.tokenizer.next.value,[])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [id, Parser.parseBoolExpression()])
                return result
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = funcCall(id, [])
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise Exception("Debería ser una nueva linea")
                else:
                    raise Exception("Deberías cerrar los paréntesis.")
            else:
                raise Exception("Debería ser un equal")
        else:
            raise Exception("Error")
        
    def parseBoolExpression():
        result = Parser.parseBoolTerm()
        while Parser.tokenizer.next.type == "OR":
            Parser.tokenizer.selectNext()
            result = BinOp("||", [result, Parser.parseBoolTerm()])
        return result
    
    def parseBoolTerm():
        result = Parser.relExpression()
        while Parser.tokenizer.next.type == "AND":
            Parser.tokenizer.selectNext()
            result = BinOp("&&", [result, Parser.relExpression()])
        return result

    def relExpression():
        result = Parser.parseExpression()
        while Parser.tokenizer.next.type == "BIGGER" or Parser.tokenizer.next.type == "SMALLER" or Parser.tokenizer.next.type == "EQUAL_EQUAL":
            if Parser.tokenizer.next.type == "BIGGER":
                Parser.tokenizer.selectNext()
                result = BinOp(">", [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "SMALLER":
                Parser.tokenizer.selectNext()
                result = BinOp("<", [result, Parser.parseExpression()])
            elif Parser.tokenizer.next.type == "EQUAL_EQUAL":
                Parser.tokenizer.selectNext()
                result = BinOp("==", [result, Parser.parseExpression()])
        return result
    

    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "CONCAT":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.selectNext()
                result = BinOp("+", [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.selectNext()
                result = BinOp("-", [result, Parser.parseTerm()])
            elif Parser.tokenizer.next.type == "CONCAT":
                Parser.tokenizer.selectNext()
                result = BinOp(".", [result, Parser.parseTerm()])
            else:
                raise Exception("Deberia ser un numero")
        return result
        
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                result = BinOp("*", [result, Parser.parseFactor()])
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                result = BinOp("/", [result, Parser.parseFactor()])
            else:
                raise Exception("Deberia ser un numero")
        return result
        
    def parseFactor():
        result = None
        if Parser.tokenizer.next.type == "INT":
            result = IntVal(Parser.tokenizer.next.value,[])
            Parser.tokenizer.selectNext()
            return result

        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.selectNext()
            result = UnOp("+", [Parser.parseFactor()])
            return result
        
        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.selectNext()
            result = UnOp("-", [Parser.parseFactor()])
            return result

        elif Parser.tokenizer.next.type == "OPEN_PAR":
            Parser.tokenizer.selectNext()
            result = Parser.parseBoolExpression()
            if Parser.tokenizer.next.type == "CLOSE_PAR":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception("Sintaxis inválida")
            
        elif Parser.tokenizer.next.type == "ID":
            var = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = funcCall(var, [])
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                    else:
                        break
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise Exception("Deberías cerrar los paréntesis.")
            else:
                return Identifier(var, [])




        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.selectNext()
            result = UnOp("!", [Parser.parseFactor()])
            return result
        elif Parser.tokenizer.next.type == "SCANLN":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = Scanln("Scanln", [])
                if Parser.tokenizer.next.type == "CLOSE_PAR":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise Exception("Error en LeerLinea")
            else:
                raise Exception("Error en LeerLinea")
        elif Parser.tokenizer.next.type == "STRING":
            result = stringVal(Parser.tokenizer.next.value,[])
            Parser.tokenizer.selectNext()
            return result
        else:
            print(f'type: {Parser.tokenizer.next.type}')
            print(f'value: {Parser.tokenizer.next.value}')
            raise Exception("Error")
        
    def parseStatement():
        if Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                result = Print("", [Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise Exception("Devia fechar os parenteses")
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception("Deberías abrir los paréntesis.")
            
        elif Parser.tokenizer.next.type == "ID":
            var = Identifier(Parser.tokenizer.next.value,[])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                result = Assignment("=", [var, Parser.parseBoolExpression()])
                if Parser.tokenizer.next.type == "NEWLINE":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    print(f'result: {result.value}')
                    print(f'value: {Parser.tokenizer.next.value}')
                    print(f'type: {Parser.tokenizer.next.type}')
                    raise Exception("Devia ser um newline")
                
            elif Parser.tokenizer.next.type == "OPEN_PAR":
                    Parser.tokenizer.selectNext()
                    result = funcCall(var.value, [])
                    while Parser.tokenizer.next.type != "CLOSE_PAR":
                        result.children.append(Parser.parseBoolExpression())
                        if Parser.tokenizer.next.type == "COMMA":
                            Parser.tokenizer.selectNext()
                        else:
                            break
                    if Parser.tokenizer.next.type == "CLOSE_PAR":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "NEWLINE":
                            Parser.tokenizer.selectNext()
                            return result
                        else:
                            raise Exception("Debería ser una nueva linea")
                    else:
                        raise Exception("Deberías cerrar los paréntesis.")
            else:
                raise Exception("Deberias abrir los parentesis")
            
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            result = If("IF", [Parser.parseBoolExpression()])
            result.children.append(Parser.parseBlock())
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                result.children.append(Parser.parseBlock())
            if Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.selectNext()
                return result   
            else:
                raise Exception("Debería ser una nueva linea")

        elif Parser.tokenizer.next.type == "FOR":
            Parser.tokenizer.selectNext()
            result = For("FOR", [Parser.parseAssignment()])
            if Parser.tokenizer.next.type == "POINT_COMMA":
                Parser.tokenizer.selectNext()
                result.children.append(Parser.parseBoolExpression())
                if Parser.tokenizer.next.type == "POINT_COMMA":
                    Parser.tokenizer.selectNext()
                    result.children.append(Parser.parseAssignment())
                    result.children.append(Parser.parseBlock())
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise Exception("Deberia ser un ;")
                else:
                    raise Exception("Deberia ser un ;")
            else:
                raise Exception("Deberia ser un ;")
            
        elif Parser.tokenizer.next.type == "VAR":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "ID":
                id = Identifier(Parser.tokenizer.next.value,[])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "INT_DECLARE" or Parser.tokenizer.next.type == "STR_DECLARE":
                    value = Parser.tokenizer.next.value
                    result = varDec(value, [id])
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.selectNext()
                        result.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.type == "NEWLINE":
                        Parser.tokenizer.selectNext()
                        return result
                    else:
                        raise Exception("Devia ser um newline")
                    
        elif Parser.tokenizer.next.type == "RETURN":
            Parser.tokenizer.selectNext()
            result = Return("Return", [Parser.parseBoolExpression()])
            if Parser.tokenizer.next.type == "NEWLINE":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception("Debería ser una nueva linea")
            
        elif Parser.tokenizer.next.type == "NEWLINE":
            Parser.tokenizer.selectNext()
            return NoOp("", [])

        else:
            raise Exception("Dio un símbolo que no debería haber sido dado")
        

    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseProgram()
        if Parser.tokenizer.next.type == "EOF":
            return result
        else:
            raise TypeError("Error EOF")

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        code = f.read()
        code = PrePro.filter(code)
    
    Parser.tokenizer = Tokenizer(code)
    result = Parser.run(code)
    st = SymbolTable()
    result.Evaluate(st)