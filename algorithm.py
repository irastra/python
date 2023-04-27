import random

#选择排序
def SSort(data, n):
	for _i in range(n):
		for _j in range(_i+1, n):
			if data[_j] < data[_i]:
				data[_i], data[_j] = data[_j], data[_i]

#冒泡排序
def PSort(data, n):
	for i in range(n):
		for j in range(0, n-i-1):
			idx_1 = j
			idx_2 = j+1
			if data[idx_1] > data[idx_2]:
				data[idx_1], data[idx_2] = data[idx_2], data[idx_1]

#归并排序
def MSort(data, l, r):
	if r - l <= 1:
		return
	m = int((l + r) / 2)
	MSort(data, l, m)
	MSort(data, m, r)
	n_data = []
	i1 = l
	i2 = m
	while(i1 < m or i2 < r):
		if i1 < m and i2 < r and data[i1] < data[i2] or i2 >= r:
			n_data.append(data[i1])
			i1+=1
		else:
			n_data.append(data[i2])
			i2+=1
	for _idx in range(len(n_data)):
		data[l + _idx] = n_data[_idx]

#快速排序
def QSort(data, l, r):
	if r - l <= 1:
		return
	c_idx = l 
	li = l + 1
	ri = r - 1
	while(li < ri):
		while data[li] < data[c_idx] and li < ri:
			li+=1
		while data[ri] >= data[c_idx] and li < ri:
			ri-=1
		if ri > li:
			data[li], data[ri] = data[ri], data[li]
			if data[ri] == data[li]:
				ri -= 1
	if data[li] < data[c_idx]:
		data[c_idx], data[li] = data[li], data[c_idx]
	else:
		data[c_idx], data[li-1] = data[li-1], data[c_idx]
	QSort(data, l, li)
	QSort(data, li, r)

def BinarySearch(data, a):
	l = 0
	r = len(data)
	while(l < r):
		m = int((l + r)/2)
		if data[m] == a:
			return m
		elif data[m] > a:
			r = m
		else:
			l = m + 1
	return -1

def UpperBounds(data, a):
	l = 0
	r = len(data)
	ret = -1
	while(l < r):
		m = int((l + r)/2)
		if data[m] <= a:
			if data[m] == a:
				ret = m
			l = m + 1
		else:
			r = m
	return ret

def LowerBounds(data, a):
	l = 0
	r = len(data)
	ret = -1
	while(l < r):
		m = int((l + r)/2)
		if data[m] >= a:
			if data[m] == a:
				ret = m
			r = m 
		else:
			l = m + 1
	return ret

def GenArray(n, m):
	l = []
	for _ in range(n):
		l.append(int(round(random.random(), m) * pow(10, m)))
	return l

def Check(data):
	for _idx in range(len(data)-1):
		if data[_idx] > data[_idx+1]:
			return False
	return True

def X():
	print(1)
	yield 1
	print(2)

def MyNext(gen):
	try:
		return next(gen)
	except:
		return None

array = [5, 1, 4, 3, 2, 2, 2, 6, 6, 6, 0, 7, 7]
for _ in range(1):
	array = GenArray(2000, 2)
	#print(array)
	#QSort(array, 0, len(array))
	#MSort(array, 0, len(array))
	#SSort(array, len(array))
	PSort(array, len(array))
	print(array)
	b = BinarySearch(array, 5)
	lb = LowerBounds(array, 5)
	ub = UpperBounds(array, 5)
	print(b, lb, ub)
	if not Check(array):
		print("False")
		#print(array)
		break
print("Ok")
gen = X()
print(MyNext(gen))
print(MyNext(gen))