# Sistema Bancário

(PT-BR)
Esse projeto foi desenvolvido com a finalidade de criar funções de saque, depósito e visualização de extrato para a conta de clientes de um banco. É a resolução de um Desafio de Projeto proposto pelo Bootcamp de Ciência de Dados da [DIO](https://dio.me), por isso não utiliza banco de dados para armazenamento de dados, o que seria mais recomendado para a segurança dos dados.

### Feito com

[![Python](https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python)](https://docs.python.org/3/)

### Como usar

(PT-BR)
Para rodar o programa, abra o terminal e use o comando
`python app.py` . <br>
O usuário pode se cadastrar, criando assim uma conta corrente no banco. O usuário pode ter mais de 1 conta associada a seu CPF, é só entrar no sistema e escolher para criar uma nova conta. <br>
Se é a primeira vez rodando o programa, ele irá criar 3 arquivos na pasta raiz:
* `saldos.json` - armazena o histórico de saldo da conta;
* `depositos.json` - armazena o histórico de depósitos da conta;
* `saques.json` - armazena o histórico de saques da conta.
* `clientes.json` - armazena dados dos clientes do banco.
* `contas.json` - armazena dados das contas bancárias.
<br>
A aplicação em si apresenta 3 funções básicas: <br/>
 - **Realizar saque** - permite ao o usuário realizar saques, atualizando o valor do saldo posteriormente.
 - **Realizar depósito** - permite ao usuário realizar depósitos, atualizando então o saldo da conta.
 - **Visualização de extrato** - permite ao usuário visualizar todas as operações de saque e depósito da conta ativa ao longo dos últimos 30 dias.

### Screenshots

![MENU](https://i.imgur.com/PUUdLcx.png)
![EXTRATO](https://i.imgur.com/eOI8lww.png)

### Requirements

As dependências estão listadas no arquivo `requirements.txt` o qual o link é encontrado abaixo.

* [requirements.txt](https://github.com/jotapesp/)
