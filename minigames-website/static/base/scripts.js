const botoes_jogar = document.getElementsByClassName('btn-jogar');

console.log(botoes_jogar.length)
function emJogarApertado(botao){
    rota = botao.dataset.rota
    console.log("Oiiiii")
    if (rota){
        console.log("TEM ROTA!!")
        window.location.href = "/" + rota
    }
    
}

for (i=0; i<botoes_jogar.length; i++){
    const botao = botoes_jogar[i]
    botao.addEventListener('click',function(){
        try{
             emJogarApertado(botao);
        }catch(erro){
            console.log(erro)
        }
    
    })
}
