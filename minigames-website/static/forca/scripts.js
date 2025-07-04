
const URL_ALVO = '/forca';

// elementos do html
const estado_forca = document.getElementById('estado_forca')
const palavra_atual = document.getElementById('palavra_descobrir')

// funcoes uteis
function setarEstadoForca(estagio){
    img_caminho = 'static\\forca\\'  + 'forca' +elemento.dataset.escolha +'.png';
    return elemento.dataset.escolha;
}

function atualizar_dados_rodada(palavra_atual, erros){
    // alterando a mensagem de aviso que aparece depois de cada rodada
    palavra_atual.innerText = palavra_atual
    estado_forca.src = 'static\\forca\\'+"forca"  + erros +'.png'
  
   

}

/*function mostar_mensagem_vitoria(vencedor){
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
    */
async function mandar_escolha_player(letra_escolhida){
    console.log(letra_escolhida)
    const post_data = {
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({escolha_player : letra_escolhida})
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
        atualizar_dados_rodada(data.letras_descobertas,data.erros)
      
    }
}




 
