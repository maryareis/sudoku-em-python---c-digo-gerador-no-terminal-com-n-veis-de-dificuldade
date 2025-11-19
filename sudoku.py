import os
import random
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_fachada():
    limpar_tela()
    print("=" * 60)
    print("  ███████ ██    ██ ██████  ███████ ██  ██ ██   ██")
    print("  ██      ██    ██ ██   ██ ██   ██ ██ ██  ██   ██")
    print("  ███████ ██    ██ ██   ██ ██   ██ ████   ██   ██")
    print("       ██ ██    ██ ██   ██ ██   ██ ██ ██  ██   ██")
    print("  ███████  ██████  ██████  ███████ ██  ██  █████  ")
    print("=" * 60)
    print("            SUPER JOGO DE SUDOKU")
    print("-" * 60)
    print("Objetivo:")
    print("Complete o tabuleiro 9x9 com números de 1 a 9,")
    print("sem repetir em linhas, colunas e subgrades 3x3 (3x3).")
    print()
    input("Pressione Enter para iniciar o jogo...")


class SudokuBoard:
    
    DIFFICULTIES = {
        "1": {
            "nome": "Fácil",
            "board": [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
        },
        "2": {
            "nome": "Médio",
            "board": [
                [0, 0, 0, 6, 0, 0, 4, 0, 0],
                [7, 0, 0, 0, 0, 3, 6, 0, 0],
                [0, 0, 0, 0, 9, 1, 0, 8, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 5, 0, 1, 8, 0, 0, 0, 3],
                [0, 0, 0, 3, 0, 6, 0, 0, 0],
                [0, 0, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 3, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 9]
            ]
        },
        "3": {
            "nome": "Difícil",
            "board": [
                [0, 0, 0, 0, 0, 0, 0, 1, 2],
                [0, 0, 0, 0, 0, 5, 4, 0, 0],
                [0, 0, 0, 6, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 0],
                [0, 0, 3, 7, 0, 0, 6, 0, 0],
                [0, 7, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 8, 1, 0, 0]
            ]
        }
    }
    
    def __init__(self, difficulty_key):
        if difficulty_key not in self.DIFFICULTIES:
            raise ValueError("Dificuldade inválida.")
        
        initial_board = self.DIFFICULTIES[difficulty_key]["board"]
        self.initial_board = [row[:] for row in initial_board]
        self.current_board = [row[:] for row in initial_board]

    def imprimir(self):
        print("  | 1 2 3 | 4 5 6 | 7 8 9")
        print("--+-------+-------+-------+")
        for i in range(9):
            linha_str = f"{i+1} | "
            for j in range(9):
                valor = self.current_board[i][j]
                
                if self.initial_board[i][j] != 0:
                    linha_str += f"\033[1m{valor}\033[0m "
                else:
                    linha_str += f"{valor if valor != 0 else '.'} "
                
                if (j + 1) % 3 == 0 and j != 8:
                    linha_str += "| "
            
            print(linha_str)
            
            if (i + 1) % 3 == 0 and i != 8:
                print("--+-------+-------+-------+")
        print("--+-------+-------+-------+")

    def _get_coluna(self, coluna):
        return [self.current_board[i][coluna] for i in range(9)]

    def _get_subgrade(self, linha, coluna):
        inicio_linha = (linha // 3) * 3
        inicio_coluna = (coluna // 3) * 3
        subgrade = []
        for i in range(inicio_linha, inicio_linha + 3):
            for j in range(inicio_coluna, inicio_coluna + 3):
                subgrade.append(self.current_board[i][j])
        return subgrade

    def jogada_valida(self, linha, coluna, num):
        
        if num in self.current_board[linha]:
            return False 

        if num in self._get_coluna(coluna):
            return False

        if num in self._get_subgrade(linha, coluna):
            return False
            
        return True

    def verificar_vitoria(self):
        for i in range(9):
            for j in range(9):
                num = self.current_board[i][j]
                if num == 0:
                    return False

                if len(set(self.current_board[i])) != 9 or 0 in self.current_board[i]:
                    return False
                
                coluna = self._get_coluna(j)
                if len(set(coluna)) != 9 or 0 in coluna:
                    return False
                    
                if i % 3 == 0 and j % 3 == 0:
                    subgrade = self._get_subgrade(i, j)
                    if len(set(subgrade)) != 9 or 0 in subgrade:
                        return False
        
        return True

    def fazer_jogada(self, linha, coluna, num):
        if self.initial_board[linha][coluna] != 0:
            return "fixo"
        
        if self.jogada_valida(linha, coluna, num):
            self.current_board[linha][coluna] = num
            return "valida"
        else:
            return "invalida"


class SudokuGame:
    
    def __init__(self):
        self.tabuleiro = None
        self.history = []
        self.difficulty_key = None
    
    def _selecionar_dificuldade(self):
        limpar_tela()
        print("## Seleção de Dificuldade")
        print("-" * 30)
        
        difficulties_list = SudokuBoard.DIFFICULTIES.items()
        for key, info in difficulties_list:
            print(f"[{key}] - {info['nome']}")
        
        print("-" * 30)
        
        while True:
            choice = input("Digite o número da dificuldade (1, 2 ou 3): ").strip()
            if choice in SudokuBoard.DIFFICULTIES:
                return choice
            print("Seleção inválida. Tente novamente.")

    def _receber_jogada(self):
        while True:
            try:
                print("\nComandos: 'lin col num' para jogar (ex: 2 3 5), '0 0 0' para remover, 'menu' para opções.")
                entrada = input("Digite sua jogada: ").strip().lower()
                
                if entrada == 'menu':
                    return "menu"
                if entrada == 'sair':
                    return "sair"
                    
                partes = entrada.split()
                if len(partes) != 3:
                    raise ValueError
                    
                linha, coluna, numero = map(int, partes)
                
                if not (1 <= linha <= 9 and 1 <= coluna <= 9 and 0 <= numero <= 9):
                    print("Os valores devem estar entre 1 e 9 para linha/coluna e 0-9 para o número.")
                    continue
                
                return linha - 1, coluna - 1, numero
            
            except ValueError:
                print("Entrada inválida. Tente novamente no formato correto.")

    def _recomecar(self):
        if self.difficulty_key:
            initial_board = SudokuBoard.DIFFICULTIES[self.difficulty_key]["board"]
            self.tabuleiro.current_board = [row[:] for row in initial_board]
            self.history = []
            return True
        return False

    def _selecionar_nova_dificuldade(self):
        self.difficulty_key = self._selecionar_dificuldade()
        self.tabuleiro = SudokuBoard(self.difficulty_key)
        self.history = []

    def _ver_jogada_anterior(self):
        if not self.history:
            print("\nNão há jogadas anteriores registradas.")
            input("Pressione Enter para continuar...")
            return

        limpar_tela()
        print("## Jogada Anterior (Estado pré-última jogada)")
        print("-" * 50)
        
        previous_board_state = self.history[-1] 
        
        temp_board = SudokuBoard(self.difficulty_key)
        temp_board.current_board = previous_board_state
        temp_board.imprimir()

        choice = input("\nDeseja desfazer a última jogada e retornar a este estado? (s/n): ").strip().lower()
        if choice == 's':
            restored_board = self.history.pop()
            self.tabuleiro.current_board = restored_board
            print("Tabuleiro restaurado para o estado anterior.")
        else:
            print("Mantendo o estado atual do tabuleiro.")
            
        input("Pressione Enter para continuar...")


    def _mostrar_menu_principal(self):
        while True:
            limpar_tela()
            print("## Menu Principal")
            print("-" * 30)
            print("[1] Sair do Jogo")
            print("[2] Recomeçar Tabuleiro Atual")
            print("[3] Selecionar Nova Dificuldade")
            print("[4] Ver/Desfazer Última Jogada")
            print("[0] Voltar ao Jogo")
            print("-" * 30)

            choice = input("Escolha uma opção: ").strip()

            if choice == '1':
                return "sair"
            elif choice == '2':
                self._recomecar()
                print("\nTabuleiro reiniciado!")
                input("Pressione Enter para continuar...")
                return "voltar"
            elif choice == '3':
                self._selecionar_nova_dificuldade()
                print("\nNova dificuldade selecionada. O tabuleiro foi reiniciado.")
                input("Pressione Enter para continuar...")
                return "voltar"
            elif choice == '4':
                self._ver_jogada_anterior()
                return "voltar"
            elif choice == '0':
                return "voltar"
            else:
                print("Opção inválida.")
                input("Pressione Enter para continuar...")

    def jogar(self):
        
        mostrar_fachada()
        
        self.difficulty_key = self._selecionar_dificuldade()
        self.tabuleiro = SudokuBoard(self.difficulty_key)
        
        while True:
            limpar_tela()
            dificuldade_nome = SudokuBoard.DIFFICULTIES[self.difficulty_key]['nome']
            print(f"## Sudoku - Nível: {dificuldade_nome}")
            print("-" * 40)
            self.tabuleiro.imprimir()

            if self.tabuleiro.verificar_vitoria():
                print("\nParabéns! Você completou o Sudoku!")
                break

            jogada = self._receber_jogada()
            
            if jogada == "sair":
                print("\nJogo encerrado. Obrigado por jogar!")
                break
            
            if jogada == "menu":
                menu_result = self._mostrar_menu_principal()
                if menu_result == "sair":
                    print("\nJogo encerrado. Obrigado por jogar!")
                    break
                continue

            linha, coluna, numero = jogada

            current_state_copy = [row[:] for row in self.tabuleiro.current_board]
            
            if numero == 0:
                if self.tabuleiro.initial_board[linha][coluna] != 0:
                     print(" Você não pode remover um número pré-preenchido!")
                else:
                    if self.tabuleiro.current_board[linha][coluna] != 0:
                        self.history.append(current_state_copy)
                        
                    self.tabuleiro.current_board[linha][coluna] = 0
                    print(" Número removido.")
                input("Pressione Enter para continuar...")
                continue
                
            
            resultado = self.tabuleiro.fazer_jogada(linha, coluna, numero)

            if resultado == "valida":
                self.history.append(current_state_copy)
                print(f" Jogada ({linha+1},{coluna+1}) = {numero} feita com sucesso.")
            elif resultado == "invalida":
                print(f" Jogada inválida! Conflito com linha, coluna ou subgrade.")
            elif resultado == "fixo":
                print(" Você não pode alterar uma célula já preenchida!")
            
            input("Pressione Enter para continuar...")
            
        print("\nObrigado por jogar!")

if __name__ == "__main__":
    game = SudokuGame()
    game.jogar()