import connect as cn
import minmax as ia

print("Connect Four")
linhas = 0
colunas = 0
while True:
  linhas = input("Insira a quantidade de linhas do jogo (mínimo 4): ")
  colunas = input("Insira a quantidade de colunas do jogo (mínimo 4): ")
  try:
    linhas = int(linhas)
    colunas = int(linhas)
  except:
    print("Valores inválidos.\n")
    continue

  if linhas >= 4 and colunas >= 4:
    break
  print("Valores insuficientes.\n")

game = cn.Connect(linhas, colunas)
game.set_Players(input("\n Insira o nome do primeiro jogador: "),
                 input(" Insira o nome do segundo jogador : "))

print("Insira a coluna para posicionar a peça\n")

vez = ""
while game.turn != None:
  
  if game.turn: 
    game.print()
    coord = input("\n {} >> ".format(vez))
    try:
      coord = int(coord)
    except:
      coord = -1
    vez = game.turnPlayer
    print("\033[{}A \033[J".format(game.lines + 5))
    flag = game.play(coord)
   
  else: 
    vez = game.nturnPlayer
    ia.minmax_init(game)
  
  if not flag:
    print("Movimento inválido")
    print("\033[2A")

print("\n O jogador venceu (ou deu caca no programa): {}".format(vez))
game.print()


