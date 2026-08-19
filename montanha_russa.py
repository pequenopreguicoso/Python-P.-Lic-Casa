#Projeto de lição de casa na Kodland

print("=" * 45)
print("---Bem-vindo à montanha russa!---")
print("=" * 45)

print(" ")

idade = int(input("Qual é a sua idade? "))
print(" ")
altura = float(input("Qual é a sua altura em metros? "))

if altura < 1.30:
    print(" ")
    print("Você não pode entrar.")
else:
    if idade < 10:
        print(" ")
        print("Você não pode entrar.")
    elif idade <= 12:
        print(" ")
        print("Você pode entrar acompanhado de um adulto.")
    else:
        print(" ")
        print("Você pode entrar sozinho!")
