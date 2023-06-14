from mip import *


class Solver():

    def __init__(self):
        pass

    # Definicao das variaveis
    num_variaveis = 0
    num_restricoes = 0
    coef_func_obj = []
    x = []
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
            restrincoes[i] = [int(val) for val in ResValores]

        self.coef_func_obj = valFunObj
        self.restricoes = restrincoes
        print(self.num_variaveis)
        print(self.num_restricoes)
        print(valFunObj)
        print(restrincoes)

        arquivo.close() #fechamos o arquivo

    def cria_modelo(self):
        model = Model(sense=MAXIMIZE, solver_name="CBC")

        self.x = [model.add_var(var_type=CONTINUOUS, lb=0, ub=1, name=f'x_{i}') for i in range(self.num_variaveis)]

        model.objective = xsum([self.coef_func_obj[i]*self.x[i] for i in range(self.num_variaveis)])

        for restr in range(self.num_restricoes):
            sum_expr = xsum([self.restricoes[restr+1][i]*self.x[i] for i in range(self.num_variaveis)])

            model += sum_expr <= self.restricoes[restr+1][self.num_variaveis]

        return model
    
    def branch_and_bound(self, model):
        fila = []  # Inicializa uma fila vazia
        melhor_solucao = None
        melhor_valor_obj = float('-inf')

        # Começa com o nó raiz (modelo original)
        fila.append(model)

        while fila:
            modelo_atual = fila.pop(0)  # Obtém o próximo modelo da fila

            # print(f'Tamanho da fila {len(fila)}\n')

            # Resolve o modelo atual
            modelo_atual.optimize()
            
            for var in modelo_atual.vars:
                print(f"{var.name}: {var.x}")

            # Se uma solução ótima for encontrada
            if modelo_atual.status == OptimizationStatus.OPTIMAL:
                valor_obj_atual = modelo_atual.objective_value

                # Cria modelos filhos ramificando em uma variável inteira
                # Pega o valor, multiplica por 10 e tira 5. O que for mais perto de 0 é o melhor valor
                menor_valor_variavel = 2    # As variáveis variam entre 0 e 1
                index_var_escolhida = -1
                for i,var in enumerate(modelo_atual.vars):
                    
                    if var.x.is_integer():
                        continue
                
                    valor_atual = abs(var.x - 0.5)
                    
                    if valor_atual < menor_valor_variavel:
                        menor_valor_variavel = valor_atual
                        index_var_escolhida = i

                if index_var_escolhida != -1 and valor_obj_atual > melhor_valor_obj:
                    modelo_filho0 = modelo_atual.copy()
                    modelo_filho0.add_constr(modelo_atual.vars[index_var_escolhida] == 0)
                    fila.append(modelo_filho0)

                    modelo_filho1 = modelo_atual.copy()
                    modelo_filho1.add_constr(modelo_atual.vars[index_var_escolhida] == 1)
                    fila.append(modelo_filho1)
                else:
                    # Atualiza a melhor solução se necessário
                    if valor_obj_atual > melhor_valor_obj:
                        melhor_solucao = modelo_atual
                        melhor_valor_obj = valor_obj_atual

        # Retorna a melhor solução encontrada
        return melhor_solucao
    
    def resolver(self):
        print("Bem-vindo! Vamos começar lendo os dados de entrada.")
        nome_do_arquivo = input("Informe o nome do arquivo da instância: ")

        self.le_instancia(nome_do_arquivo)

         # Cria o modelo de otimização nos padrões pedidos pelo projeto
        modelo = self.cria_modelo()

        # Aplica o branch and bound para encontrar a melhor solução
        melhor_solucao = self.branch_and_bound(modelo)

        if melhor_solucao:
            melhor_solucao.write("melhor_solucao.lp")  # Salva a melhor solução em um arquivo
            print("Melhor solução encontrada:")
            print(f"Valor objetivo: {melhor_solucao.objective_value}")
            print("Valores das variáveis:")
            for var in melhor_solucao.vars:
                print(f"{var.name}: {var.x}")
        else:
            print("Nenhuma solução viável encontrada.")
    