class Token:
    def __init__(self, tipo, nome):
        self.tipo = tipo
        self.nome = nome

import string

palavras_reservadas = ['program', 'if', 'then', 'else', 'while', 'do', 'until', 'repeat', 'int', 'double', 'char', 'case', 'switch', 'end', 'procedure', 'function', 'for', 'begin']

def lexico(num_linha, indice):
    token = ''
    global estado
    global comentario
    mensagem = ''
    with open('teste.txt', 'r') as arquivo:
      linhas = arquivo.readlines()
      if num_linha >= len(linhas):
        return None
      linha = linhas[num_linha]
    if '\n' not in linha:
        linha += '\n'
    while indice < len(linha):
        caractere = linha[indice]
        if comentario == False:
            if estado == 0:
                if (caractere in string.ascii_lowercase or
                    caractere in string.ascii_uppercase):
                    token += caractere
                    estado = 1
                elif caractere == "-":
                    token += caractere
                    estado = 11
                elif caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 12
                elif caractere in [';', ',', '.', '(', ')', '{', '}', '=']:
                    estado = 0
                    return Token('SIMBOLO_ESPECIAL', caractere), num_linha, indice + 1
                elif caractere == "<":
                    token += caractere
                    estado = 16
                elif caractere in [')', ':', '*', '+']:
                    token += caractere
                    estado = 17
                elif caractere == "@":
                    token += caractere
                    estado = 5
                elif caractere == "/":
                    token += caractere
                    estado = 7
                elif caractere == '\t' or caractere == ' ':
                    pass
                elif caractere == '\n':
                  return '\n', num_linha + 1, 0
                else:
                    mensagem = f'Erro lexico: caractere não reconhecido "{caractere}".'
                    estado = -1
            elif estado == 1:
                if (caractere in [str(x) for x in range(0, 9)] or
                    caractere in string.ascii_lowercase):
                    token += caractere
                    estado = 2
                elif caractere == "_":
                    token += caractere
                    estado = 3
                elif caractere == "$":
                    token += caractere
                    estado = 4
                else:
                    estado = 0
                    return Token('IDENTIFICADOR', token), num_linha, indice
            elif estado == 3:
                if caractere in string.ascii_lowercase or caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 2
                else:
                    mensagem = f'Erro lexico: você tem "{token}". "{token[-1]}" não pode finalizar um identificador.'
                    estado = -1
            elif estado == 4:
                if caractere in string.ascii_lowercase:
                    token += caractere
                    estado = 2
                else:
                    mensagem = f'Erro lexico: você tem "{token}". "{token[-1]}" não pode finalizar um identificador.'
                    estado = -1
            elif estado == 2:
                if (caractere in [str(x) for x in range(0, 9)] or
                    caractere in string.ascii_lowercase):
                    token += caractere
                    estado = 2
                    if indice + 1 == len(linha):
                        estado = 0
                        if token in palavras_reservadas:
                            return Token('PALAVRA_RESERVADA', token), num_linha, indice
                        else:
                            return Token('IDENTIFICADOR', token), num_linha, indice
                elif caractere == "$":
                    token += caractere
                    estado = 4
                else:
                    estado = 0
                    if token in palavras_reservadas:
                        return Token('PALAVRA_RESERVADA', token), num_linha, indice
                    else:
                        return Token('IDENTIFICADOR', token), num_linha, indice
            elif estado == 5:
                if caractere == "@":
                    estado = 6
                else:
                    estado = 0
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice
            elif estado == 6:
                token = ''
                estado = 0
                return '\n', num_linha + 1, 0
            elif estado == 7:
                if caractere == "/":
                    token += caractere
                    comentario = True
                    token = ''
                    estado = 8
                    return '\n', num_linha + 1, 0
                elif caractere == "*":
                    token += caractere
                    comentario = True
                    token = ''
                    estado = 22
                    return '\n', num_linha + 1, 0
                else:
                    estado = 0
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice
            elif estado == 11:
                if caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 12
                else:
                    estado = 0
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice
            elif estado == 12:
                if caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 12
                elif caractere == ",":
                    token += caractere
                    estado = 13
                else:
                    estado = 0
                    return Token('DIGITO', token), num_linha, indice
            elif estado == 13:
                if caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 14
                else:
                    mensagem = f'Erro lexico: você tem "{token}". "{token[-1]}" não pode finalizar um dígito.'
                    estado = -1
            elif estado == 14:
                if caractere in [str(x) for x in range(0, 9)]:
                    token += caractere
                    estado = 14
                    if indice + 1 == len(linha):
                        estado = 0
                        return Token('DIGITO', token), num_linha, indice
                else:
                    estado = 0
                    return Token('DIGITO', token), num_linha, indice
            elif estado == 16:
                estado = 0
                if caractere == "=":
                    token += caractere
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice + 1
                elif caractere == ">":
                    token += caractere
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice + 1
                else:
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice
            elif estado == 17:
                estado = 0
                if caractere == "=":
                    token += caractere
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice + 1
                else:
                    return Token('SIMBOLO_ESPECIAL', token), num_linha, indice

        else:
            if estado == 8:
                if caractere == "/":
                    estado = 9
                else:
                  if '//' in linha:
                    return lexico(num_linha, linha.find('/'))
                  return '\n', num_linha + 1, 0
            elif estado == 9:
                if caractere == "/":
                    comentario = False
                    estado = 0
            elif estado == 22:
                if caractere == "*":
                    estado = 23
                else:
                  if '*/' in linha:
                    return lexico(num_linha, linha.find('*'))
                  return '\n', num_linha + 1, 0
            elif estado == 23:
                if caractere == "/":
                    comentario = False
                    estado = 0

        indice += 1
        if mensagem != '':
            sys.exit(f'{mensagem} Linha: {num_linha + 1}.')

