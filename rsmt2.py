from base import *
import math
import networkx
import matplotlib.pyplot as plt
import matplotlib
from graph import *
import random
from collections import deque, defaultdict
from plot import *
import bisect
import numpy
import cProfile
import timeit
from perf import *
geo = my.geo

"""
	fsts:
		dfst: node<tuple>
		wfst: node<int>
	smt_info: len, time, full<list>

	p: 在树上（可能端点），可能存在
	general_node: 包括斜边的直角点(Lnode)

	vscode color #
	hightlight 删去后重置不显示

	data:
		nodes_info: (count, seed) : [sorted(nodes)]
	概念
		p-node: 任意
		D-node: 定义点
		R-node: 真实节点
		S-node：Steiner点
		v-node: 依赖于斜边的虚点
		L-node: 斜边折点

	todo
		grid最近算法 可视方向
		grid更新按顺序?
		grid 菱形 -》正方形
		标题和注释分开
		rpair对称性
	"""
"""test-result
	已验证
		u=0
			u0(abc) - max( u0(ab) u0(ac) ) ~ r(bc)
		u=1
			u0(abc) - min( u0(ab) u0(ac) ) ~ r(bc)
	统计验证
		r(ab) + r(bc) <= r(abc)
		u=0
			u(abc) - min( u(ab) u(ac) ) >= r(bc)
				99% > 1% =
			u(abc) - min( u(ab) u(ac) ) == u(bc)
	"""
if "perf":
	
	names = 'gb r'.split()
	name_fname_map = dict(
		gb='gb', r='gbr'
	)
	performance = Name()
	active_name = 'gb'
	for name in names:
		if name == active_name:
			perf = Performance()
			setattr(performance, name, perf)
			setattr(performance, 'active', perf)
			perf.name = active_name
			perf.func_name = name_fname_map[active_name]
		else:
			setattr(performance, name, lambda method:method)
if "timer":
	timer_cap = 8
	for i in range(timer_cap):
		timer = my.dummy
		globals()[f'timer{i}'] = timer

class de:
	tmp = 0
	debug = __debug__ and 1

	generate = debug and 1
	generate_order = generate and 0
	generate_short = generate and 1
	gb = generate and 0
	r = evolve_replace = debug and 1
	m = evolve_edgeMove = debug and 1
	# check
	check = debug and 1
	rpairs_check = debug and 1
	# misc
	count_cycle = debug and 1
	draw_to_show = debug and 0
	grid = debug and 1 
	# inspect
	cpfp = gb and 1
	rpairs = r and 1
	rpairMap = r and 1
	#light
	flag_light = Flag(0)
	highlight_edge = 0
	highlight_node = 0
	lowlight_edge = 0
	lowlight_node = 0
	hl = set()
	ll = set()
	def light_on():
		if not de.debug: return
		de.flag_light.turnto(1)
		de.highlight_edge = 1
		de.highlight_node = 0
		de.lowlight_edge = 1
		de.lowlight_node = 0

	def light_off():
		if not de.debug: return
		de.flag_light.turnto(0)
		de.highlight_edge = 0
		de.highlight_node = 0
		de.lowlight_edge = 0
		de.lowlight_node = 0
class default: 
	@my.des.dict
	class arrow:
		color = 'green'
	@my.des.dict
	class Dnode:
		color = 'red'
	
	@my.des.dict
	class hl_Dnode:
		color = 'purple'
		size_rate = 3
		shape = '^'
	@my.des.dict
	class Snode:
		color = 'blue'
	@my.des.dict
	class hl_Snode:
		color = 'blue'
		size_rate = 3
		shape = '^'

	@my.des.dict
	class edge:
		color = 'gray'

	@my.des.dict
	class hl_edge:
		color = 'black'
		width_rate = 2
		style = 'solid'

	@my.des.dict
	class ll_edge:
		width_rate = 1
		color = 'black'
		style = 'dashed'

	max_iter = 1e4
	test_cap = 1000000
	test_timeout = 10
class data:
	nodes = my.Data('rsmt\\nodes', {}) 
	smt_info = my.Data('rsmt\\smt_info', {}) # (len, time_s, full)
	fsts_info = my.Data('rsmt\\fsts_info', {})
	pruned_fsts_info = my.Data('rsmt\\pruned_fsts_info', {})
	tmp_info = my.Data('rsmt\\tmp_info', tuple())
	#
	# test_keys = my.Data('rsmt\\test_keys', []) # [ (size, seed, accuracy) ]
	smt_simple_time = my.Data('rsmt\\smt_simple_time', {}) # key: time
	smt_filter_time = my.Data('rsmt\\smt_filter_time', {}) # key: time
	smt_match_time = my.Data('rsmt\\smt_match_time', {}) # key: time

smt_note_path = 'ground\\rsmt\\smt_info.txt'
keys_note_name = 'ground\\rsmt\\keys.txt'

class setting:
	save_interval = 1
	floor_per_square = 3

def nodes_random(count, *, cap=None):
	if cap == None: cap = count
	r = []
	tail = cap - 1
	assert count < cap ** 2 / 2
	for i in range(count):
		while True:
			x = random.randint(0, tail)
			y = random.randint(0, tail)
			node = (x, y)
			if node not in r:
				r.append(node)
				break
	return sorted(r)
def nodes_random_seed( count, *, seed, cap=None):
	"""
		seed >= 1
		cap = count [0, count-1]
		"""
	assert isinstance(count, int) and count >= 1, f'{count}'
	assert isinstance(seed, int) and seed >= 0, f'{seed}'

	if cap == None: cap = count
	my.random.seed(seed)
	nodes = my.random.sample_tuple2(cap, cap, k=count)
	nodes = sorted(nodes)
	return nodes
def nodes_by_key(key):
	return data.nodes()[key]
	# count, seed = key
	# return nodes_random_seed(count, seed=seed)
def read_nodes(string, type_=int):
	nodes = []
	strs = string.split()
	nums = [type_(s) for s in strs]
	for i in range(0, len(nums), 2):
		nodes.append( (nums[i], nums[i+1]))
	return nodes
if "unused":
	@staticmethod
	def sedge_include_node(sedge, n, *, inclusive=[0,0]):
		self = SG
		dim = self.dim_sedge(sedge)
		key = enum.key_dim[dim]
		n1, n2 = sorted(sedge, key=key)
		if not inclusive[0] and not inclusive[1]:
			res = key(n1) < key(n) < key(n2)
		elif not inclusive[0] and inclusive[1]:
			res = key(n1) < key(n) <= key(n2)
		elif inclusive[0] and not inclusive[1]:
			res = key(n1) <= key(n) < key(n2)
		elif inclusive[0] and inclusive[1]:
			res = key(n1) <= key(n) <= key(n2)
		else: raise Exception(f'{0}')
		
		return res
	@staticmethod
	def distance_n_sedgedge_include(n, sedge):
		self = SG
		dim = self.dim_sedge(sedge)
		key = enum.key_dim[1-dim]
		n1, n2 = sedge
		r = abs( key(n) - key(n1) )
		return r
if "geo":
	# base
	def dfsts_to_wfsts(dfsts, nodes) -> list:
		map = { n: i for i, n in enumerate(nodes) }
		wfsts = []
		for dfst in dfsts:
			weight = dfst.weight()
			Dnodes = [ map[n] for n in dfst.Dnodes ]
			wfsts.append( (Dnodes, weight) )
		return wfsts
	# fsts line
	def lines_to_wfst(lines): ##
		"""
				% fs2: 0 2
					0 T	0	1	S
					2 T	0	1	S
				(FST 2,  Length = 2)
			"""
		Dnodes = {int(n) for n in lines[0].split()[2:]}
		edges = set()
		Snodes = set()
		# for line in lines[1:-1]:
		# 	a1, a2, b1, b2, t = line.split()
		# 	assert t == 'S'
		# 	pair = []
		# 	for x1, x2 in (a1, a2), (b1, b2):
		# 		if x2 == 'T':
		# 			pair.append(x1)
		# 		else:
		# 			snode = (x1, x2)
		# 			Snodes.add(snode)
		# 			pair.append( snode)
		# 	edges.add(tuple(pair))
		# len
		t, t, t, t, le_ = lines[-1].split()
		le = int(le_[:-1])
		wfst = (Dnodes, le)
		return wfst
	def line_to_fst(line):
		"""
			% fs2: 0 2
			"""
		Dnodes = {int(n) for n in line.split()[2:]}
		return Dnodes
	def lines_to_fsts(lines):
		lines = [ line for line in lines if line.startswith(' %') ]
		fsts = [ line_to_fst(line) for line in lines ]
		return fsts
	def lines_to_wfsts(lines):
		d(lines)
		groups = my.list.group_by_brace(lines, ('\tPlot_Terminals', 'EndSmallPlot2'), inclusive=False)
		wfsts = [ lines_to_wfst(g) for g in groups ]
		return wfsts
	def lines_to_pos(lines): ##
		r = []
		groups = my.list.group_by_brace(lines, ('%%BeginSetup', '%%EndSetup'), inclusive=False )
		assert len(groups) == 1, lines
		lines_ = groups[0]
		for line in lines_[4:-1]:
			x, y, t = line.split()
			r.append((x, y))
		return r
	# smt-line
	def smt_lines_to_wfsts(lines, pos):
		dfsts = smt_lines_to_dfsts(lines, pos)
		wfsts = dfsts_to_wfsts(dfsts, pos)
		return wfsts
	def smt_lines_to_hg(lines, pos):
		wfsts = smt_lines_to_wfsts(lines, pos)
		hg = HyperGraph.from_wedges(wfsts, pos=pos)
		return hg
	# tmp_info
	def tmp_analyze_info():
		tmp_info = data.tmp_info()
		nodes, fsts, pruned, smt_info = tmp_info
		pos = nodes
		fsts_hg = HyperGraph.from_wedges(fsts, pos=pos)
		#
		pruned_hg = HyperGraph.from_wedges(pruned, pos=pos)
		#
		smt_hg = smt_lines_to_hg(smt_info[2], pos=pos)
		return nodes, fsts_hg, pruned_hg, smt_hg
	# smt-by-lines
	# def smt_wfsts_by_lines(lines):
	def smt_lines_to_dfsts(lines, Dnodes):
		# d('\n'.join(lines))
		lines = lines[1:-1]
		groups = my.list.split_by_index( lines, [ i for i, line in enumerate(lines) if line.startswith(' %') ] )
		dfsts = set()
		for group in groups:
			Snodes = set()
			edges = []
			Dnodes_ = set()
			for line in group:
				items = line.split()[:-1]
				edge = []
				for a_, b_ in my.list.group_by_len(items, 2):
					if b_ == 'T':
						a = int(a_)
						node = Dnodes[a]
						Dnodes_.add(node)
					else:
						a = int(a_)
						b = int(b_)
						node = (a, b)
						Snodes.add(node)
					edge.append(node)
				edges.append(sorted2(edge))
				assert len(edge) == 2, line
			dfsts.add( Dfst(Dnodes_, Snodes, edges) )
		return dfsts
		
	# by_key
	def smt_len(key):
		le, time, info = smt_info(key)
		return le
	def smt_info(key):
		return data.smt_info()[key]
	def geo_output_lines(key):
		le, time, full = data.smt_info()[key]
		return full
	def smt_Snodes_edges(key) -> 'Snodes, edges':
		le, time, lines = smt_info(key)
		Dnodes = nodes_by_key(key)
		# d('\n'.join(lines))
		lines = lines[1:-1]
		groups = my.list.split_by_index( lines, [ i for i, line in enumerate(lines) if line.startswith(' %') ] )
		Snodes = set()
		edges = []
		for group in groups:
			for line in group:
				items = line.split()[:-1]
				edge = []
				for a_, b_ in my.list.group_by_len(items, 2):
					if b_ == 'T':
						a = int(a_)
						node = Dnodes[a]
					else:
						a = int(a_)
						b = int(b_)
						node = (a, b)
						Snodes.add(node)
					edge.append(node)
				edges.append(tuple(edge))
				assert len(edge) == 2, line
		return Snodes, edges
	def smt_graph(key):
		Snodes, edges = smt_Snodes_edges(key)
		Dnodes = nodes_by_key(key)
		# nodes = Dnodes | Snodes
		g = SG(Dnodes=Dnodes, nodes=Snodes | set(Dnodes), edges=edges)
		g.clear_nodes(Snodes)
		if de.debug:
			assert g.length() == smt_len(key), f'{0}'
		g.check()
		return g
	def fsts_hg_by_key(key):

		wfsts = data.fsts_info()[key]
		pos = data.nodes()[key]
		hg = HyperGraph(pos=pos).add_wedges(wfsts)
		return hg
	def pruned_hg_by_key(key):

		wfsts = data.pruned_fsts_info()[key]
		pos = data.nodes()[key]
		hg = HyperGraph(pos=pos).add_wedges(wfsts)
		return hg
		
	def geosmt_hg_by_key(key):
		lines = smt_info(key)[2]
		pos = data.nodes()[key]
		hg = smt_lines_to_hg(lines, pos)
		return hg
if "misc":
	def set_hg_odd(hg, *, mst=None):
		if mst is None:
			for e in hg.edges:
				w = hg.weight[e]
				w_ = w + my.random.rand_float(0, 0.001)
				hg.set_edge_weight(e, w_)
		else:
			for e in hg.edges:
				w = hg.weight[e]
				assert w >= 1
				if mst.has_edge(e):
					w_ = w + my.random.rand_float(-0.001, 0)
				else:
					w_ = w + my.random.rand_float(0, 0.001)
				hg.set_edge_weight(e, w_)
			
