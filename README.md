# Web App BottlePy

Este repositório contém pequenos exemplos de aplicações web em Python utilizando o microframework Bottle. O objetivo principal é demonstrar conceitos básicos de rotas, requisições HTTP (`GET` e `POST`), formulários, arquivos estáticos e orientação a objetos com o modelo de uma bicicletaria.

## 🚲 Sobre o projeto

O projeto é de caráter didático e foi construído para praticar:

- criação de páginas web com Bottle
- uso de rotas e métodos HTTP
- processamento de formulários
- manipulação de parâmetros via query string e formulário
- uso de arquivos estáticos (`CSS` e imagens)
- implementação de classes em Python para representar objetos reais

## 📁 Estrutura do repositório

```text
web-app-bottlepy/
├── .gitignore
├── bottle.py                 # Biblioteca Bottle incluída no projeto
├── bicicletario.py           # Classe Bicicleta e menu interativo em console
├── bicicletarioweb.py        # Aplicação web da bicicletaria
├── metodoget.py              # Exemplo de rota GET
├── metodopost.py             # Exemplo de rota POST e formulário
├── exemploComImagem.py       # Exemplo com imagem estática
├── static/
│   ├── image.png
│   └── style.css
└── README.md
```

## 🧩 Descrição dos arquivos

### `bicicletario.py`
Armazena a classe `Bicicleta`, com atributos como cor, modelo, ano e valor, além dos métodos `buzinar()`, `parar()` e `correr()`. Também contém um menu interativo em terminal para adicionar bicicletas e simulá-las.

### `bicicletarioweb.py`
Aplicação web que usa Bottle para criar uma interface inicial de uma bicicletaria, permitindo cadastro de bicicletas e navegação entre páginas.

### `metodoget.py`
Exemplo simples de página em Bottle que recebe um parâmetro na URL e altera a cor de fundo da página.

### `metodopost.py`
Exemplo de formulário com método `POST`, onde os dados do usuário são enviados para uma rota de processamento e exibidos na resposta.

### `exemploComImagem.py`
Demonstra o uso de arquivos estáticos em Bottle, incluindo uma imagem e um arquivo CSS.

### `static/`
Pasta contendo recursos estáticos usados nos exemplos web.

## ▶️ Como executar

Certifique-se de ter o Python 3 instalado.

### 1. Clone o repositório

```bash
git clone https://github.com/profjocile/web-app-bottlepy.git
cd web-app-bottlepy
```

### 2. Execute um dos exemplos

```bash
python metodoget.py
```

ou

```bash
python metodopost.py
```

ou

```bash
python bicicletarioweb.py
```

Depois, abra no navegador:

```text
http://localhost:8080
```

## 🛠️ Dependências

O projeto usa a biblioteca Bottle, que já está incluída no repositório como `bottle.py`. Não é necessário instalar dependências extras para rodar os exemplos básicos.

## 📝 Observações

- Este projeto é educacional e foi desenvolvido para fins de aprendizagem.
- Os exemplos são simples e podem servir como base para aplicações web mais completas.
- O uso de arquivos estáticos e formulários é uma boa introdução ao desenvolvimento web com Python.

## 👨‍💻 Autor

Projeto desenvolvido por profjocile.

## 📌 Licença

Este projeto não contém uma licença explícita no repositório. Se for usar em ambiente acadêmico ou profissional, verifique antes de publicar ou redistribuir o código.

## Atualizações

[Atualizações](Atualizacoes.md)
