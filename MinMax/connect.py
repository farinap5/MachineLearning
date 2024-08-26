import numpy as np


class Connect:
  def __init__(self, columns, lines):
    if columns < 4 or lines < 4:
      return None
    self.grid = np.full((lines, columns), "⚪")
    self.columns = columns
    self.lines = lines
    self.turnPlayer = "Blue"
    self.nturnPlayer = "Red"
    self.turn = True

  """Define os jogadores"""
  def set_Players(self, player1, player2):
    self.turnPlayer = player1
    self.nturnPlayer = player2

  """Printa o tabuleiro"""
  def print(self):
    #print print print print print print print print
    print("\n", end="   ")
    for i in range(0, self.columns):
      print(i, end="  ")
    print()
    for i in range(0, self.lines):
      print(i, end=" ")
      for j in self.grid[i]:
        print(j, end=" ")
      print()

  """Verifica empate"""
  def tied_game(self):
    c = 0
    for i in range(self.lines):
      for j in range(self.columns):
        if self.grid[i][j] == "⚪":
          return False
        else:
          c+=1
          
    if c == (self.lines * self.columns):
      return True
    else:
      return False
    
  """Checa a condição de vitória para uma coordenada"""
  def check_win(self, line, column)->bool:
    if line >= self.lines or column >= self.columns:
      return None
    if self.tied_game():
      return None
      
    # Contemos as coordenadas na vertical, horizontal e diagonal
    circle = self.grid[line][column]
    if circle == "⚪":
      return False

    # Vertical
    sequence = 1
    i = line + 1
    while i < self.lines:
      if self.grid[i][column] == circle:
        i += 1
        sequence += 1
      else:
        break
    i = line - 1
    while i >= 0:
      if self.grid[i][column] == circle:
        i -= 1
        sequence += 1
      else:
        break
    if (sequence >= 4):
      return True

    # Horizontal
    sequence = 1
    i = column + 1
    while i < self.columns:
      if self.grid[line][i] == circle:
        i += 1
        sequence += 1
      else:
        break
    i = column - 1
    while i >= 0:
      if self.grid[line][i] == circle:
        i -= 1
        sequence += 1
      else:
        break
    if (sequence >= 4):
      return True

  # Diagonal 1
    sequence = 1
    i = line + 1
    j = column + 1
    while i < self.lines and j < self.columns:
      if self.grid[i][j] == circle:
        i += 1
        j += 1
        sequence += 1
      else:
        break
    i = line - 1
    j = column - 1
    while i >= 0 and j >= 0:
      if self.grid[i][j] == circle:
        i -= 1
        j -= 1
        sequence += 1
      else:
        break
    if sequence >= 4:
      return True

    # Diagonal 2
    sequence = 1
    i = line - 1
    j = column + 1
    while i >= 0 and j < self.columns:
      if self.grid[i][j] == circle:
        i -= 1
        j += 1
        sequence += 1
      else:
        break
    i = line + 1
    j = column - 1
    while i < self.columns and j >= 0:
      if self.grid[i][j] == circle:
        i += 1
        j -= 1
        sequence += 1
      else:
        break
    if sequence >= 4:
      return True

    return False
  
  """ Realiza uma jogada """
  # Retorna false em uma jogada inválida
  # Setta o turno para None em vitória
  def play(self, column):
    if (column >= self.columns or column < 0):
      return False

    for i in range(0, self.lines):
      if self.grid[
      i][column] == "⚪":
        if self.turn == True:
          self.grid[i][column] = "🔵"
          if self.check_win(i, column):
            self.turn = None
            return True
          self.turn = False
          return True
        elif self.turn == False:
          self.grid[i][column] = "🔴"
          self.check_win(i, column)
          if self.check_win(i, column):
            self.turn = None
            return True
          self.turn = True
          return True
    return False
