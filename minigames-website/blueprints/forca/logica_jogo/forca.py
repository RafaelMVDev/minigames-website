from random import choice
from typing import Tuple

class Forca():
    def __init__(self):
      self.opcoes_validas = 'abcdefghijklmnopqrstuvwxyz'
      self.banco_palavras = ['banana','girino']
     

    def validarEscolha(self,escolha):
       
        try:
            if escolha in self.opcoes_validas:
                return escolha
            else:
                return False
        except RuntimeError:
            return False
 

    def analisarTentativa(self,palavra_original, estado_atual_palavra, letra) -> Tuple[str,str] :
        """
        Função que além de retornar o estado atual da palavra após a tentativa, retorna o resultado do jogo: Se ele ganhou,apenas acertou alguma das letras, ou se errou.
        """
        atual = list(estado_atual_palavra)
    
        for i in range(0,len(palavra_original)):
            if palavra_original[i] == letra:
                print("É FILHA DA PUT")
                atual[i] = letra
        str_atual = "".join(atual)
        resultado_jogo = False
        if str_atual == palavra_original:
            resultado_jogo = "ganhou"
        elif str_atual != estado_atual_palavra: # se chegar nesse elif, letra(s) foram descobertas, então ele acertou, mas não ganhou!
            resultado_jogo = "acertou_letra"
        else:
            resultado_jogo = "errou"
        print(palavra_original)
        print(str_atual)
        print(estado_atual_palavra)
        print(letra)
        return [str_atual,resultado_jogo]

    def palavraAleatoria(self):
        return self.banco_palavras[choice(range(len(self.banco_palavras)))]




  