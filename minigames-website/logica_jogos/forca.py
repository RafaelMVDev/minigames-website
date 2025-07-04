from random import choice

class Forca():
    def __init__(self):
      self.opcoes_validas = ['abcdefghijklmnopqrstuvwxyz']
      self.banco_palavras = ['banana','girino']
     

    def validarEscolha(self,escolha):
        try:
            if escolha in self.opcoes_validas:
                return escolha
            else:
                return False
        except RuntimeError:
            return False
 

    def checarLetraForca(self,palavra_original, estado_atual_palavra, letra):
        atual = estado_atual_palavra
   
        for i in range(0,len(palavra_original)):
            if palavra_original[i] == letra:
                atual[i] = letra

        return atual

    def palavraAleatoria(self):
        return self.banco_palavras[choice(range(len(self.banco_palavras)))]



  