import np
import math

def EulerToMatrix(h, b, p):
	cos = math.cos
	sin = math.sin
	param = '%s %s %s 0;%s %s %s 0;%s %s %s 0;%s %s %s 1' % (
		cos(h)*cos(b) + sin(h)*sin(p)*sin(b), -cos(h)*sin(b) + sin(h)*sin(p)*cos(b), sin(h)*cos(p),
		sin(b)*cos(p), cos(b)*cos(p), -sin(p),0
		-sin(h)*cos(b) + cos(h)*sin(p)*sin(b), sin(b)*sin(h) + cos(h)*sin(p)*cos(b), cos(h)*cos(p),
	)
	return np.matrix(param)

def ctan(x):
	return math.tan(math.pi / 2 - x)

def perspect_matrix(near, far, fov_y, aspect):
	param = '%s 0.0 0.0 0.0;0.0 %s 0.0 0.0;0.0 0.0 %s %s;0.0 0.0 -1 0.0' % (
		ctan(fov_y/2.0) / aspect,
		ctan(fov_y/2.0),
		far * 1.0 / (near - far),
		(near * 1.0 * far) / (near - far)
		)
	return np.matrix(param)

def clip(pos):
	return pos / pos[3]

def view_port_matrix(min_x, min_y, min_z, w, h, max_z):
	param = '%s 0 0 %s;0 %s 0 %s;0 0 %s %s;0 0 0 1' % (
		w/2.0, min_x + w / 2.0,
		-(h/2.0), min_y + h/2.0,
		max_z - min_z, min_z,
		)
	return np.matrix(param)

def generate_vertex(pos, radious):
	center_pos = pos
	vertext_list = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
	vertext_list_3d = []
	for pair in vertext_list:
		pos = np.matrix('%s;%s;%s;%s' % (center_pos[0] + pair[0] * radious, center_pos[1] + pair[1] * radious, center_pos[2], 1))
		vertext_list_3d.append(pos)
	return vertext_list_3d

def c_pos(pos):
	return "(%s, %s, %s, %s)" % (pos[0], pos[1], pos[2], pos[3])

def view_to_vp(view_pos, projection, vp_matrix, debug=False):
	# view -> projection
	if debug:
		print "view_pos:", c_pos(view_pos)
	
	projection_pos = projection * view_pos
	if debug:
		print "projection pos:", c_pos(projection_pos)
	
	clip_pos = clip(projection_pos)
	if debug:
		print "clip pos:", c_pos(clip_pos)

	vp_pos = vp_matrix * clip_pos
	if debug:
		print "view port pos", c_pos(vp_pos)
	return vp_pos

def H_X(h_matrix):
	return h_matrix.tolist()[0][0]

def H_Y(h_matrix):
	return h_matrix.tolist()[1][0]

def H_Z(h_matrix):
	return h_matrix.tolist()[2][0]

def H_W(h_matrix):
	return h_matrix.tolist()[3][0]