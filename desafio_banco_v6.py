import csv
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

# Variáveis iniciais
ROOT_PATH = Path(__file__).parent


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
        return (
            f"Cliente: {self.nome}, CPF: {self.cpf}, "
            f"Data de Nascimento: {self.data_nascimento}, "
            f"Endereço: {self.endereco}"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')>"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    @staticmethod
    def registrar_transacao(func):
        nomes_metodos = {
            "registrar": "Registro de Transação",
            "adicionar_conta": "Criação de Conta",
            "depositar": "Depósito",
            "sacar": "Saque",
        }

        def wrapper(*args, **kwargs):
            nome_metodo = func.__name__
            nome_amigavel = nomes_metodos.get(nome_metodo, nome_metodo.capitalize())
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            try:
                result = func(*args, **kwargs)

                with open(ROOT_PATH / "log.txt", "a") as log_file:
                    log_file.write(
                        f"[{data_hora}] Função '{func.__name__}' "
                        f"executada com argumentos "
                        f"'{repr(args)} e {repr(kwargs)}.' "
                        f"Retornou {repr(result)}\n"
                    )

            except FileNotFoundError as e:
                result = None
                with open(ROOT_PATH / "log.txt", "a") as log_file:
                    log_file.write(
                        f"[{data_hora}] Erro ao executar '{nome_amigavel}': "
                        f"Arquivo não encontrado. Detalhes: {e}"
                    )

                print(
                    f"[{data_hora}] Erro ao executar '{nome_amigavel}'. "
                    f"Veja mais detalhes do arquivo de log."
                )

            except PermissionError as e:
                result = None
                with open(ROOT_PATH / "log.txt", "a") as log_file:
                    log_file.write(
                        f"[{data_hora}] Erro ao executar '{nome_amigavel}': "
                        f"Permissão negada. Detalhes: {e}"
                    )
                print(
                    f"[{data_hora}] Erro ao executar '{nome_amigavel}'. "
                    f"Veja mais detalhes do arquivo de log."
                )

            print(f"[{data_hora}] Transação: {nome_amigavel}")
            return result

        return wrapper

    def adicionar_transacoes(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def gerar_transacoes(self, tipo=None):
        for transacao in self._transacoes:
            if tipo is None or transacao["tipo"].lower() == tipo.lower():
                yield transacao


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.limite_transacoes = 10
        self._historico = Historico()

    @Historico.registrar_transacao
    def sacar(self, valor):
        hoje = datetime.now().date()
        numero_transacoes = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if datetime.strptime(transacao["data"], "%d/%m/%Y %H:%M:%S").date()
                == hoje
            ]
        )

        if numero_transacoes >= self.limite_transacoes:
            print("Número máximo de transações diárias atingido")
        elif valor > self._saldo:
            print("Saldo insuficiente")
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Valor inválido")
        return False

    @Historico.registrar_transacao
    def depositar(self, valor):
        hoje = datetime.now().date()
        numero_transacoes = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if datetime.strptime(transacao["data"], "%d/%m/%Y %H:%M:%S").date()
                == hoje
            ]
        )

        if numero_transacoes >= self.limite_transacoes:
            print("Número máximo de transações diárias atingido")
        elif valor > 0:
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

        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

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
        return (
            f"Agência {self.agencia} - Conta Corrente "
            f"{self.numero} - Cliente: {self.cliente.nome}"
        )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}: "
            f"('{self.agencia}', "
            f"'{self.numero}', "
            f"'{self.cliente.nome}')>"
        )


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


class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._indice >= len(self._contas):
            raise StopIteration

        conta = self._contas[self._indice]
        self._indice += 1

        return {
            "número": conta.numero,
            "agência": conta.agencia,
            "cliente": conta.cliente.nome,
            "saldo": conta.saldo,
        }


