import datetime
import os
from json import dump, dumps, load, loads

menu_inicio = """
LOGIN
=============
[a] - ENTRAR
[r] - CADASTRAR
[s] - SAIR
"""

menu = """
MENU
==============
[d] - DEPOSITO
[s] - SAQUE
[e] - EXTRATO
[c] - CRIAR NOVA CONTA
[q] - ENCERRAR
==============
"""

def pegar_string_nao_nula(texto):
    while True:
        try:
            string = input(texto)
            if not string.strip():
                raise ValueError("Valor não pode ser nulo")
            return string
        except Exception as e:
            print(f"ERRO: {e}")

def pegar_cpf():
    while True:
        try:
            cpf = pegar_string_nao_nula("CPF (apenas números): ")
            if not cpf.isdigit():
                raise ValueError("CPF INVÁLIDO. DIGITE APENAS NÚMEROS.")
            return cpf
        except Exception as erro:
            print(f"ERRO: {erro}")


def pegar_nascimento(texto):
    while True:
        try:
            valor = input(texto)
            for char in valor:
                if not char.isdigit() and char != '/':
                    raise ValueError("Only valid numbers accepted. DD/MM/YYYY")
            if int(valor[:2]) > 31:
                raise ValueError("Only valid numbers accepted. DD/MM/YYYY")
            if valor.count("/") == 0:
                if len(valor) != 8:
                    raise ValueError("Wrong format. DD/MM/YYYY")
                valor = list(valor)
                if len(valor) == 8:
                    valor.insert(2, "/")
                    valor.insert(5, "/")
                valor = "".join(valor)
            if valor.count("/") == 1:
                if valor.find("/") != 2 and valor.find("/") != 4:
                    raise ValueError("Wrong format. DD/MM/YYYY")
                if valor.find("/") == 2:
                    valor = list(valor)
                    valor.insert(5, "/")
                    valor = "".join(valor)
                if valor.find("/") == 4:
                    valor = list(valor)
                    valor.insert(2, "/")
                    valor = "".join(valor)
            return valor
        except Exception as e:
            print(f"ERRO: {e}")

def criar_usuario(cpf):
    try:
        nome = pegar_string_nao_nula("NOME: ")
        nascimento = pegar_nascimento("NASCIMENTO (dd/mm/aaaa): ")
        endereco = pegar_string_nao_nula("ENDEREÇO: ")
        pessoa = {"nome": nome,
               "cpf": cpf,
               "nascimento": nascimento,
               "endereco": endereco}
        return pessoa
    except Exception as e:
        print(f"ERRO: {e}")

def criar_conta(cpf, numero):
    agencia = "0001"
    numero += 1
    usuario = cpf
    conta = {"agencia": agencia,
             "numero": numero,
             "usuario": cpf}
    return conta

def deposito(valor, saldo, depositos, conta_ativa):
    dp = depositos.copy()
    if valor > 0:
        saldo += valor
        deposito = {"valor": valor,
                    "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ope": "+",
                    "conta": conta_ativa["numero"]}
        dp.append(deposito)
        print("DEPOSITO EFETUADO COM SUCESSO!")
    else:
        print("OCORREU UM ERRO E O DEPÓSITO NÃO FOI EFETUADO.")
    return saldo, dp

def contar_saques(saque, conta_ativa):
    contador = 0
    for saque in saques:
        now = datetime.datetime.now()
        dia = datetime.date(now.year, now.month, now.day)
        dia_saque_dt = datetime.datetime.strptime(saque["data"], "%d/%m/%Y %H:%M:%S")
        dia_saque = datetime.date(dia_saque_dt.year, dia_saque_dt.month, dia_saque_dt.day)
        if dia_saque == dia and saque["conta"] == conta_ativa["numero"]:
            contador += 1
    return contador

def saque(*, valor, saldo, saques, conta_ativa):
    sq = saques.copy()
    if contar_saques(sq, conta_ativa) >= 3:
        print("LIMITE DE SAQUES DIÁRIOS ATINGIDO")
    elif valor > LIMITE_SAQUE:
        print(f"VALOR LIMITE DE R$ {LIMITE_SAQUE:.2f} POR SAQUE EXCEDIDO")
    elif valor > saldo:
        print("SALDO INDISPONÍVEL PARA SAQUE")
    else:
        saldo -= valor
        saque_ = {"valor": valor,
                 "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                 "ope": "-",
                 "conta": conta_ativa["numero"]}
        sq.append(saque_)
        print("SAQUE EFETUADO COM SUCESSO.")
    return saldo, sq

