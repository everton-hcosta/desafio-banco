from datetime import datetime
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self._historico = Historico()

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Valor inválido")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Valor inválido")
            return False

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):

        numero_saques = len([transacao for transacao in self.historico.transacao if transacao['tipo'] == Saque.__name__])

        if numero_saques >= self.limite:
            print("Número máximo de saques diários atingido")
        
        elif valor > self.saldo:
            print("Saldo insuficiente")

        elif valor > self.limite:
            print("O saque é maior que o valor permitido")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"Agência {self.agencia} - Conta Corrente {self.numero} - Cliente: {self.cliente.nome}"
    
    
class Historico:
    def __init__(self):
        self.transacoes = []

    def transacoes(self):
        return self.transacoes

    def adicionar_transacoes(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacoes(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacoes(self)


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def adicionar_cliente(self, cliente):
        if any(c.cpf == cliente.cpf for c in self.clientes):
            print("Cliente já cadastrado.")
            return False
        self.clientes.append(cliente)
        print("Cliente adicionado com sucesso.")
        return True

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        conta.cliente.adicionar_conta(conta)
        print(f"Conta {conta.numero} criada com sucesso.")

    def buscar_cliente_por_cpf(self, cpf):
        return next((c for c in self.clientes if c.cpf == cpf), None)

    def listar_clientes(self):
        for c in self.clientes:
            print(c)

    def listar_contas(self):
        for c in self.contas:
            print(c)


menu = """

Bem-vindo ao BankMancer
Selecione uma operação:
[C] Criar conta corrente
[CC] Criar cliente
[D] Depositar
[E] Extrato
[LCC] Listar contas correntes
[LC] Listar clientes
[S] Sacar
[Q] Sair

=> """

# Variáveis iniciais
banco = Banco()
clientes = []
contas = []
contas_correntes = []
indice_conta = 1
saldo = 0
extrato = []
numero_saques = 0

while True:

    opcao = input(menu)

    if opcao.upper() == "C":
        # Solicita os dados da conta corrente
        cpf = input("Informe o CPF do cliente: ")

        # Verifica se o CPF existe
        cliente = banco.buscar_cliente_por_cpf(cpf)

        if not cliente:
            print("Cliente não encontrado. Por favor, crie um cliente antes de criar uma conta corrente.")
            continue
        
        try:
            banco.adicionar_conta(conta=ContaCorrente(numero=indice_conta, cliente=cliente))
            indice_conta += 1
        except ValueError as e:
            print(f"Erro ao criar conta corrente: {e}")

    elif opcao.upper() == "CC":
        print("Para criar um cliente, por favor, forneça as seguintes informações:")
        nome = input("Nome: ")
        data_nascimento = input("Data de nascimento: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")

        cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        banco.adicionar_cliente(cliente)

    # elif opcao.upper() == "D":
    #     cpf = input("Digite o CPF do cliente: ")
    #     cliente = next((c for c in clientes if c.cpf == cpf), None)

    #     if not cliente:
    #         print("Usuário não encontrado.")
    #         continue

    #     if not cliente.contas:
    #         print("O cliente não possui contas.")
    #         continue

    #     print("\nContas do cliente:")
    #     for i, conta in enumerate(cliente.contas):
    #         print(f"[{i}] Agência: {conta.agencia}, Número: {conta.numero}")

    #     try:
    #         indice = int(input("Escolha o número da conta para depósito: "))
    #         conta = cliente.contas[indice]
    #     except (ValueError, IndexError):
    #         print("Conta inválida.")
    #         continue

    #     try:
    #         valor = float(input("Digite o valor a depositar: "))
    #         deposito = Deposito(valor)
    #         cliente.realizar_transacao(conta, deposito)
    #     except ValueError:
    #         print("Valor inválido.")
     
    # elif opcao.upper() == "S":
    #     try:
    #         # Solicita os dados da conta corrente
    #         numero_conta = input("Informe o numero da conta: ")

    #         # Busca a conta corrente do usuário
    #         conta = listar_contas_correntes(numero_conta)

    #         if not conta:
    #             print("Número da conta não encontrado. Por favor, crie uma conta antes de realizar um depósito.")
    #             continue

    #         valor_saque = float(input("Informe o valor que deseja sacar: "))

    #         if valor_saque > 0:
    #                 conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(saldo=conta['saldo'], valor_saque=valor_saque, extrato=conta['extrato'], limite=limite, numero_saques=conta['numero_saques'], limite_saque=LIMITE_SAQUES)
    #                 print(f"O saque no valor de R$ {valor_saque: .2f} foi realizado com sucesso!\nSaldo atual: R$ {conta['saldo']: .2f}")
    #         else:
    #             print("Não foi possível executara operação, o valor inserido é inválido")
    #     except ValueError:
    #         print("O valor inserido é inválido")
    #     except TypeError:
    #         continue

    # elif opcao.upper() == "E":
    #     try:
    #         # Solicita os dados da conta corrente
    #         numero_conta = input("Informe o numero da conta: ")

    #         # Busca a conta corrente do usuário
    #         conta = listar_contas_correntes(numero_conta)

    #         if not conta:
    #             print("Número da conta não encontrado. Por favor, crie uma conta antes de realizar um depósito.")
    #             continue

    #         extrato = conta['extrato']

    #         if extrato:
    #             extrato_bancario(conta['saldo'], extrato=extrato)
    #         else:
    #             print("Esta conta ainda não executou operações")  
    #     except ValueError:
    #         print("O valor inserido é inválido")
    #     except TypeError:
    #         continue

    elif opcao.upper() == "LCC":
        banco.listar_contas()

    elif opcao.upper() == "LC":
        banco.listar_clientes()

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")