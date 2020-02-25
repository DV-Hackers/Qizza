class Table:
  def __init__(self, rows, cols):
    self.arr = [[0 for _ in range(cols)] for _ in range(rows)]

  def set(self, x, y, val):
    self.arr[x][y] = val

  def get(self, x, y):
    return self.arr[x][y]