def obter_token():
    global linha, indice, token
    token, linha, indice = lexico(linha, indice) if lexico(linha, indice) is not None else (Token('ERROR', 'none'), linha, indice)
    if isinstance(token, Token):
        return token
    elif token == '\n':
        token, linha, indice = lexico(linha, indice) if lexico(linha, indice) is not None else (Token('ERROR', 'none'), linha, indice)
        if isinstance(token, Token):
            return token

def relacao():
  global linha, token
  if token.nome in ['=', '<>', '<', '<=', '>', '>=']:
      return
  else:
      sys.exit(f'Erro Sintatico: esperava um operador de relação. Linha: {linha + 1}.')

def lista_de_expressoes():
    expressao()
    if token.nome == ',':
        lista_de_expressoes
    else:
        return

def fator():
    global linha, token
    if token.tipo in ['IDENTIFICADOR', 'DIGITO']:
        return
    elif token.nome == '(':
        expressao()
        obter_token()
        if token.nome == ')':
            return
        else:
            sys.exit(f'Erro Sintatico: foi aberto ")" e não foi fechado. Linha: {linha + 1}.')
    else:
        sys.exit(f'Erro Sintatico: era esperado uma composição de fator. Linha: {linha + 1}.')

def termo():
    global linha, token
    fator()
    obter_token()
    if token.nome == '(':
        lista_de_expressoes()
        obter_token()
        if token.nome == ')':
            return
        else:
            sys.exit(f'Erro Sintatico: foi aberto "(" e não foi fechado. Linha: {linha + 1}.')
    elif token.nome in ['*', 'div', 'and']:
        obter_token()
        termo()
    else:
        return

def expressao_simples():
    global linha, token
    if token.nome in ['+', '-']:
        obter_token()
        termo()
    elif token.tipo in ['IDENTIFICADOR', 'DIGITO']:
        termo()
    else:
        sys.exit(f'Erro Sintatico: era esperado uma composição de expressão simples. Linha: {linha + 1}.')
    if token.nome in ['+', '-', 'or']:
        obter_token()
        termo()
        while token.nome in ['+', '-', 'or']:
          obter_token()
          termo()
        return
    else:
        return

def expressao():
    obter_token()
    expressao_simples()
    if token.nome in ['=', '<>', '<', '<=', '>', '>=']:
        relacao()
        obter_token()
        expressao_simples()
    return

def comando_sem_rotulo():
    global linha, token
    if token.tipo == 'IDENTIFICADOR' and token.nome != 'end':
        obter_token()
        if token.nome == ':=':
            expressao()
        elif token.nome == '(':
            lista_de_expressoes()
            if token.nome == ')':
                obter_token()
                return
            else:
                sys.exit(f'Erro Sintatico: foi aberto "(" e não foi fechado. Linha: {linha + 1}.')
        else:
            sys.exit(f'Erro Sintatico: era esperado uma composição de atribuição ou chamada de procedimento. Linha: {linha + 1}.')
    elif token.nome == 'if':
        expressao()
        if token.nome == 'then':
            obter_token()
            comando_sem_rotulo()
            if token.nome == 'else':
                print(token.nome)
                obter_token()
                comando_sem_rotulo()
            else:
                return
        else:
            sys.exit(f'Erro Sintatico: bloco condicional incompleto. Linha: {linha + 1}.')
    elif token.nome == 'while':
        expressao()
        if token.nome == 'do':
            obter_token()
            comando_sem_rotulo()
            return
        else:
            sys.exit(f'Erro Sintatico: era esperado uma composição de loop. Linha: {linha + 1}.')
    else:
        sys.exit(f'Erro Sintatico: era esperado uma composição de comando sem rotulo ou "end" para finalizar o codigo. Linha: {linha + 1}.')

def comando_composto():
    comando_sem_rotulo()
    if token.nome == ';':
        obter_token()
        if token.nome == 'end':
            print('compilado')
        else:
            comando_composto()
    else:
        sys.exit(f'Erro Sintatico: era esperado um ";". Linha: {linha + 1}.')

def bloco():
    global linha, token
    if token.nome == 'begin':
        obter_token()
        comando_composto()
    else:
        sys.exit(f'Erro Sintatico: era uma composição de bloco. Linha: {linha + 1}.')

def sintatico():
    global linha, token
    obter_token()
    if token.nome == 'program':
        obter_token()
        if token.tipo == 'IDENTIFICADOR':
            obter_token()
            if token.nome == ';':
                obter_token()
                bloco()
            else:
                sys.exit(f'Erro Sintatico: era esperado ";". Linha: {linha + 1}.')
        else:
            sys.exit(f'Erro Sintatico: era esperado um IDENTIFICADOR. Linha: {linha + 1}.')
    else:
        sys.exit(f'Erro Sintatico: era esperado "program". Linha: {linha + 1}.')

import sys

global linha
linha = 0
global indice
indice = 0
global comentario
comentario = False
global estado
estado = 0
global token
token = Token('', '')
sintatico()