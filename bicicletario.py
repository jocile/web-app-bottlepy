"""
João tem uma bicicletaria e deseja um programa para registrar e exibir 
as bicicletas vendidas. 
Cada bicicleta possui características próprias e é capaz de executar 
alguns comportamentos básicos.

Características (Atributos): Cor, modelo, ano e valor.
Comportamentos (Métodos): Buzinar, parar e correr.
"""

class Bicicleta:
    numero = 1
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
        self.numero += 1

    def buzinar(self):
        print("Plim plim...")
 
    def parar(self):
        print("Bicicleta parada.")
 
    def correr(self):
        print("Vrummmmm!")

    def __str__(self):
        return f'Cor: {self.cor}, modelo: {self.modelo}, ano: {self.ano}, valor: {self.valor}'

'''
# Instanciando os objetos (criando bicicletas)
b1 = Bicicleta("Vermelha", "Caloi", 2022, 600)
b2 = Bicicleta("Verde", "Monark", 2000, 189)
 
# Chamando os comportamentos (métodos)
b1.buzinar()
b1.correr()
b1.parar()
 
# Acessando atributos diretamente
print(b1.cor) # Saída: Vermelha
print(b2.modelo) # Saída: Monark
'''

def menu():
    bicicletas = []
    bicicletas_vendidas = []
    while True:
        print('Escolha a opção:')
        print('1: Adicionar bicicleta')
        print('2: Mostrar informações da bicicleta')
        print('3: Ações da bicicleta')
        print('4: Vender uma bicicleta')
        print('5: Sair')
        opcao = input("Opcao: ")
        match opcao:
            case "1":
                cor = input('Qual a cor: ')
                modelo = input('Qual o modelo: ')
                ano = input('Qual o ano: ')
                valor = input('Qual o valor: ')
                bicicletas.append(Bicicleta(cor, modelo, ano, valor))
                print(f"Bicicleta número {len(bicicletas)} adicionada")
            case "2":
                num = int(input('Entre com o número da bicicleta: '))
                print(bicicletas[num-1])
            case "3":
                num = int(input('Entre com o número da bicicleta: '))
                bicicletas[num].buzinar()
                bicicletas[num].correr()
                bicicletas[num].parar()
            case "4":
                if not bicicletas:
                    print('Nenhuma bicicleta disponível para venda.')
                    continue

                for i, bicicleta in enumerate(bicicletas, start=1):
                    print(f'{i}: {bicicleta}')

                num = int(input('Entre com o número da bicicleta para vender: '))
                if 1 <= num <= len(bicicletas):
                    bicicleta = vender_bicicleta(
                        bicicletas, bicicletas_vendidas, num
                    )
                    print(f'Bicicleta vendida: {bicicleta}')
                else:
                    print('Número de bicicleta inválido.')
            case "5":
                break


def vender_bicicleta(bicicletas, bicicletas_vendidas, numero):
    """Move uma bicicleta do estoque para a lista de bicicletas vendidas."""
    bicicleta = bicicletas.pop(numero - 1)
    bicicletas_vendidas.append(bicicleta)
    return bicicleta


if __name__ == "__main__":
    menu()