def extrato(saldos, depositos, saques, conta_ativa):
    saldos.sort(key=lambda x : x["data"])
    depositos.sort(key=lambda x : x["data"])
    saques.sort(key=lambda x : x["data"])
    delta = datetime.timedelta(days=30)
    saldos_e = []
    extrato = []
    for saq in saques:
        if saq["conta"] == conta_ativa["numero"]:
            extrato.append(saq)
    for deposito in depositos:
        if deposito["conta"] == conta_ativa["numero"]:
            extrato.append(deposito)
    extrato.sort(key=lambda x : x["data"])
    for saldo in saldos:
        sald_data = datetime.datetime.strptime(saldo["data"], "%d/%m/%Y %H:%M:%S")
        if datetime.datetime.now() - delta <= sald_data <= datetime.datetime.now():
            if saldo["conta"] == conta_ativa["numero"]:
                saldos_e.append(saldo)
    saldos_e.sort(key=lambda x : x["data"])
    print(f"AG {conta_ativa['agencia']} - CC {conta_ativa['numero']}".rjust(29))
    for i in range(len(saldos_e) - 1):
        data = datetime.datetime.strptime(saldos_e[i]["data"], "%d/%m/%Y %H:%M:%S")
        hoje = datetime.datetime.now()
        valor = saldos_e[i]["valor"]
        prox_data = datetime.datetime.strptime(saldos_e[i + 1]["data"], "%d/%m/%Y %H:%M:%S")
        prox_valor = saldos_e[i + 1]["valor"]
        data_ant = datetime.datetime(year=1991, month=11, day=4)
        if i > 0:
            data_ant = datetime.datetime.strptime(saldos_e[i - 1]["data"], "%d/%m/%Y %H:%M:%S")
        if i == 0 or ((data.day, data.month, data.year) != (data_ant.day, data_ant.month, data_ant.year)):
            print(f"{data.day:2}/{data.month}/{data.year}", end=" ")
            valor_str = f"{valor:.2f}"
            print(f"SALDO: R${valor_str.rjust(10)}")
        for operacao in extrato:
            data_op = datetime.datetime.strptime(operacao["data"], "%d/%m/%Y %H:%M:%S")
            valor_op = operacao["valor"]
            sinal = operacao["ope"]
            if data < data_op <= prox_data:
                print(f"{data_op.day:2}/{data_op.month}/{data_op.year}", end=" ")
                valor_op_str = f"{valor_op:.2f}"
                print(f"{sinal:>6} R${valor_op_str.rjust(10)}")
        if i == len(saldos_e) - 2:
            print(f"{prox_data.day:2}/{prox_data.month}/{prox_data.year}", end=" ")
            prox_valor_str = f"{prox_valor:.2f}"
            print(f"SALDO: R${prox_valor_str.rjust(10)}")

todos_saldos = []
depositos = []
saques = []
clientes = []
contas = []
saldos = []
if os.path.exists("saldos.json"):
    with open("saldos.json", "r") as file:
        todos_saldos = load(file)
if os.path.exists("saques.json"):
    with open("saques.json", "r") as file:
        saques = load(file)
if os.path.exists("depositos.json"):
    with open("depositos.json", "r") as file:
        depositos = load(file)
if os.path.exists("clientes.json"):
    with open("clientes.json", "r") as file:
        clientes = load(file)
if os.path.exists("contas.json"):
    with open("contas.json", "r") as file:
        contas = load(file)
LIMITE_SAQUE = 500.00
numero_ultima_conta = 0
if contas:
    numero_ultima_conta = contas[-1].get("numero", 0)