if "lib":
	# dire dim
	def dire_nn(n1, n2):
		assert n1 != n2
		x1, y1 = n1
		x2, y2 = n2
		if x1 == x2:
			if y1 < y2: r = enum.up
			else: r = enum.down
		if y1 == y2:
			if x1 < x2: r = enum.right
			else: r = enum.left
		return r
	def dire_nn_in_dim(n1, n2, dim):
		if n1[dim] < n2[dim]: pos = 1
		else: 
			assert n1[dim] > n2[dim]
			pos = 0
		r = enum.dim_to_dire_pos[dim][pos]
		return r	
	# distance
	def distance(n1, n2):
		x1, y1 = n1
		x2, y2 = n2
		return abs(x1 - x2) + abs(y1 - y2)
	def edge_length(edge):
		(ax, ay), (bx, by) = edge
		return abs(ax - bx) + abs(ay - by)
	# misc
	def norm_pinfo(pinfo):
		p, e = pinfo
		if e != None and p in e: return p, None
		return pinfo
	def Lnodes_by_skewed_edge(e):
		(x1, y1), (x2, y2) = e
		return (x1, y2), (x2, y1)
	def Linfo_dires(Linfo):
		# 从L点到边的端点
		p, e = Linfo
		n1, n2 = e
		return { dire_nn(p, n1), dire_nn(p, n2) }
	# quartrants
	def quartrantAxisOri_by_nn(n1, n2) -> 'typ, val':
		"""
			typ:
				0: quartrant
				1: axis
				2: ori (val=None)
			"""
		x1, y1 = n1
		x2, y2 = n2
		if x1 < x2:
			if y1 < y2: return 0, 0
			elif y1 > y2: return 0, 3
			else: return 1, enum.right
		elif x1 > x2:
			if y1 < y2: return 0, 1
			elif y1 > y2: return 0, 2
			else: return 1, enum.left
		else:
			if y1 < y2: return 1, enum.up
			elif y1 > y2:return 1, enum.down
			else: return 2, None
		
	def quartrant_by_nn(n1, n2):
		#. 轴上的会被固定分配到某个象限
		x1, y1 = n1
		x2, y2 = n2
		dx = x2 - x1
		dy = y2 - y1
		if dy > 0:
			if dx > 0:
				return enum.qua0
			else:
				return enum.qua1
		else:
			if dx > 0:
				return enum.qua3
			else:
				return enum.qua2
	def quartrants_by_nn(n1, n2):
		x1, y1 = n1
		x2, y2 = n2
		if x1 < x2:
			if y1 < y2: return {0}
			elif y1 > y2: return {3}
			else: return {0, 3}
		elif x1 > x2:
			if y1 < y2: return {1}
			elif y1 > y2: return {2}
			else: return {1, 2}
		else:
			if y1 < y2: return {0, 1}
			elif y1 > y2:return {2, 3}
			else: return {0, 1, 2, 3}
	# p - e
	def pnode_by_pe(n ,e):
		x, y = n
		n1, n2 = (x1, y1), (x2, y2) = sorted(e) ###
		if x1 == x2:
			if y1 < y < y2: return (x1, y)
			elif y <= y1: return (x1, y1)
			elif y2 <= y: return (x1, y2)
		elif y1 == y2:
			if x1 < x < x2: return (x, y1)
			elif x <= x1: return (x1, y1)
			elif x2 <= x: return (x2, y1)
		elif y1 < y2:
			if x < x1:
				if y < y1: return n1
				elif y2 < y: return (x1, y2)
				else: return (x1, y)
			elif x2 < x:
				if y < y1: return x2, y1
				elif y2 < y: return n2
				else: return x2, y
			else:
				if y < y1: return x, y1
				elif y2 < y: return x, y2
				else: return n
		elif y2 < y1:
			if x < x1:
				if y < y2: return x1, y2
				elif y1 < y: return n1
				else: return x1, y
			elif x2 < x:
				if y < y2: return n2
				elif y1 < y: return x2, y1
				else: return x2, y
			else:
				if y < y2: return x, y2
				elif y1 < y: return x, y1
				else: return n
	def pinfodis_by_pe(n, e): ###
		p = pnode_by_pe(n, e)
		dis = distance(n, p)
		if p in e: e = None
		return (p, e), dis
	def pinfo_by_pe(n, e):
		p = pnode_by_pe(n, e)
		if p in e: return p, None
		else: return p, e
	def pedis_by_pe(n ,e): ###
		p = pnode_by_pe(n, e)
		dis = distance(n, p)
		if p in e: e = None
		return p, e, dis
	if "grid":
		"""
			边界上不能有点
			"""
		# misc
		def quarter_dire_nn(n1, n2):
			"""
				边界上随意 ?
				"""
			x1, y1 = n1
			x2, y2 = n2
			dx = x2 - x1
			dy = y2 - y1
			#
			if dy > dx:
				if dy > -dx: r = enum.up
				else: r = enum.left
			else:
				if dy > -dx: r = enum.right
				else: r = enum.down
			return r
		def expand_distance_by_i(i, short, unit):
			return short + i * unit
	if "square":
		# index
		def squareIndexVals_by_val(x, unit) -> set:
			q = x // unit
			r = x % unit
			if r == 0:
				return {q - 1, q}
			else: return {q}
		# val
		def squareIndexVal_lowerbound(x, unit):
			return x // unit
		def squareIndexVal_greaterbound(x, unit):
			return (x - 1) // unit + 1 # ceildiv
		def squareIndexVal_lower(x, unit):
			return ( x - 1 ) // unit # ceildiv - 1
		def squareIndexVal_greater(x, unit):
			return ( x // unit )
	if "expand":
		# expand_dire
		def expandDire_index(nx, ny, dire, i):
			if dire == enum.left:
				return (nx - i, ny)
			elif dire == enum.right:
				return (nx + i, ny)
			elif dire == enum.down:
				return (nx, ny - i)
			elif dire == enum.up:
				return (nx, ny + i)
			else: raise Exception(f'unexpected [{dire}], expecting[{enum.left} {enum.right} {enum.down} {enum.up}')
		# square-expand
		def get_expandDiamond_ri(i):
			if i == 0:
				r = { (0, 0) }
			else:
				r = { (0, i) }
				for j in range(1, i+1):
					r.add( (j, i+1-j) )
				
				for c1 in list(r):
					c2 = my.geo.rotate(c1)
					c3 = my.geo.rotate(c2)
					c4 = my.geo.rotate(c3)
					r.add(c2)
					r.add(c3)
					r.add(c4)
			return r
		def get_expandDiamondSpan_ri(span, i):
			"""
				无视完全在被包围的区块
				参考是左下角
				"""
			spanx, spany = span
			if i == 0:
				r = set()
				for y in range(spany):
					r.add((0, y))
					r.add((spanx-1, y))
				for x in range(1, spanx-1):
					r.add((0, x))
					r.add((spany-1, x))
			else: # 上和左上
				r = set() 
				# 上
				y0 = spany+i-1 #上方y坐标
				for j in range(-1, spanx+1):
					r.add( (j, y0) )
				# 右
				x0 = spanx+i-1 #右方x坐标
				for j in range(-1, spany+1):
					r.add( (x0, j) )
				
				#左上
				for j in range(i-2):
					r.add( ( -2 - j, y0 - 1 - j ) )
				# mirror
				center2 = spanx - 1, spany - 1
				for c1 in r.copy():
					c2 = my.geo.mirror_on_xline2_int(c1, spanx - 1)
					r.add(c2)
				for c1 in r.copy():
					c2 = my.geo.mirror_on_yline2_int(c1, spany - 1)
					r.add(c2)
			return r
		def get_expandPlain_ri(i):
			if i == 0: return { (0, 0) }
			r = set()
			for x in range(-i, i):
				r.add((x, i))
			# rotate
			r |= geo.nodes.rotate(r)
			r |= geo.nodes.mirror(r)
			return r
	# judge
	def is_Linfo(pinfo):
		p, e = pinfo
		if e == None: return False
		n1, n2 = e
		x1, y1 = n1
		x2, y2 = n2
		return p == (x1, y2) or p == (x2, y1)
	def in_line_nn(n1, n2):
		x1, y1 = n1
		x2, y2 = n2
		return x1 == x2 or y1 == y2
	# block
	def is_edge_block_node_dim(e, n, dim):
		#. dim 是n延长的方向
		#. 端点也算
		dimv = 1 - dim
		n1, n2 = e
		z1, z2 = n1[dimv], n2[dimv]
		z = n[dimv]
		return z1 <= z <= z2 or z2 <= z <= z1
	def is_plain_block_nnn(n1, n2, n3):
		"""
			要求： 三点不同
			算法：
				在矩形内
			"""
		assert n1 != n2, n1
		assert n1 != n3
		assert n2 != n3
		x1, y1 = n1
		x2, y2 = n2
		x3, y3 = n3
		return my.math.in_range(x2, x1, x3) and my.math.in_range(y2, y1, y3)
if "data":
	def save_nodes(nodes, count, seed, *, save): ###
		key = (count, seed)
		assert seed >= 0 and count > 0 and count == len(nodes)
		nodes_info = data.nodes()
		if key in nodes_info:
			if save == True: return
			assert save == 'cover', f'{save}'
		nodes_info[key] = nodes
		data.nodes.dump(nodes_info)
	def add_key(key, *, cover=False):
		assert isinstance(key, tuple)
		if len(key) == 2: 
			count, seed = key
			cap = None
		elif len(key) == 3: count, seed, cap = key
		else: raise Exception(f'{key}')
		
		nodes_info = data.nodes()
		if not cover and key in nodes_info: return
		nodes = nodes_random_seed(count, seed=seed, cap=cap)
		# save
		nodes_info[key] = nodes
		data.nodes.save()
	def update_basic_note():
		smt_info = data.smt_info.load()
		# smt_info
		lines = []
		for key, info in sorted(smt_info.items()):
			le, time, full = info
			lines.append(f'{key}  len = {le}  time = {time}')
		my.file.writelines(smt_note_path, lines)
		# keys
		lines = []
		nodes_info = data.nodes()
		for key, nodes in sorted(nodes_info.items()):
			lines.append(f'{key}')
		my.file.writelines(keys_note_name, lines)
if "differ":
	"""
		differ: 不同的边
		fdiffer:
			有区别的整组
		fdiffer_len:
			长度不同的整组
		"""
	def differ_fst4444(g1, g2):
		"""
			g1: perfect
			说明：
				返回一组整子图对，每个子图对要么完全相同，要么不同且尽可能小
			算法：
				先找不同的fst
				根据连点连线定理确定对面的fst
				根据对面fst的奇异点确定己方fst
				往复
			定理：
				若两个fst相同，一定位于同一组
				两个点属于一组，则路径上所有fst属于一组
			
			"""
		F1 = g1.fsts()
		F2 = g2.fsts()
		D1 = g1.fst_dict()
		D2 = g2.fst_dict()

		#
		
		node_groups = []
		groups1, groups2 = [], [] # [ fsts .. ]
		while 1:
			# 寻找奇异
			flag_found = False
			for fst1 in F1:
				if fst1 not in F2:
					flag_found = True
					break
			if not flag_found: break
			nodes1 = fst1.copy()
			nodes2 = set()
			for i in range(math.inf):
				if i % 2 == 0: res = blance_fst(nodes1, nodes2, F1, F2, D1, D2)
				elif i % 2 == 1:res = blance_fst(nodes2, nodes1, F2, F1, D2, D1)
				if res: break
			# nodes1 = self.set.union_m(group1)
			# nodes2 = self.set.union_m(group2)
			assert nodes1 == nodes2
			node_groups.append(nodes1)
			# groups1.append(group1)
			# groups2.append(group2)
		assert F1 == F2
		return nodes_groups
	def blance_fstfff(nodes1, nodes2, F1, F2, D1, D2):
		"""
			nodes1 > nodes2 且 nodes1 是树
			说明：
				要求让nodes2 >= nodes1 且 nodes2是树
				等于时返回True
			"""
		assert nodes2.issubset(nodes1)
		#补全奇异点
		nodes_differ = nodes1.difference(nodes2)
		for n in nodes_differ:
			if n in nodes2: continue
			fst2 = D2[n]
			nodes2 |= fst2
		#补全树
		hg = HyperGraph.from_edges
		fst_complete_tree(fst2)
	def differ(g1, g2) -> 'subgraph1, subgraph2':
		fd_map1 = g1.fd_map()
		fd_map2 = g2.fd_map()
		fsts1 = fd_map1.keys()
		fsts2 = fd_map2.keys()
		h1 = HyperGraph.from_edges(fsts1)
		h2 = HyperGraph.from_edges(fsts2)
		differ1, differ2 = HyperGraph.differ(h1, h2)
		sub1 = g1.sub_from_dfsts(fd_map1[fst] for fst in differ1)
		sub2 = g2.sub_from_dfsts(fd_map2[fst] for fst in differ2)
		return sub1, sub2
	def fdiffer(g1, g2) -> 'subgraph1, subgraph2':
		fd_map1 = g1.fd_map()
		fd_map2 = g2.fd_map()
		fsts1 = fd_map1.keys()
		fsts2 = fd_map2.keys()
		h1 = HyperGraph.from_edges(fsts1)
		h2 = HyperGraph.from_edges(fsts2)
		differ1, differ2 = HyperGraph.fdiffer(h1, h2)
		sub1 = g1.sub_from_dfsts(fd_map1[fst] for fst in differ1)
		sub2 = g2.sub_from_dfsts(fd_map2[fst] for fst in differ2)
		return sub1, sub2
	def fdiffer_weight(g1, g2) -> 'subgraph1, subgraph2':
		fd_map1 = g1.fd_map()
		fd_map2 = g2.fd_map()
		fsts1 = fd_map1.keys()
		fsts2 = fd_map2.keys()
		h1 = HyperGraph.from_edges(fsts1, weight=lambda fst: fd_map1[fst].len())
		h2 = HyperGraph.from_edges(fsts2, weight=lambda fst: fd_map2[fst].len())
		differ1, differ2 = HyperGraph.fdiffer_weight(h1, h2)
		sub1 = g1.sub_from_dfsts(fd_map1[fst] for fst in differ1)
		sub2 = g2.sub_from_dfsts(fd_map2[fst] for fst in differ2)
		return sub1, sub2
	def fdiffer_weight_misc(g1, g2) -> 'sub1, sub2, pairs':
		fd_map1 = g1.fd_map()
		fd_map2 = g2.fd_map()
		fsts1 = fd_map1.keys()
		fsts2 = fd_map2.keys()
		h1 = HyperGraph.from_edges(fsts1, weight=lambda fst: fd_map1[fst].len())
		h2 = HyperGraph.from_edges(fsts2, weight=lambda fst: fd_map2[fst].len())
		#
		pairs_ = HyperGraph.fdiffer_gen_pairs_weight(h1, h2) # [ edges, edges .. ]
		if empty(pairs_): groups1_, groups2_ = [], []
		else: groups1_, groups2_ = zip(*pairs_)
		sub1_ = my.list.unionm(groups1_)
		sub2_ = my.list.unionm(groups2_)
		sub1 = g1.sub_from_dfsts(fd_map1[fst] for fst in sub1_)
		sub2 = g2.sub_from_dfsts(fd_map2[fst] for fst in sub2_)
		#
		pairs = []
		for group1_, group2_ in pairs_:
			group1 = g1.sub_from_dfsts(fd_map1[fst] for fst in group1_)
			group2 = g1.sub_from_dfsts(fd_map2[fst] for fst in group2_)
			pairs.append( (group1, group2) )
		return sub1, sub2, pairs
if "experiment":
	def draw_time_map(time_map,*, h, color, **ks):
		xlist = []
		ylist = []
		for key, time in time_map.items():
			if len(key) == 2: continue
			if time is not None and time.s() > default.test_timeout: time = None
			size, seed, cap = key
			assert cap == default.test_cap
			xlist.append(size ** 1)
			if time is None: 
				val = h
			else: val = time.s()
			ylist.append(val)
		# draw
		myplt.scatter(xlist, ylist, color=color, **ks)
		plt.yscale('log')

	# match
	def mst_match(hg):
		
		solver = hg.mst_test(
			solver_args=dict(debug=0, verbose_text=0, verbose_pic=0, ishow=0,
				_print=dict(expand_state=1, set_map=0, update_net=1, combine=1),
				_show=dict(models=0, net=0, valid_add=1, invalid_add=0, set_map=0),
				filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace= None,
				best1=0, no_cycle=1, combine=1,
				order_mode=None, cut_mode=0, 
				state_threshold=2000, iter_threshold=my.inf,
				threshold_addState_edgeRate=0.1, pick_start='auto1',
				# threshold_addState_model=12,
			),
			solve_args=dict(
				return_solver=1,
			),
		)
		mst = solver.mst
		return mst
	def update_smt_match_time(save=True):
		nodes_map = data.nodes()
		time_map = data.smt_match_time()
		for key, nodes in my.dict.sorted_items_by_key(nodes_map):
			if len(key) == 3:
				size, seed, cap = key
				assert size == len(nodes)
				# if key in time_map and time_map[key] is not None: continue
				if key in time_map: continue
				hg = pruned_hg_by_key(key)	
				mst0_len = smt_len(key)
				assert size == len(hg.nodes)
				mst, time = my.time.time(lambda:mst_match(hg), time_floor=0.5, timeout=default.test_timeout)
				if time is False:
					time_map[key] = None
					print(f'smt_match_time {key} timeout')
					data.smt_match_time.save()

				else:
					le = mst.len()
					assert le == mst0_len
					time_val = time.ns()
					time_map[key] = time
					data.smt_match_time.save()
					print(f'smt_match_time {key} {time}')
	def draw_smt_match_time():
		time_map = data.smt_match_time()
		draw_time_map(time_map)
	# filter
	def mst_filter(hg):
		
		solver = hg.mst_test(
			solver_args=dict(debug=0, verbose_text=0, verbose_pic=0, ishow=0,
				_print=dict(expand_state=1, set_map=0, update_net=1, combine=1),
				_show=dict(models=0, net=0, valid_add=1, invalid_add=0, set_map=0),
				filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace= None,
				filter_mode=1,
				best1=0, no_cycle=1, combine=1,
				order_mode=None, cut_mode=0, 
				state_threshold=1000, iter_threshold=my.inf,
				threshold_addState_edgeRate=0.1, pick_start='auto1',
				# threshold_addState_model=12,
			),
			solve_args=dict(
				return_solver=1,
			),
		)
		mst = solver.mst
		return mst
	def update_smt_filter_time():
		nodes_map = data.nodes()
		time_map = data.smt_filter_time()
		for key, nodes in my.dict.sorted_items_by_key(nodes_map):
			if len(key) == 3:
				# if key in time_map and time_map[key] is not None: continue
				if key in time_map: continue
				hg = pruned_hg_by_key(key)	
				mst0_len = smt_len(key)

				mst, time = my.time.time(lambda:mst_filter(hg), time_floor=0.5, timeout=default.test_timeout)
				if time is False:
					time_map[key] = None
					print(f'smt_filter_time {key} timeout')
					data.smt_filter_time.save()

				else:
					le = mst.len()
					assert le == mst0_len
					time_val = time.ns()
					time_map[key] = time
					data.smt_filter_time.save()
					print(f'smt_filter_time {key} {time}')
		
	def draw_smt_filter_time():
		time_map = data.smt_filter_time()
		draw_time_map(time_map)

	# simple
	def mst_simple(hg):
		
		solver = hg.mst_test(
			solver_args=dict(debug=0, verbose_text=0, verbose_pic=0, ishow=0,
				_print=dict(expand_state=1, set_map=0, update_net=1, combine=1),
				_show=dict(models=0, net=0, valid_add=1, invalid_add=0, set_map=0),
				filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace= None,
				best1=0, no_cycle=1, combine=1,
				order_mode=None, cut_mode=0, 
				state_threshold=my.inf, iter_threshold=my.inf,
				threshold_addState_edgeRate=0.1, pick_start='node0',
				# threshold_addState_model=12,
			),
			solve_args=dict(
				return_solver=1,
			),
		)
		mst = solver.mst
		return mst
	def update_smt_simple_time():
		nodes_map = data.nodes()
		time_map = data.smt_simple_time()
		for key, nodes in my.dict.sorted_items_by_key(nodes_map):
			if len(key) == 3:
				# if key in time_map and time_map[key] is not None: continue
				if key in time_map: continue
				hg = pruned_hg_by_key(key)	
				mst0_len = smt_len(key)

				mst, time = my.time.time(lambda:mst_simple(hg), time_floor=0.5, timeout=default.test_timeout)
				if time is False:
					time_map[key] = None
					print(f'smt_simple_time {key} timeout')
					data.smt_simple_time.save()

				else:
					le = mst.len()
					assert le == mst0_len
					time_val = time.ns()
					time_map[key] = time
					data.smt_simple_time.save()
					print(f'smt_simple_time {key} {time}')
		
	def draw_smt_simple_time():
		time_map = data.smt_simple_time()
		draw_time_map(time_map)

	#
	def draw_test():
		c1, c2, c3 = colors = my.color.constract(3, background='white')
		# simple
		time_map = data.smt_simple_time()
		draw_time_map(time_map, h=30, color=c1)
		
		# filter
		time_map = data.smt_filter_time()
		color = my.color
		draw_time_map(time_map, new=False, h=40, color=c2)
		
		# match
		time_map = data.smt_match_time()
		draw_time_map(time_map, new=False, h=50, color=c3)
		# matplotlib.rc("font",family='SimHei', size=24)
		# plt.rcParams['font.sans-serif'] = ['FangSong']
		myplt.xlabel('端点数n')
		myplt.ylabel('时间t(s)')
		myplt.legend( ('简单平推法', '过滤法', '匹配法') )
		# geo
		# info_map = data.smt_info()
		# data.smt_info.save()
		# time_map = {key: my.unit.time.s(time) for key, (le, time, full) in info_map.items() }
		# draw_time_map(time_map, new=False)
		

		# draw
		
class Process:
	name_dict = {}
	def __init__(self, name, data_, note_path):
		self.name = name
		self.data = data_
		self.note_path = note_path
	if "str":
		@staticmethod
		def str_time(time1, time2=None):
			r = f'time= {my.format.science_move(time1, '>10.2', -9)}'
			if time2 != None: 
				r += f'/{my.format.science_move(time2, '>10.2', -9)}'
			return r
		@staticmethod
		def str_len(le, *, key):
			le_ = le - smt_len(key)
			r = f'len={le:>6}/{le_:>6}'
			return r
		@staticmethod
		def str_key_info(key, info):
			le, time = info
			le_ = le - smt_len(key)
			return (
				f'{my.format(str(key)+':', '<13', expr='***')} '
				f'len={le:>6}/{le_:>6}    '
				f'{Process.str_time(time, None)} '
			)
	#public
	def run(self, *, keys=None, save=0, cover=0):
		count = 0
		unsaved = 0
		data_ = self.data()
		nodes_info = data.nodes()
		if keys == None: nodes_items = sorted(nodes_info.items())
		else:
			nodes_items = [ (key, nodes_info[key]) for key in keys ]
		nodes_items = sorted(nodes_items)
		assert my.is_unique(keys)
		for key, nodes in nodes_items:
			if not cover and key in data_: continue
			print(f'{self.name} {key}')
			with Timer() as timer:
				g = getattr(SG, self.name)(nodes, debug=False)
			count += 1
			unsaved += 1
			time = timer.time()
			le = g.length()
			data_[key] = (le, time)
			print(
				f'{self.str_len(le, key=key)}    '
				f'{Process.str_time(time, None)} '
			)
			if save and count % setting.save_interval == 0:
				self.data.save()
				unsaved = 0
		if save and unsaved > 0: self.data.save()
		print(f'{count} {self.name} updated')
		#note
		if save: self.update_note()
	def update_note(*gs):
		"""
			Process.update_note: all
			self.update_note
			"""
		if len(gs) == 0:
			for name, process in Process.name_dict.items():
				process.update_note_()
		elif len(gs) == 1:
			gs[0].update_note_()
		else: raise Exception(f'{gs}')
	def update_note_(self):
		
		lines = []
		data_ = self.data()
		# average
		size_list = [key[0] for key in data_.keys()]
		count_dict = {size: size_list.count(size) for size in size_list}
		for size, count in count_dict.items():
			if count < 5: continue
			keys = [key for key, info in data_.items() if key[0] == size]
			infos = [info for key, info in data_.items() if key[0] == size]
			avg_le = sum( info[0] for info in infos ) / len(infos)
			avg_le_delta = sum( data_[key][0] - smt_len(key) for key in keys ) / len(keys)
			avg_time = sum( info[1] for info in infos ) / len(infos)
			lines.append(
				f'average-{size:<5} '
				f'delta={avg_le_delta/avg_le:>12.2e}    '
				f'{self.str_time(avg_time)}'
			)
		lines.append('')
		# full
		for key, info in sorted(data_.items()):
			lines.append(self.str_key_info(key, info))
		
		my.file.writelines(self.note_path, lines)
		print(f'{self.name} set note')

class Dfst:
	def __init__(self, Dnodes, Snodes, edges):
		self.Dnodes = set(Dnodes)
		self.Snodes = set(Snodes)
		assert all(is_std(e) for e in edges), (e, edges)
		self.edges = set(edges) # sorted
		self._weight = sum( edge_length(e) for e in edges )
	def __str__(self):
		r = f'Dnodes={self.Dnodes} Snodes={self.Snodes} edges={self.edges}'
		return r
	__repr__ = __str__

	# info
	def len(self):
		return self._weight
	weight = len
	def fst(self):
		return self.Dnodes.copy()
class SteinerGraph(PosGraph):
	"""
		结构
			std_edges: {}
			skewed_edges: {} # std
		"""
	def __init__(self, *, Dnodes=None, edges=[], nodes=None, Snodes=None, skew=None):
		super().__init__()
		# nodes
		if Dnodes != None:
			self.define_Dnodes(Dnodes)
		if nodes != None:
			assert Snodes == None
		if Snodes != None:
			assert nodes == None
			nodes = my.set.union_nonlap(Dnodes, Snodes)
		# nnd
		self.strict_nnd = {}
		self.nnd = {}
		#
		self._skew = skew
		self.skewed_edges = set()
		self.std_edges = set()
		self.snd = {} # sorted_nodes_dim snd[dim]
		for dim in enum.dims:
			self.snd[dim] = SortedList(key=enum.key_dim[dim], rkey=enum.rkey_dim[dim])
		self.nodes_index = {dim: defaultdict(list) for dim in enum.dims}
		#oper
		if nodes != None: self.add_nodes(nodes)
		if edges != None: self.connectm(edges)
	if "info":
		#basic
		@staticmethod
		def distance_ne(n, e):
			self = SG
			dis = self.distance(n, self.pnode_by_pe(n ,e))
			return dis
		@staticmethod
		def distance(n1, n2):
			x1, y1 = n1
			x2, y2 = n2
			return abs(x1 - x2) + abs(y1 - y2)
		@staticmethod
		def dires_nn(n1, n2) -> 'xdire, ydire':
			x1, y1 = n1
			x2, y2 = n2
			if x1 < x2: dire1 = enum.right
			elif x1 > x2: dire1 = enum.left
			else: raise
			if y1 < y2: dire2 = enum.up
			elif y1 > y2: dire2 = enum.down
			else: raise
			return dire1, dire2
		#judge
		@staticmethod
		def on_line(n1, n2):
			x1, y1 = n1
			x2, y2 = n2
			return x1 == x2 or y1 == y2
		@staticmethod
		def is_sedge(e):
			return SG.on_line(*e)
		def isDnode(self, n):
			return n in self.Dnodes
		def is_used_node(self, n):
			if self.isDnode(n): 
				return True
			adjs = self.adj[n]
			if len(adjs) in (0, 2):
				return False
			elif len(adjs) == 1:
				raise
			else:
				return True
		def is_Dinfo(self, pinfo):
			p, e = pinfo
			return e == None and self.isDnode(p)
		@staticmethod
		def edge_equal(e1, e2):
			n1, n2 = e1
			m1, m2 = e2
			return (n1 == m1 and n2 == m2) or (n1 == m2 and n2 == m1)
		#graph-info
		def length(self):
			r = 0
			for edge in self.edges:
				r += edge_length(edge)
			return r
		len = length
		def Lnode_infos(self) -> '[p, e]':
			for e in self.diagonal_edges():
				(x1, y1), (x2, y2) = e
				r.append(((x1, y2), e))
				r.append(((x2, y1)), e)
			return r
		def Snodes(self):
			return [n for n in self.nodes if n not in self.Dnodes]
		def Ginfos(self, *, mode=None):
			# Gdict = {}
			# for v, es in Linfo_dict.items():
			# 	for e in es:
			# 		Gdict[v] = e
			# for n in self.nodes:
			# 	Gdict[n] = None
			# Ginfos = Gdict.items()
			return my.iter_dynamic(self.Ginfos_, mode=mode)
		def DLinfos(self) -> set:
			r = { (n, None) for n in self.Dnodes }
			r |= self.Linfos()
			return r
		def Linfos(self) -> set:
			r = set()
			for e in self.skewed_edges:
				p1, p2 = Lnodes_by_skewed_edge(e)
				r.add( (p1, e) )
				r.add( (p2, e) )
			return r
		#info-misc
		@staticmethod
		def dim_sedge(sedge):
			n1, n2 = (x1, y1), (x2, y2) = sedge
			if x1 == x2: return 1
			elif y1 == y2: return 0
			else: raise Exception(f'{sedge}')	
		@staticmethod
		def Linfos_by_nn(n1, n2):
			# 返回 e 有序
			e = n1, n2 = sorted_nn(n1, n2)
			x1, y1 = n1
			x2, y2 = n2
			if x1 == x2 or y1 == y2: r = []
			else:
				r = [ ( (x1, y2), e), ( (x2, y1), e ) ]
			return r
		@staticmethod
		def node_from_dims(dim1, value1, value2):
			if dim1 == 0:
				return value1, value2
			else:
				assert dim1 == 1, f'{0}'
				return value2, value1
		#info-algo
		def find_path_pp(self, pinfo1, pinfo2): # 包含首尾的p
			p1, e1 = pinfo1
			p2, e2 = pinfo2
			assert p1 != p2, f'{pinfo1, pinfo2}'
			
			if e1 == None: a1 = p1
			else: a1, b1 = e1
			if e2 == None: a2 = p2
			else: a2, b2 = e2

			path = self.find_path(a1, a2)
			if e1 != None: #v
				if len(path) > 1 and path[1] == b1:
					path.pop(0)
				path.insert(0, p1)
			if e2 != None: #v
				if path[-2] == b2:
					path.pop()
				path.append(p2)
			return path
	if "oper":
		#oper-basic
		def add_node(self, n):
			super().add_node(n)
			# nnd
			self.nnd[n] = [None, None, None, None]
			self.strict_nnd[n] = [None, None, None, None]
			#
			for dim in enum.dims:
				self.snd[dim].add(n)
				self.nodes_index[dim][n[dim]].append(n)
			if de.highlight_node:
				de.hl.add(n)
		def remove_node(self, n):
			super().remove_node(n)
			# nnd
			del self.nnd[n]
			del self.strict_nnd[n]
			#
			for dim in enum.dims:
				self.snd[dim].remove(n)
				self.nodes_index[dim][n[dim]].remove(n)
			if de.lowlight_node:
				de.ll.add(n)
		def define_Dnodes(self, nodes):
			assert not hasattr(self, 'Dnodes')
			self.Dnodes = set(nodes)
		#connect
		def connect(self, n1, n2):
			n1, n2 = sorted_nn(n1, n2)
			return self.connect_sorted(n1, n2)
		def connect_sorted(self, n1 ,n2): #自动排序
			assert n1 != n2, (n1, n2)
			assert is_std((n1, n2)), (n1, n2)
			super().connect(n1, n2)
			e = (x1, y1), (x2, y2) = (n1, n2)
			if x1 != x2 and y1 != y2: # skewed
				v1 = x1, y2
				v2 = x2, y1
				self.skewed_edges.add(e)
				self.signal_new_Lnode(v1, e)
				self.signal_new_Lnode(v2, e)
			self.std_edges.add(e)
			# nnd strict_nnd
			if y1 < y2:
				self.nnd[n1][enum.up] = n2
				self.nnd[n2][enum.down] = n1
			elif y1 > y2:
				self.nnd[n1][enum.down] = n2
				self.nnd[n2][enum.up] = n1
			else:
				self.strict_nnd[n1][enum.right] = n2
				self.strict_nnd[n2][enum.left] = n1
			if x1 < x2:
				self.nnd[n1][enum.right] = n2
				self.nnd[n2][enum.left] = n1
			elif x1 > x2:
				self.nnd[n1][enum.left] = n2
				self.nnd[n2][enum.right] = n1
			else: 
				self.strict_nnd[n1][enum.up] = n2
				self.strict_nnd[n2][enum.down] = n1
			#
			if de.highlight_edge:
				de.hl.add(e)
		def disconnect(self, n1, n2, *, clear=False):
			n1, n2 = sorted_nn(n1, n2)
			self.disconnect_sorted(n1, n2)
			if clear:
				self.clear_node(n1)
				self.clear_node(n2)
			return self
		def disconnect_sorted(self, n1, n2):
			assert is_std((n1, n2)), (n1, n2)
			super().disconnect(n1, n2)
			e = (x1, y1), (x2, y2) = tuple(sorted((n1, n2)))
			# nnd
			if y1 < y2:
				self.nnd[n1][enum.up] = None
				self.nnd[n2][enum.down] = None
			elif y1 > y2:
				self.nnd[n1][enum.down] = None
				self.nnd[n2][enum.up] = None
			else:
				self.strict_nnd[n1][enum.right] = None
				self.strict_nnd[n2][enum.left] = None
			if x1 < x2:
				self.nnd[n1][enum.right] = None
				self.nnd[n2][enum.left] = None
			elif x1 > x2:
				self.nnd[n1][enum.left] = None
				self.nnd[n2][enum.right] = None
			else: 
				self.strict_nnd[n1][enum.up] = None
				self.strict_nnd[n2][enum.down] = None
			#
			if x1 != x2 and y1 != y2: # skewed
				v1 = x1, y2
				v2 = x2, y1
				self.skewed_edges.remove(e)
				self.signal_del_Lnode(v1, e)
				self.signal_del_Lnode(v2, e)
			self.std_edges.remove(e)
			if de.lowlight_edge:
				de.ll.add(e)
		def connectm(self, edges):
			for n1, n2 in edges:
				self.connect(n1, n2)
		def remove_edges(self, edges):
			raise
		#special
		def set_p(self, pinfo):
			p, e = pinfo
			if self.has_node(p): return
			self.set_v(pinfo)
		def set_v(self, vinfo):
			v, e = vinfo
			n1, n2 = e
			assert v != n1 and v != n2
			self.disconnect(n1, n2)
			self.add_node(v)
			self.connect(n1, v)
			self.connect(n2, v)
		def connect_ne(self, n, e):
			pinfo = pinfo_by_pe(n, e)
			self.connect_np(n, pinfo)
		def connect_np(self, n, pinfo):
			p, e = pinfo
			self.set_p(pinfo)
			self.connect(n, p)
		def connect_pp(self, pinfo1, pinfo2):
			p1, e1 = pinfo1
			p2, e2 = pinfo2
			assert p1 != p2, f'{pinfo1, pinfo2}'
			
			self.set_p(pinfo1)
			self.set_p(pinfo2)
			self.connect(p1, p2)
		# close
		def disconnect_close(self, n1, n2): # clear=True
			n1, n2 = e = sorted_nn(n1, n2)
			self.disconnect_sorted(n1, n2)
			# clear-close
			self.clear_close(n1)
			self.clear_close(n2)
			return self
		def clear_close(self, n):
			assert self.has_node(n)
			if self.isDnode(n): return False
			adjs = self.adj[n]
			if len(adjs) == 0: 
				raise
				self.remove_node(n)
				return True
			elif len(adjs) == 1:
				raise
			elif len(adjs) == 2:
				n1, n2 = adjs
				self.disconnect(n, n1)
				self.disconnect(n, n2)
				self.remove_node(n)
				self.connect_close(n1, n2)
			else: return False
		def connect_close(self, n1, n2):
			n1, n2 = sorted_nn(n1, n2)
			self.connect_close_sorted(n1, n2)
			return self
		def connect_close_sorted(self, n1, n2):
			e = n1, n2
			# 合并
			for dim in enum.dims: # 两个方向
				if n1[dim] == n2[dim]: continue
				dire12 = dire_nn_in_dim(n1, n2, dim)
				dire21 = enum.opposite_dire[dire12]
				for n5, n6, dire in (n1, n2, dire12), (n2, n1, dire21): #两个点都考虑
					n7 = self.nnd[n5][dire] # 尝试找到可以合并的边
					if n7 != None: # 找到可以合并的边
						edge = (n5, n7) # 合并边
						# set_p
						px, ex = pinfo = pinfo_by_pe(n6, edge)
						self.set_p(pinfo)
						# connect
						self.connect_close(n6, px)
						self.clear_node(n5) #??
						return
			self.connect_sorted(n1, n2)
		# clear
		def clear_node(self, n) -> bool:
			#中间或孤立
			#if not self.has_node(n): return False
			assert self.has_node(n)
			if self.isDnode(n): return False
			adjs = self.adj[n]
			if len(adjs) == 0: 
				raise
				self.remove_node(n)
				return True
			elif len(adjs) == 1:
				raise
			elif len(adjs) == 2:
				n1, n2 = adjs
				self.disconnect(n, n1)
				self.disconnect(n, n2)
				self.remove_node(n)
				self.connect(n1, n2)
			else: return False
		def clear_nodes(self, nodes):
			for node in nodes:
				self.clear_node(node)
		add_edge = NotImplemented
		#react
		def signal_new_Lnode(self, v, e):
			...
		def signal_del_Lnode(self, v, e):
			...
		#oper-complex
		def extend_np(self, n, pinfo):
			p, e = pinfo
			self.set_p(pinfo)
			if n == p: return
			self.add_node(n)
			self.connect(n, p)
	if "algo":
		def mst(nodes, *, debug=0):
			debug = de.debug and debug
			mst_ = Graph.mst(Graph.full_graph(nodes, weight=lambda e: SG.distance(*e)))
			nodes, edges = mst_.nodes, mst_.edges
			self = SG(Dnodes=nodes, nodes=nodes, edges=edges)
			if debug:
				self.draw(title_a='mst')
			return self
	if "fst":
		"""
			dfst: Dnodes Snodes edges
			"""
		def dfsts(self) -> list:
			"""
				starts = []

				while 完成一个fst
					starts中拿出一个起点start
					start找出一个未走过的方向first加入fst
					fst = [ first ]
					waiting = [ first ]
					while 
						将waiting中的值取出一个，展开，更新waiting和fst
						waiting空：返回
					starts空：返回
				"""
			r = []
			starts = { my.set.pick(self.Dnodes) } #Dnode
			walked = set(starts)
			while 1:
				if empty(starts): break
				start = starts.pop()
				for first in self.adj[start]: # 单个fst
					if first in walked: continue
					#
					if self.isDnode(first): # 仅有一条边
						edges = { sorted_nn(start, first) }
						Dnodes = {start, first}
						Snodes = set()
						starts.add(first)
						walked.add(first)
					else:
						Snodes = {first}
						edges = { sorted_nn(first, start) }
						Snodes_waiting = {first}
						Dnodes = {start}
						walked.add(first)
						while 1:
							w = Snodes_waiting.pop()
							for n in self.adj[w]: # 单步行走
								if n in walked: continue
								elif self.isDnode(n): 
									Dnodes.add(n)
									starts.add(n)
									walked.add(n)
									edges.add( sorted_nn(w, n) )
								else:
									Snodes.add(n)
									Snodes_waiting.add(n)
									walked.add(n)
									edges.add( sorted_nn(w, n) )
							if empty(Snodes_waiting): break
					dfst = Dfst(Dnodes, Snodes, edges)
					r.append(dfst)
			return r
		def fsts(self) -> list: ###
			dfsts = self.dfsts()
			r = [ dfst.fst() for dfst in dfsts ]
			return r
		def fd_map(self):
			dfsts = self.dfsts()
			r = DictHash( ((dfst.fst() , dfst) for dfst in dfsts), hash=my.set.hash )
			return r
		@classmethod
		def sub_from_dfsts(cls, dfsts) -> 'graph':
			dfsts = list(dfsts)
			Dnodes = my.set.union_m( dfst.Dnodes for dfst in dfsts )
			Snodes = my.set.union_m( dfst.Snodes for dfst in dfsts )
			edges = my.set.union_m( dfst.edges for dfst in dfsts )
			return cls(Dnodes=Dnodes, Snodes=Snodes, edges=edges)
	if "generate":
		#generate-order
		def generate_order(Dnodes, *, debug=1):
			axs = []
			self = SG()
			debug = debug and de.generate_order
			assert empty(self.Dnodes)
			self.define_Dnodes(Dnodes)
			self.add_node(Dnodes[0])
			for node in Dnodes[1:]:
				if debug:
					de.light_on()
				self.extend_D_near(node)
				if debug:
					de.light_off()
					self.draw(hl=[node], title_a=' go')
					axs.append(myplt.ax())
			for ax in axs[:-1]:
				ax.axis(axs[-1].axis())
			self.check()
			return self
		def extend_D_near(self, D):
			pinfo = self.extend_nearest_p(D)
			self.extend_np(n, pinfo)
		def extend_nearest_p(self, n) -> 'pinfo':
			if n == (47, 56):
				pass
			if len(self.nodes) == 1: 
				n0 = list(self.nodes)[0]
				return n0, None
			else:
				assert len(self.edges) != 0, self.nodes

				pinfo = min([pinfo_by_pe(n, e) for e in self.edges], key=lambda inf: self.distance(inf[0], n))
				return pinfo
		#generate-short
		def generate_short(Dnodes, *, debug=1): ###
			debug = debug and de.generate_short
			#
			self = SG()
			self.define_Dnodes(Dnodes)
			assert empty(self.Dnodes)
			Dnodes = set(Dnodes)
			start = Dnodes.pop()
			self.add_Dnode(start, add_node=True)
			
			axs = []
			while not empty(Dnodes):
				extend_pairs = [ (n, self.extend_nearest_p(n)) for n in Dnodes ]
				n, pinfo = min( extend_pairs, key=lambda pair: self.distance(pair[0], pair[1][0]) )
				if debug:
					de.light_on()
				self.extend_np(n, pinfo)
				Dnodes.remove(n)
				if debug:
					de.light_off()
					self.draw(hl=[n], title_a=' gs')
					axs.append(myplt.ax())
			for ax in axs[:-1]:
				ax.axis(axs[-1].axis())
				self.check()
			return self
	if "evolve":
		#evolve-general
		def evolve_method(self, method, name, *, debug=0):
			debug = de.debug and debug
			cycle_count = 0
			if debug:
				self.draw(title_a=f'start-{name}')
			while 1:
				flag_modified = method(debug=debug)
				if not flag_modified: break
				cycle_count += 1
			if debug and de.count_cycle: 
				print(f'cycle: {cycle_count}')
			self.check()
			if debug:
				self.draw(title_a=f'end-{name}')
		def evolve_methods(self, methods, names, *, debug=0, classes=None): ###
			"""
				compatible: 能否共用类方法
				"""
			debug = de.debug and debug
			size = len(methods)
			valid_cycle_record = []
			blank_cycle_count = 0
			cycles = []

			for j in range(100):
				i = j % size
				method = methods[i]
				name = names[i]
				if classes == None:
					modified = self.evlove_methods_cycle(method, name, debug=debug)
				else:
					cls = classes[i]
					self = cls.copy_from(self)
					modified = self.evlove_methods_cycle(getattr(self, method), name, debug=debug)
				cycles.append(name)
				if modified: 
					blfank_cycle_count = 0
					valid_cycle_record.append(name)
				else:
					blank_cycle_count += 1
					if blank_cycle_count == size: break
			assert i <= 50
			
			if debug:
				print(f'valid-cycle: {valid_cycle_record}')
				print(f'cycles: {cycles}')
			self.check()
			return self
		def evlove_methods_cycle(self, method, name, *, debug=0):
			debug = de.debug and debug
			if debug:
				self.draw(title_a=f'start-{name}')
			fm = method(debug=debug)
			if debug:
				self.draw(title_a=f'end-{name}')
			return fm
	if "build":
		@classmethod
		def copy_from(cls, g):
			self = cls(Dnodes=g.Dnodes, nodes=g.nodes, edges=g.std_edges, skew=g._skew)
			return self
		@classmethod
		def from_subs(cls, subs):
			Dnodes = set()
			nodes = set()
			edges = set()
			for sub in subs:
				Dnodes |= sub.Dnodes
				nodes |= sub.nodes
				edges |= sub.edges
			return cls(Dnodes=Dnodes, nodes=nodes, edges=edges)
	if "public":
		#misc
		def draw(self, *gs, new=True, **ks):
			ks = self.prepare_draw(title=f'<{self.length()}>', new=new, **ks)
			ks = self._draw(**ks)
			ks = self.draw_after(**ks)
			assert empty(ks), ks
			if de.draw_to_show: myplt.show()
			return self
		def _draw(self, *, nodes=None, edges=None, draw_Snodes=True, hl=[], ll=[], new=True, full=False, 
			supress=False, **ks) -> None:
			#pre
			if de.flag_light and 0:
				if supress: 
					print(f'[unexpected] de.flag_light == True')
				else: raise Exception(f'{de.flag_light}')
			if full:
				new = False
				myplt.new_figure(cap=1)
				myplt.new()
			hl = set(hl) | de.hl
			ll = set(ll) | de.ll
			de.hl.clear()
			de.ll.clear()
			#
			if edges == None: edges = self.edges
			edges = [tuple(sorted(e)) for e in edges]
			assert nodes == None
			nodes = self.nodes
			#pre-hl
			hl_edges = set()
			hl_nodes = set()
			ll_edges = set()
			for item in hl:
				if isinstance(item[0], tuple):
					item = tuple(sorted(item))
					#assert item in edges, f'{item}'
					hl_edges.add(item)
				else:
					#assert item in nodes
					hl_nodes.add(item)
			for item in ll:
				# assert supress or item not in hl, f'{item}\n{ll}\n{hl}'
				if isinstance(item[0], tuple): 
					item = tuple(sorted(item))
					#assert item in edges, f'{item, edges}'
					ll_edges.add(item)
				else:
					#assert item in nodes
					ll_nodes.add(item)
			spec = set(hl_edges | hl_nodes | ll_edges)
			# nodes
			self._draw_nodes([n for n in self.Dnodes if n not in spec], look=default.Dnode, **ks)
			self._draw_nodes(hl_nodes, look=default.hl_Dnode, **ks)
			if draw_Snodes:
				Snodes = self.Snodes()
				self._draw_nodes([n for n in Snodes if n not in spec], look=default.Snode, **ks)
				self._draw_nodes(hl_nodes, look=default.hl_Snode, **ks)
			# edges
			self._draw_edges([e for e in edges if e not in spec], look=default.edge, **ks)
			self._draw_edges(hl_edges, look=default.hl_edge, **ks)
			self._draw_edges(ll_edges, look=default.ll_edge, **ks)
			return ks
		def check(self):
			"""
				没有冗余节点
				"""
			if de.check:
				for Dnode in self.Dnodes: 
					assert self.has_node(Dnode)
				# 树
				if not self.is_tree():
					subs = self.subs()
					output = f'check: not a tree, {len(subs)} subs'
					print(output)
					self.show()
					raise Exception(output)
				#
				for node in self.nodes:
					x, y = node
					# 无用节点
					if not self.is_used_node(node):
						print(f'{node} unused')
						self.show(hl=[node])
						raise Exception(f'{node} unused')
					# 节点每个方向不重叠
					dire_count = [0] * 4
					for n2 in self.adj[node]:
						x2, y2 = n2
						if x2 > x: dire_count[enum.right] += 1
						elif x2 < x: dire_count[enum.left] += 1
						if y2 > y: dire_count[enum.up] += 1
						elif y2 < y: dire_count[enum.down] += 1
					for i in range(4):
						count = dire_count[i]
						if not count <= 1:
							txt = f'node={node} {enum.toStr_dire[i]} count={count} adjs={list(self.adj[node])}'
							print(txt)
							self.show(title_a='check', full=True)
							raise Exception(txt)
					assert self.degree[node] <= 4, f'{node}'
				for edge in self.edges:
					n1, n2 = edge
					assert n1 != n2
		def skew(self, skew=None) -> 'skew|SG':
			if skew == None: return self._skew
			else:
				sx, sy = skew
				Dnodes = my.geo.points.skew(self.Dnodes, skew)
				nodes = my.geo.points.skew(self.nodes, skew)
				edges = my.geo.segs.skew(self.edges, skew)
				return SG(Dnodes=Dnodes, nodes=nodes, edges=edges)
		def skew_back(self) -> 'SG':
			sx, sy = self._skew
			skew = -sx, -sy
			return self.skew(skew)
		#generate
		gs = generate_short
		#evolve
		#process
		def gsr(Dnodes, **ks):
			self = SG.gs(Dnodes, **ks)
			self.evolve_replace(**ks)
			return self
		gm = mst
		def gmr(Dnodes, **ks):
			self = SG.gm(Dnodes, **ks)
			self.evolve_replace(**ks)
			return self
		def gb(Dnodes, **ks):
			self = GB.generate_best(Dnodes, **ks)
			self = self.skew_back()
			return self
		def gbr(Dnodes, **ks):
			gb = GB.generate_best(Dnodes, **ks)
			self = ReplacePlain.copy_from(gb)
			self.evolve_replace(**ks) 
			self = self.skew_back()
			return self
		def gbm(Dnodes, **ks):
			gb = GB.generate_best(Dnodes, **ks)
			self = EdgeMove.copy_from(gb)
			self.evolve_edgeMove(**ks)
			#self = SG.copy_from(gb)
			self = self.skew_back()
			return self
		def gbmr(Dnodes, **ks):
			self = GB.generate_best(Dnodes, **ks)
			# self = EdgeMove.copy_from(gb)
			self = self.evolve_methods(['evolve_edgeMove', 'evolve_replace', ], ['m', 'r',  ], classes=[EdgeMove, ReplacePlain], **ks)
			self = self.skew_back()
			return self
	
SG = SteinerGraph
class Square():
	def __init__(self, owner, nx, ny):
		self.Dnodes = set()
		self.Linfos = set()
		self.edges = set()
		self.owner = owner
		self.index = nx, ny
	def __str__(self):
		nx, ny = self.index
		unit = self.owner.unit
		r = f'{self.index} : {(nx*unit, ny*unit)} -> {( (nx+1)*unit, (ny+1)*unit)}'
		return r
	__repr__ = __str__
	
	# info
	def DLinfos(self):
		r = { (n, None) for n in self.Dnodes }
		r |= self.Linfos
		return r
	def isolated_Dnodes(self):
		return [ n for n in self.Dnodes if self.owner.degree(n) == 0 ]
	#
	def nonstd_pinfos_by_p(self, pinfo1, sub):
		"""
			包括边和孤立D点
			排除自己
			排除同树
			"""
		r = set()
		p1, e1 = pinfo1
		# edges
		for e2 in self.edges:
			if e2[0] in sub: continue
			p2 = pnode_by_pe(p1, e2)
			r.add((p2, e2))
		# isolated_Dnodes
		for n2 in self.isolated_Dnodes():
			if n2 in sub: continue
			r.add((n2, None))
		return r
class withGrid(SteinerGraph):
	"""grid
		结构
			grid_size, size_x, size_y
			grid: grids[nx][ny] -> square
			square: .Dnodes .Linfos .edges
				edges: 矩形边经过的单元 ###
				包含边界
			unit: 单元边长
			size_max
			_skew, skew_x, skew_y:
				new - old
			expand_cap: size_x + size_y - 1
		概念
			node_short:
				点到单元格边界的最短值
		todo
			无重复
		"""
	expandDiamond_ri_map = []
	expandDiamondSpan_ri_map = defaultdict(list) # _rel[span][i] -> expands
	expandDiamondSpan_ri_map[(1,1)] = expandDiamond_ri_map
	def __init__(self, *gs, **ks):
		super().__init__(*gs, **ks)
	if "overload":
		def define_Dnodes(self, Dnodes_):
			Dnodes = self.setup(Dnodes_)
			super().define_Dnodes(Dnodes)
			return Dnodes
		def signal_new_Lnode(self, n, e):
			squares = self.squares_by_n(n)
			for squ in squares:
				squ.Linfos.add((n, e))
			super().signal_new_Lnode(n, e)
		def signal_del_Lnode(self, n, e):
			squares = self.squares_by_n(n)
			for squ in squares:
				squ.Linfos.remove((n, e))
			super().signal_del_Lnode(n, e)
		def connect_sorted(self, n1, n2):
			e = n1, n2
			# edges
			squares = self.squares_by_nn(n1, n2)
			for squ in squares:
				# if squ.index == (0, 0) and not isinstance(squ.edges, my.Inspector):
				# 	squ.edges = my.Inspector(squ.edges, 'edges').inspect(
				# 		e=((7, 4), (10, 7)),
				# 		breakhere=1,
				# 	)
				squ.edges.add(e)
				
			super().connect_sorted(n1, n2)
		def disconnect_sorted(self, n1, n2, **ks):
			e = n1, n2
			squares = self.squares_by_nn(n1, n2)
			super().disconnect_sorted(n1, n2, **ks)
			for squ in squares:
				squ.edges.remove(e)
	if "info":
		# lib
		# basic
		def node_short(self, n):
			x, y = n
			unit = self.unit
			delta_x1 = x % unit
			delta_x2 = unit - delta_x1
			delta_y1 = y % unit
			delta_y2 = unit - delta_y1
			return min( delta_x1, delta_x2, delta_y1, delta_y2, )
		def edge_short(self, e):
			n1, n2 = e
			x1, y1 = n1
			x2, y2 = n2
			unit = self.unit
			#
			if x1 > x2: x1, x2 = x2, x1
			if y1 > y2: y1, y2 = y2, y1
			#
			dis1 = x1 % unit
			dis2 = ( -x2 ) % unit
			dis3 = y1 % unit
			dis4 = ( -y2 ) % unit
			return min( dis1, dis2, dis3, dis4 )
		def locate_edge(self, e) -> 'span refer': ###
			n1, n2 = e
			x1, y1 = n1
			x2, y2 = n2
			unit = self.unit
			size_x, size_y = self.grid_size
			#
			if x1 > x2: x1, x2 = x2, x1
			if y1 > y2: y1, y2 = y2, y1
			#
			nx_min = squareIndexVal_lower(x1, unit)
			nx_max = squareIndexVal_greater(x2, unit)
			ny_min = squareIndexVal_lower(y1, unit)
			ny_max = squareIndexVal_greater(y2, unit)
			#
			span_x = nx_max - nx_min + 1
			span_y = ny_max - ny_min + 1
			span = span_x, span_y
			refer = nx_min, ny_min
			return span, refer
		def grid_len_dim(self, dim):
			return self.unit * self.grid_size[dim]
		def grid_bound_dire(self, dire):
			if enum.dire[dire].is_pos:
				dim = enum.dire[dire].dim
				return self.unit * self.grid_size[dim]
			else:
				return 0
			
	if "squs":
		#
		def squares_cover_bound(self, bound):
			indexs = self.squareIndexs_cover_bound(bound)
			return { self.grid[x][y] for x,y in indexs }
		def squareIndexs_cover_bound(self, bound):
			xmin, xmax, ymin, ymax = bound
			unit = self.unit
			nx_floor = squareIndexVal_lowerbound(xmin, unit)
			nx_cap = squareIndexVal_greaterbound(xmax, unit)
			ny_floor = squareIndexVal_lowerbound(ymin, unit)
			ny_cap = squareIndexVal_greaterbound(ymax, unit)
			return { ( nx, ny ) for ny in range(ny_floor, ny_cap) for nx in range(nx_floor, nx_cap) }
		#
		def squareIndex_by_n(self, n):
			x, y = n
			unit = self.unit
			nx = x // unit
			ny = y // unit
			return nx, ny
			# nx
		#
		def squares_by_n(self, n):
			indexs = self.squareIndexs_by_n(n)
			r = [ self.grid[nx][ny] for nx, ny in indexs ]
			assert len(r) > 0
			return r
		def squareIndexs_by_n(self, n):
			size_x, size_y = self.grid_size
			unit = self.unit
			x, y = n
			# x
			nx_q = x // unit # 0 - size_x
			nx_r = x % unit
			if nx_r == 0:
				if nx_q == 0: nx_list = [ nx_q ]
				else: nx_list = [ nx_q - 1, nx_q]
			else:
				nx_list = [ nx_q ]
			# y
			ny_q = y // unit # 0 - size_y
			ny_r = y % unit
			if ny_r == 0:
				if ny_q == 0: ny_list = [ ny_q ]
				else: ny_list = [ ny_q - 1, ny_q]
			else:
				ny_list = [ ny_q ]
			# squares
			r = []
			for nx in nx_list:
				for ny in ny_list:
					r.append((nx, ny))
			return r
		#
		def squares_by_nn(self, n1, n2):
			indexs = self.square_indexs_by_nn(n1, n2)
			r = [ self.grid[nx][ny] for nx, ny in indexs ]
			return r
		def square_indexs_by_nn(self, n1, n2): ###
			size_x, size_y = self.grid_size
			unit = self.unit
			x1, y1 = n1
			x2, y2 = n2
			x_max = max(x1, x2)
			x_min = min(x1, x2)
			y_max = max(y1, y2)
			y_min = min(y1, y2)
			
			xspec = squareIndexVals_by_val(x1, unit)
			xspec |= squareIndexVals_by_val(x2, unit)
			yspec = squareIndexVals_by_val(y1, unit)
			yspec |= squareIndexVals_by_val(y2, unit)
			xspec = set(xspec)
			yspec = set(yspec)
			# 
			nx_max = squareIndexVal_greater(x_max, unit)
			ny_max = squareIndexVal_greater(y_max, unit)
			nx_min = squareIndexVal_lower(x_min, unit)
			ny_min = squareIndexVal_lower(y_min, unit)
			# squares
			# r = []
			# for nx in range(nx_min, nx_max+1):
			# 	for ny in range(ny_min, ny_max+1):
			# 		r.append(( nx, ny ))
			# return r
			r = set()
			for nx in xspec:
				for ny in range(ny_min, ny_max+1):
					r.add( (nx, ny) )
			for ny in yspec:
				for nx in range(nx_min, nx_max):
					r.add( (nx, ny) )
			return r
	if "expand":
		#expand single square
		def expandDiamond(self, nx, ny, i):
			size_x, size_y = self.grid_size
			rel_indexs = self.expandDiamond_ri(i)
			pre_indexs = [ (nx + dx ,ny + dy) for dx, dy in rel_indexs ]
			r = [ self.grid[nx_][ny_] for nx_, ny_ in pre_indexs if 0 <= nx_ < size_x and 0 <= ny_ < size_y ]
			return r
		def expandDiamond_ri(self, i):
			#
			"""
				i:
				"""
			if i < len(self.expandDiamond_ri_map):
				return self.expandDiamond_ri_map[i]
			else:
				assert len(self.expandDiamond_ri_map) == i
				r = get_expandDiamond_ri(i)
			
				self.expandDiamond_ri_map.append( r)
				return r
		#expand edge
		def expandDiamond_edge(self, e, i):
			size_x, size_y = self.grid_size
			span, refer = self.locate_edge(e)
			nx, ny = refer
			rel_indexs = self.expandDiamond_ri_edge(span, i)
			pre_indexs = [ (nx + dx ,ny + dy) for dx, dy in rel_indexs ]
			r = [ self.grid[nx_][ny_] for nx_, ny_ in pre_indexs if 0 <= nx_ < size_x and 0 <= ny_ < size_y ]
			return r
		def expandDiamond_ri_edge(self, span, i):
			lis = self.expandDiamondSpan_ri_map[span]
			if i < len(lis):
				return lis[i]
			else:
				assert i == len(lis)
				r = get_expandDiamondSpan_ri(span, i)
				lis.append(r)
				return r
		# expandDire
		def expandDire(self, nx, ny, dire, i):
			x, y = index = expandDire_index(nx, ny, dire, i)
			squ = self.grid[x][y]
			return squ
			
		def expandDire_limit(self, nx, ny, dire):
			sizex, sizey = self.grid_size
			if dire == enum.left:
				return nx
			elif dire == enum.right:
				return sizex - nx - 1
			elif dire == enum.down:
				return ny
			elif dire == enum.up:
				return sizey - ny - 1
			else: raise Exception(f'unexpected [{dire}], expecting[{enum.left} {enum.right} {enum.down} {enum.up}')
			
	# setup
	def setup(self, Dnodes_):
		
		"""
			定义偏差
			加入squares
			_skew:
				最小的点横纵坐标皆是1
				不会有点在边界上
				old + skew = new
			"""
		# pre
		min_x = min(node[0] for node in Dnodes_)
		min_y = min(node[1] for node in Dnodes_)
		skew_x = 1 - min_x
		skew_y = 1 - min_y
		self._skew = self.skew_x, self.skew_y = skew_x, skew_y
		# skew
		Dnodes = [ ( x + skew_x, y + skew_y ) for x, y in Dnodes_ ]
		# pre
		count = len(Dnodes)
		max_x = max(node[0] for node in Dnodes)
		max_y = max(node[1] for node in Dnodes)
		cap_x = max_x + 1
		cap_y = max_y + 1
		ceil_square_count = count // setting.floor_per_square 
		# get_size
		def fit_unit(unit):
			size_x = ceildiv_int(cap_x, unit)
			size_y = ceildiv_int(cap_y, unit)
			total = size_x * size_y
			return total <= ceil_square_count
		unit = my.bisect.find_min(list(range(1, max(cap_x, cap_y) + 1 ) ), fit_unit, value=True )
		if unit == None: unit = 1
		self.unit = unit
		self.size_x = size_x = ceildiv_int(max_x + 1, unit)
		self.size_y = size_y = ceildiv_int(max_y + 1, unit)
		self.grid_size = size_x, size_y
		self.size_max = max(size_x, size_y)
		if de.grid:
			print(f'grid-size = {size_x} {size_y}')
		# setup grid
		self.grid = [ [ Square(self, nx, ny) for ny in range(size_y) ] for nx in range(size_x) ]
		# expand_cap
		self.expand_cap = size_x + size_y - 1
		# put Dnodes into squares
		for n in Dnodes:
			squares = self.squares_by_n(n)
			for squ in squares:
				squ.Dnodes.add(n)
		return Dnodes
class GB(withGrid):
	"""
		cpfp: DL
			随时保持数据有效
			更新：增加边 删除边
		"""
	"""
		结构
			cpfp: dl_info: rv_info, dis
			rcpfp_e: 仅仅当v在边内时
			isolated_Dnodes:
			dis_map: { dis/unit: pinfo1s }
				该距离以内的
			nL_map: { n: Lnode }
				较小的n

		需求
			共子树判定：dl-dlsv
		伪码
			add_node(s)
			new_Lnode(v, e)
			connect(n1 n2) ##
			disconnect(e=n1 n2)
		性质
			r+v不会有重复 ？
		"""
	"""subs
			subs: rl: {rl_info..} #v通过e
		说明
			断连不会改变
			gb 创建新节点，gb.connect_pp 改变
			加入Lnode会导致增删Lnode麻烦
			加入Lnode是为了同树重连
		"""
	def __init__(self, *gs, **ks):
		super().__init__(*gs, **ks)
		self.subs = {}
		self.dis_map = defaultdict(set)
		self.nL_map = {}
	if "overload":
		def signal_new_Lnode(self, n, e):
			self.nL_map[e[0]].add((n, e))
			super().signal_new_Lnode(n, e)
		def signal_del_Lnode(self, n, e):
			self.nL_map[e[0]].remove((n, e))
			super().signal_del_Lnode(n, e)

	if "sub":
		def get_sub(self, pinfo):
			p, e = pinfo
			if e == None: return self.subs[p]
			else: return self.subs[e[0]]
		def pinfo_in_sub(self, pinfo, sub):
			#p: DS V(L)
			p, e = pinfo
			if e == None:
				return p in sub
			else:
				return e[0] in sub
	if "struct-oper":
		def cpfp_add(self, pinfo1, pinfo2, dis):
			"""
				新点
				"""
			p1, e1 = pinfo1 ###
			assert e1 == None or is_std(e1)
			p2, e2 = pinfo2
			assert pinfo1 not in self.cpfp
			self.cpfp[pinfo1] = pinfo2, dis
			if e2 != None:
				self.rcpfp_e[e2].add(pinfo1)
			# dis_map
			self.dis_map[ ceildiv_int(dis, self.unit) ].add( pinfo1 )
		def cpfp_change(self, pinfo1, pinfo2, dis):
			p1, e1 = pinfo1 ###
			p2, e2 = pinfo2
			# if p1 == (55, 46):
			# 	pass
			assert e1 == None or is_std(e1)
			pinfo2_, dis_ = self.cpfp[pinfo1]
			assert pinfo2 != pinfo2_, pinfo2
			#add
			self.cpfp[pinfo1] = pinfo2, dis
			if e2 != None:
				self.rcpfp_e[e2].add(pinfo1)
			# del
			p2_, e2_ = pinfo2_
			if e2_ != None:
				self.rcpfp_e[e2_].remove(pinfo1)
			# dis_map
			index = ceildiv_int(dis, self.unit)
			index_ = ceildiv_int(dis_, self.unit)
			if index != index_:
				self.dis_map[ index_ ].remove( pinfo1 )
				self.dis_map[ index ].add( pinfo1 )
		def cpfp_change_nonDelR(self, pinfo1, pinfo2, dis):
			p1, e1 = pinfo1 ###
			p2, e2 = pinfo2
			assert e1 == None or is_std(e1)
			pinfo2_, dis_ = self.cpfp[pinfo1]
			assert pinfo2 != pinfo2_, pinfo2
			#add
			self.cpfp[pinfo1] = pinfo2, dis
			if e2 != None:
				self.rcpfp_e[e2].add(pinfo1)
			# del
			# dis_map
			index = ceildiv_int(dis, self.unit)
			index_ = ceildiv_int(dis_, self.unit)
			if index != index_:
				self.dis_map[ index_ ].remove( pinfo1 )
				self.dis_map[ index ].add( pinfo1 )
		def cpfp_del(self, pinfo1):
			pinfo2, dis = self.cpfp.pop(pinfo1)
			p2, e2 = pinfo2
			if e2 != None:
				self.rcpfp_e[e2].remove(pinfo1)
			index = ceildiv_int(dis, self.unit)
			self.dis_map[ index ].remove( pinfo1 )
		def cpfp_add_auto(self, pinfo1):
			pinfo2, dis = self.find_closest_pinfodis(pinfo1)
			self.cpfp_add(pinfo1, pinfo2, dis)
		
		def cpfp_change_auto_nonDelR(self, pinfo1):
			pinfo2, dis = self.find_closest_pinfodis(pinfo1)
			self.cpfp_change_nonDelR(pinfo1, pinfo2, dis)
		def cpfp_change_auto(self, pinfo1):
			pinfo2, dis = self.find_closest_pinfodis(pinfo1)
			self.cpfp_change(pinfo1, pinfo2, dis)
		def settle_Dnode(self, n):
			self.isolated_Dnodes.remove(n)
			self.connected_Dnodes.add(n)
	if "info":
		def find_closest_pinfodis000(self, pinfo1):
			"""
				对所有非连通边和孤立点搜索
				pinfo1：DL
				"""
			
			p, e = pinfo1
			if p == (1 ,4) and e == None:
				pass
			sub = self.get_sub(pinfo1)
			min_dis = math.inf
			# isolated_Dnodes
			min_node = None
			for n in self.isolated_Dnodes:
				# n == p => e == None
				if n == p: continue
				dis = self.distance(p, n)
				if dis < min_dis:
					min_dis = dis
					min_node = n
			min_info = min_node, None
			# edges
			for e2 in self.std_edges:
				assert my.is_sorted(e2), f'{e2}'
				if e2[0] in sub: continue
				p2 = pnode_by_pe(p, e2)
				dis = self.distance(p, p2)
				if dis < min_dis:
					min_dis = dis
					min_info = p2, e2 # 可能为实点
			p9, e9 = min_info
			if e9 != None and self.has_node(p9):
				e9 = None
			assert p9 != p, f'{min_info, pinfo1}'
			assert e9 == None or my.is_sorted(e9), e9
			assert e == None or my.is_sorted(e), e
			return (p9, e9), min_dis
		def find_closest_pinfodis(self, pinfo1):
			"""
				pinfo1: dl
				pinfo2: p (考虑e和独立D）
				算法：
					菱形外展，每个菱形对应一个边界值和一个最小值
					若某个菱形最小值 <= 边界值：返回该最小点
				概念
					long, short: 单元格内距离
					unit <= long <= unit * 2
					0 <= short <= unit
					菱形i：
						最远距离: long + i * unit
						最近距离：short + i * unit
				定理：
					n外的值大于等于n边界值
					菱形 i+2 的最短距离 >= 菱形 i 的最长距离
						i.e. 若菱形i里有点， 一定在菱形i+2的内包中
				"""
			size_x, size_y = self.grid_size
			unit = self.unit
			p1, e1 = pinfo1
			nx, ny = self.squareIndexs_by_n(p1)[0]
			node_short = self.node_short(p1)
			#
			min_dis = math.inf
			# min_pinfo2 = None
			sub = self.get_sub(pinfo1)
			for i in range(size_x+size_y-1):
				expands = self.expandDiamond(nx, ny, i)
				bound = node_short + unit * i
				# get min
				for expand in expands:
					for p2, e2 in expand.nonstd_pinfos_by_p(pinfo1, sub):
						dis = distance(p1, p2)
						if dis < min_dis:
							min_dis = dis
							min_pinfo2 = p2, e2
				# 
				if min_dis <= bound:
					break
			min_pinfo2 = norm_pinfo(min_pinfo2)
			p2, e2 = min_pinfo2
			assert p2 != p1, p1
			return min_pinfo2, min_dis
		def expand_edge_limit(self):
			"""
				avg * count(i) * rate <= dis_map[i]
				avg * ( 4 * i ) * rate <= dis_map[i]
				"""
			keys = sorted(self.dis_map.keys())
			i_ = 0
			for i in keys: ###
				if setting.floor_per_square * 4 * i <= len(self.dis_map[i]):
					i_ = i
				else:
					return i_
			return keys[-1]
	if "generate":
		#generate-best
		@performance.gb
		def generate_best(Dnodes_, *, debug=0):
			debug = debug and de.gb
			axs = []
			self = GB()
			#
			Dnodes = self.define_Dnodes(Dnodes_)
			self.isolated_Dnodes = set(Dnodes)
			self.connected_Dnodes = set()

			# cpfp
			self.cpfp = {} # pinfo1:  pinfo2, distance
			self.rcpfp_e = {} # e: {pinfo1 ...}
			if debug and de.cpfp:
				self.cpfp = my.Inspector(self.cpfp, name='cpfp', pause=0)
			# Dnodes
			for n in sorted(Dnodes):
				self.add_node(n)
				self.subs[n] = {n}
				self.nL_map[n] = set()
				# cpfp
				n1 = min([n0 for n0 in Dnodes if n0 != n], key=lambda n_: self.distance(n_, n))
				dis = self.distance(n1, n)
				# self.cpfp[(n, None)] = (n1, None), dis
				self.cpfp_add((n, None), (n1, None), dis)
			#
			edge_size = len(Dnodes)-1
			if debug:
				self.draw(hl=[], title_a=' gb-start', direct=True)
			# main
			for i in range(edge_size):
				# beginProcess
				min_dis = math.inf
				min_item = None
				for item in self.cpfp.items():
					pinfo1, (pinfo2, dis) = item
					if dis < min_dis:
						min_dis = dis
						min_item = item
				
				pinfo1, (pinfo2, dis) = min_item
				#
				p1, e1 = pinfo1
				p2, e2 = pinfo2
				if debug:
					print(f'\n>> connect {pinfo1} {pinfo2}')
					de.light_on()
				final = i == edge_size - 1
				if ((65, 45), None) in (pinfo1, pinfo2):
					pass
				if ((55, 46), None) in (pinfo1, pinfo2):
					pass
				if ((52, 46), None) in (pinfo1, pinfo2):
					pass
				if (55, 39) in (p1, p2):
					pass
				if p1 == (55, 39) and p2 == (52, 46):
					... 
				if pinfo1 == ((14, 31), None):
					pass
				# if (pinfo1, pinfo2) == (, ((16, 35), None)):
				self.connect_pp_(pinfo1, pinfo2, debug=debug, final=final)
				if debug:
					de.light_off()
					self.draw(hl=[], title_a=' gb', direct=True)
					axs.append(myplt.ax())
			
			if debug:
				for ax in axs[:-1]:
					ax.axis(axs[-1].axis())
				self.draw(hl=[], title_a=' gb-end', direct=True)
			self.check()
			return self
		def connect_pp_(self, pinfo1_, pinfo2_, *, debug=0, final):
			"""
			connect_pp
				连通子树
				若其中的端点为孤立Dnode，刷新孤立状态
				#cpfp
					共树重连
						只考虑原有sub1
					连到删除边上的重连
					除了重连过的，其他子树上的的点根据新增边刷新
					增删L点刷新
				#misc
					新增边rcgfg
				"""
			# rv
			timer1.start()
			pnode1, edge1 = pinfo1_
			pnode2, edge2 = pinfo2_
			assert pnode1 != pnode2, f'{pinfo1_, pinfo2_}'
			unit = self.unit
			sub1 = self.get_sub(pinfo1_)
			sub2 = self.get_sub(pinfo2_)
			extra = set() # 新增的s点
			redirected = set() # pinfo
			edges_removed = []
			edges_new = [sorted_nn(pnode1, pnode2)]
			Linfos_removed = []
			Linfos_new = []
			# 分析增删信息
			for pinfo in (pinfo1_, pinfo2_):
				p, e = pinfo
				if e == None: pass
				else:
					n1, n2 = e
					edges_removed.append(e)
					assert p not in e
					edges_new.append(sorted_nn(p, n1))
					edges_new.append(sorted_nn(p, n2))
					extra.add(p)
					self.subs
					#Lnode
					Linfos_removed += self.Linfos_by_nn(n1, n2)
					Linfos_new += self.Linfos_by_nn(p, n1) + self.Linfos_by_nn(p, n2)
			Linfos_new += self.Linfos_by_nn(pnode1, pnode2)
			# rcpfp_e
			for edge in edges_new:
				self.rcpfp_e[edge] = set()
			# 连通子树
			assert sub1 is not sub2, sub1
			if len(sub1) > len(sub2): sub_min, sub = sub2, sub1
			else: sub_min, sub = sub1, sub2
			sub |= sub_min
			sub |= extra
			for n in sub_min: #r
				self.subs[n] = sub
			# extra
			for n in extra: #r
				self.subs[n] = sub
				self.nL_map[n] = set()
			sub = sub
			timer4.start()
			# main
			super().connect_pp(pinfo1_, pinfo2_)
			# 若其中的端点为孤立Dnode，刷新孤立状态
			if edge1 == None and pnode1 in self.isolated_Dnodes:
				self.settle_Dnode(pnode1)
			if edge2 == None and pnode2 in self.isolated_Dnodes:
				self.settle_Dnode(pnode2)
			# 删除Lnodes
			for Linfo in Linfos_removed:
				self.cpfp_del(Linfo)
			# 若是最后：返回
			if final: return
			# 连到删除边上的重连
			"""
				一定不需要连到新增的边
				"""
			for edge in edges_removed:
				pinfo1s = self.rcpfp_e[edge]
				for pinfo1 in pinfo1s:
					if debug and de.cpfp: print(f'remove edge')
					self.cpfp_change_auto_nonDelR(pinfo1)
					redirected.add(pinfo1)
				del self.rcpfp_e[edge]
			# 同树重连 ### n**2 不包含extra
			"""
				对原有两棵树的并进行重连
				"""
			timer4.stop()
			timer2.start()
			# p1, e1 = pinfo1
			# p2, e2 = pinfo2
			for n in sub: ### # 实节点
				for Linfo in self.nL_map[n]: # 虚节点
					if Linfo in redirected: continue
					if Linfo not in self.cpfp: continue # 新增虚节点
					pinfo2, dis = self.cpfp[ Linfo ]
					if self.pinfo_in_sub(pinfo2, sub): # 同树重连
						if debug and de.cpfp: print(f'share sub')
						self.cpfp_change_auto(Linfo)
					else: continue
				pinfo1 = (n, None)
				if pinfo1 in redirected: continue
				if pinfo1 not in self.cpfp: continue
				pinfo2, dis = self.cpfp[ pinfo1 ]
				if self.pinfo_in_sub(pinfo2, sub): # 同树重连
					if debug and de.cpfp: print(f'share sub')
					self.cpfp_change_auto(pinfo1)
				else: continue
			
			timer2.stop()
			timer3.start()
			#新边刷新周围 ###
			for edge in edges_new:
				# expand
				expand_limit = self.expand_edge_limit()
				short = self.edge_short(edge)
				assert short < unit
				for i in range(expand_limit+1):
					if i == 0: floor_dis = 0 # 这次i能提供的距离底线
					elif i == 1: floor_dis = short
					else: floor_dis = short + (i-1) * self.unit
					expands = self.expandDiamond_edge(edge, i)
					1
					for expand in expands:
						for Dnode in expand.Dnodes: # 重连D点
							if Dnode in sub: continue
							pinfo1 = (Dnode, None)
							pinfo2, dis2 = self.cpfp[pinfo1] # 当前
							if dis2 < floor_dis: continue
							pinfo3, dis3 = pinfodis_by_pe(Dnode, edge) # 连接到e以后
							if dis3 < dis2:
								if debug and de.cpfp: print(f'new edge1')
								self.cpfp_change(pinfo1, pinfo3, dis3)
						for Linfo in expand.Linfos: # 重连L点
							p, e = Linfo
							if e[0] in sub: continue
							pinfo2, dis2 = self.cpfp[Linfo]
							if dis2 < floor_dis: continue
							pinfo3, dis3 = pinfodis_by_pe(p, edge)
							if dis3 < dis2:
								if debug and de.cpfp: print(f'new edge2')
								self.cpfp_change(Linfo, pinfo3, dis3)
					# pick
					# expand_limit - 1 以内的已经测试完
					# 接下来测试 
					for j in list(self.dis_map): # j: (j-1, j]
						if j <= expand_limit - 1: continue
						pinfo1s = self.dis_map[j]
						for pinfo1 in list(pinfo1s):
							if self.pinfo_in_sub(pinfo1, sub): continue
							p1, e1 = pinfo1
							pinfo2, dis2 = self.cpfp[pinfo1]
							pinfo3, dis3 = pinfodis_by_pe(p1, edge)
							if dis3 < dis2:
								if debug and de.cpfp: print(f'new edge3')
								self.cpfp_change(pinfo1, pinfo3, dis3)

						# pedis_list = [ self.pedis_by_pe(p1, e) for e in edges_new ]
						# pedis_min = min(pedis_list, key=lambda pedis: pedis[2])
						# p3, e3, dis3 = pedis_min
						# if dis3 < dis2:
						# 	if debug and de.cpfp: print(f'new edge')
						# 	self.cpfp_change(pinfo1, (p3, e3), dis3)
			# 新增Lnode点
			timer3.stop()
			for pinfo in Linfos_new:
				if debug and de.cpfp: print(f'new Lnode')
				self.cpfp_add_auto(pinfo)
			timer1.stop()
	if "public":
		def draw(self, *gs, direct=False, **ks):
			ks = self.prepare_draw(**ks)
			if direct:
				directs = []
				for pinfo1, (pinfo2, dis) in self.cpfp.items():
					p1, e1 = pinfo1
					p2, e2 = pinfo2
					directs.append( (p1, p2) )
				self._draw_edges(directs, arrows=True, arrowstyle='->', alpha=0.2, color=default.color.arrow)
			ks = super().draw(*gs, new=False, **ks)
class EdgeMove(SteinerGraph):
	"""
		结构
			nnd: nnd[node][dire] -> node | None
			strict_nnd: nnd[node][dire] -> node | None
		说明
			clear 时自动同向边合并
		伪码
			add_node
				nnd, strict_nnd
			remove_node
				nnd, strict_nnd
			connect
				考虑合并
			
		"""
	def __init__(self, *gs, **ks):
		super().__init__(*gs, **ks)
	if "overload":
		# def disconnect(self, n1, n):
		# 	.
		# def clear_node(self, n):
		# 	res = super().clear_node(n)
		def add_node(self, n):
			super().add_node(n)
		def remove_node(self, n):
			super().remove_node(n)
		def connect(self, n1, n2):
			"""
				若是斜边：考虑合并
				"""
			assert n1 != n2, (n1, n2)
			e = (x1, y1), (x2, y2) = (n1, n2) = sorted((n1, n2))
			# 合并
			# d((n1, n2))
			for dim in enum.dims:
				# dire12 = self.dire_in_dim_nn(n1, n2)
				if n1[dim] == n2[dim]: continue
				dire12 = dire_nn_in_dim(n1, n2, dim)
				dire21 = enum.opposite_dire[dire12]
				for n5, n6, dire in (n1, n2, dire12), (n2, n1, dire21):
					n7 = self.nnd[n5][dire]
					if n7 != None:
						self.connect_ne(n6, (n5, n7))
						self.clear_node(n5)
						return
			#
			super().connect(n1, n2)
		def disconnect(self, n1, n2, *, clear=False):
			e = (x1, y1), (x2, y2) = (n1, n2) = sorted((n1, n2))

			super().disconnect(n1, n2, clear=clear)
		...
	if "oper":
		...
			
	#evlove
	def evolve_edgeMove(self, *, debug=0): # 一轮长度轮空则退出
		debug = debug and de.evolve_edgeMove
		cycle_count = 0
		last_len = self.length()
		len_modified = False
		fm = False
		if debug:
			self.draw(title_a=f'start-m')
		while 1:
			flag_modified = self.evolve_edgeMove_cycle(debug=debug)
			le = self.length()
			if flag_modified: pass
			else: break
			if le < last_len:
				last_len = le
				fm = True
			else: break
			cycle_count += 1
		if debug and de.count_cycle: 
			print(f'cycle: {cycle_count}')
		self.check()
		if debug:
			self.draw(title_a=f'end-m')
		return fm
	def evolve_edgeMove_cycle(self, *, debug): ###
		debug = debug and de.evolve_edgeMove
		flag_modified = False
		for e in my.iter_dynamic(self.std_edges, cond='exist', mode='turn'):
			if debug: de.light_on()
			fm, dire = self.evolve_edgeMove_edge(e)
			if debug: de.light_off()
			if fm:
				flag_modified = True
				if debug:
					print(f'move-edge {e} {enum.toStr_dire[dire]}')
					self.draw(hl=[], ll=[], title_a=' m')
		return flag_modified
	def evolve_edgeMove_edge(self, e):
		"""
			"""
		dire, pinfo1, pinfo2 = self.judge_edgeMove(e)
		if dire == None:
			return False, None
		else:
			# self.move_edge(e, dire)
			self.connect_pp(pinfo1, pinfo2)
			self.disconnect(*e, clear=True)
			return True, dire
	def judge_edgeMove(self, e) -> 'dire, pinfo1, pinfo2':
		"""
			要求
				要求不能下翻
				允许上方外翻
			总value == 0 且 一边是spec
			<=> 两边上方都有边且 一边spec
			spec：非D且外向有边

			code:
				判断直边
				判断value
				对两个方向：
					获取1， 2信息：
						na, nb, nc=None: 最后直边和最后斜边
						nm: 最高点
						主动移动
						斜2：满足斜spec 中途没点 nc存在 且 nb<=另一边nm
						直1：满足直spec
						非0：

					斜+斜：返回 较大斜nb
					斜+直非：返回斜nb
					直+直非：
						vm1 <= nb2: 返回nc1 #?
						: 返回较大nb
						返回 pb较短直
					非+非：无
					
				一边满足spec
				对两个方向尝试
			定义
				_type: 210 准类型
				type: 比较后的
				vc: 斜边的值 （一般更大）
				vm：最大值
			"""
		n1, n2 = e
		if n1 == (0, 0) and n2 == (3, 0):
			...
		if not self.is_sedge(e): return None, None, None
		dimh = self.dim_sedge(e)
		dimv = 1 - dimh
		dire12 = dire_nn(n1, n2)
		dire21 = 1 - dire12
		for dire in enum.dim_to_dires[dimv]:
			keyc = enum.keyv_dire[dire]
			key = enum.key_dire[dire]
			#
			if (not self.nnd[n1][dire] ) or ( not self.nnd[n2][dire] ): 
				continue
			vb1, vc1, vm1, _type1 = self.analyze_edgeMove_node(n1, dire, dire21)
			vb2, vc2, vm2, _type2 = self.analyze_edgeMove_node(n2, dire, dire12)
			if _type1 == _type2 == 0: 
				continue
			if _type1 == 2 and keyc(vb1) > keyc(vm2): type1 = 1
			else: type1 = _type1
			if _type2 == 2 and keyc(vb2) > keyc(vm1): type2 = 1
			else: type2 = _type2
			# 按照type，vb排序
			if type1 < type2 or ( type1 == type2 and keyc(vb1) < keyc(vb2) ): 
				vb3, vc3, vm3, type3, n3 = vb2, vc2, vm2, type2, n2
				vb4, vc4, vm4, type4, n4 = vb1, vc1, vm1, type1, n1
			else:
				vb3, vc3, vm3, type3, n3 = vb1, vc1, vm1, type1, n2
				vb4, vc4, vm4, type4, n4 = vb2, vc2, vm2, type2, n1
			#
			if type3 == 2:
				endv = vb3
			elif type3 == 1:
				if keyc(vm3) <= keyc(vb4): endv = vm3
				elif keyc(vm4) <= keyc(vb3): endv = vm4
				else: endv = vb3
			else: raise Exception(f'{type1}')
			assert keyc(endv) <= keyc(vm3)
			assert keyc(endv) <= keyc(vm4)
			assert keyc(endv) > key(n1)
			# endv -> target
			pinfo3 = self.endv_to_target(n3, dire, endv)
			pinfo4 = self.endv_to_target(n4, dire, endv)
			return dire, pinfo3, pinfo4
		return None, None, None
	def analyze_edgeMove_node(self, n, dire, dire_out):
		"""
			输入：向上大致有边
			伪码
				Dnode/向上斜边: type0
				: 
					斜边满足要求：
						spec2：type2
						: type0
					:
						spec1: type1
						: type0
			"""
		nodes = self.walk_dire(n, dire)
		nb = nodes[-1]
		nc = self.nnd[nb][dire] #使用dire，包含内翻
		dim = enum.dire_to_dim[dire]
		keyc = enum.keyv_dire[dire]
		#
		# va = na[dim]
		vb = nb[dim]
		if nc == None: vc = None
		else: vc = nc[dim]
		#
		if vc == None: vm = vb
		else: 
			vm = vc
		assert keyc(vm) >= keyc(vb)
		if self.isDnode(n) or not self.strict_nnd[n][dire]: _type = 0
		else:
			if len(nodes) == 2 and vm != None:
				nc = self.nnd[n][dire_out]
				if nc != None:
					_type = 2
				else: _type = 0
			else:
				if self.strict_nnd[n][dire_out] != None: _type = 1
				else: _type = 0
		
		return vb, vc, vm, _type

	def endv_to_target(self, n, dire, endv) -> 'pinfo':
		"""
			找到第一个>=endv的
			"""
		nodes = self.walk_dire(n, dire)
		dim = enum.dire_to_dim[dire]
		dimh = 1 - dim
		keyc = enum.keyv_dire[dire]
		for i in range(len(nodes)):
			node = nodes[i]
			if node[dim] == endv:
				return node, None
			elif keyc(node[dim]) > keyc(endv):
				end_n = self.node_from_dims(dimh, n[dimh], endv)
				return end_n, (nodes[i-1], node)
			else: continue
		node_ = self.nnd[node][dire]
		assert keyc(node_[dim]) >= keyc(endv)
		end_n = self.node_from_dims(dimh, n[dimh], endv)
		return end_n, (node, node_)
	def walk_dire(self, n, dire):
		"""
			包含n
			严格
			"""
		w = n
		r = [w]
		while 1:
			w = self.strict_nnd[w][dire]
			if w == None: break
			r.append(w)
		return r
	if "unused":
		def move_edge(self, e, dire):
			"""
				较短边中点
					一直走直边，到斜边终点时停止
						？内斜
				可能会出现重叠
				"""
			#
			n1, n2 = e
			end_node1 = self.move_edge_end_node(n1, dire)
			end_node2 = self.move_edge_end_node(n2, dire)
			dimv = enum.dire_to_dim[dire]
			dimh = 1 - dimv
			key = enum.key_dire[dire]
			if key(end_node1) < key(end_node2):
				node_short = n1
				node_long = n2
				end_node = end_node1
			else:
				node_short = n2
				node_long = n1
				end_node = end_node2
			endv = end_node[dimv]
			n3, n4 = self.node_from_dims(dimh, node_short[dimh], endv), self.node_from_dims(dimh, node_long[dimh], endv) # 上方点
			#实化长边上的点
			walker = node_long
			key_endv = key(end_node)
			while 1:
				walker_ = walker
				walker = self.nnd[walker][dire]
				if key(walker) == key_endv:
					break
				elif key(walker) > key_endv:
					e4 = walker_, walker
					self.set_p((n4, e4))
					break
				else: continue
			#实化短边上的点
			if self.has_node(n3): pass
			else:
				end_node_below = self.nnd[end_node][enum.opposite_dire[dire]]
				self.set_v((n3, sorted_nn(end_node_below, end_node)))
			self.disconnect(n1, n2, clear=True)
			self.connect(n3, n4)
		def move_edge_end_node(self, n, dire):
			walker = n
			while 1:
				next = self.strict_nnd[walker][dire]
				if next == None:
					break
				else:
					walker = next
			next = self.nnd[walker][dire]
			if next != None:
				walker = next
			assert walker != n, n
			return walker
# r
class FieldPlain:
	"""
		结构
			pinfo2s
			short
			quas: [ pinfos ]
				不包含（轴上的点）极点
			bounds:
				0: 邻边
			imax 最大屏蔽单维距离 // unit
			blockDistances

		性质
			屏蔽区域是实的（除了邻边的情况）
			邻边能直接屏蔽所在方向两边的两个象限
		"""	
	def __init__(self, pinfo1, *, owner:'graph'):
		self.pinfo1 = pinfo1
		node1, edge1 = pinfo1
		nodex, nodey = node1
		#
		self.owner = owner
		self.short = self.owner.node_short(node1)
		

	def cacu(self):
		"""
			说明
				除了边界以外不会出现横跨两个象限的边
			算法
				四向边界，加入四个极点
				穷举矩形边界内的点
			具体算法
				考虑邻边
				对四个方向
					对每一个单元
						找到所有阻挡边中最近的
						若没有，到下一个单元
				计算实矩形区域内所有边对应的p点
				将p点分到四象限 （由于极点的存在，不会有在轴上的点）
				对每个象限：
					建立保留点集合
					对集合中的每个点：
						若保留点中存在比这个点更小的，删除该点
			"""
		# pre
		graph = self.owner
		pinfo1 = self.pinfo1
		node1, edge1 = pinfo1
		nodex, nodey = node1
		caculated_edges = set()
		pinfos2 = set() # std
		# if 1: pinfos2 = my.Inspector(pinfos2, 'pinfos2')
		size_x, size_y = graph.grid_size
		unit = graph.unit
		nx, ny = graph.squareIndex_by_n(node1)
		if edge1 == None: 
			flags_adj = [ bool(graph.nnd[node1][dire]) for dire in enum.dires ]
			for n in graph.adj[node1]:
				caculated_edges.add( sorted_nn(node1, n) )
		else:
			Ldires = Linfo_dires(pinfo1)
			flags_adj = [ ( dire in Ldires ) for dire in enum.dires ]
			caculated_edges.add(edge1)
		block_pinfos = [None] * 4 # None: 边界 邻边
		bounds = [None] * 4 # 不为None
		flags_inf = [ False ] * 4
		quas = [ set() for i in range(4) ]
		# 四向极点
		for dire in enum.dires:
			_dire = enum.dire[dire]
			dim = _dire.dim
			if flags_adj[dire]: # 邻边
				bounds[dire] = node1[dim]
				continue
			key = _dire.key
			k_node1 = key(node1)
			i_limit = graph.expandDire_limit(nx, ny, dire)
			for i in range(i_limit+1):
				expand = graph.expandDire(nx, ny, dire, i)
				# block_pinfo = /
				k_min = math.inf
				for e in expand.edges: # 每个边
					1
					if is_edge_block_node_dim(e, node1, dim):
						pinfo2 = p2, e2 = pinfo_by_pe(node1, e)
						k_p2 = key(p2)
						if k_p2 <= k_node1: continue # 阻拦边在另一个方向 或 自己
						caculated_edges.add(e) # 排除阻拦边
						if k_p2 < k_min:
							k_min = k_p2
							min_pinfo2 = pinfo2
				if k_min is not math.inf: # 找到阻拦边
					p2, e2 = min_pinfo2
					block_pinfos[dire] = min_pinfo2
					bounds[dire] = p2[dim]
					break
			else: # 没找到阻拦边
				assert block_pinfos[dire] == None # mw
				flags_inf[dire] = True
				bounds[dire] = graph.grid_bound_dire(dire)
		# pre
		ebounds = [] # 实用边界（对象限中）
		#. inf -> 扩大
		for dire in range(4):
			if flags_inf[dire]:
				b = enum.dire[dire].keyv(1) + bounds[dire]
			else:
				b = bounds[dire]
			ebounds.append(b)
		# 遍历pinfo2，放到对应象限
		squs = graph.squares_cover_bound(bounds)
		for squ in squs:
			for e in squ.edges:
				###
				if e in caculated_edges: continue # 排除自己所在边, 极点边
				p2, e2 = pinfo2 = pinfo_by_pe(node1, e)

				typ, res = quartrantAxisOri_by_nn(node1, p2)
				if typ == 0: # qua
					x2, y2 = p2
					# 排除超出范围的
					blocked = x2 <= ebounds[0] or x2 >= ebounds[1] or y2 <= ebounds[2] or y2 >= ebounds[3]
					if blocked: continue
					quas[res].add(pinfo2)
				elif typ == 1: # axis
					pass
				else: raise Exception(f'{typ}')
				
		1
		# 每个象限过滤
		for qi in enum.quas:
			qua = quas[qi]
			dires = enum.qua[qi].dires
			for pinfo2 in list(qua):
				n2, e2 = pinfo2
				for pinfo3 in qua:
					n3, e3 = pinfo3
					if n2 == n3: continue
					if is_plain_block_nnn(node1, n3, n2):
						qua.remove(pinfo2)
						break
		#
		self.quas = quas
		self.block_pinfos = block_pinfos
		self.bounds = bounds
		self.blockDistances = [ abs( bounds[dire] - node1[enum.dire[dire].dim] ) for dire in enum.dires ]
		self.pinfo2s = my.set.unionm(quas) | {pi for pi in block_pinfos if pi != None}
		self.block_max = max(self.blockDistances)
		self.imax = self.block_max // self.owner.unit
		return self
class Bfield:
	"""
		attr
			pinfo1: dl
			owner
			quarters: 绝对距离
			short
		说明：
			出生完全屏蔽：四面有线
			完全屏蔽：最大角距离小于等于已探测距离(距离点node）
			用每个四分之一角的距离指代
		"""
	def __init__(self, pinfo1, *, owner:'graph'):
		...
		self.pinfo1 = pinfo1
		node1, edge1 = pinfo1
		nodex, nodey = node1
		#
		self.owner = owner
		self.short = grid_get_short(node1, self.owner.unit)
		# adj_edges
		if edge1 == None:
			if self.nnd[node1][enum.up]: blocks[enum.up] = nodey
			if self.nnd[node1][enum.down]: blocks[enum.down] = nodey
			if self.nnd[node1][enum.left]: blocks[enum.left] = nodex
			if self.nnd[node1][enum.right]: blocks[enum.right] = nodex
		else:
			assert node1 not in edge1
			for x, y in edge1:
				if nodex > x: blocks[enum.left] = nodex
				elif nodex < x: blocks[enum.right] = nodex
				if nodey > y: blocks[enum.down] = nodey
				elif nodey < y: blocks[enum.up] = nodey
	# judge
	def born_blocked(self):
		# 在0探测区域时完全屏蔽外界
		return ( blocks[0] == blocks[1] ) and ( blocks[2] == blocks[3] )		
	def is_blocked_node(self, n, blocks):
		# dis > quarters[dire]
		dire = quarter_dire_nn(self.node1, n)
		dis = distance(self.node1, n)
		return dis > self.quarters[dire]
	def is_complete(self, i):
		"""
			计算
				最大角距离小于等于已探测距离(距离点node）
			i是距离扩展参数
			"""
		short = grid_
		return self.quarter_max() <= expand_distance_by_i(i, self.short)
	
	# info
	def quarter_max(self):
		return max(self.quarters)
		return self._quarter_max
	def imax(self):
		return self.quarter_max() // self.owner.unit
class Rpair(withGrid):
	def __init__(self, *gs, **ks):
		# pre
		self.rpairs = set()
		self.bfmap = {}
		if de.rpairs and 1:
			self.rpairs = my.Inspector(self.rpairs, name='rpairs', conditional=1).inspect(
				# expre=lambda ele: ((16,12) in (ele[0][0], ele[1][0] ) ),
				e = (((7, 15), ((4, 15), (7, 16))), ((16, 12), None)),
				breakhere=True,
				
			)
		if de.rpairMap and 0:
			self.rpairMap = my.Inspector(self.rpairMap, name='rpairMap',).inspect( 
				k=((2, 12), None), 
				exprv=lambda v: ((9, 7), ((9, 6), (11, 7))) in v,
				breakhere=True,
			).inspect(
				k=((9, 7), ((9, 6), (11, 7))),
				exprv =lambda v: ((2, 12), None) in v,
			)
		#
		super().__init__(*gs, **ks)
		# setup Dnodes.rpairs
		for pinfo1 in self.DLinfos():
			self.rpairs_new(pinfo1)
		assert self.rpairs_check()
		# setup
		self._expand_limit = self.get_expand_limit()
		self.connect_sorted = self._connect_sorted
		self.disconnect_sorted = self._disconnect_sorted
		self.signal_new_Lnode = self._signal_new_Lnode
		self.signal_del_Lnode = self._signal_del_Lnode
	def _draw(self, *gs, rpairs=True, **ks):
		# ks = self.prepare_draw(**ks)
		if rpairs:
			rpairs = []
			for pinfo1, pinfo2 in self.rpairs:
				p1, e1 = pinfo1
				p2, e2 = pinfo2
				rpairs.append( (p1, p2) )
			self._draw_edges(rpairs, 
				# arrows=True, arrowstyle='-', 
				alpha=0.2, color=default.color.arrow)
		ks = super()._draw(*gs, new=False, **ks)
		return ks
	# oper
	def rpairs_new(self, pinfo1):
		bf = self.analyze_rpairs(pinfo1)
		assert pinfo1 not in self.bfmap
		self.bfmap[pinfo1] = bf
		# rpairs
		for pinfo2 in bf.pinfo2s:
			self.rpairs.add( sorted_nn(pinfo1, pinfo2))
		# block_max
		self.blockDisMap[bf.imax].add(pinfo1)
	def rpairs_change(self, pinfo1):
		bf = self.analyze_rpairs(pinfo1)
		bf_ = self.bfmap[pinfo1]
		self.bfmap[pinfo1] = bf
		# rpairs
		for pinfo2_ in bf_.pinfo2s:
			if pinfo2_ not in self.bfmap or pinfo1 not in self.bfmap[pinfo2_].pinfo2s: ###
				self.rpairs.remove( sorted_nn(pinfo1, pinfo2_) )
		for pinfo2 in bf.pinfo2s:
			self.rpairs.add( sorted_nn(pinfo1, pinfo2))
		# block_max
		my.dict_set.remove_clear_empty(self.blockDisMap, bf_.imax, pinfo1)
		self.blockDisMap[bf.imax].add(pinfo1)
	def rpairs_del(self, pinfo1): # Lnode
		bf_ = self.bfmap.pop(pinfo1)
		# rpairs
		for pinfo2_ in bf_.pinfo2s:
			if pinfo2_ not in self.bfmap or pinfo1 not in self.bfmap[pinfo2_].pinfo2s: ###
				self.rpairs.remove( sorted_nn(pinfo1, pinfo2_) )
		# block_max
		my.dict_set.remove_clear_empty(self.blockDisMap, bf_.imax, pinfo1)
	def rpairs_sweep00(self):
		"""
			说明
				从左往右扫
			"""
		self.rpairs.clear()
		self.rpairMap.clear()
	# tool
	def expand_limit(self):
		return self._expand_limit
	def get_expand_limit(self):
		"""
			需要继续扩展
			avg * count(i) * rate <= blockDisMap[i]
			avg * ( 4 * i ) * rate <= blockDisMap[i]
			"""
		keys = sorted(self.blockDisMap.keys())
		i_ = 0
		for i in keys: ###
			if setting.floor_per_square * 4 * i <= len(self.blockDisMap[i]):
				i_ = i
			else:
				return i_
		return keys[-1]
	# misc
	def rpairs_check(self):
		if not de.rpairs_check: return
			
		# 对称
		for pair in self.rpairs:
			pinfo1, pinfo2 = pair
			assert my.is_sorted(pair)
			p1, e1 = pinfo1
			p2, e2 = pinfo2
			if self.is_Dinfo(pinfo1) or is_Linfo(pinfo1): # 1是主动
				assert pinfo2 in self.bfmap[pinfo1].pinfo2s, pinfo2
			if self.is_Dinfo(pinfo2) or is_Linfo(pinfo2): # 2是主动
				assert pinfo1 in self.bfmap[pinfo2].pinfo2s
		return True
	# unused
	def squares_expand_plain_block(self, x0, y0, i, blocks):
		indexs = self.squareIndexs_expand_plain_block(x0, y0, i, blocks)
		return [ self.grid[x][y] for x, y in indexs ]
	def squareIndexs_expand_plain_block(self, x0, y0, i, blocks):
		rindexs = self.squareRelIndexs_expand_plain_map[i]
		unit = self.unit
		r = []
		# block的子范围（更大）
		x_floor = squareIndexVal_lowerbound(blocks[0], unit) - 1 #向左遇到的第一条边界左边的格子
		x_ceil = squareIndexVal_greaterbound(blocks[1], unit)
		y_floor = squareIndexVal_lowerbound(blocks[2], unit) - 1
		y_ceil = squareIndexVal_greaterbound(blocks[3], unit)
		#
		for dx, dy in rindexs:
			x = x0 + dx
			y = y0 + dy
			if x_floor < x < x_ceil and y_floor < y < y_ceil:
				r.append( (x, y) )
		return r
	def update_blocks_by_pe(self, n, p, e, blocks):
		"""
			算法：
				依次计算p n1 n2
			"""
		# p
		x, y = n
		wait = list(e)
		if p not in e: wait.append(p)
		for n2 in wait:
			dire = quarter_dire_nn(self.node1, n)
			return (n, n2)
			dim = enum.dire_to_dim[dire]
			dis = distance(n, n2)
			# key = enum.key_dire[dire]
			keyv = enum.keyv_dire[dire]
			delta = keyv(dis)
			block = n[dim] + delta
			if keyv(blocks[dire]) > keyv(block):
				blocks[dire] = block
		#

class RpairPlain(Rpair):
	"""
		算法
			复杂度：n2
			找到所有可视<p, p>对
			对每一对计算环路增益
		说明：
			不自动合并
			修改时p-p自动更新
		结构
			rpairs：{ sorted(pinfo1, pinfo2) }
			rpairMap: { pinfo1: pinfo2s }
			blockDisMap: { j: pinfo1s }
				j-pinfo1: pinfo1.block_max >= j * unit
			bfmap
			_expand_limit: 反向查询时的极限
		更新
			rpairs
				new_node
					向外扩展，直到屏蔽范围够大
				connect

				增加边和删除边时
		"""
	def __init__(self, *gs, **ks):
		super().__init__(*gs, **ks)
	if "overload":
		...
		# def defineDnodes(self, Dnodes):
		def _signal_new_Lnode(self, v, e):
			super().signal_new_Lnode(v, e)
			self.rpairs_new((v, e))
		def _signal_del_Lnode(self, v, e):
			super().signal_del_Lnode(v, e)
			self.rpairs_del((v, e))
		def _connect_sorted(self, n1, n2):
			super().connect_sorted(n1, n2)
			self.rpairs_update_connect_sorted(n1, n2)
		def _disconnect_sorted(self, n1, n2):
			super().disconnect_sorted(n1, n2)
			self.rpairs_update_disconnect_sorted(n1, n2)
		def rpairs_update_connect_sorted(self, n1, n2):
			"""
				说明
					1: 缩小屏蔽区
					2：增加可视点
					必要条件：单维距离最小值（严格）小于屏蔽距离最大值
				算法
					扩展，每次扩展可以排除一定屏蔽距离内（包含）的点并更新，当剩下的点数足够少时穷举
				"""
			
			e = n1, n2
			expand_limit = self.expand_limit()
			span, refer = self.locate_edge(e)
			# expand ( 0, expand_limit + 0.x]
			for i in range(expand_limit+1):
				expands = self.expandDiamond_edge(e, i)
				for expand in expands:
					for DLinfo in expand.DLinfos():
						self.rpairs_change(DLinfo)
			# enum ( j, oo)
			for j, pinfo1s in list(self.blockDisMap.items()):# [j, j+1)
				
				if j < expand_limit: continue # j >= expand_limit
				for pinfo1 in list(pinfo1s):
					self.rpairs_change(pinfo1)
		def rpairs_update_disconnect_sorted(self, n1, n2):
			"""
				说明
					扩大屏蔽范围，屏蔽范围变需要刷新节点
					刚好位于边缘时需要删除节点到该边的连线
					同时更新屏蔽和连接
				算法
					扩展，每次扩展可以排除一定屏蔽距离内(包含）的点，当剩下的点数足够少时穷举
				"""
			e = n1, n2
			expand_limit = self.expand_limit()
			span, refer = self.locate_edge(e)
			# expand ( 0, expand_limit + 0.x]
			for i in range(expand_limit+1):
				expands = self.expandDiamond_edge(e, i)
				for expand in expands:
					for DLinfo in expand.DLinfos():
						self.rpairs_change(DLinfo)
			# enum ( j, oo) 
			for j, pinfo1s in list(self.blockDisMap.items()): # [j, j+1)
				if j < expand_limit: continue # j >= expand_limit
				for pinfo1 in list(pinfo1s):
					self.rpairs_change(pinfo1)
		# info
	def analyze_rpairs(self, pinfo1:'dl') -> 'bf':
		"""
			说明
				考虑dl-e
				方形屏蔽
					一条边可能屏蔽1-3个面
					被视觉挡住的边会自动计算进去
					整条边被屏蔽 <=> 最近点被屏蔽
					被屏蔽的边没必要用来计算屏蔽
				第一步屏蔽屏蔽区块和未来的加入点
				扩展方式：正方形
				？使用次数少，应该用更复杂的算法，可以得到更精简的集合
			算法
				邻接边屏蔽所在方向
				（简化）非邻接每条边每个四分角上找到最近点，根据距离计算屏蔽
				计算完成后根据细节屏蔽清理加入点
			结构
				caculated: 计算过的边
				pinfos2：加入点
				
			伪码
				计算邻接边(Linfo所在边）
				扩展区块：
					在每个区块中计算边和屏蔽
				直到：所有未扩展区块都被屏蔽
			"""
		
		bf = FieldPlain(pinfo1, owner=self)
		bf.cacu()
		return bf
		# pre
		node1, edge1 = pinfo1
		nodex, nodey = node1
		caculated = set()
		pinfos2 = set() # std
		# if 1: pinfos2 = my.Inspector(pinfos2, 'pinfos2')
		size_x, size_y = self.grid_size
		unit = self.unit
		#
		blocks = [0, size_x*unit, 0, size_y*unit] # 四个方向屏蔽绝对值
		if 0 and node1 == (9, 7):
			blocks = my.Inspector(blocks, name='blocks', print_self=True)
		# 计算特殊两边界完全屏蔽 ( 四面　）
		blocked = bf.born_blocked()
		# main
		if not blocked:
			# 删除邻边, 所在边
			if edge1 == None: 
				for n in self.adj[node1]: caculated.add(sorted_nn(node1, n))
			else:
				caculated.add(edge1)
			# expand
			nx, ny = self.squareIndex_by_n(node1)
			bounds = [nodex, nodex, nodey, nodey] # i = -1
			for i in range(self.expand_cap):
				# 计算边界
				bounds = [ (nx - i) * unit, (nx + i + 1) * unit, (ny - i) * unit, (ny + i + 1) * unit ]
				# expand
				expands = self.expandDiamond_block(nx, ny, i, blocks)
				for expand in expands: # 单个区块
					for edge2 in expand.edges: # 一条边
						if edge2 in caculated: continue
						caculated.add(edge2) #包括屏蔽边
						#
						pinfo2 = p2, e2 = pinfo_by_pe(node1, edge2)
						if bf.is_edge_blocked(edge2): continue
						bf.update_by_e(edge2)
						pinfos2.add(pinfo2)
				# 计算是否完全屏蔽
				blocked = bf.is_complete(i)
				# blocked = (bounds[0] <= blocks[0]) and (bounds[1] >= blocks[1]) and (bounds[2] <= blocks[2]) and (bounds[3] >= blocks[3])
				if blocked: break
		# clear
		for pinfo2 in list(pinfos2):
			p2, e2 = pinfo2
			if self.is_blocked_node(p2, blocks):
				pinfos2.remove(pinfo2)
		# block_max
		# block_dis_list = [ nodex - blocks[0], blocks[1] - nodex, nodey - blocks[2], blocks[3] - nodey ]
		# assert all( dis >= 0 for dis in block_dis_list ), block_dis_list
		# block_max = max(block_dis_list)
		return pinfos2, blocks, bf

class RpairConcrete(Rpair):
	def __init__(self, *gs, **ks):
		super().__init__(*gs, **ks)
	# info
	def analyze_rpairs(self, pinfo1:'dl'):
		"""
			说明
				考虑dl-e
				方形屏蔽
					一条边可能屏蔽1-3个面
					被视觉挡住的边会自动计算进去
					整条边被屏蔽 <=> 最近点被屏蔽
					被屏蔽的边没必要用来计算屏蔽
				第一步屏蔽屏蔽区块和未来的加入点
				扩展方式：正方形
				？使用次数少，应该用更复杂的算法，可以得到更精简的集合
			算法
				邻接边屏蔽所在方向
				（简化）非邻接每条边每个四分角上找到最近点，根据距离计算屏蔽
				计算完成后根据细节屏蔽清理加入点
			结构
				caculated: 计算过的边
				pinfos2：加入点
				
			伪码
				计算邻接边(Linfo所在边）
				扩展区块：
					在每个区块中计算边和屏蔽
				直到：所有未扩展区块都被屏蔽
			"""
		# pre
		node1, edge1 = pinfo1
		nodex, nodey = node1
		caculated = set()
		pinfos2 = set() # std
		# if 1: pinfos2 = my.Inspector(pinfos2, 'pinfos2')
		size_x, size_y = self.grid_size
		unit = self.unit
		bf = Bfield(pinfo1, owner=self)
		#
		blocks = [0, size_x*unit, 0, size_y*unit] # 四个方向屏蔽绝对值
		if 0 and node1 == (9, 7):
			blocks = my.Inspector(blocks, name='blocks', print_self=True)
		# 计算特殊两边界完全屏蔽 ( 四面　）
		blocked = bf.born_blocked()
		# main
		if not blocked:
			# 删除邻边, 所在边
			if edge1 == None: 
				for n in self.adj[node1]: caculated.add(sorted_nn(node1, n))
			else:
				caculated.add(edge1)
			# expand
			nx, ny = self.squareIndex_by_n(node1)
			bounds = [nodex, nodex, nodey, nodey] # i = -1
			for i in range(self.expand_cap):
				# 计算边界
				bounds = [ (nx - i) * unit, (nx + i + 1) * unit, (ny - i) * unit, (ny + i + 1) * unit ]
				# expand
				expands = self.expandDiamond_block(nx, ny, i, blocks)
				for expand in expands: # 单个区块
					for edge2 in expand.edges: # 一条边
						if edge2 in caculated: continue
						caculated.add(edge2) #包括屏蔽边
						#
						pinfo2 = p2, e2 = pinfo_by_pe(node1, edge2)
						if bf.is_edge_blocked(edge2): continue
						bf.update_by_e(edge2)
						pinfos2.add(pinfo2)
				# 计算是否完全屏蔽
				blocked = bf.is_complete(i)
				# blocked = (bounds[0] <= blocks[0]) and (bounds[1] >= blocks[1]) and (bounds[2] <= blocks[2]) and (bounds[3] >= blocks[3])
				if blocked: break
		# clear
		for pinfo2 in list(pinfos2):
			p2, e2 = pinfo2
			if self.is_blocked_node(p2, blocks):
				pinfos2.remove(pinfo2)
		# block_max
		# block_dis_list = [ nodex - blocks[0], blocks[1] - nodex, nodey - blocks[2], blocks[3] - nodey ]
		# assert all( dis >= 0 for dis in block_dis_list ), block_dis_list
		# block_max = max(block_dis_list)
		return pinfos2, blocks, bf

class _Replace():
	#evolve-replace
	def evolve_replace(self, *, debug=0):
		"""
			说明
				循环方式：
					依次循环，最近连续无变化的会被收集到已测中，变化后清空 ### 清空条件
			伪码
			"""
		debug = debug and de.evolve_replace
		#
		if debug:
			print(f'begin replace')
			self.draw(hl=[], ll=[], title_a=' begin-r')
		# main
		tested = set() # pairs
		for pair in my.iter_dynamic(self.rpairs, mode='cycle'):
			pinfo1, pinfo2 = pair
			if pair in tested: continue
				#
			if debug: de.light_on()
			fm = self.try_replace_pp(pinfo1, pinfo2)
			if debug: de.light_off()
			if fm:
				tested.clear()
				if debug:
					print(f'replace {pair}')
					self.draw(hl=[], ll=[], title_a=' r')
			else:
				tested.add(pair)
				if len(tested) == len(self.rpairs):
					assert tested == self.rpairs, my.d.differ_set(tested, self.rpairs, spliter='\n')
					break
		#
		if debug:
			print(f'end replace')
			self.draw(hl=[], ll=[], title_a=' end-r')
		return self
	def try_replace_pp(self, pinfo1, pinfo2):
			p1, e1 = pinfo1
			p2, e2 = pinfo2
			dis = self.distance(p1, p2)
			path = self.find_path_pp(pinfo1, pinfo2)
			size = len(path) - 1 #路径中边数
			dis_list = [self.distance(path[i], path[i+1]) for i in range(size)]
			index, dis_max = my.list.find_max(dis_list, value=True)
			
			if dis_max <= dis: return False
			else: # replace
				self.connect_pp(pinfo1, pinfo2)
				self.disconnect_close(path[index], path[index+1])
				# self.check()
				return True
class ReplacePlain(RpairPlain, _Replace, ):
	"""
		算法
			复杂度：n2
			找到所有可视<p, p>对
			对每一对计算环路增益
		说明：
			不自动合并
			修改时p-p自动更新
		结构
		"""
	"""scratch
		增边会新增屏蔽，减少连接
		删边会减少屏蔽，新增连接
		"""
	def __init__(self, *gs, **ks):
		self.blockDisMap = defaultdict(set)
		super().__init__(*gs, **ks)
		_Replace.__init__(self)
		1
	# public

# accurate

for name in 'gs gm gsr gmr gb gbr gbm gbmr'.split():
	#
	data_ = my.Data(f'rsmt\\{name}_info', {}) # (len, time_ns)
	note_path = f'ground\\rsmt\\test\\{name}_info.txt'
	#
	process = Process(name, data_, note_path)
	setattr(Process, name, process)
	Process.name_dict[name] = process
def test0(): # manual
	myplt.cap(12)
	g = SG()
	d0, d1, d2, d3, d4 = Dnodes1 = read_nodes(""" 0 0  0 1  1 2  2 0  2 1 """)
	Dnodes = Dnodes1
	Dnodes = sorted(Dnodes)
	s, = S = Snodes = read_nodes(""" 1 1 """)
	edges = [ (d0, d1), (d1, s), (s, d4), (s, d2), (d3,d4) ]
	print(Dnodes)
	g = SG(Dnodes=Dnodes, nodes=Dnodes+Snodes, edges=edges)
	d(my.str(g.dfsts(), splitor='\n'))
	dfsts = g.dfsts()
	sub = SG.sub_from_dfsts(dfsts)
	sub.draw()
	g.show(hl=[], ll=[])
def test0(): # key
	Dnodes10 = [(7, 9), (1, 8), (0, 7), (8, 5), (4, 5), (8, 7), (2, 3), (9, 1), (9, 3), (6, 3)] #gb 示范
	Dnodes11 = nodes_by_key((10, 5))
	myplt.cap(12)
	g = SG()
	Dnodes0 = nodes_random(3)
	Dnodes1 = read_nodes(""" 0 0  2 0  1 4  0 2  0 4 """)
	Dnodes2 = [(7, 9), (1, 8), (0, 7), (8, 5), (4, 5), (8, 7), (2, 3), (9, 1), (9, 3), (6, 3)]
	Dnodes3 = nodes_by_key((40, 4))
	Dnodes = Dnodes3
	Dnodes = sorted(Dnodes)
	print(Dnodes)
	g = SG.gbr(Dnodes, debug=1)
	g.show(hl=[], ll=[])
def test0(): #
	Dnodes10 = [(7, 9), (1, 8), (0, 7), (8, 5), (4, 5), (8, 7), (2, 3), (9, 1), (9, 3), (6, 3)] #gb 示范
	Dnodes11 = nodes_by_key((10, 5))
	myplt.cap(12)
	myplt.new()
	Dnodes0 = nodes_random(3)
	Dnodes1 = read_nodes(""" 0 0  2 0  1 4  0 2  0 4 """)
	Dnodes2 = [(7, 9), (1, 8), (0, 7), (8, 5), (4, 5), (8, 7), (2, 3), (9, 1), (9, 3), (6, 3)]
	Dnodes3 = nodes_by_key((70, 7))
	Dnodes = Dnodes3
	Dnodes = sorted(Dnodes)
	print(Dnodes)
	self = SG.gb(Dnodes)
	self.show(hl=[], ll=[])
def test0(): # add key
	if 0:
		for count in range(100, 600, 100):
			for seed in range(10):
				add_key((count, seed), cover=False)
	if 0:
		add_key((1000, 0))
	if 1:
		for seed in range(50):
			add_key((20, seed))
		update_basic_note()
def test0(): # run
	# data.gsr_info.clear()
	keys = list(data.smt_info())
	process = Process.gbmr
	# process.data.clear()
	process.run(keys=[k for k in keys if k[0] <= 500], save=1, cover=0)
def test0(): # update note
	Process.update_note()
def test0(): # performance
	perf = performance.active
	name = perf.name
	func_name = perf.func_name
	for n in range(50, 500, 50):
		nodes = nodes_random(n)
		path = f'ground\\rsmt\\performance\\{name}\\{n}.txt'
		#if my.file.exists(path): continue
		#
		perf.set_path(path)
		perf.clear()
		getattr(SG, func_name)(nodes)
		# perf.run(test)
		perf.print( sort='ncalls', filter=lambda line: 'rsmt' in line)
def test0(): # timer
	cap = timer_cap
	timers = [ Timer(split=True, discard_tail=True) for i in range(cap) ]
	# globals
	for i in range(cap):
		globals()[f'timer{i}'] = timers[i]
	# clabels, table
	clabels = ['n']
	for i in range(1, cap):
		clabels.append(f't{i}/t0')
	for i in range(1, cap):
		clabels.append(f't{i}/n')
	table = my.Table(clabels=clabels)
	# main
	for n in range(100, 800, 100):
		nodes = nodes_random(n)
		timers[0].start()
		SG.gb(nodes, debug=0)
		timers[0].stop()
		times = [ timers[i].time() // 1000 for i in range(cap) ]

		row = [n]
		row += [ my.format.div_allow0(times[i], times[0], format='.4') for i in range(1, cap) ]
		row += [ f'{int(times[i]/n)}' for i in range(1, cap) ]
		table.append(row)
		#print(f'{t1} / {t2} { my.format(, '<5') } { t2 / n }')
		for i in range(cap):
			timers[i].clear()
	table.print()
def test0(): # compare
	myplt.cap(12)
	key = (100, 8)
	Dnodes = nodes_by_key(key)
	g1 = smt_graph(key=key)
	g2 = SG.gbmr(Dnodes, debug=0)
	myplt.cap(4)
	t1, t2, pairs = fdiffer_weight_misc(g1, g2)
	g1.draw(title_a=' optimal')
	axis = myplt.axis()
	#
	g2.draw()
	t1.draw(axis=axis, title_a='differ1')
	t2.draw(axis=axis, title_a='differ2')
	# pairs
	myplt.cap(2)
	for sub1, sub2 in pairs:
		sub1.draw()
		sub2.draw()
	myplt.show()
def test0(): #
	s = _Replace.squareRelIndexs_expand_plain_map[0]
	d(s)
	g = PosGraph()
	g.add_nodes(s)
	g.show()
	#for index in s:
def test(): # bb
	key = (50, 0)
	perf = my.Performance()
	# setting
	trace = 0
	# fsts
	hg1 = fsts_hg_by_key(key)
	hg2 = pruned_hg_by_key(key)
	if trace:
		hg = hg1
	else:
		1
		hg = hg2

	nodes = data.nodes()[key]
	myplt.share_axis_by_nodes(nodes)
	# geo
	mst0 = geosmt_hg_by_key(key)
	mst0_len = smt_len(key)
	d.mst0 = mst0
	# mst0_len = mst0.len()
	# mst
	my.random.seed(2)
	#
	cut_mode = 0
	if trace and 0:
		for e in list(hg.edges):
			if not hg2.has_edge(e) and not mst0.has_edge(e):
				hg.disconnect(e)
	if 0:
		flag_simplify = 0
		del_nodes_ = []
		del_edges_ = []
		del_nodes_ = []
		del_edges_ = []
		reserve = 66
		del_nodes = mst0.getDelNodes_delNodesClear_reserveNode(del_nodes_, reserve)
		for h in (hg, mst0):
			h.del_nodes_clear(del_nodes)
		assert mst0.is_subgraph(hg)
		# myplt.cap(2)
		# mst0.draw()
		# hg.show()
		def try_(edges=[], nodes=[]):
			hg_ = hg.copy()
			mst0_ = mst0.copy()
			if 1: # del-node
				del_nodes =  set(del_nodes_ + nodes) & hg.nodes
				if reserve in del_nodes: return False
				assert reserve in hg.nodes
				del_nodes = mst0_.getDelNodes_delNodesClear_reserveNode(del_nodes, reserve)

				# del_nodes =  list(range(60)) + [109, 150, 80, 147, 139]
				del_edges = del_edges_ + edges
				# del_edges = [ {88, 92}, {138, 135}, {144, 146}]
				for h in (hg_, mst0_):
					h.del_nodes_clear(del_nodes)
				# hg_.delNode_cutSmallerSub(
					for e in del_edges:
						if h.has_edge(e): h.disconnect(e)
					if not h.is_span(): return False
					# assert h.check_span(), h.show(node_label=1)
				assert mst0_.is_subgraph(hg_)	
			d.mst = mst0_
			d.mst_len = mst0_len
			myplt.cap(12)
			set_hg_odd(hg_, mst=mst0_)

			main = lambda: hg_.mst_test(
				solver_args=dict(debug=4, verbose_text=1, verbose_pic=1, ishow=12,
					_print=dict(expand_state=1, set_map=1, update_net=1, combine=1),
					_show=dict(models=0, net=0, valid_add=1, invalid_add=0, set_map=0),
					filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace=mst0 if trace else None,
					best1=0, no_cycle=1, combine=1,
					order_mode=None, cut_mode=cut_mode, 
					state_threshold=100, iter_threshold=10000,
					threshold_addState_edgeRate=0.1, pick_start=None,
					# threshold_addState_model=12,
				),
				solve_args=dict(
					return_solver=1,
				),
			)
			try: main()
			except my.Exception:
				if not flag_simplify: raise
				return True
			else:
				return False
		if flag_simplify:
			for i in range(2):
				assert try_()
			# node
			count = 0
			for n in my.iter.loop(hg.nodes):
				if n in del_nodes_: continue
				for i in range(8):
					flag = try_(nodes=[n])
					if not flag:
						print(f'fail node[{i}]')
						break
				else:
					
					flag_ = try_(nodes=[n])
					del_nodes_.append(n)
		
					d(del_nodes_=str(del_nodes_))

					# pause()
					count = 0
				count += 1
				if count >= len(hg.edges): break
			# edge
			count = 0
			for e in my.iter.loop(hg.edges):
				if e in del_edges_: continue
				for i in range(8):
					flag = try_(edges=[e])
					if not flag:
						print(f'fail edge[{i}]')
						break
				else:
					
					flag_ = try_(edges=[e])
					del_edges_.append(e)
		
					d(del_edges_=str(del_edges_))

					# pause()
					count = 0
				count += 1
				if count >= len(hg.edges): break
			return 
		else:
			try_()
			myplt.show()
		return
	d.mst = mst0
	d.mst_len = mst0_len
	myplt.cap(12)
	if trace: # odd
		set_hg_odd(hg, mst=mst0)
	else:
		set_hg_odd(hg, mst=mst0)
		1
	# d.mst = hg.mst()
	if 1: # 简单平推
		mst = hg.cacu_mst2(verbose_pic=4, debug=6)
		hg.draw()
		mst.draw()
		myplt.show()
		return
	# main
	if 1:
		main = lambda: hg.mst_test(
			solver_args=dict(debug=4, verbose_text=1, verbose_pic=1, ishow=12,
				_print=dict(expand_state=1, set_map=0, update_net=1, combine=1),
				_show=dict(models=0, net=0, valid_add=1, invalid_add=0, set_map=0),
				filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace=mst0 if trace else None,
				best1=0, no_cycle=1, combine=1,
				order_mode=None, cut_mode=cut_mode, 
				state_threshold=100, iter_threshold=10000,
				threshold_addState_edgeRate=0.1, pick_start=None,
				# threshold_addState_model=12,
			),
			solve_args=dict(
				return_solver=1,
			),
		)
	elif 1:
		main = lambda: hg.mst_test(debug=5, debug_filter=4, filter=0, return_solver=1, restore=0,
			cut_mode=0, cut_cycle=1, order_mode='delta', cond=0, verbose_text=3, verbose_pic=2, start=None,
			 cacu_v=2)
	else:
		main = lambda: hg.mst_test(debug=4, debug_filter=4, filter=0,
			cut_mode=0, cut_cycle=1, order_mode='x', cond=0, verbose_text=3, verbose_pic=1,
			return_solver=1, restore=0, cacu_v=1)
	# print
	if 0: 
		solver = perf.run(main)
		perf.print(filter=lambda line: 'graph' in line)
	else: 
		for i in range(1):
			solver = main()
	reduced_hg, mst_, mst = solver.hg, solver.mst_, solver.mst
	if 0:
		reduced_hg.test_print_rb()
	mst_len = mst.len() + solver.shrink
	#
	# myplt.cap(4)
	flag_succeed = mst == mst0 or mst_len == mst0_len
	if not flag_succeed and isinstance(mst_len, float):
		if abs(mst_len - mst0_len) < 0.3:
			flag_succeed = True
	if not flag_succeed:
		hg.draw(node_label=1, title=f'fsts')
		reduced_hg.draw(node_label=0, title=f'reduced')
		mst.draw(title=f'mst<{mst_len}>')
		mst0.draw(title=f'geo<{mst0_len}>')
		#hg.draw(edges=filter(hg.edges, lambda e: len(e) == 2) )
		print(f'mst fail mst[{mst_len}] geo[{mst0_len}]')
		myplt.show()
		raise
	else:
		print(f'mst succeed')
		hg.draw(node_label=0, title=f'fsts')
		reduced_hg.draw(node_label=0, title=f'reduced')
		mst.draw(title=f'mst<{mst_len}>')
		myplt.show()
def test0(): # bug
	keys = nodes_by_key((500, 0))
	path = 'ground\\tmp\\1.txt'
	d(os.getcwd())
	d(os.listdir('ground\\tmp'))
	lines = []
	for x, y in keys:
		lines.append(f'{x} {y}')
	my.file.writelines(path, lines)
def test0(): # tmp_info
	myplt.cap(3)
	nodes, fsts_hg, pruned_hg, smt_graph = tmp_analyze_info()
	myplt.share_axis_by_nodes(nodes)
	fsts_hg.draw()
	pruned_hg.draw()
	smt_graph.draw()
	myplt.show()
def test0(): # prune
	key = (100,8)
	pos = nodes = data.nodes()[key]
	myplt.share_axis_by_nodes(nodes)
	hg1 = fsts_hg_by_key(key)
	hg2 = pruned_hg_by_key(key)
	smt = geosmt_hg_by_key(key)
	r_graph = smt_graph(key)
	# g = SG.mst(nodes)
	if 'check_edge2_in_gmst()' and 0:
		for e in hg1.edges:
			if len(e) == 2:
				e_ = sorted2( [pos[n] for n in e])
				if not e_ in g.std_edges:
					myplt.cap(2)
					hg1.draw(hl_edges=[e])
					g.draw()
					myplt.show()
					break
	wedges = hg2.wedges()
	print(f'wedges={wedges}\n' f'pos = {hg2.get_pos()}\n')
	#test
	# hg2.test_Ru1_tri()

	#
	myplt.cap(12)
	hg1.draw()
	hg2.draw()
	smt.draw(node_label=1)
	r_graph.draw(draw_Snodes=1)
	myplt.show()
def test0(): # pic
	debug = 7
	import graph
	def draw_edges_r():
		graph.Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
		# HyperGraph._draw_edges([edge_adding], pos=pos, edge_look=dict(color='black', width_rate=2))
		# HyperGraph._draw_edges(my.list.removed(edges_used, edge_adding), pos=pos, edge_look=dict(color='black', width_rate=2))
		HyperGraph._draw_nodes(used_nodes, look=dict(alpha=0), label=1, pos=pos)
		HyperGraph._draw_edges(edges_used, pos=pos, edge_look=dict(color='black', width_rate=2))
		Graph._draw_nodes(unused_nodes, pos=pos, look=dict(color='grey', alpha=0.2))
		# myplt.title(f's={len(igroups)} a={len(anodes)}')
	def debug_draw(i=debug):
		cond2 = cond and len(igroups) >= 12
		cond1 = cond2
		if i >= 6 or cond2:
			myplt.new_figure()
		# edges-remained
		if i >= 5 or cond1:
			draw_edges_r()
		if i >= 6 or cond2:
			# igs
			matched_found = 0
			for ig in igroups_:
				ig.draw_(inodes, anodes, used_nodes, pos)
		1
	def debug(i=debug):
		cond2 = cond and len(igroups) >= 12
		cond1 = cond2
		if i >= 6 or cond2:
			myplt.new_figure()
		# edges-remained
		if i >= 5 or cond1:
			draw_edges_r()
		if i >= 6 or cond2:
			# igs
			matched_found = 0
			for ig in igroups_:
				ig.draw_(inodes, anodes, used_nodes, pos)
		1
	def check_possible():
		if debug and 0:
			flag = any(ig.is_possible(edges_used, mst_len=mst_len) for ig in igroups_)
			flag |= min_ig != None and min_weight == mst_len
			assert flag, igroups
			return flag
	def draw_igroup(iedges):
		edges = [ i_e_map[i] for i in iedges ]

		title = f''
		ks = Graph.prepare_draw(title=title)
		ks = HyperGraph._draw_edges(edges, pos=pos)
		Graph._draw_nodes(inodes, pos=pos, look=dict(color='blue'))
		Graph._draw_nodes(anodes, pos=pos, look=dict(color='red'))



	key = (10,1)
	pos = nodes = data.nodes()[key]
	myplt.share_axis_by_nodes(nodes)
	hg1 = fsts_hg_by_key(key)
	hg2 = pruned_hg_by_key(key)
	smt = geosmt_hg_by_key(key)
	r_graph = smt_graph(key)
	edges = list(hg2.edges)
	i_e_map = { i: e for i, e in enumerate(edges) }
	e_i_map = DictOfSet( (e, i) for i, e in i_e_map.items() )
	# g = SG.mst(nodes)
	if 'check_edge2_in_gmst()' and 0:
		for e in hg1.edges:
			if len(e) == 2:
				e_ = sorted2( [pos[n] for n in e])
				if not e_ in g.std_edges:
					myplt.cap(2)
					hg1.draw(hl_edges=[e])
					g.draw()
					myplt.show()
					break
	wedges = hg2.wedges()
	print(f'wedges={wedges}\n' f'pos = {hg2.get_pos()}\n')
	#test
	# hg2.test_Ru1_tri()

	#
	iedges_used = [ 0,3,7,8 ]
	edges_used = [ i_e_map[i] for i in iedges_used ]
	anodes = hg2.get_anodes_by_edges(edges_used)
	used_nodes = my.set.unionm(edges_used)
	nodes = set(hg2.nodes)
	edges_r = my.set_like.difference(edges, edges_used)
	pos = hg2.get_pos()
	# inodes = hg2.get_inodes_by_edges(edges_used)
	inodes = my.set_like.difference(used_nodes, anodes)
	unused_nodes = nodes.difference(used_nodes)
	igroups = [ [0], [3,7],  ]
	titles = [ '{{1,2,3}}', '{{1},{2,3}}']
	#
	myplt.cap(12)
	draw_edges_r()
	for i,ig in enumerate(igroups):
		draw_igroup(ig)
		myplt.title(titles[i])


	# hg1.draw()
	hg2.draw(edge_label=e_i_map)
	hg2.draw()
	smt.draw(node_label=1)
	# r_graph.draw(draw_Snodes=1)
	myplt.show()
def test0(): # test-keys
	for size in range(10, 201):
		key = (size, 0, default.test_cap)
		add_key(key, cover=1)
def test0(): # test
	# data.smt_simple_time.clear()
	update_smt_simple_time()
	#

	# data.smt_filter_time.clear()
	# update_smt_filter_time()
	
	# data.smt_match_time.clear()
	# update_smt_match_time()
	...
	if 0:
		map1 = data.smt_simple_time()
		for k, t in list(map1.items()):
			if t is None:
				del map1[k]
		data.smt_simple_time.save()
		#
		map2 = data.smt_match_time()
		for k, t in list(map2.items()):
			if t is None:
				del map2[k]
		data.smt_match_time.save()
def test0(): # test-draw
	
	# draw_smt_simple_time()
	# draw_smt_match_time()
	draw_test()
	myplt.show()

def test0(): # solve
	# key = (199, 1, default.test_cap)
	key = (200,8)
	hg = pruned_hg_by_key(key)
	set_hg_odd(hg, mst=None)
	if 1:
		solver = hg.mst_test(
			solver_args=dict(debug=1, verbose_text=1, verbose_pic=2, ishow=12,
				_print=dict(expand_state=1, set_map=0, update_net=1, combine=1),
				_show=dict(models=0, net=0, valid_add=1, invalid_add=1, set_map=0),
				filter=0, dynamic_filter=2, restore=1, cacu_v=2, trace= None,
				best1=0, no_cycle=1, combine=1,
				filter_mode=1,
				order_mode=None, cut_mode=0, 
				state_threshold=2000, iter_threshold=10000,
				threshold_addState_edgeRate=0.1, pick_start='auto1',
				# threshold_addState_model=12,
			),
			solve_args=dict(
				return_solver=1,
			),
		)
		mst = solver.mst
	else:
		mst = mst_match(hg)
	hg.draw() 
	mst.draw()
	myplt.show()
def test0(): # compare-nodes
	for size in range(10, 15, ):
		# key0 = (size, 0)
		key0 = (size, 0, default.test_cap)
		hg0 = pruned_hg_by_key(key0)

		# key1 = (size, 1)
		key1 = (size, 1, default.test_cap)
		hg1 = pruned_hg_by_key(key1)

		assert size == len(hg0.nodes)
		d(size)
		myplt.cap(2)
		hg0.draw(edges=[])
		# hg1.draw(edges=[])
	myplt.show()
def test0(): # 整齐
	nodes = [ (i, j) for i in range(5) for j in range(5) ]
	edges = []
	for n in nodes:
		i, j = n
		n1 = (i+1, j)
		if n1 in nodes:
			edges.append((n, n1))
		n1 = (i, j+1)
		if n1 in nodes:
			edges.append((n, n1))
	graph = PosGraph(nodes=nodes, edges=edges)
	graph.draw()
	myplt.show()
if __name__ == '__main__':
	test()

	# update()
	#update_gs(keys=[(10,1)], cover=1)

