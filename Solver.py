

class Solver():

    def __init__(self):
        pass

    # Definicao das variaveis
    num_variaveis = 0
    num_restricoes = 0
    coef_func_obj = []
    restricoes = dict()

    def le_instancia(self, arquivo):
        
        try:
            # Tentamos abrir o arquivo para leitura
            fileOpened = True
            arquivo = open("entradas/"+arquivo, 'r')

        #Tratamento de erros de leitura do arquivo 'entrada.txt'
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
            fileOpened = False
        except PermissionError:
            print("Você não tem permissão para ler o arquivo.")
            fileOpened = False
        except Exception as e:
            print("Ocorreu um ERRO durante a leitura do arquivo:", str(e))
            fileOpened = False

        if fileOpened == False:
            exit(-1)#retornamos -1 como erro

        print("\nDados de entrada lidos com sucesso!")

        linha1 = arquivo.readline()#lê a primeira linha do arquivo

        self.num_variaveis = int(linha1.split()[0])#numero de variaveis
        self.num_restricoes = int(linha1.split()[1])#numero de restrinções

        linha2 = arquivo.readline()#lê a segunda linha do arquivo
        valores = linha2.split()
        valFunObj = [int(val) for val in valores]#adiciona os valores int na lista, esses são os valores das Função Objetivo

        restrincoes = {} #cria um dicionario vazio para as restrinções

        for i in range(1, self.num_restricoes+1):#Vamos pegar os valores das N linhas relacionadas as restrinções
            linhas = arquivo.readline()
            ResValores = linhas.split()  
            restrincoes[f"Restrincoes{i}"] = [int(val) for val in ResValores]

        self.coef_func_obj = valFunObj
        self.restricoes = restrincoes
        print(self.num_variaveis)
        print(self.num_restricoes)
        print(valFunObj)
        print(restrincoes)

        arquivo.close() #fechamos o arquivo

    def resolver(self):
        print("Bem vindo, vamos começar lendo os dados de entrada!")
        nome_do_arquivo = input("Informe o nome do arquivo da instancia: ")

        self.le_instancia(nome_do_arquivo)

        

    