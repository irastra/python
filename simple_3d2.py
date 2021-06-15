import math


def index2ij(idx, col):
    r = idx / col
    return r, idx - r * col


def ij2iindex(i, j, col):
    return i * col + j


def GetTBN(pos1, u1, v1, pos2, u2, v2, pos3, u3, v3):
    dU1 = (u1 - u2).Mol()
    dU2 = (u1 - u3).Mol()
    dV1 = (v1 - v2).Mol()
    dV2 = (v1 - v3).Mol()
    dPos1 = pos2 - pos1
    dPos2 = pos3 - pos1
    mat1 = Matrix([dPos1, dPos2], 2, 1)
    mat2 = Matrix([dU1, dV1, dU2, dV2], 2, 2)
    res = mat1 * mat2.Inverse()
    u = res.getAt(0, 0)
    v = res.getAt(1, 0)
    return u.normalize(), v.normalize()


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
        return Vector3(
            self.y * b.z - self.z * b.y, self.z * b.x - b.z * self.x,
            self.x * b.y - b.x * self.y
        )

    def Mol(self):
        math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        mol = self.Mol()
        self.x /= mol
        self.y /= mol
        self.z /= mol


class Matrix(object):
    def __init__(self, args, r, c):
        self._data = args
        self.r = r
        self.c = c

    def Det(self):
        if self.r != self.c:
            raise "error"
        if self.r == 1:
            return self.GetAt(0, 0)
        elif self.r == 2:
            return self.GetAt(0, 0) * self.GetAt(1, 1) - self.GetAt(0, 1
                                                                   ) * self.GetAt(1, 0)
        if (self.r == 1):
            return self.GetAt(0, 0)
        s_r = 0
        s_l = 0
        for r in xrange(self.r):
            sr_r = r
            sc_r = self.r - 1
            sr_l = r
            sc_l = 0
            adapt = 1
            adapt_l = 1
            for t in xrange(self.r):
                adapt *= self.GetAt(sr_r % self.r, sc_r % self.c)
                adapt_l *= self.GetAt(sr_l % self.r, sc_l % self.c)
                sr_r += 1
                sc_r -= 1
                sr_l += 1
                sc_l += 1
            s_r += adapt
            s_l += adapt_l
        #print s_l , s_r
        return s_l - s_r

    def _A(self, ix, jx):
        if self.r == 1:
            return self
        data = []
        for i in xrange(self.r):
            for j in xrange(self.c):
                if i != ix and j != jx:
                    data.append(self.GetAt(i, j))
        mat = Matrix(data, self.r - 1, self.c - 1)
        #mat.Show()
        a = mat.Det() * pow(-1, ix + jx)
        return a

    def A(self):
        mat = Matrix.MakeEmpty(self.r, self.c)
        for i in xrange(self.r):
            for j in xrange(self.c):
                mat.SetAt(i, j, self._A(i, j))
        return mat

    def Ap(self):
        return self.A().Transpose()

    def Inverse(self):
        ap = self.Ap()
        a = self.Det()
        for i in xrange(self.r):
            for j in xrange(self.c):
                ap._data[ij2iindex(i, j, ap.c)] /= a
        return ap

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
            r.x,
            u.x,
            d.x,
            0,
            r.y,
            u.y,
            d.y,
            0,
            r.z,
            u.z,
            d.z,
            0,
            ip.x,
            ip.y,
            ip.z,
            1,
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
#(Vector3(1, 1, 1).MulMatrix(lookAt)).Show()

t = Matrix([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 1], 4, 4)
t.Inverse().Show()

mat = Matrix([1, 0, 0, 0, 1, 0, 0, 0, 1], 3, 3)
mat.Inverse().Show()
