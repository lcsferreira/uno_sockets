# Projeto UNO Multiplayer

Este é um projeto em Python para jogar o famoso jogo UNO com dois jogadores usando a biblioteca sockets para comunicação cliente-servidor. Ele também utiliza a biblioteca termcolor para uma melhor visualização das cartas no terminal.

## Requisitos

- Python 3.x
- Bibliotecas: socket e termcolor
  ## Como executar
- Altere a variável host para corresponder ao IP da máquina que será usada como servidor e a variável port para uma porta disponível.
- Execute python3 server.py para iniciar o servidor.
- Cada jogador precisa executar python3 client.py em sua própria máquina.
- Altere a variável host em client.py para corresponder ao IP do servidor e a variável port para uma porta diferente da do servidor.
- Conecte-se com outro jogador usando o software Hamachi ou outro método para conectar os IPs das máquinas.
- _Jogue o UNO!_

## Como jogar

O jogo UNO é um jogo de cartas em que os jogadores jogam cartas de suas mãos combinando cor ou número com a carta do topo da pilha. Os jogadores também podem jogar cartas de ação que afetam o próximo jogador. O objetivo é ficar sem cartas na mão antes do outro jogador.

## Agradecimentos

Este projeto foi inspirado em outros projetos de UNO multiplayer em Python disponíveis no GitHub. Ele foi criado para fins educacionais e de aprendizado. Se você encontrar erros ou tiver sugestões para melhorias, sinta-se à vontade para abrir um problema ou solicitação de pull request no repositório.
