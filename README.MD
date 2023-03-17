# Projeto UNO Multiplayer

Este é um projeto em Python para jogar o famoso jogo UNO com dois jogadores usando a biblioteca sockets para comunicação cliente-servidor. Ele também utiliza a biblioteca termcolor para uma melhor visualização das cartas no terminal.

## Requisitos

- Python 3.x
- Bibliotecas: socket e termcolor
  ## Comandos para instalação
  ```sh
  pip install termcolor
  ```
  ```sh
  pip install socket
  ```

## Como executar

- Altere a variável _'HOST'_ para corresponder ao IP da máquina que será usada como servidor e a variável _'PORT'_ para uma porta disponível.
- Execute o comando abaixo para iniciar o servidor.
  ```sh
  python3 server.py
  ```
- Cada jogador precisa executar o comando abaixo em sua própria máquina.
  ```sh
  python3 client.py
  ```
- Altere a variável _'HOST'_ em client.py para corresponder ao IP do servidor e a variável _'PORT'_ para uma porta diferente da do servidor.
- Conecte-se com outro jogador usando o software _Hamachi_ ou outro método para conectar os IPs das máquinas.
- _Jogue o UNO!_

## Como jogar

O jogo UNO é um jogo de cartas em que os jogadores jogam cartas de suas mãos combinando cor ou número com a carta do topo da pilha. Os jogadores também podem jogar cartas de ação que afetam o próximo jogador. O objetivo é ficar sem cartas na mão antes do outro jogador.

## Agradecimentos

Este projeto foi inspirado em outros projetos de UNO multiplayer em Python disponíveis no GitHub. Ele foi criado para fins educacionais e de aprendizado. Se você encontrar erros ou tiver sugestões para melhorias, sinta-se à vontade para abrir um problema ou solicitação de pull request no repositório.
