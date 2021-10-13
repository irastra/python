import cv2
import numpy as np

def Bresenham(sx, sy, ex, ey, data, col_num):
	ix = int(sx)
	iy = int(sy)
	nx = int(ex)
	ny = int(ey)
	if ix == nx:
		for i in xrange(iy, ny):
			print ix, i
	elif iy == ny:
		for i in xrange(ix, nx):
			print i, iy
	else:
		ch  = abs(ey - sy) > abs(ex - sx)
		if ch:
			sx, sy = sy, sx 
			ex, ey = ey, ex 
			ix, iy = iy, ix
			nx, ny = ny, nx
		d = (ey - sy) * 1.0 / (ex - sx)
		y = iy
		error = 0
		for i in xrange(ix, nx):
			if ch:
				data[idx(y, i, col_num)] = 1
			else:
				data[idx(i, y, col_num)] = 1
			error += d
			if error > 0.5:
				error -= 1
				y += 1

class MyCanvas(object):

	def __init__(self, w, h, name):
		self.canvas = np.zeros((w, h, 3), dtype="uint8")
		self.w = w
		self.h = h
		self.cs = 20
		self.begin_x = self.cs + 2
		self.begin_y = self.cs + 2
		self.nx, self.ny = self.w / self.cs , self.h / self.cs

	def Pos(self, x, y):
		return x, -y + self.h

	def DrawGrad(self, n, nx):
		begin_x = self.begin_x
		begin_y = self.begin_y
		canvas = self.canvas
		cs = self.cs
		ny = n / nx
		red = (255, 0, 0)
		for yi in xrange(ny + 1):
			cv2.line(canvas, self.Pos(begin_x, begin_y + yi * cs), self.Pos(begin_x + nx * cs , begin_y + yi * cs), red)
			self.DrawText(begin_x - cs, begin_y + yi * cs, str(yi))
		for xi in xrange(nx + 1):
			cv2.line(canvas, self.Pos(begin_x + xi * cs, begin_y), self.Pos(begin_x + xi * cs, begin_y + ny * cs), red)
			self.DrawText(begin_x + xi * cs, begin_y - cs, str(xi))

	def DrawText(self, x, y, text):
		org = self.Pos(x, y)
		fontFace = cv2.FONT_HERSHEY_COMPLEX
		fontScale = 0.35
		fontcolor = (0, 255, 0) # BGR
		thickness = 1 
		lineType = 4
		bottomLeftOrigin = 1
		# cv.putText(img, text, org, fontFace, fontScale, fontcolor, thickness, lineType, bottomLeftOrigin)
		cv2.putText(self.canvas, text, org, fontFace, fontScale, fontcolor, thickness, lineType)

	def DrawLine(self, sx, sy, ex, ey, color=(255, 0, 0)):
		sx += self.begin_x
		ex += self.begin_x
		sy += self.begin_y
		ey += self.begin_y
		cv2.line(self.canvas, self.Pos(sx, sy), self.Pos(ex, ey), color)

	def DrawCellLine(self, sx, sy, ex, ey):
		n = 10
		data = [ 0 for x in xrange(self.nx * self.ny)]
		Bresenham(sx, sy, ex, ey, data, self.nx)
		Draw(data, self.nx)
		self.DrawData(data, self.nx)

	def DrawData(self, data, nx):
		ny = len(data) / nx
		for iy in xrange(ny):
			for ix in xrange(nx):
				if data[idx(ix, iy, self.nx)]:
					x = self.begin_x + ix * self.cs
					y = self.begin_y + iy * self.cs
					cv2.rectangle(self.canvas, self.Pos(x, y), self.Pos(x + self.cs, y + self.cs), (0,0,255), 2)

	def Show(self):
		cv2.imshow("Canvas", self.canvas)

def idx(i, j, nx):
	return j * nx + i

def Draw(data, nx):
	col = len(data) / nx
	for j in xrange(col):
		s = ''
		for i in xrange(nx):
			s += '-' if not data[idx(i, col - j - 1, nx)] else '*'
		print s

canvas = MyCanvas(500, 500, 'MyCanvas')
canvas.DrawGrad(900, 30)

canvas.DrawLine(5 * canvas.cs, 5 * canvas.cs, 10 * canvas.cs , 20 * canvas.cs, (0, 255, 0))
canvas.DrawCellLine(5, 5, 10, 20)

canvas.DrawLine(1 * canvas.cs, 1 * canvas.cs, 25 * canvas.cs , 10 * canvas.cs, (0, 255, 0))
canvas.DrawCellLine(1, 1, 25, 10)

canvas.Show()
cv2.waitKey(0)