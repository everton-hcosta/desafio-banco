from datetime import datetime
from abc import ABC, abstractmethod, classmethod

class Cliente:
    def __init__(self, endereco, contas):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"Nome: {self.nome}, Endereço: {self.endereco}"
    
class PessoaFisica:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

        @property
        def saldo(self):
            return self._saldo
        
        @property
        def nova_conta(cls, cliente, numero):
            return cls(cliente, numero)
        
        @property
        def sacar(self, valor, numero_saques, limite_saque, limite):
            if valor > self.saldo:
                print("Saldo insuficiente")

            elif valor > 0:
                self._saldo -= valor
                print("Saque realizado com sucesso!")
                return True
                # self._extrato.append(f"Saque: R${valor: .2f} | Data:{date.today().strftime('%d/%m/%Y')}")
                # self._numero_saques += 1
            else:
                print("Não foi possível executar a operação, o valor inserido é inválido")

            return False
        
        @property
        def depositar(self, valor, conta):
            if not conta:
                print("Conta não encontrada.")
                return False

            if valor > 0:
                self._saldo += valor
                print("Depósito realizado com sucesso!")
                return True
                # extrato.append(f"Depósito: R${valor_deposito: .2f} | Data:{date.today().strftime('%d/%m/%Y')}")

            else:
                print("O valor inserido é inválido")
                return False
        
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
               

def depositar(saldo, valor_deposito, extrato, /):
    if not usuario:
        print("Usuário não encontrado.")
        return

    if valor_deposito > 0:
        saldo += valor_deposito
        extrato.append(f"Depósito: R${valor_deposito: .2f} | Data:{date.today().strftime('%d/%m/%Y')}")

    else:
        print("O valor inserido é inválido")
        return
    return saldo, extrato

def extrato_bancario(saldo, /, *, extrato):
    print("Extrato".center(50, "="))

    for operacao in extrato:
        print(operacao)

    print(f"\nSaldo atual: R${saldo: .2f}")
    print("".center(50, "="))

def listar_usuarios(cpf=None):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    if cpf is None:
        print("Usuários cadastrados:".center(50, "="))
        for usuario in usuarios:
            print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Endereço: {usuario['endereco']}")
        print("".center(50, "="))
    else:   
        for usuario in usuarios:
            if usuario['cpf'] == cpf:
                return usuario

def listar_contas_correntes(numero_conta_buscada=None):
    if not contas_correntes:
        print("Nenhuma conta corrente cadastrada.")
        return

    if numero_conta_buscada is None:
        print("Contas correntes cadastradas:".center(50, "="))
        for conta in contas_correntes:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']}")
        print("".center(50, "="))
    else:
        for conta in contas_correntes:
            if conta['numero_conta'] == int(numero_conta_buscada):
                return conta

def sacar(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saque):

    if numero_saques >= limite_saque:
        print("Número máximo de saques diários atingido")
        return
    
    elif valor_saque > saldo:
        print("Saldo insuficiente")
        return

    elif valor_saque > limite:
        print("O saque é maior que o valor permitido")
        return

    elif valor_saque > 0:
        saldo -= valor_saque
        extrato.append(f"Saque: R${valor_saque: .2f} | Data:{date.today().strftime('%d/%m/%Y')}")
        numero_saques += 1
    else:
        print("Não foi possível executar a operação, o valor inserido é inválido")

    return saldo, extrato, numero_saques

