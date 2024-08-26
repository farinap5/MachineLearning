from connect import Connect
import copy


def minmax_init(game: Connect, max_part="🔴", min_part="🔵", maxDepth=10):
  b_point = float("-inf")  # melhor jogada
  b_state = None  # melhor versão do jogo, melhor coluna para jogar

  for j in range(0, game.columns):
    aux = copy.deepcopy(game)
    for i in range(0, game.lines):
      if game.grid[i][j] == "⚪":
        aux.grid[i][j] = max_part
        val = minmax(aux, max_part, min_part, False, 0, maxDepth)
        if val > b_point:
          b_point = val
          b_state = j
        break
  game.play(b_state)


def calcular_utilidade(game, part="🔴"):
  pontos = 0
  for line in range(0, game.lines):
    for column in range(0, game.columns):
      # Contemos as coordenadas na vertical, horizontal e diagonal
      circle = game.grid[line][column]
      if circle != part:
        break

      # Vertical
      sequence = 1
      pont_temp = 0
      i = line + 1
      while i < game.lines:  # game.lines
        if game.grid[i][column] == circle or game.grid[i][column] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[i][column] == circle):
            pont_temp += 1
          i += 1
        else:
          break

      i = line - 1
      while i >= 0:
        if game.grid[i][column] == circle or game.grid[i][column] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[i][column] == circle):
            pont_temp += 1
          i -= 1
        else:
          break

      if (sequence >= 4):
        pontos += pont_temp

      # Horizontal
      sequence = 1
      pont_temp = 0
      i = column + 1
      while i < game.columns:
        if game.grid[line][i] == circle or game.grid[line][i] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[line][i] == circle):
            pont_temp += 1
          i += 1
        else:
          break

      i = column - 1
      while i >= 0:
        if game.grid[line][i] == circle or game.grid[line][i] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[line][i] == circle):
            pont_temp += 1
          i -= 1
        else:
          break

      if (sequence >= 4):
        pontos += pont_temp

    # Diagonal 1
      sequence = 1
      pont_temp = 0
      i = line + 1
      j = column + 1
      while i < game.lines and j < game.columns:
        if game.grid[i][j] == circle or game.grid[i][j] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[i][j] == circle):
            pont_temp += 1
          i += 1
          j += 1
        else:
          break

      i = line - 1
      j = column - 1
      while i >= 0 and j >= 0:
        if game.grid[i][j] == circle or game.grid[i][j] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[i][j] == circle):
            pont_temp += 1
          i -= 1
          j -= 1
        else:
          break

      if sequence >= 4:
        pontos += pont_temp

      # Diagonal 2
      sequence = 1
      pont_temp = 0
      i = line - 1
      j = column + 1
      while i >= 0 and j < game.columns:
        if game.grid[i][j] == circle or game.grid[i][j] == "⚪":
          sequence += 1
          pont_temp += 1
          if (game.grid[i][j] == circle):
            pont_temp += 1
          i -= 1
          j += 1
        else:
          break

      i = line + 1
      j = column - 1
      while i < game.columns and j >= 0:
        if game.grid[i][j] == circle or game.grid[i][j] == "⚪":
          sequence += 1
          pont_temp += 1
          if game.grid[i][j] == circle:
            pont_temp += 1
          i += 1
          j -= 1
        else:
          break

      if sequence >= 4:
        pontos += pont_temp
  return pontos


def minmax(game: Connect,
           max_part="🔴", # MinMax
           min_part="🔵", # Oponente
           maximize=True,
           depth=0,
           maxDepth=3
          ):
            
  for i in range(0, game.lines):
    for j in range(0, game.columns):
      if game.check_win(i, j):
        if game.grid[i][j] == max_part:
          return 100
        elif game.grid[i][j] == min_part:
          return -100

  if depth == maxDepth:
    if maximize:
      return calcular_utilidade(game, max_part)
    else:
      return -calcular_utilidade(game, min_part)

    # pseudo
    """
    for j in range(0, game.columns)?
    i = 0
    while (aux[i][j] 1= "branco") {
      i += 1
    } 
    aux[i][j]
    """
  max_p = float('-inf')
  min_p = float('inf')
  for j in range(0, game.columns):
    aux = copy.deepcopy(game)
    for i in range(0, game.lines):
      if aux.grid[i][j] == "⚪":

        if maximize:
          aux.grid[i][j] = max_part
          val = minmax(aux, max_part, min_part, False, depth + 1)
          max_p = max(max_p, val)
        else:
          aux.grid[i][j] = min_part
          val = minmax(aux, max_part, min_part, True, depth + 1)
          min_p = min(min_p, val)

        break

  if maximize: return max_p
  else: return min_p
  """
  if maximize:
    max_p = float('-inf')
    for i in range(0, game.lines):
      for j in range(0, game.columns):
        if game.grid[i][j] == default:
          aux = copy.deepcopy(game.grid)
          aux[i][j] = part
          val = minmax(game, part, default, False,depth+1)
          max_p = max(max_p, val)
    return max_p
  else:
    min_p = float('inf')
    for i in range(0, game.lines):
      for j in range(0, game.columns):
        if game.grid[i][j] == default:
          aux = copy.deepcopy(game.grid)
          aux[i][j] = part
          val = minmax(game, part, default, True, depth+1)
          min_p = min(min_p, val)
    return min_p"""
