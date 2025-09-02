
const URL_ALVO = '/forca';

// elementos do html
const estado_forca = document.getElementById('estagio_forca')
const palavra_atual = document.getElementById('palavra_descobrir')
const form_letra = document.getElementById('form_escolher_letra')
const div_vitoria = document.getElementById("v_div")
const msg_final = document.getElementById("msg_final")
const botao_novo_jogo  = document.getElementById("btn_jogar_novamente")
const label_erros = document.getElementById("erros")
const tentativas = document.getElementById("letras_tentadas")
// funcoes uteis
function setarEstadoForca(estagio){
    console.log(__dirname)
    img_caminho = 'forca\\static\\'  + 'forca' +elemento.dataset.escolha +'.png';
    return elemento.dataset.escolha;
}

function atualizar_dados_rodada(pa, erros, letras_tentadas){
    console.log("Atualizando dados!")
    console.log(letras_tentadas)
    // alterando a mensagem de aviso que aparece depois de cada rodada
    label_erros.innerText = "Erros: "+erros
    estado_forca.src = 'forca\\static\\'+"forca"  + erros +'.png'
    tentativas.innerText = "Tentativas: "+letras_tentadas.join(" ")
    if (!pa){return}
    palavra_atual.innerText = pa.replace(/(.)/g, "$1 ").trim(); // para que fique um espaço entre cada letra. Ex: b _ n _ n _ a (fica melhor no visual)

  
}

function mostrar_mensagem_vitoria(resultado_jogo, palavra_original){
    if (div_vitoria.style.display === 'none' || div_vitoria.style.display === ''){
        div_vitoria.style.display = 'block'
        botao_novo_jogo.style.display = 'none'
        if (resultado_jogo === "ganhou"){
            msg_final.innerText = "Você ganhou! A palavra original era: " + palavra_original;
            div_vitoria.style.backgroundColor = "green"
            botao_novo_jogo.style.display = 'block'
        }
        else{
            msg_final.innerText = "Você perdeu! A palavra original era: " + palavra_original;
            div_vitoria.style.backgroundColor = "red"
        }
        setTimeout(function() { // se setar direto, a animação de opacidade não ocorre, por isso a gente espera um pouco
            div_vitoria.style.opacity = "1"
        }, 0);
       
    }
    else{
        tentativas.innerText = ""
        div_vitoria.style.opacity = "0"
        botao_novo_jogo.style.display = "inline-block"
        div_vitoria.style.display = 'none'
    }
   
    
}

async function mandar_escolha_player(evento){
    evento.preventDefault()

    const dados = new FormData(this)
    const letra = dados.get("letraInput")
    console.log(letra)
    const post_data = {
        method:'POST',
        
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({escolha_player : letra})
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
            mostrar_mensagem_vitoria(data.resultado_jogo,data.palavra_original)
        }
        /* se não existir, os dados enviados 
        são só para atualizar o estado da rodada */
        console.log(data.letras_tentadas)
        atualizar_dados_rodada(data.letras_descobertas,data.erros,data.letras_tentadas)
      
    }
}

form_letra.addEventListener("submit",mandar_escolha_player)
botao_novo_jogo.addEventListener('click',function(){
    try{
        exibir_mensagem_vitoria()
    }catch(erro){
        console.log(erro)
    }
})

 
