## Execução

1. No terminal, abra o jogo com
```sh
py main.py
```

___
# To-Do
## Refatoração
- 
- [ ] Singleton para as settings
  - [ ] Tirar variáveis soltas no meio do código que deveriam estar nos settings (tipo algumas soltas no UI.py da posição dos botões)
- [ ] Renomear waves.py para wave_manager.py
- [ ] Singleton para carregar todos os sprites de uma só vez.
- [ ] Dividir melhor a ui.py
  - Criar uma pasta para os elementos da UI
- [ ] Tirar o Game do main.py e colocar ele em um arquivo próprio
- [ ] Alterar lógica de instanciação de sprites para algo mais intuitivo
___

# To-Do para o protótipo

Roteiro original
disponível [aqui](https://docs.google.com/document/d/189AMDekPZeVRerxjPzfzko3lhdjk1klbzrnkBnuZqAE/edit?usp=sharing).

## Inimigos

- [x] Criar a classe Enemy e um inimigo básico
- Dá pra se basear bastante na classe Player. O inimigo seria uma Entity com um funcionamento parecido com o Player, mas
  em vez de se mover pelo teclado, seria um algoritmo que realiza o movimento e decide atacar
    - [x] Interação entre o player e os inimigos
        - [x] Fazer o EnemyDamageArea dar dano nos inimigos
        - ~~[ ] Criar o PlayerDamageArea~~
        - ~~[ ] Fazer o PlayerDamageArea dar dano no Player~~
    - etc...

## Outras partes da gameplay que faltam

- [x] Fazer lógica de morte do Player
    - Usar a função check_death() do Enemy como referência
- [x] Ataque de dano em área
    - Criar uma nova classe que estende o Attack, configurar o create() dela (isto é, a parte que cria as DamageAreas no
      mapa), adicionar o ataque na lista de ataques definida no init do Player e a seleção no input()
    - Sugestão: remover o LineAttack e fazer o ataque em área como uma ult com cooldown longo utilizada ao pressionar Q
- [x] Sistema de experiência e níveis
    - Adicionar um atributo de exp ao Player e exp no Enemy. Quando o Enemy morrer, incrementar enemy.exp em player.exp.
    - Talvez, seja possível fazer isso no check_death() do Enemy, mas será necessário mover ele para o enemy_update()
      para receber o parâmetro player, colocar o player no check_death() e chamar uma função para incrementar o exp do
      Player quando o Enemy morrer.
    - Acredito que seria legal fazer que, a cada nível, o player ganha um ponto de upgrade que permite ele comprar algum
      upgrade.
- [x] Upgrades
    - Alguns upgrades estão listados no roteiro
    - Os upgrades, de uma maneira geral, vão ter uma função que altera um atributo do Player quando chamada. Essa função
      vai ser chamada somente uma vez ao adquirir o upgrade
- [ ] ~~Fazer o flickering do Player e do Enemy serem brancos em vez de transparente~~
    - ~~Precisa mudar a parte que confere o self.vulnerable e altera o alpha no animate() do Player e do Enemy.
      Conferir [este vídeo aqui](https://www.youtube.com/watch?v=uW3Fhe-Vkx4) sobre como fazer uma máscara.~~
- [ ] ~~Dash do Player~~
    - Sugestão: substituir pelo SliceAttack?
    - Funcionamento descrito no roteiro

## Outros ajustes

- [x] Separar as classes Level e Room baseado no diagrama
    - O level só controlaria a room atual, e as rooms seriam responsáveis por criar e manter o mapa

- [ ] Arrumar a visibilidade dos atributos (transformar em privado) nas classes restantes

- [x] Adicionar um crosshair para ajudar o Player a mirar

- [ ] Fazer os inimigos desviarem de paredes ao se movimentar em direção do Player

- [ ] Sugestão: uma outra opção para as Rooms seria, em vez de ter várias Rooms, ter uma só e recriar o mapa toda vez que o Player
  avança de sala, posicionando ele no "p" da nova sala

- [ ] Fazer as outras classes que faltam do diagrama

# Não obrigatórios para o protótipo

## Sprites

Os sprites são feitos em uma resolução menor e aumentados em 4 vezes pra resultar em um jogo mais fluido. Por exemplo,
um sprite 16x16 é aumentado para 64x64

- [ ] Menus
- [ ] Ataques do player
- [ ] Player
- [ ] Mapa e seus obstáculos
- [ ] Inimigos
- [ ] HUD
- [ ] Power-ups
- [ ] Partículas
    - De maneira geral, só para decorar o jogo mesmo, fazendo partículas para a bola de fogo, para o cajado criando
      ataques, para os inimigos tomando dano e morrendo, etc...

## Save

- [ ] Sistema de save

---

Nesse diretório, o grupo irá trabalhar em cima do primeiro protótipo do jogo.

A ideia do protótipo não é que ele seja uma versão demo do jogo completo, mas sim que o principal mecanismo do jogo
esteja implementado com certo grau de sucesso. Exemplo: em um jogo do tipo plataforma 2D, basta mostrar um retângulo
colidindo com objetos e saltando/destruindo com alguma comando do usuário. A interface gráfica (com sprites) é opcional
nessa etapa.
