
const botoes_escolha = document.querySelectorAll('.select_div');
const URL_ALVO = '/jokenpo';

// elementos do html
div_img_bot = document.getElementById('img_escolha_bot');
div_img_player = document.getElementById('img_escolha_player');
botao_jogar = document.getElementById("acao_jogar")
msg_aviso = document.getElementById("mensagem_aviso")
placar = document.getElementById("placar")
div_vitoria = document.getElementById("v_div")
msg_final = document.getElementById("msg_final")

// funcoes uteis
function setar_escolha(elemento){
    img_caminho = 'static\\jokenpo\\'  +  elemento.dataset.escolha +'_img.png';
    div_img_player.src = img_caminho;
    return elemento.dataset.escolha;
}

function atualizar_dados_rodada(pontuacao,msg,class_msg,escolha_bot){
    // alterando a mensagem de aviso que aparece depois de cada rodada
    msg_aviso.innerText = msg
    msg_aviso.className = class_msg
    placar.innerText = pontuacao
    div_img_bot.src = 'static\\jokenpo\\'  +  escolha_bot +'_img.png';

}

function mostar_mensagem_vitoria(vencedor){
    if (div_vitoria.style.display === 'none' || div_vitoria.style.display === ''){
        div_vitoria.style.display = 'block'
        botao_jogar.style.display = 'none'
        if (vencedor === "player"){
            msg_final.innerText = "Você ganhou!";
            div_vitoria.style.backgroundColor = "green"
        }
        else{
            msg_final.innerText = "Você perdeu!"
            div_vitoria.style.backgroundColor = "red"
        }
        setTimeout(function() { // se setar direto, a animação de opacidade não ocorre, por isso a gente espera um pouco
            div_vitoria.style.opacity = "100%"
        }, 0);
       
    }
    else{
        botao_jogar.style.display = "none"
        div_vitoria.style.display = 'none'
    }
   
    
}
async function mandar_escolha_player(){
    const post_data = {
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({escolha_player : sessionStorage.getItem("escolha_player")})
    }
    response = await fetch(URL_ALVO, post_data)
    if (!response.ok){
        throw new Error('Erro com a resposta...');
    }
    
    if (response.redirected) 
    { /* redirecionar se o tipo for para isso */
        window.location.href = response.url; 
    } 
    else 
    {   
        data = await response.json();
        /* se a chave "resultado_jogo" existe, indica o fim do jogo */
        if (data.resultado_jogo){ 
            // exibir tela final aqui
            mostar_mensagem_vitoria(data.resultado_jogo)
        }
        /* se não existir, os dados enviados 
        são só para atualizar o estado da rodada */
        atualizar_dados_rodada(data.placar,data.mensagem_aviso,data.cor_aviso,data.escolha_bot)
      
    }
}

botoes_escolha.forEach(function(botao){
    botao.addEventListener('click',function(){
        setar_escolha(botao);

        /*Guardando informação da escolha na sessão ativa ( post request ira manda-la para a aplicação python) */
        sessionStorage.setItem("escolha_player",botao.dataset.escolha)
        /* above it saves the choice on a sessiom */
    })
})
botao_jogar.addEventListener('click',function(){
    try{
        mandar_escolha_player()
    }catch(erro){
        console.log(erro)
    }
    
 
}
)