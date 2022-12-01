## Execução

1. No terminal, abra o jogo com

```sh
py main.py
```

___

# To-Do

Roteiro original
disponível [aqui](https://docs.google.com/document/d/189AMDekPZeVRerxjPzfzko3lhdjk1klbzrnkBnuZqAE/edit?usp=sharing).

## Refatoração

- [ ] Singleton para as settings
    - [ ] Tirar variáveis soltas no meio do código que deveriam estar nos settings (tipo algumas soltas no UI.py da
      posição dos botões)
- [x] Alterar lógica de instanciação de sprites para algo mais intuitivo (refatorar a parte dos grupos)
- [x] Passar o enemy_obstacle_sprites e o player_obstacle_sprites para o singleton dos grupos (assim, não é necessário
  atualizar os grupos de cada inimigo individualmente)
- [x] Ajustar a classe da câmera
- [x] Renomear waves.py para wave_manager.py
- [x] Singleton para carregar todos os sprites de uma só vez.
- [x] Dividir melhor a ui.py
    - Criar uma pasta para os elementos da UI
- [ ] Arrumar a visibilidade dos atributos (transformar em privado) nas classes restantes
- [x] Tirar o Game do main.py e colocar ele em um arquivo próprio

## Coisas que faltam

- [ ] Sistema de save
- [ ] Adicionar os inimigos que já tem sprites
    - Criar a classe do inimigo no enemies, adicionar a classe no enemy_classes do wave_manager, adicionar o inimigo em
      algum spawn do wave.json de alguma sala
    - Dá pra usar o bat.py como referência
- [ ] Fazer outras salas
- [ ] Criar o menu inicial
- [ ] Criar o menu de pause

## Ajustes menores

- [ ] Fazer o player ser posicionado no meio do mapa ao bugar e sair da tela
- [ ] Adicionar uma animação de morte aos inimigos
    - Eu estava pensando em algo tipo uma explosãozinha
- [ ] Corrigir bug em que a luz do cajado não é destruída ao fazer dois ataques rapidamente
- [x] Corrigir bug em que o cajado é desenhado na frente dos tiles
- [x] Separar as classes Level e Room baseado no diagrama
    - O level só controlaria a room atual, e as rooms seriam responsáveis por criar e manter o mapa
- [x] Adicionar um crosshair para ajudar o Player a mirar
- [ ] Fazer os inimigos desviarem de paredes ao se movimentar em direção do Player
- [ ] Sugestão: uma outra opção para as Rooms seria, em vez de ter várias Rooms, ter uma só e recriar o mapa toda vez
  que o Player
  avança de sala, posicionando ele no "p" da nova sala

---

Nesse diretório, o grupo irá trabalhar em cima do primeiro protótipo do jogo.

A ideia do protótipo não é que ele seja uma versão demo do jogo completo, mas sim que o principal mecanismo do jogo
esteja implementado com certo grau de sucesso. Exemplo: em um jogo do tipo plataforma 2D, basta mostrar um retângulo
colidindo com objetos e saltando/destruindo com alguma comando do usuário. A interface gráfica (com sprites) é opcional
nessa etapa.
