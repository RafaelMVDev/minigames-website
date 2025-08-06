from random import choice

class Jokenpo():
    def __init__(self):
      self.escolhas = ['pedra','papel','tesoura']
      self.fraquezas = {
          'pedra':'papel',
          'papel': 'tesoura',
          'tesoura': 'pedra'
      }

    def validarEscolha(self,escolha):
     
        if escolha.lower() in self.escolhas:
            return escolha
        return False

    def escolherAleatorio(self):
        return self.escolhas[choice(range(0,len(self.escolhas)))]

    def validarVencedorRodada(self,escolha_player:str,escolha_bot:str):
       if escolha_player == escolha_bot:
           return 'empate'
       if self.fraquezas[escolha_bot] == escolha_player:
           return 'player'
       else:
           return 'bot'

    def validarVencedorJogo(self,pts_player,pts_bot):
       if pts_player == 3:
           return 'player'
       elif pts_bot == 3:
            return 'bot'
       else:
           return 'continuar'

    def formatarPlacar(self,pts_player,pts_bot):
        return f'{pts_player}x{pts_bot}'