lista_cpf = [cliente["cpf"] for cliente in clientes] if clientes else []
conta_ativa = {}
contas_cliente = []
saldo = 0
while True:
    try:
        if os.path.exists("saldos.json"):
            with open("saldos.json", "r") as file:
                todos_saldos = load(file)
        if os.path.exists("saques.json"):
            with open("saques.json", "r") as file:
                saques = load(file)
        if os.path.exists("depositos.json"):
            with open("depositos.json", "r") as file:
                depositos = load(file)
        if os.path.exists("clientes.json"):
            with open("clientes.json", "r") as file:
                clientes = load(file)
        if os.path.exists("contas.json"):
            with open("contas.json", "r") as file:
                contas = load(file)
        print(menu_inicio)
        op_inicio = input("ESCOLHA UMA OPÇÃO: ")
        if op_inicio.lower() == 'a':
            if clientes:
                cpf_inicio = pegar_cpf()
                if cpf_inicio in lista_cpf:
                    for cliente in clientes:
                        if cliente["cpf"] == cpf_inicio:
                            print("\nUSUÁRIO ENCONTRADO:")
                            print(f"{cliente['nome'].upper()} - {cliente['cpf']}\n")
                            break
                    contas_cliente = [conta for conta in contas if conta['usuario'] == cpf_inicio]
                    if len(contas_cliente) > 1:
                        print(f"{len(contas_cliente)} CONTAS ENCONTRADAS PARA {cliente['nome'].upper()}:")
                        for i, conta in enumerate(contas_cliente):
                            print(f"[{i}] - AGÊNCIA {conta['agencia']} - CC {conta['numero']}")
                        print("[s] - ENCERRAR")
                        opcao = input("CONTA A ACESSAR: ")
                        if opcao.lower() == 's':
                            break
                        elif not (0 <= int(opcao) <= len(contas_cliente) - 1):
                            raise ValueError("OPÇÃO INVÁLIDA.")
                        else:
                            conta_ativa = contas_cliente[int(opcao)]
                    else:
                        conta_ativa = contas_cliente[0]
                    for saldo in todos_saldos:
                        if saldo["conta"] == conta_ativa["numero"]:
                            saldos.append(saldo)
                    saldos.sort(key=lambda x : x["data"])
                    # for saldo in saldos:
                    #     print(saldo)
                    saldo = saldos[-1]["valor"]
                    while True:
                        try:
                            print(menu)
                            op = input("ESCOLHA UMA OPÇÃO: ")
                            if op.lower() == 'd':
                                valor = float(input("ENTRE O VALOR A DEPOSITAR: "))
                                saldo, depositos = deposito(valor, saldo, depositos, conta_ativa)
                                saldo_d = {"valor": saldo,
                                           "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                           "conta": conta_ativa["numero"]}
                                saldos.append(saldo_d)
                            elif op.lower() == 's':
                                valor = float(input("ENTRE O VALOR A SACAR: "))
                                saldo, saques = saque(valor=valor, saldo=saldo, saques=saques, conta_ativa=conta_ativa)
                                saldo_d = {"valor": saldo,
                                           "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                           "conta": conta_ativa["numero"]}
                                saldos.append(saldo_d)
                            elif op.lower() == 'e':
                                print("\nEXTRATO DOS ÚLTIMOS 30 DIAS")
                                print("-" * 30)
                                extrato(saldos, depositos, saques, conta_ativa)
                                print("-" * 30)
                            elif op.lower() == 'q':
                                print("OBRIGADO POR UTILIZAR O NOSSO SISTEMA! ATÉ A PRÓXIMA.")
                                break
                            elif op.lower() == 'c':
                                cpf = conta_ativa["usuario"]
                                confirma = input("CONFIRMA CRIAÇÃO DE NOVA CONTA? (s/n) ")
                                if confirma.strip().lower() == "s":
                                    nova_conta = criar_conta(cpf, numero_ultima_conta)
                                    numero_ultima_conta = nova_conta.get("numero", 0)
                                    pessoa = {}
                                    for cliente in clientes:
                                        if cliente["cpf"] == conta_ativa["usuario"]:
                                            pessoa = cliente
                                    print(f"NOVA CONTA - AGÊNCIA: {nova_conta['agencia']} CC: {nova_conta['numero']} - ASSOCIADA A {pessoa['nome'].upper()}.")
                                    contas.append(nova_conta)
                                    novo_saldo = {"valor": 0, "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "conta": nova_conta["numero"]}
                                    saldos.append(novo_saldo)
                            else:
                                print("POR FAVOR, ENTRE UMA OPÇÃO VÁLIDA: 'd', 's' ou 'e'.")
                        except ValueError as e:
                            print("POR FAVOR, INSIRA UM VALOR VÁLIDO")
                        except Exception as e:
                            print(f"ERRO: {e}")
                        # finally:
                        with open("saldos.json", "w") as file:
                            todos_saldos.extend(saldos)
                            dump(todos_saldos, file)
                        with open("saques.json", "w") as file:
                            dump(saques, file)
                        with open("depositos.json", "w") as file:
                            dump(depositos, file)
                    saldos = []
                    saques = []
                    depositos = []
                else:
                    raise ValueError("USUÁRIO NÃO ENCONTRADO.")
            else:
                raise ValueError("NENHUM CLIENTE CADASTRADO.")
        elif op_inicio.lower() == 'r':
            cpf = pegar_cpf()
            if cpf in lista_cpf:
                raise ValueError("USUÁRIO JÁ CADASTRADO.")
            novo_cliente = criar_usuario(cpf)
            clientes.append(novo_cliente)
            lista_cpf = [cliente["cpf"] for cliente in clientes] if clientes else []
            print(f"CRIAÇÃO DE CONTA PARA {novo_cliente['nome'].upper()} FEITA COM SUCESSO!\n")
            nova_conta = criar_conta(cpf, numero_ultima_conta)
            contas.append(nova_conta)
            print(f"DADOS DA CONTA: Agência {nova_conta['agencia']} - CC {nova_conta['numero']}")
            numero_ultima_conta = nova_conta.get("numero", 0)
            saldos = [{"valor": 0, "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "conta": nova_conta["numero"]},]
        elif op_inicio.lower() == 's':
            print("ATÉ A PRÓXIMA!")
            break
        else:
            raise ValueError("ESCOLHA UMA OPÇÃO VÁLIDA.")
    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        if clientes:
            with open("clientes.json", "w") as file:
                dump(clientes, file)
        if contas:
            with open("contas.json", "w") as file:
                dump(contas, file)
        with open("saldos.json", "w") as file:
            todos_saldos.extend(saldos)
            dump(todos_saldos, file)
