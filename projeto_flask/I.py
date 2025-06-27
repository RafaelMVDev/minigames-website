total_frames = 10
jogoda_p_frames = 2

pontuacao = 0

ponto_frames = {}
jogadores = int(input())
frame_atual = 0
n_jogada = 0

n_frame = 0
bonus_restantes = {}
jogada_adicional = False
for c in range(0,jogadores):
   
    n_jogador = input()
    jogadas = input()
    ponto_frames[n_jogador] = {}
    tot_derrubado = 0
    jogada_adicional = False
    jogoda_p_frames = 2
    n_frame = 0
    bonus_restantes = 0

    for pinos_derrubados in jogadas:
        n_jogada += 1
        v_a = 10 if pinos_derrubados == "X" else int(pinos_derrubados)
        tot_derrubado += v_a
       
        if bonus_restantes :
            print("N frame: ",n_frame)
            if n_frame != 0:
                bonus_restantes -= 1
                print(f"ADICIONANDO O Ú BONUS {bonus_restantes}")
                print(f"Valor adicionado: {v_a} N jogada = : {n_jogada} N SET: {n_frame}")
                
                ponto_frames[n_jogador][n_frame - 1] += v_a
                print(ponto_frames[n_jogador])
            else:
                bonus_restantes -= 1
                
        if v_a == 10 and n_jogada == 1:
            if n_frame == 9:
                jogada_adicional = True
            else:
                print(f"STRIKE NA JOGADA {n_frame}: ")
                bonus_restantes= 2
        elif tot_derrubado == 10:
            print(f"SPARE NA JOGADA {n_frame}: ")
            if n_frame == 9:
                jogada_adicional = True
            else:
                bonus_restantes = 1
        
        if n_jogada == jogoda_p_frames:
            if jogada_adicional:
                jogoda_p_frames = 3
            else:
                n_jogada = 0
                pinos_derrubados = 0
                n_jogada = 0
                
                ponto_frames[n_jogador][n_frame] = 0
                ponto_frames[n_jogador][n_frame]+= tot_derrubado
                n_frame += 1
                tot_derrubado = 0
    print("FINAL: ", ponto_frames[n_jogador])   
    


for nome, pontos in ponto_frames.items():
    print()
    print(f"{nome} : ",end="")
    pontuacao = 0
    print("|",end = "")
    for i in range(0,10):
        pontuacao += pontos[i]
        print( f"{pontuacao}|", end = "")
    print(f" Total = {pontuacao}")
