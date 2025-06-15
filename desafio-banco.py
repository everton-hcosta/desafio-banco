from datetime import date
menu = """

[D] Depositar
[S] Sacar
[E] Extrato
[Q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao.upper() == "D":
        valor_deposito = float(input("Informe o valor que deseja depositar: ")) 

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato.append(f"Depósito: R${valor_deposito: .2f} | Data:{date.today().strftime("%d/%m/%Y")}")
        else:
            print("O valor inserido é inválido")
     

    elif opcao.upper() == "S":

        if numero_saques >= LIMITE_SAQUES:
            print("Limite de saques diários excedido")
            continue

        valor_saque = float(input("Informe o valor que deseja sacar: "))

        if valor_saque > saldo:
            print("Saldo insuficiente")

        elif valor_saque > limite:
            print("O saque é maior que o valor permitido")

        elif valor_saque > 0:

            saldo -= valor_saque
            extrato.append(f"Saque: R${valor_saque: .2f} | Data:{date.today().strftime("%d/%m/%Y")}")
            numero_saques += 1

        else:
            print("Não foi possível executara operação, o valor inserido é inválido")  

    elif opcao.upper() == "E":

        if extrato:
            print("Extrato".center(50,"="))

            for operacoes in extrato:
                print(operacoes)
            
            print("".center(50,"="))            
            print(f"\nSaldo: R$ {saldo: .2f}\n")
            print("".center(50,"=")) 

        else:
            print("Esta conta ainda não executou operações")  

    elif opcao.upper() == "Q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")