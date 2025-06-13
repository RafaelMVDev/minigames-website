div_img_player = document.getElementById('img_escolha_player')
const botoes_escolha = document.querySelectorAll('.select_div')

function setar_imagem(elemento){
img_caminho = 'static\\jokenpo\\'  +  elemento.dataset.escolha +'_img.png'
    div_img_player.src = img_caminho
}
botoes_escolha.forEach(function(botao){
    botao.addEventListener('click',function(){
        setar_imagem(botao)
    })
})