class Banco:
    def __init__(self):
        self.clientes = self.carregar_clientes()
        self.contas = self.carregar_contas()
        self.indice_conta = len(self.contas) + 1 if self.contas else 1

    def carregar_clientes(self):
        clientes = []
        caminho = ROOT_PATH / "clientes.csv"

        if not caminho.exists():
            return clientes  # Arquivo ainda não existe

        with open(caminho, mode="r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                nome = linha.get("Nome")
                cpf = linha.get("CPF")
                data_nascimento = linha.get("Data de Nascimento")
                endereco = linha.get("Endereço")

                cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
                clientes.append(cliente)

        return clientes

    def carregar_contas(self):
        caminho = ROOT_PATH / "contas.csv"
        contas = []

        if not caminho.exists():
            return contas

        with open(caminho, mode="r", newline="", encoding="utf-8") as arquivo:
            reader = csv.DictReader(arquivo)
            for linha in reader:
                cliente = self.buscar_cliente_por_cpf(linha["CPF"])
                if cliente:
                    conta = ContaCorrente(
                        numero=int(linha["Número"]),
                        cliente=cliente,
                        limite=float(linha.get("Limite", 500)),
                        limite_saque=int(linha.get("Limite Saque", 3)),
                    )
                    contas.append(conta)
        return contas

    @Historico.registrar_transacao
    def adicionar_cliente(self, cliente):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if any(c.cpf == cliente.cpf for c in self.clientes):
            print("Cliente já cadastrado.")
            return False

        try:
            caminho = ROOT_PATH / "clientes.csv"
            escrever_cabecalho = not caminho.exists()

            with open(caminho, mode="a", newline="", encoding="utf-8") as arquivo:
                writer = csv.writer(arquivo)

                if escrever_cabecalho:
                    writer.writerow(["Nome", "CPF", "Data de Nascimento", "Endereço"])

                writer.writerow(
                    [
                        cliente.nome,
                        cliente.cpf,
                        cliente.data_nascimento,
                        cliente.endereco,
                    ]
                )

            self.clientes.append(cliente)  # <- Adiciona à lista em memória
            print("Cliente adicionado com sucesso.")

        except FileNotFoundError as e:
            with open(ROOT_PATH / "log.txt", "a") as log_file:
                log_file.write(
                    f"[{data_hora}] Erro ao salvar cliente: "
                    f"Arquivo não encontrado. Detalhes: {e}"
                )

            print(
                f"[{data_hora}] Erro ao salvar cliente. "
                f"Veja mais detalhes do arquivo de log."
            )

        except PermissionError as e:
            with open(ROOT_PATH / "log.txt", "a") as log_file:
                log_file.write(
                    f"[{data_hora}] Erro ao salvar cliente: "
                    f"Permissão negada. Detalhes: {e}"
                )
            print(
                f"[{data_hora}] Erro ao salvar cliente. "
                f"Veja mais detalhes do arquivo de log."
            )

        return True

    @Historico.registrar_transacao
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        conta.cliente.adicionar_conta(conta)
        self.indice_conta += 1
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            caminho = ROOT_PATH / "contas.csv"
            file_exists = caminho.exists()

            with open(caminho, mode="a", newline="", encoding="utf-8") as arquivo:
                writer = csv.writer(arquivo)
                if not file_exists:
                    writer.writerow(
                        ["Número", "Agência", "CPF", "Limite", "Limite Saque"]
                    )
                writer.writerow(
                    [
                        conta.numero,
                        conta.agencia,
                        conta.cliente.cpf,
                        conta.limite,
                        conta.limite_saque,
                    ]
                )
            print(f"Conta {conta.numero} criada com sucesso.")
        except FileNotFoundError as e:
            with open(ROOT_PATH / "log.txt", "a") as log_file:
                log_file.write(
                    f"[{data_hora}] Erro ao salvar conta: "
                    f"Arquivo não encontrado. Detalhes: {e}"
                )

            print(
                f"[{data_hora}] Erro ao salvar conta. "
                f"Veja mais detalhes do arquivo de log."
            )

        except PermissionError as e:
            with open(ROOT_PATH / "log.txt", "a") as log_file:
                log_file.write(
                    f"[{data_hora}] Erro ao salvar conta: "
                    f"Permissão negada. Detalhes: {e}"
                )
            print(
                f"[{data_hora}] Erro ao salvar conta. "
                f"Veja mais detalhes do arquivo de log."
            )

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

    def iterar_contas(self):
        return ContaIterador(self.contas)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


menu = """

Bem-vindo ao BankMancer
Selecione uma operação:
[C] Criar conta corrente
[CC] Criar cliente
[D] Depositar
[E] Extrato
[IC] Listar contas
[LCC] Listar contas correntes
[LC] Listar clientes
[LT] Listar transações
[S] Sacar
[Q] Sair

=> """

banco = Banco()

while True:

    opcao = input(menu)

    if opcao.upper() == "C":
        # Solicita os dados da conta corrente
        cpf = input("Informe o CPF do cliente: ")

        # Verifica se o CPF existe
        cliente = banco.buscar_cliente_por_cpf(cpf)

        if not cliente:
            print(
                "Cliente não encontrado. Por favor, crie um cliente antes de criar uma conta corrente."
            )
            continue

        try:
            banco.adicionar_conta(
                conta=ContaCorrente(numero=banco.indice_conta, cliente=cliente)
            )
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
                print(
                    f"Conta única encontrada: Agência: "
                    f"{conta.agencia}, Número: {conta.numero}"
                )
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
                print(
                    f"Conta única encontrada: "
                    f"Agência: {conta.agencia}, Número: {conta.numero}"
                )
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
                    print(
                        f"Data: {transacao['data']} "
                        f"| Tipo: {transacao['tipo']} "
                        f"| Valor: R$ {transacao['valor']:.2f}"
                    )
                print(
                    f"\nQuantidade de transações realizadas hoje, "
                    f"{datetime.today().date().strftime('%d/%m/%Y')}: {len(extrato)}"
                    f"\nSaldo atual: R$ {conta.saldo:.2f}"
                )
            else:
                print("Esta conta ainda não executou operações.")
        except ValueError:
            print("O número da conta deve ser um número inteiro.")
        except TypeError:
            continue

    elif opcao.upper() == "IC":
        if not banco.contas:
            print("Nenhuma conta cadastrada.")
            continue

        print("Lista de Contas:")
        for conta in banco.iterar_contas():
            print(
                f"Número: {conta['número']}, Agência: {conta['agência']}, "
                f"Cliente: {conta['cliente']}, Saldo: R$ {conta['saldo']:.2f}"
            )

    elif opcao.upper() == "LCC":
        banco.listar_contas()

    elif opcao.upper() == "LC":
        banco.listar_clientes()

    elif opcao.upper() == "LT":
        cpf = input("Informe o CPF do cliente: ")
        cliente = banco.buscar_cliente_por_cpf(cpf)

        if not cliente:
            print("Cliente não encontrado.")
            continue

        if not cliente.contas:
            print("O cliente não possui contas.")
            continue

        try:
            if len(cliente.contas) == 1:
                conta = cliente.contas[0]
                print(
                    f"Conta única encontrada: Agência: {conta.agencia}, Número: {conta.numero}"
                )
            else:
                print("\nContas do cliente:")
                for i, c in enumerate(cliente.contas):
                    print(f"[{i}] Agência: {c.agencia}, Número: {c.numero}")

                indice = int(input("Escolha uma conta para listar as transações: "))
                conta = cliente.contas[indice]
        except (ValueError, IndexError):
            print("Conta inválida.")
            continue

        tipo_transacao = (
            input(
                "Informe o tipo de transação "
                "(Saque, Depósito, Registro de Transação, Criação de Conta): "
            )
            .strip()
            .lower()
        )

        print("\nTransações encontradas:")
        for t in conta.historico.gerar_transacoes(tipo=tipo_transacao):
            print(f"Data: {t['data']} | Tipo: {t['tipo']} | Valor: R$ {t['valor']:.2f}")

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
