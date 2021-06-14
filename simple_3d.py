def index2ij(idx, col):
  r = idx / col
  return r , idx - r * col

def ij2iindex(i, j, col):
  return i * col + j

class Vector3(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
  
  def Show(self):
    print self.x, " ", self.y, " ", self.z

  def ToMatrix(self):
    return Matrix([self.x, self.y, self.z, 1], 1, 4)

  def MulMatrix(self, mat):
    res = self.ToMatrix() * mat
    return Vector3(res._data[0], res._data[1], res._data[2])

  def __sub__(self, vec):
    return Vector3(self.x - vec.x, self.y - vec.y, self.z - vec.z)

  def __add__(self, vec):
    return Vector3(self.x + vec.x, self.y + vec.y, self.z + vec.z)
  
  def Dot(self, vec):
    return self.x * vec.x + self.y * vec.y + self.z * vec.z

  def Cross(self, b):
    return Vector3(self.y * b.z - self.z * b.y, self.z * b.x - b.z * self.x, self.x * b.y - b.x * self.y)

class Matrix(object):
  def __init__(self, args, r, c):
    self._data = args
    self.r = r
    self.c = c

  def GetAt(self, i, j):
    return self._data[ij2iindex(i, j, self.c)]

  def SetAt(self, i, j, val):
    self._data[ij2iindex(i, j, self.c)] = val

  def Show(self):
    out_str = ""
    for i in xrange(self.r):
      for j in xrange(self.c):
        out_str += str(self.GetAt(i, j)) + " "
      out_str += "\n"
    print out_str

  @staticmethod
  def MakeEmpty(r, c):
    data = [0 for i in xrange(r * c)]
    return Matrix(data, r, c)

  @staticmethod
  def MakeI(r, c):
    data = [1 if i == j else 0 for i in xrange(r) for j in xrange(c)]
    return Matrix(data, r, c)

  @staticmethod
  def MakeVec(args):
    n = len(args)
    cnt = 0
    data = []
    for i in xrange(n):
        for j in xrange(n):
          data.append(0)
          if i == j:
            data[ij2iindex(i, j, n)] = args[cnt]
            cnt += 1
          else:
            data[ij2iindex(i, j, n)] = 0
    return Matrix(data, n, n)

  @staticmethod
  def MakeLookAt(pos, target_pos, up):
    d = target_pos - pos
    r = up.Cross(d)
    u = d.Cross(r)
    ip = Vector3(-pos.x, -pos.y, -pos.z)
    data = [
      r.x, u.x, d.x, 0,
      r.y, u.y, d.y, 0,
      r.z, u.z, d.z, 0,
      ip.x,ip.y,ip.z,1,
    ]
    return Matrix(data, 4, 4)
  
  def __mul__(self, m):
    r_r = self.r
    r_c = m.c
    kk = self.c
    m_result = Matrix.MakeEmpty(r_r, r_c)
    for i in xrange(r_r):
      for j in xrange(r_c):
        for k in xrange(kk):
          val = m_result.GetAt(i, j)
          m_result.SetAt(i, j, val + self.GetAt(i, k) * m.GetAt(k, j)) 
    return m_result

  def __add__(self, m):
    data = []
    for i in xrange(self.r * self.c):
      data.append(self._data[i] + m._data[i])
    return Matrix(data, self.r, self.c)

  def __sub__(self, m):
    data = []
    for i in xrange(self.r * self.c):
      data.append(self._data[i] - m._data[i])
    return Matrix(data, self.r, self.c)

  def Transpose(self):
    result = Matrix.MakeEmpty(self.c, self.r)
    for i in xrange(self.r):
      for j in xrange(self.c):
        result.SetAt(j, i, self.GetAt(i, j))
    return result

lookAt = Matrix.MakeLookAt(Vector3(1, 1, 1), Vector3(1, 1, 2), Vector3(0, 1, 0))
lookAt.Show()
(Vector3(1, 1, 1).MulMatrix(lookAt)).Show()