def criar_usuario():
    try:
        # Solicita os dados do usuário
        print("Para criar seu usuário de acesso, preencha os campos a seguir:")
        nome = input("Informe o seu nome: ")
        data_nascimento = input("Informe a sua data de nascimento (dd/mm/aaaa): ")
        cpf = input("Informe o seu CPF (apenas números): ")
        endereco = input("Informe o seu endereço: ")

        # Verifica se todos os campos foram preenchidos
        if not nome or not data_nascimento or not cpf or not endereco:
            print("Todos os campos devem ser preenchidos")
            return
        
        # Verifica se o CPF já existe
        for usuario in usuarios:
            if usuario['cpf'] == cpf:
                print("CPF já cadastrado")
                return  

        # Retorna um dicionário com os dados do usuário
        return {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
    except ValueError as e:
        print(f"Erro ao criar usuário: {e}")
        return None

def criar_conta_corrente(agencia, numero_conta, usuario):
    # Retorna um dicionário com os dados da conta corrente
    return {
        "usuario": usuario["nome"],
        "cpf": usuario["cpf"],
        "numero_conta": numero_conta,
        "agencia": agencia,
        "saldo": 0.0,
        "extrato": [],
        "numero_saques": 0,
    }

menu = """

Bem-vindo ao BankMancer
Selecione uma operação:
[C] Criar conta corrente
[U] Criar usuário
[D] Depositar
[E] Extrato
[LC] Listar contas correntes
[LU] Listar usuários
[S] Sacar
[Q] Sair

=> """

# Variáveis iniciais
usuarios = []
agencia = "0001"
contas_correntes = []
indice_conta = 1
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao.upper() == "C":
        # Solicita os dados da conta corrente
        cpf = input("Informe o cpf do usuário: ")

        # Verifica se o CPF existe
        usuario = listar_usuarios(cpf)

        if not usuario:
            print("Usuário não encontrado. Por favor, crie um usuário antes de criar uma conta corrente.")
            continue
        
        try:
            conta_corrente = criar_conta_corrente(agencia, indice_conta, usuario)
            contas_correntes.append(conta_corrente)
            indice_conta += 1
            print(f"Conta corrente criada com sucesso! Número da conta: {conta_corrente['numero_conta']}")
        except ValueError as e:
            print(f"Erro ao criar conta corrente: {e}")

    elif opcao.upper() == "U":
        try:
            usuario = criar_usuario()

            if not usuario:
                continue

            # Adiciona o usuário à lista de usuários
            usuarios.append(usuario)
            print("Usuário criado com sucesso!")
        except ValueError as e:
            print(f"Erro ao criar usuário: {e}")

    elif opcao.upper() == "D":
        try:
            # Solicita os dados da conta corrente
            numero_conta = input("Informe o numero da conta: ")

            # Busca a conta corrente do usuário
            conta = listar_contas_correntes(numero_conta)

            if not conta:
                print("Número da conta não encontrado. Por favor, crie uma conta antes de realizar um depósito.")
                continue
        
            # Solicita o valor do depósito
            valor_deposito = float(input("Informe o valor que deseja depositar: ")) 

            if valor_deposito > 0:
                    # Chama a função depositar passando o saldo, valor_deposito e extrato
                    conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor_deposito, conta['extrato'])

                    print(f"O depósito no valor de R$ {valor_deposito: .2f} foi realizado com sucesso!\nSaldo atual: R$ {conta['saldo']: .2f}")
            else:
                print("O valor inserido é inválido")

        except ValueError:
            print("O valor inserido é inválido")
     
    elif opcao.upper() == "S":
        try:
            # Solicita os dados da conta corrente
            numero_conta = input("Informe o numero da conta: ")

            # Busca a conta corrente do usuário
            conta = listar_contas_correntes(numero_conta)

            if not conta:
                print("Número da conta não encontrado. Por favor, crie uma conta antes de realizar um depósito.")
                continue

            valor_saque = float(input("Informe o valor que deseja sacar: "))

            if valor_saque > 0:
                    conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(saldo=conta['saldo'], valor_saque=valor_saque, extrato=conta['extrato'], limite=limite, numero_saques=conta['numero_saques'], limite_saque=LIMITE_SAQUES)
                    print(f"O saque no valor de R$ {valor_saque: .2f} foi realizado com sucesso!\nSaldo atual: R$ {conta['saldo']: .2f}")
            else:
                print("Não foi possível executara operação, o valor inserido é inválido")
        except ValueError:
            print("O valor inserido é inválido")
        except TypeError:
            continue

    elif opcao.upper() == "E":
        try:
            # Solicita os dados da conta corrente
            numero_conta = input("Informe o numero da conta: ")

            # Busca a conta corrente do usuário
            conta = listar_contas_correntes(numero_conta)

            if not conta:
                print("Número da conta não encontrado. Por favor, crie uma conta antes de realizar um depósito.")
                continue

            extrato = conta['extrato']

            if extrato:
                extrato_bancario(conta['saldo'], extrato=extrato)
            else:
                print("Esta conta ainda não executou operações")  
        except ValueError:
            print("O valor inserido é inválido")
        except TypeError:
            continue

    elif opcao.upper() == "LC":
        listar_contas_correntes()

    elif opcao.upper() == "LU":
        listar_usuarios()

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")