idade = int(input("Qual é a sua idade? "))
altura = float(input("Qual é a sua altura em metros? "))

if altura < 1.30:
    print("Você não pode entrar.")
else:
    if idade < 10:
        print("Você não pode entrar.")
    elif idade <= 12:
        print("Você pode entrar acompanhado de um adulto.")
    else:
        print("Você pode entrar sozinho!")
