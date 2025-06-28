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

    def __str__(self):
        return f"Cliente: {self.nome}, CPF: {self.cpf}, Data de Nascimento: {self.data_nascimento}, Endereço: {self.endereco}"

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

        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        #FIXME: Verificar as datas dos saques para garantir que não exceda o limite diário
        if numero_saques >= self.limite_saque:
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
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacoes(self, transacao):
        self._transacoes.append({
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
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacoes(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

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
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        print("Lista de Clientes:")
        for c in self.clientes:
            print(c)

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrado.")
            return
        
        print("Lista de Contas:")
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

    elif opcao.upper() == "D":
        # Solicita os dados do cliente
        cpf = input("Digite o CPF do cliente: ")
        cliente = next((c for c in banco.clientes if c.cpf == cpf), None)

        if not cliente:
            print("Usuário não encontrado.")
            continue

        if not cliente.contas:
            print("O cliente não possui contas.")
            continue

        try:
            if len(cliente.contas) == 1:
                conta = cliente.contas[0]
                print(f"Conta única encontrada: Agência: {conta.agencia}, Número: {conta.numero}")
            else:
                print("\nContas do cliente:")

                for i, conta in enumerate(cliente.contas):
                    print(f"[{i}] Agência: {conta.agencia}, Número: {conta.numero}")
                
                indice = int(input("Escolha uma das opções para realizar o depósito: "))
                conta = cliente.contas[indice]
        except (ValueError, IndexError):
            print("Conta inválida.")
            continue

        try:
            valor = float(input("Digite o valor a depositar: "))
            deposito = Deposito(valor)
            cliente.realizar_transacao(conta, deposito)
        except ValueError:
            print("Valor inválido.")
     
    elif opcao.upper() == "S":
        # Solicita os dados do cliente
        cpf = input("Digite o CPF do cliente: ")
        cliente = next((c for c in banco.clientes if c.cpf == cpf), None)

        if not cliente:
            print("Usuário não encontrado.")
            continue

        if not cliente.contas:
            print("O cliente não possui contas.")
            continue

        try:
            if len(cliente.contas) == 1:
                conta = cliente.contas[0]
                print(f"Conta única encontrada: Agência: {conta.agencia}, Número: {conta.numero}")
            else:
                print("\nContas do cliente:")

                for i, conta in enumerate(cliente.contas):
                    print(f"[{i}] Agência: {conta.agencia}, Número: {conta.numero}")

                indice = int(input("Escolha uma das opções para realizar o saque: "))
                conta = cliente.contas[indice]
        except (ValueError, IndexError):
            print("Conta inválida.")
            continue

        try:
            valor = float(input("Digite o valor do saque: "))
            saque = Saque(valor)
            cliente.realizar_transacao(conta, saque)
        except ValueError:
            print("Valor inválido.")

    elif opcao.upper() == "E":
        try:
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero == numero_conta), None)

            if not conta:
                print("Número da conta não encontrado.")
                continue

            extrato = conta.historico.transacoes

            if extrato:
                print("\nEXTRATO:")
                for transacao in extrato:
                    print(f"Data: {transacao['data']} | Tipo: {transacao['tipo']} | Valor: R$ {transacao['valor']:.2f}")
                print(f"Saldo atual: R$ {conta.saldo:.2f}")
            else:
                print("Esta conta ainda não executou operações.")
        except ValueError:
            print("O número da conta deve ser um número inteiro.")
        except TypeError:
            continue


    elif opcao.upper() == "LCC":
        banco.listar_contas()

    elif opcao.upper() == "LC":
        banco.listar_clientes()

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")