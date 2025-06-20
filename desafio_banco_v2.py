from datetime import date

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

def listar_contas_correntes(usuario=None):
    if not contas_correntes:
        print("Nenhuma conta corrente cadastrada.")
        return

    if usuario is None:
        print("Contas correntes cadastradas:".center(50, "="))
        for conta in contas_correntes:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']}")
        print("".center(50, "="))
    else:
        for conta in contas_correntes:
            if conta['cpf'] == usuario['cpf']:
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
        # Solicita os dados da conta corrente
        cpf = input("Informe o cpf do usuário: ")

        # Verifica se o CPF existe
        usuario = listar_usuarios(cpf)

        if not usuario:
            print("Usuário não encontrado. Por favor, crie um usuário antes de criar uma conta corrente.")
            continue

         # Busca a conta corrente do usuário
        conta = listar_contas_correntes(usuario)

        # Solicita o valor do depósito
        valor_deposito = float(input("Informe o valor que deseja depositar: ")) 

        if valor_deposito > 0 and conta:
            try:
                # Chama a função depositar passando o saldo, valor_deposito e extrato
                conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor_deposito, conta['extrato'])

                print(f"O depósito no valor de R$ {valor_deposito: .2f} foi realizado com sucesso!\nSaldo atual: R$ {conta['saldo']: .2f}")
            except ValueError as e:
                print(f"Erro ao realizar depósito: {e}")
        else:
            print("O valor inserido é inválido")
     
    elif opcao.upper() == "S":
        # Solicita os dados da conta corrente
        cpf = input("Informe o cpf do usuário: ")

        usuario = listar_usuarios(cpf)

        if not usuario:
            print("Usuário não encontrado. Por favor, crie um usuário antes de realizar um saque.")
            continue

        # Busca a conta corrente do usuário
        conta = listar_contas_correntes(usuario)

        valor_saque = float(input("Informe o valor que deseja sacar: "))

        if valor_saque > 0 and usuario and conta:
            try:
                conta['saldo'], conta['extrato'], conta['numero_saques'] = sacar(saldo=conta['saldo'], valor_saque=valor_saque, extrato=conta['extrato'], limite=limite, numero_saques=conta['numero_saques'], limite_saque=LIMITE_SAQUES)
                print(f"O saque no valor de R$ {valor_saque: .2f} foi realizado com sucesso!\nSaldo atual: R$ {conta['saldo']: .2f}")
            except ValueError:
                continue
            except TypeError:
                continue
        else:
            print("Não foi possível executara operação, o valor inserido é inválido")  

    elif opcao.upper() == "E":
        # Solicita os dados da conta corrente
        cpf = input("Informe o cpf do usuário: ")

        # Verifica se o CPF existe
        usuario = listar_usuarios(cpf)

        if not usuario:
            print("Usuário não encontrado. Por favor, crie um usuário antes de criar uma conta corrente.")
            continue

         # Busca a conta corrente do usuário
        conta = listar_contas_correntes(usuario)

        extrato = conta['extrato']

        if extrato:
            extrato_bancario(conta['saldo'], extrato=extrato)
        else:
            print("Esta conta ainda não executou operações")  

    elif opcao.upper() == "LC":
        listar_contas_correntes()

    elif opcao.upper() == "LU":
        listar_usuarios()

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")