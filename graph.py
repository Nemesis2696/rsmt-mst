from base import *
import base
import math
import networkx as nx
import networkx
import matplotlib.pyplot as plt
from plot import myplt
import random
from perf import *

"""
	nx.Graph:
		edges: n1, n2 的顺序按照nodes中的顺序
	Graph
		highlight
			Pos时才有用
			即使对象不在图中也有效
	"""
"""概述
	add_edge,connect
		connect: 要求点存在
		add_edge 当点不存在 
		connect_nn(n1, n2)
		connect(e)
		add_edge_nn(n1, n2)
		add_edge(e)
	
	
	"""
__all__ = '''
	Graph PosGraph HyperGraph PosHyperGraph
	'''.split()

class de:
	debug = __debug__ and 1
	mst = debug and 1
	cut_equal_cover = mst and 1
	list_count_state = mst and 1
	print_getter_created = debug and 0
	check_mst_span = mst and 1
	check_possible = mst and 1
if "timer":
	timer1 = my.Timer()

class default:
	alpha = 0.5
	label_alpha = 1
	#
	@my.des.dict
	class node:
		color = 'blue'
		shape = 'o'
		
	@my.des.dict
	class hl_node:
		color = 'red'
		size_rate = 1
		shape = 'o'
	@my.des.dict
	class edge:
		color = 'black'
		style = '-'
	@my.des.dict
	class hl_edge:
		color = 'orange'
		width_rate = 1
		style = '-'
		width_rate = 0.5
	class HyperGraph:
		@my.des.dict
		class edge:
			color = 'gray'
			style = '-'
			width_rate = 0.5
		@my.des.dict
		class hl_edge:
			color = 'orange'
			width_rate = 1.5
			style = '-'
		@my.des.dict
		class hl_edge1:
			color = 'purple'
			width_rate = 1.5
			style = '-'
		@my.des.dict
		class node:
			color = 'blue'
			shape = 'o'
		@my.des.dict
		class hl_node:
			color = 'red'
			size_rate = 1
			shape = 'o'
		@my.des.dict
		class enode:
			color = 'gray'
			size_rate = 0.5
			shape = 'o'
			alpha = 0
		@my.des.dict
		class hl_enode:
			color = 'gray'
			size_rate = 0
			shape = 'o'
			alpha = 0
		@my.des.dict
		class hl_enode1:
			color = 'purple'
			size_rate = 0
			shape = 'o'
			alpha = 0.5
		
def nodes_random(count, *, cap=10):
	r = []
	assert count <= cap ** 2
	for i in range(count):
		while True:
			x = random.randint(0, cap)
			y = random.randint(0, cap)
			node = (x, y)
			if node not in r:
				r.append(node)
				break
	return r
def get_pos_random(nodes):
	nodes = list(nodes)
	poss = nodes_random(len(nodes))
	return { nodes[i] : poss[i] for i in range(len(nodes)) }
def pos_get_pos(nodes=None, edges=None):
	assert nodes is not None or edges is not None
	pos = {}
	if nodes is not None:
		for n in nodes:
			pos[n] = n
	if edges is not None:
		for e in edges:
			for n in e:
				pos[n] = n
	return pos
def auto_get_pos(nodes):
	return get_pos_random(nodes)

class Edge2Comparer:
	def max_edges(edges, weight): ###
		wedges = [ (e, weight[e]) for e in edges ]
		max_e, max_w = max_wedge = max(wedges, key=Edge2Comparer.key_wedge)
		return max_e
	def key_wedge(ew):
		e, w = ew
		return (w, e)
nx_graph = nx.Graph()
if "weight pos":
	class PosDict(dict):
		__setitem__ = NotImplemented
		__delitem__ = NotImplemented
		pop = NotImplemented
		update = NotImplemented
	class WeighterCall:
		def __init__(self, func):
			self.func = func
		def __getitem__(self, e):
			return self.func(e)
	class WeighterFalse:
		def __init__(self):
			...
		def __getitem__(self, e):
			raise Exception(f'{e}')
class GraphBase:
	"""
		overload: connect_nn
		"""
	if "node":
		def add_node(self, node):
			assert node not in self.nodes
			self.nodes.add(node)
			return self
		def add_nodes(self, nodes):
			for n in nodes: self.add_node[n]
			return self		#
		def update_node(self, n):
			if n in self.nodes: return
			else: return self.add_node(n)
		def update_nodes(self, ns):
			for n in ns:
				self.update_node(n)
			return self
	if "edge":
		...
		def connect(self, e):
			n1, n2 = e
			return self.connect_nn(n1, n2)
		def add_edge(self, e):
			n1, n2 = e
			return self.add_edge_nn(n1, n2)
		def add_edge_nn(self, n1, n2):
			if n1 not in self.nodes: self.add_node(n1)
			if n2 not in self.nodes: self.add_node(n2)
			return self.connect_nn(n1, n2)

	if "draw":
		@dynamicmethod
		def prepare_draw(self, *, axis=None, new=True, title=None, title_a=None, **ks):
			if new: myplt.new()
			ax = plt.gca()
			ax.set_aspect(1./ax.get_data_ratio())
			plt.axis('on')
			if axis != None:
				myplt.axis(axis)
			myplt.title( title=title, title_a=title_a )
			return ks
		@dynamicmethod
		def draw_after(self, axis=None, **ks):
			if axis != None:
				myplt.axis(axis)
			return ks
		def draw(self, nodes=None, edges=None, *, hl_nodes=set(), hl_edges=set(), pos=None, **ks):
			"""
				没有pos时，使用原始draw，hl不使用
				"""
			#pre
			if nodes == None: nodes = self.nodes
			if edges == None: edges = self.edges
			#pos
			# if pos == None: pos = self.pos
			# if pos == None and not isinstance(self, PosGraph): # without pos
			# 	pos = self.default_pos(nodes=nodes, edges=edges)
			# 	# myplt.block_share_axis(1)
			# 	# ks = self.prepare_draw(**ks)
			# 	# nx.draw_networkx(self, nodelist=nodes, edgelist=edges)
			# 	# myplt.block_share_axis(0)
			# 	# return self
			flag_ori = pos == None and self.pos == None and not self.flag_pos_from_nodes_edges 
			pos = self.get_pos(nodes=nodes, edges=edges, pos=pos)
			if flag_ori: myplt.block_share_axis(1)
			ks = self.prepare_draw(**ks)
			if flag_ori: myplt.block_share_axis(0)
			if not myplt.flag_axis_set(): # auto-axis
				myplt.set_axis_by_nodes(pos.values())
			# pre
			hl_edges = {tuple(sorted(e)) for e in hl_edges}
			#
			ks = self._draw(nodes=nodes, edges=edges, hl_nodes=hl_nodes, hl_edges=hl_edges, pos=pos, **ks)
			assert empty(ks), ks
			return self
		def _draw(self, *, nodes, edges, hl_nodes=set(), hl_edges=set(), pos, node_label=False, edge_label=False, **ks):
			"""
				edge: sorted
				hl_edges: sorted
				"""
			# pre
			assert 'label' not in ks
			edges = {tuple(sorted(e)) for e in edges}
			# highlight
			spec = set(hl_edges | hl_nodes) # sorted
			# nodes
			self._draw_nodes([n for n in nodes if n not in spec], look=default.node, pos=pos, label=node_label, **ks)
			self._draw_nodes(hl_nodes, look=default.hl_node, pos=pos, label=node_label, **ks)
			# edges
			self._draw_edges([e for e in edges if e not in spec], look=default.edge, pos=pos, label=edge_label, **ks)
			self._draw_edges(hl_edges, look=default.hl_edge, pos=pos, label=edge_label, **ks)
			return ks
		@dynamicmethod
		def draw_nodes(self, *gs, **ks):
			assert myplt.initialized()
			ks = self.prepare_draw(**ks)
			return self._draw_nodes(*gs, **ks)
		@dynamicmethod
		def draw_edges(self, *gs, **ks):
			assert myplt.initialized()
			ks = self.prepare_draw(**ks)
			return self._draw_edges(*gs, **ks)
		@dynamicmethod
		def _draw_nodes(self, nodes=None, *, pos=None, look={}, label=False): ## pos
			look = dict(look)
			# pos
			pos = self.get_pos(nodes=nodes, pos=pos)
			# color
			color = look.get('color', None)
			if callable(color):
				color = [color(n) for n in nodes]
			look['color'] = color
			#
			size = self.appropriate_node_size(len(nodes))
			# look
			my.dict.set_default(look, alpha=default.alpha, size_rate=1)
			look_ = {}
			for name, val in look.items():
				match name:
					case 'color': look_['node_color'] = val
					case 'shape': look_['node_shape'] = val
					case 'size_rate': look_['node_size'] = val * size
					case _: look_[name] = val

			#label
			if label == False: pass
			else:
				if label == True:
					label = { n: str(n) for n in nodes }
				elif isinstance(label, dict): 
					label = label
				else: raise Exception(f'{label, type(label)}')
				nx.draw_networkx_labels(self, pos=pos, labels=label)
			
			#
			nx.draw_networkx_nodes(nx_graph, nodelist=nodes, pos=pos, **look_)
			return self
		@dynamicmethod
		def _draw_edges(self, edges=None, *, pos=None, label=False, look={}):
			if edges == None: edges = self.edges
			nodes = my.set.unionm_iterable(edges)
			look = dict(look)
			# pos
			pos = self.get_pos(edges=edges, pos=pos)
			# color
			color = look.get('color', None)
			if callable(color):
				color = [color(n) for n in nodes]
			look['color'] = color
			#
			# width
			is_adj = look.get('is_adj', None)
			if self.is_adj != None:
				assert is_adj == None
				is_adj = self.is_adj
			width = self.appropriate_edge_width(len(edges), is_adj=is_adj)
			# look
			look_ = {}
			my.dict.set_default(look, alpha=default.alpha, width_rate=1)
			for name, val in look.items():
				match name:
					case 'color': look_['edge_color'] = val
					case 'width_rate': look_['width'] = val * width
					case _: look_[name] = val
			#
			nx.draw_networkx_edges(nx_graph, edgelist=edges, pos=pos, **look_)
			# label
			if label in [False, 0]: pass
			else:
				if isinstance(label, str):
					label = nx.get_edge_attributes(self, label)
					#d(label)
				elif isinstance(label, dict): pass
				elif callable(label):
					label = {e: label(e) for e in edges}
				elif label in [True, 1]:
					label = {e: self.weight[e] for e in edges}
				else: raise Exception(f'{label}')
				label = {edge:value for edge, value in label.items() if edge in edges}
				nx.draw_networkx_edge_labels(nx_graph, pos=pos, edge_labels=label, alpha=default.label_alpha)
				return self
		
		def show(self, *gs, **ks):
			self.draw(*gs, **ks)
			myplt.show()

class Graph(nx.Graph, GraphBase):
	"""
		weight:
			随时添加
			删除边时删除
			@weight dict | callable | False
			interface: weight[e]
		pos: dict | callable(nodes=, edges=)->dict
			@pos <PosDict-readonly>
			flag_pos_from_nodes_edges: 能从nodes,edges得到固定的pos
		attr
			weight <dict>
			_std_edges <set>
		args:
			pos: dict | callable(nodes) -> dict | Graph | HyperGraph
			color: name | func(n) -> color
			node-look:
				shape: '
			edge-look:
				style: '
			node/edge-label: bool | dict
		usage:
			draw( node_look=, edge_look=, node_label=, edge_label=)
			draw_nodes( look=, label= )
				label<bool>
		"""
	is_adj = None # 边连接相邻节点
	flag_pos_from_nodes_edges = False
	def __init__(self, graph=None, *, nodes=[], edges=[], pos=None, weight={}):
		super().__init__()
		self._std_edges = set()
		#
		self.add_nodes(nodes)
		self.connectm(edges)
		self.set_pos(pos)
		self.set_weight(weight)
		if graph != None:
			raise
	if "draw":
		@dynamicmethod
		def prepare_draw(self, *, axis=None, new=True, title=None, title_a=None, **ks):
			if new: myplt.new()
			ax = plt.gca()
			ax.set_aspect(1./ax.get_data_ratio())
			plt.axis('on')
			if axis != None:
				myplt.axis(axis)
			myplt.title( title=title, title_a=title_a )
			return ks
		@dynamicmethod
		def draw_after(self, axis=None, **ks):
			if axis != None:
				myplt.axis(axis)
			return ks
		def draw(self, nodes=None, edges=None, *, hl_nodes=set(), hl_edges=set(), pos=None, **ks):
			"""
				没有pos时，使用原始draw，hl不使用
				"""
			#pre
			if nodes == None: nodes = self.nodes
			if edges == None: edges = self.edges
			#pos
			# if pos == None: pos = self.pos
			# if pos == None and not isinstance(self, PosGraph): # without pos
			# 	pos = self.default_pos(nodes=nodes, edges=edges)
			# 	# myplt.block_share_axis(1)
			# 	# ks = self.prepare_draw(**ks)
			# 	# nx.draw_networkx(self, nodelist=nodes, edgelist=edges)
			# 	# myplt.block_share_axis(0)
			# 	# return self
			flag_ori = pos == None and self.pos == None and not self.flag_pos_from_nodes_edges 
			pos = self.get_pos(nodes=nodes, edges=edges, pos=pos)
			if flag_ori: myplt.block_share_axis(1)
			ks = self.prepare_draw(**ks)
			if flag_ori: myplt.block_share_axis(0)
			if not myplt.flag_axis_set(): # auto-axis
				myplt.set_axis_by_nodes(pos.values())
			# pre
			hl_edges = {tuple(sorted(e)) for e in hl_edges}
			#
			ks = self._draw(nodes=nodes, edges=edges, hl_nodes=hl_nodes, hl_edges=hl_edges, pos=pos, **ks)
			assert empty(ks), ks
			return self
		def _draw(self, *, nodes, edges, hl_nodes=set(), hl_edges=set(), pos, node_label=False, edge_label=False, **ks):
			"""
				edge: sorted
				hl_edges: sorted
				"""
			# pre
			assert 'label' not in ks
			edges = {tuple(sorted(e)) for e in edges}
			# highlight
			spec = set(hl_edges | hl_nodes) # sorted
			# nodes
			self._draw_nodes([n for n in nodes if n not in spec], look=default.node, pos=pos, label=node_label, **ks)
			self._draw_nodes(hl_nodes, look=default.hl_node, pos=pos, label=node_label, **ks)
			# edges
			self._draw_edges([e for e in edges if e not in spec], look=default.edge, pos=pos, label=edge_label, **ks)
			self._draw_edges(hl_edges, look=default.hl_edge, pos=pos, label=edge_label, **ks)
			return ks
		@dynamicmethod
		def draw_nodes(self, *gs, **ks):
			assert myplt.initialized()
			ks = self.prepare_draw(**ks)
			return self._draw_nodes(*gs, **ks)
		@dynamicmethod
		def draw_edges(self, *gs, **ks):
			assert myplt.initialized()
			ks = self.prepare_draw(**ks)
			return self._draw_edges(*gs, **ks)
		@dynamicmethod
		def _draw_nodes(self, nodes=None, *, pos=None, look={}, label=False): ## pos
			look = dict(look)
			# pos
			pos = self.get_pos(nodes=nodes, pos=pos)
			# color
			color = look.get('color', None)
			if callable(color):
				color = [color(n) for n in nodes]
			look['color'] = color
			#
			size = self.appropriate_node_size(len(nodes))
			# look
			my.dict.set_default(look, alpha=default.alpha, size_rate=1)
			look_ = {}
			for name, val in look.items():
				match name:
					case 'color': look_['node_color'] = val
					case 'shape': look_['node_shape'] = val
					case 'size_rate': look_['node_size'] = val * size
					case _: look_[name] = val

			#label
			if label == False: pass
			else:
				if label == True:
					label = { n: str(n) for n in nodes }
				elif isinstance(label, dict): 
					label = label
				else: raise Exception(f'{label, type(label)}')
				nx.draw_networkx_labels(self, pos=pos, labels=label)
			
			#
			nx.draw_networkx_nodes(nx_graph, nodelist=nodes, pos=pos, **look_)
			return self
		@dynamicmethod
		def _draw_edges(self, edges=None, *, pos=None, label=False, look={}):
			if edges == None: edges = self.edges
			nodes = my.set.unionm_iterable(edges)
			look = dict(look)
			# pos
			pos = self.get_pos(edges=edges, pos=pos)
			# color
			color = look.get('color', None)
			if callable(color):
				color = [color(n) for n in nodes]
			look['color'] = color
			#
			# width
			is_adj = look.get('is_adj', None)
			if self.is_adj != None:
				assert is_adj == None
				is_adj = self.is_adj
			width = self.appropriate_edge_width(len(edges), is_adj=is_adj)
			# look
			look_ = {}
			my.dict.set_default(look, alpha=default.alpha, width_rate=1)
			for name, val in look.items():
				match name:
					case 'color': look_['edge_color'] = val
					case 'width_rate': look_['width'] = val * width
					case _: look_[name] = val
			#
			nx.draw_networkx_edges(nx_graph, edgelist=edges, pos=pos, **look_)
			# label
			if label in [False, 0]: pass
			else:
				if isinstance(label, str):
					label = nx.get_edge_attributes(self, label)
					#d(label)
				elif isinstance(label, dict): pass
				elif callable(label):
					label = {e: label(e) for e in edges}
				elif label in [True, 1]:
					label = {e: self.weight[e] for e in edges}
				else: raise Exception(f'{label}')
				label = {edge:value for edge, value in label.items() if edge in edges}
				nx.draw_networkx_edge_labels(nx_graph, pos=pos, edge_labels=label, alpha=default.label_alpha)
				return self
		
		def show(self, *gs, **ks):
			self.draw(*gs, **ks)
			myplt.show()
	if "info":
		# basic
		def std_edges(self):
			return self._std_edges
		def len(self, *, weight=None):
			if weight == None: weight = self.get_weight_dict()
			return sum(self.weight[e] for e in self.std_edges())
		# judge
		def has_edge(self, edge):
			return nx.Graph.has_edge(self, *edge)
		def is_tree(self):
			return nx.is_tree(self)
		def is_span(self):
			"""
				覆盖所有点且单连通
				"""
			if len(self.nodes) <= 1: return True
			subs = self.nodeSubs()
			if len(subs) != 1: return False
			if len(subs[0]) < len(self.nodes): return False
			return True

		# subs
		# def connected_component_subgraphs(self):
		# 	cls = self.view_type
		# 	graph = cls(self)
		# 	subs = list(graph.subgraph(c) for c in nx.connected_components(graph))
		# 	return subs
		# subs = connected_component_subgraphs
	if "pos weight":
		
		def default_pos(self, *, nodes=None, edges=None):
			"""
				args:
					nodes/edges-None: -> 无
				"""
			# if nodes is None and edges is None:
			# 	return nx.drawing.spring_layout(self)
			# else:
				# if nodes == None: nodes = self.nodes
				# if edges == None: edges = self.edges
			g = Graph(nodes=nodes, edges=edges)
			pos = nx.drawing.spring_layout(g)
			return pos
		@dynamicmethod
		def get_pos(self, *, nodes=None, edges=None, pos=None) -> 'dict|None':
			if pos == None: pos = self.pos
			if pos == None: 
				return self.default_pos(nodes=nodes,edges=edges)
			if callable(pos):
				r = pos(nodes=nodes, edges=edges)
			elif isinstance(pos, dict):
				r = pos
			else:
				raise Exception(f'{pos}')
				
			assert isinstance(r, dict)
			return r
		def set_pos(self, pos):
			if isinstance(pos, PosDict):
				self.pos = pos
			elif pos == None:
				self.pos = None
			elif isinstance(pos, (Graph, HyperGraph)):
				self.copy_pos_from(pos)
			elif isinstance(pos, dict):
				self.pos = PosDict(pos)
			else: raise Exception(f'{pos}')
		def copy_pos_from(self, g):
			"""
				g: Graph | HyperGraph
				"""	
			if isinstance(g, Graph):
				self.set_pos(g.pos)
			elif isinstance(g, HyperGraph):
				self.set_pos(g.pos)
			else: raise Exception(f'{g}')
			return self
		#
		def set_weight(self, weight):
			if weight ==None:
				self.weight = {}
			elif isinstance(weight, dict):
				map = {}
				for e in self.std_edges():
					if e in weight:
						map[e] = weight[e]
				self.weight = map
			elif isinstance(weight, DictOfSet):
				map = {}
				for e in self.std_edges():
					map[e] = weight[set(e)]
				self.weight = map
			elif isinstance(weight, (Graph, HyperGraph)):
				self.copy_weight_from(weight)
			elif callable(weight):
				self.weight = WeighterCall(weight)
			elif weight == False:
				self.weight = NotImplemented
			else: raise Exception(f'{weight} {type(weight)}')
			return self
		def copy_weight_from(self, g):
			"""
				g: Graph | HyperGraph
				"""	
			if isinstance(g, Graph):
				self.set_weight(g.weight)
			elif isinstance(g, HyperGraph):
				self.set_weight(g.weight)
			else: raise Exception(f'{g}')
			return self
		def get_weight_dict(self):
			return self.weight
		def set_edge_weight(self, e, w):
			self.weight[sorted2(e)] = w
			return self
	if "oper":
		def add_node(self, n):
			assert not self.has_node(n), f'{n}'
			nx.Graph.add_node(self, n)
		def add_nodes(self, nodes):
			for n in nodes:
				self.add_node(n)
		#
		def add_wedge(self, wedge):
			e, w = wedge
			n1, n2 = e
			if n1 not in self.nodes: self.add_node(n1)
			if n2 not in self.nodes: self.add_node(n2)
			return self.connectw(n1, n2, w)
		def add_edge_weight(self, e, w):
			e = sorted2(e)
			self.weight[e] = w
			return self.add_edge(e)
		
		def add_edges(self, edges):
			for e in edges:
				self.add_edge(e)
			return self
		def add_wedges(self, wedges):
			for wedge in wedges:
				self.add_wedge(wedge)
		def add_edges_weight(self, edges, weight:dict):
			for e in edges:
				self.add_edge_weight(e, weight[e])
		#
		def del_node(self, n):
			nx.Graph.remove_node(self, n)
			return self
		def del_node_clear(self, n):
			for adj in list(self.adj[n]):
				self.disconnect(n, adj)
			return self.del_node(n)
		def del_nodes_clear(self, nodes):
			for n in nodes:
				self.del_node_clear(n)
			return self
		#
		def connect(self, n1, n2):
			e = n1, n2 = sorted_nn(n1, n2)
			assert self.has_node(n1), f'{n1} {self.nodes}'
			assert self.has_node(n2), f'{n2} {self.nodes}'
			nx.Graph.add_edge(self, n1, n2)
			self._std_edges.add(e)
			return self
		def disconnect(self, n1, n2):
			e = n1, n2 = sorted_nn(n1, n2)
			self.remove_edge(n1, n2)
			self._std_edges.remove(e)
			if e in self.weight:
				del self.weight[e]
		def connectw(self, n1, n2, w):
			e = n1, n2 = sorted_nn(n1, n2)
			self.connect(n1, n2)
			self.weight[e] = w
			return self
		def connectmw(self, wedges):
			for (n1, n2), w in wedges:
				self.connectw(n1, n2, w)
			return self
		def connectm(self, edges):
			for n1, n2 in edges:
				self.connect(n1, n2)
			return self
		# temp
		def set_wedge_temp(self, wedge):
			e, w = wedge
			n1, n2 = e = sorted2(e)
			if self.has_edge(e):
				w_ = self.weight[e]
				self.set_edge_weight(e, w)
				def goback():
					self.set_edge_weight(e, w_)
					return self
			else:
				self.connectw(n1, n2, w)
				def goback():
					self.disconnect(n1, n2)
					return self
			return goback
				
		def set_wedges_temp(self, wedges):
			"""
				覆盖原有的值
				"""
			gobacks = []
			for wedge in wedges:
				back = self.set_wedge_temp(wedge)
				gobacks.append(back)
			#
			def goback():
				for back in reversed(gobacks):
					back()
				return
			return goback
	if "fit":
		@classmethod
		def get_appropriate_font_size(self, node_count): ##
			return None
			# if node_count == None: node_count = len(self.nodes)
			if node_count == 0: return 10
			r = math.sqrt(2000 / node_count)
			if r < 5: return 5
			if r > 10: return 10
			return r
		@classmethod
		def appropriate_node_size(self, count):
			#return 3
			r = base.fit_size(count, space=1/myplt.cap(), space_dim=2, unit_dim=2, floor=3, ceil=300, floor_n=1e3)
			return r
		@classmethod
		def appropriate_edge_width(self, count, *, is_adj):
			#return 3
			#return 1
			if is_adj: r = base.fit_size(count, space=1/myplt.cap(), space_dim=2, used_dim=2, unit_dim=1, floor=0.5, ceil=4, floor_n=1e6)
			else: r = base.fit_size(count, space=1/myplt.cap(), space_dim=2, used_dim=1, unit_dim=1, floor=0.5, ceil=1, floor_n=5000)
			return r
		##algorithmn
		# sub

	def nodeSubs(self, *, isolated=True) -> ' [nodes]':
		"""
			isolated<bool>: 包含没有任何边相连的孤立点
			"""
		if isolated:
			subs = list(nx.connected_components(self))
			isolateds = my.set.differencem(set(self.nodes), subs)
			return subs + [ {iso} for iso in isolateds ]
		else:
			return list(nx.connected_components(self))
	connected_components = nodeSubs
	def group_nodes_by_connectivity(self, nodes):
		"""
			将在self中连通的节点分在一组
			"""
		subs = self.nodeSubs()
		groups = my.set.group_by_sets(nodes, subs)
		return groups
	def sub_full_graph_from_nodes(self, nodes, *, weight=None, pos=Pass):
		"""
			返回nodes的fullgraph
			默认不保存weight
			"""
		if pos == Pass: pos = self
		edges = my.comb.comb(nodes, 2)
		g = Graph.from_edges(edges, pos=pos, weight=weight)
		return g
	def seperate_sub_full_graph_from_nodes(self, nodes, *, weight=None, pos=Pass):
		"""
			根据self的连通部分, 返回nodes的几个分立的完全图
			返回nodes的fullgraph
			默认不保存weight
			"""
		if pos == Pass: pos = self
		groups = self.group_nodes_by_connectivity(nodes)
		edges = []
		for group in groups:
			edges += my.comb.comb(group, 2, typ=tuple)
		g = Graph.from_edges(edges, pos=pos, weight=weight)
		return g
	if "path":
		def find_path(self, n1, n2):
			#assert n1 != n2, f'{n1}'
			if n1 == n2: return [n1]
			for path in nx.all_simple_paths(self, n1, n2):
				return path

			# debug
			#d(self.nodes)
			#d(self.edges)
			subs = list(self.subs())
			print(f'path not found {n1} {n2}')
			# has_node
			if n1 not in self.nodes:
				print(f'{n1} not in nodes')
				# print(f'nodes: {list(self.nodes)}')
			if n2 not in self.nodes:
				print(f'{n2} not in nodes')
				# print(f'nodes: {list(self.nodes)}')
			print(f'{len(subs)} subtree found')
			myplt.new_figure(window_title='debug')
			self.draw()
			axis = myplt.axis()
			for sub in subs:
				sub.draw(axis=axis)
			myplt.show()
			raise Exception(
				f'\npath not found {n1} {n2}\n'
				f'{len(subs)} subtree found\n'
				)
		def find_path_stdedges(self, n1, n2):
			nodes = self.find_path(n1, n2)
			r = []
			for i in range(len(nodes)-1):
				r.append( sorted_nn(nodes[i], nodes[i+1] ))
			return r
		def find_path_maxEdgeVal(self, n1, n2, *, weight=None):
			if weight == None: weight = self.weight
			nodes = self.find_path(n1, n2)
			assert len(nodes) >= 2
			max_v = -my.inf
			for i in range(len(nodes)-1):
				e = sorted_nn(nodes[i], nodes[i+1])
				w = weight[e]
				if w > max_v:
					max_v = w
			return max_v

		def has_path(self, n1, n2):
			return nx.has_path(self, n1, n2)
	if "nx":
		def weighted_nx_graph(self, weight:dict=None):
			if weight == None: weight = self.get_weight_dict()
			g = nx.Graph()
			for e in self.std_edges():
				g.add_edge(*e, weight=weight[e])
			return g
	if "mst":
		def mst(self, *, weight:dict=None, fail=Pass) -> '<Graph> weighted':
			"""
				fail:
					Pass: assert span
				"""
			if fail is Pass:
				assert not de.check_mst_span or self.is_span()
			else:
				if not self.is_span():
					return fail
			if weight == None: 
				weight = self.weight
			nx_g = self.weighted_nx_graph(weight)
			nx_mst = nx.minimum_spanning_tree(nx_g)
			mst = Graph.from_edges_weight(edges_to_std(nx_mst.edges), weight)
			return mst
		def mst_len(self, *gs, fail=Pass, **ks):
			if fail is Pass:
				# assert self.check_span()
				return self.mst(**ks).len()
			else:
				if self.is_span():
					return self.mst(**ks).len()
				else:
					return fail

			return self.mst(*gs, **ks).len()			
		# group
		def group_graph(self, groups):
			"""
				只考虑group包含的点
				默认一个group内有0边连接
				返回的图节点是group对象index
				"""
			if not isinstance(groups, list): groups = list(groups)
			weight = {}
			for i in range(len(groups)):
				g1 = groups[i]
				for j in range(i+1, len(groups)):
					g2 = groups[j]
					#
					w_min = my.inf
					for n1 in g1:
						for n2 in g2:
							e = sorted_nn(n1 ,n2)
							if e not in self._std_edges: continue
							w = self.weight[e]
							if w < w_min: w_min = w
					if w_min is not my.inf:
						weight[ (i, j) ] = w_min
			# group_graph
			group_graph = Graph.from_nodes_weight(range(len(groups)), weight)
			return group_graph
		def group_mst(self, groups, **ks):
			group_graph = self.group_graph(groups)
			mst = group_graph.mst(**ks)
			return mst
		def group_mst_len(self, groups, fail=Pass, **ks):
			"""
				只考虑group包含的点
				默认一个group内有0边连接
				返回的图节点是group对象index
				"""
			group_graph = self.group_graph(groups)
			return group_graph.mst_len(fail=fail, **ks)

	def full_edges(nodes, *, weight=None):
		if weight == None:
			edges = []
			for i in range(len(nodes)):
				for j in range(i+1, len(nodes)):
					n1 = nodes[i]
					n2 = nodes[j]
					edges.append( (n1, n2) )
			return edges
		elif callable(weight): 
			wedges = []
			for i in range(len(nodes)):
				for j in range(i+1, len(nodes)):
					n1 = nodes[i]
					n2 = nodes[j]
					wedges.append( (n1, n2, weight((n1, n2))) )
			return wedges
		else: raise Exception(f'{weight}')		
	def full_graph(nodes, *, weight=None, pos=None):
		edges = my.comb.comb(nodes, 2, typ=tuple)
		g = Graph(nodes=nodes, edges=edges, weight=weight, pos=pos)
		return g
	full_graph_from_nodes = full_graph
	if "check":
		def check_weighted(self):
			if isinstance(self.weight, dict):
				std_edges = self.std_edges()
				unweighted = [e for e in std_edges if e not in self.weight]
				l_all = len(std_edges)
				l_un = len(unweighted)
				l_w = l_all - l_un
				l_wdict = len(self.weight)
				flag = l_w == l_all == l_wdict
				# print
				print(f'{l_all} edges, {l_w} weighted, {l_un} unweighted, {l_wdict} in self.weight')
				if flag:
					print(f'check succeed')
				else:
					print(f'check fail')
					print(f'edges: {mystr(std_edges)}')
					print(f'unweighted: {mystr(unweighted)}')
					print(f'self.weight: {mystr(self.weight)}')
			
			else:
				flag = True
				print(f'self.weight: {mystr(self.weight)}')
			return flag
		def check_span(self, nodes=set()):
			self = self.copy(weight=None, pos=None).update_nodes(nodes)
			r = self.is_span()
			if not r:
				subs = self.nodeSubs()
				covered = my.set.unionm(subs)
				uncovered = set(self.nodes).difference(covered)
				if not empty(uncovered):
					print(f'{len(uncovered)} nodes unspaned, {uncovered}')
				if len(subs) > 1:
					print(f'has {len(subs)} connected subs')
				self.show(title='check span')
			return r
	if "bottle-neck":
		def get_bottle_neck(self, weight:dict=None, *, mode='v') -> '{e:neck_e}':
			"""
				arg:
					mode: e | odd_e | v
				计算图中所有边的瓶颈值
				算法：
					最小生成树，路径最大值
				"""
			
			if weight == None: weight = self.weight
			mst = self.mst(weight=weight)
			return self.get_bottle_neck_from_mst(mst, weight, mode=mode)
		def get_bottle_neck_from_mst(self, mst, weight:dict=None, *, mode='v') -> '{e:neck_e}':
			"""
				arg:
					mode: e | odd_e | v
				计算图中所有边的瓶颈值
				算法：
					最小生成树，路径最大值
				要求：weight覆盖mst
				"""
			if weight == None: weight = mst.get_weight_dict()
			r = {}
			for e in self.std_edges():
				a, b = e
				path = mst.find_path_stdedges(a, b)
				match mode:
					case 'odd_e':
						neck = Edge2Comparer.max_edges(path, weight)
					case 'v':
						neck = max( weight[edge] for edge in path )
					case _:
						raise Exception(f'{mode}')
				r[e] = neck
			return r
		def R_getter(self, *, weight=None):
			"""
				要求:
					self连通
				get(set) -> r
				"""
			assert self.check_span()
			if weight == None: weight = self.weight
			mst = self.mst(weight=weight)
			mst_len = mst.len()
			map = DictOfSet()
			def get(e):
				e = set(e)
				if e in map: return map[e]
				# cacu
				if len(e) == 2:
					v = mst.find_path_maxEdgeVal(*e, weight=weight)
				else:
					v = self.get_R(e, mst_len=mst_len)
					map[e] = v
				map[e] = v
				return v
				
			return get
		def get_R(self, nodes, *, mst_len):
			wedges = [ (e, 0) for e in my.misc.get_arrow_by_nodes(list(nodes)) ]
			goback = self.set_wedges_temp( wedges )
			len_ = self.mst_len()
			goback()
			r = mst_len - len_
			return r
	class test:
		def pruned_graph(k=10, seed=0):
			import rsmt2
			hg = rsmt2.pruned_hg_by_key( (k,seed) )
			g = hg.subngraph()
			return g
	if "test":
		def test_R(self):
			"""
				r0, r1, r2, ...
				"""
			size = 6
			get_r = self.R_getter()
			count = 0
			count_fail = 0
			for nodes in my.comb(self.nodes, size, typ=set):
				count += 1
				edges = my.comb(nodes, 2)
				r0 = get_r(nodes)
				rs = [ get_r(e) for e in edges ]
				print(f'{r0} {mystr(rs)}')
				if count_fail > 0: print(f'fail {count_fail}')
				# r0 = mst(r)
				g = Graph.from_edges(edges, weight=get_r)
				mst_r = g.mst_len()
				flag = r0 == mst_r
				if flag: pass
				else:
					count_fail += 1
					d(flag)
			# summary
			if count_fail == 0:
				print(f'succeed {count}')
			else:
				print(f'fail {count_fail} / {count}')
	if "build":
		@classmethod
		def from_edges(cls, edges, **ks):
			g = cls(**ks)
			g.add_edges(edges)
			return g
		@classmethod
		def from_edges_weight(cls, edges, weight, **ks):
			g = cls(**ks)
			g.add_edges_weight(edges, weight)
			return g
		@classmethod
		def from_wedges(cls, wedges, **ks):
			g = cls(**ks)
			g.add_wedges(wedges)
			return g
		@classmethod
		def from_nodes_weight(cls, nodes, weight):
			r = cls(nodes=nodes)
			for e, w in weight.items():
				r.connectw(*e, w)
			return r
		def copy(self, *, weight=None, pos=None):
			if weight == None: weight= self
			if pos == None: pos = self
			r = type(self)(nodes=self.nodes, edges=self.edges, weight=weight, pos=pos)
			return r
class PosGraphBase(Graph):
	# def draw(self, *, hl=set(), pos=None, **ks):
	# 	# if pos == None: pos = {node:node for node in self.nodes}
	# 	# hl
	# 	hl_edges = set()
	# 	hl_nodes = set()
	# 	for ele in hl:
	# 		if isinstance(ele[0], tuple):
	# 			ele = tuple(sorted(ele))
	# 			hl_edges.add(ele)
	# 		else:
	# 			hl_nodes.add(ele)
	# 	#
	# 	return super().draw(hl_nodes=hl_nodes, hl_edges=hl_edges, **ks)

	def get_pos(self, *, nodes=None, edges=None, pos=None) -> dict:
		"""
			None -> 无
			"""
		assert nodes is not None or edges is not None
		pos = {}
		if nodes is not None:
			for n in nodes:
				pos[n] = n
		if edges is not None:
			for e in edges:
				for n in e:
					pos[n] = n
		return pos
	flag_pos_from_nodes_edges = True
class PosGraph():
	@dynamicmethod
	def get_pos(*gs, **ks) -> dict:
		return PosGraphBase.get_pos(*gs, **ks)
class DiGraph(GraphBase):
	"""
		attr
			nodes<set>
			edges<set>
			_pouts<dict> [pin] -> { pouts }
			_pins<dict> [pout] -> { pins }
		"""
	def __init__(self, di_graph=None, *, nodes=[], edges=[]):
		if di_graph is None:
			self.add_nodes(nodes)
			self.connectm(edges)
		elif isinstance(di_graph, DiGraph):
			self.copy_from(di_graph)
		else: raise Exception(f'{di_graph}')
	if "node":
		def add_node(self, n):
			assert n not in self.nodes
			self.nodes.add(n)
			self._pins[n] = set()
			self._pouts[n] = set()
		def del_node(self, n):
			self.nodes.remove(n)
			assert len(self._pins[n]) == 0
			assert len(self._pouts[n]) == 0
			del self._pins[n]
			del self._pouts[n]
	if "edges":
		def connect_nn(self, n1, n2):
			self._pouts[n1] = n2
			self._pints[n2] = n1

	

if "hyper-smt":
	class OddWeight:
		"""
			说明
				li: set无重复
			attr
				_val _li(sortedSet)
			比较
				按li前面的大小比较
				不够长的补最小的
			"""
		_li_type = SortedList # performance
		def __init__(self, val, li):
			self._val = val
			self._li = self._li_type(li)
		def __str__(self):
			return f'{self._val}({len(self._li)})'
		# compare
		def __lt__(w1, w2):
			if isinstance(w2, int) and w2 == 0: return w1._val < 0
			if w1._val == w2._val:
				return my.list.compare_lt(w1._li, w2._li)
			else:
				return w1._val < w2._val
		def __gt__(w1, w2):
			if isinstance(w2, int) and w2 == 0: return w1._val > 0
			if w1._val == w2._val:
				return my.list.compare_gt(w1._li, w2._li)
			else:
				return w1._val > w2._val
		def __ge__(w1, w2):
			return not w1 < w2
		def __le__(w1, w2):
			return not w1 > w2
			
		def __eq__(w1, w2):
			# assert isinstance(w2, OddWeight) or isinstance(w2, int) and w2 == 0 
			if isinstance(w2, OddWeight):
				if w1._val != w2._val: return False
				if w1._li != w2._li: return False
				return True
			elif isinstance(w2, int):
				assert w2 == 0
				return False
			else:
				raise Exception(f'{w2, type(w2)}')
			raise
				
		# oper`
		def __isub__(self, w):
			if isinstance(w, int) and w == 0: return self
			self._val -= w._val
			for a in w._li:
				self._li.remove(a)
			return self
		def __iadd__(self, w):
			if isinstance(w, int) and w == 0: return self
			self._val += w._val
			for a in w._li:
				self._li.add(a)
			return self
		def __radd__(self, w):
			if w == 0:
				return self.copy()
			else:
				raise
		def __add__(self, w):
			if isinstance(w, int) and w == 0: return self.copy()
			val = self._val + w._val
			li = self._li + w._li
			return OddWeight.build(val, li)
		def __sub__(self, w):
			if isinstance(w, int) and w == 0: return self.copy()
			val = self._val - w._val
			li = self._li.copy()
			for a in w._li:
				li.remove(a)
			return OddWeight.build(val, li)
		
		# build
		def build(val, li): # no li.copy()
			r = object.__new__(OddWeight)
			r._val = val
			r._li = li
			return r
		def copy(self):
			r = OddWeight(self._val, self._li)
			return r
			
	MstGroupMap = my.GroupMap
	class Model:
		"""
			attr
				states: <set>igroups
				field_set: <set>iedges
				field: <list>sorted iedges
				weight<dict>: i:w
				nodes, anodes, inodes, used_nodes, unused_nodes, edges()
			graph-attr
				a_oe_map
				anodes
				inodes
				onodes

			Lmodel:	{ Lstate }
			Lstate: hash(state)
			更新反应
				assert1: 删除多余边，合并节点
				assert0: 删除边
			"""
		def __init__(self, *, states:'set'=None, field:'iter', debug=0, verbose_text=0, verbose_pic=0,  solver):
			"""
				"""
			self.debug = debug
			self.verbose_text = verbose_text
			self.verbose_pic = verbose_pic
			self.solver = solver
			self._print = solver._print
			self._show = solver._show
			self.net = solver.model_net
			self.graph = solver.hg
			self.i_e_map = solver.i_e_map
			self.e_i_map = solver.e_i_map
			self.iweight = solver.iweight
			self.no_cycle = solver.no_cycle
			# variable
			# if field is not None:
			self.set_field(field)
			self.inter_info = {}
			if states is not None:
				self.set_states(states)
			#
		def __lt__(m1, m2):
			return id(m1) < id(m2)
		# update
		def do_del_state(self, state):
			for e in state.iedges:
				self.count_map[e] -= 1
				assert self.count_map[e] >= 0 ###
			self.states.remove(state)
			# self._states.remove(state)

		
		def update(self):
			"""
				说明: 新建的model
					
				算法
					检查所有邻边, 删除所有不匹配的sub节点(不匹配: 只有其中一方sub_states_map有)
					为匹配的邻边设置count
				"""
			del_states1 = set() # 有可能重复
			del_states2 = [] # (m, state)
			#
			for m2, inter_info in self.inter_info.items():
				state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = inter_info
				for sub in list(sub_states_map1):
					if sub not in sub_states_map2: # 只与1有联系
						# 删除与1的联系
						states1 = sub_states_map1.pop(sub)
						for state1 in states1: # 孤立sub相连的每个state
							# self.do_del_state(state1)
							del state_sub_map1[state1]
							del_states1.add(state1)
				counter_combine.count = sum( len(sub_states_map1[sub]) * len(sub_states_map2[sub]) for sub in sub_states_map1 )
				for sub in list(sub_states_map2):
					if sub not in sub_states_map1: # 只与2有联系
						states2 = sub_states_map2.pop(sub)
						for state2 in states2:
							# m2.do_del_state(state2)
							del state_sub_map2[state2]
							del_states2.append((m2, state2))
			# 
			for state in del_states1:
				# if state not in self.states: continue # 循环
				self.del_state_rcr(state)
			for m, state in del_states2:
				# if state not in m.states: continue # 循环
				m.del_state_rcr(state)
			self.net.check_list.add(self)
			return self
		def del_sub_directed_rcr(m1, m2, sub, *, check_combine=True):
			"""
				前提:
					m1的联系断了
				操作
					删除与m2的联系
					触发m2相关states的删除
				触发相连state的删除
				uomk
				"""
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
			#
			assert sub not in sub_states_map1
			# states1 = sub_states_map1.pop(sub)
			if sub not in sub_states_map2: return
			states2 = sub_states_map2.pop(sub)
			# states1 = sub_states_map1[sub]
			# states2 = sub_states_map2[sub]
			#
			# counter_combine.count -= len(states1) * len(states2)
			#
			# for state1 in states1:
			# 	m1.del_state_rcr(state1)
			#2
			del_states = []
			for state2 in states2:
				state_sub_map2.pop(state2)
				del_states.append(state2)

			#
			for state2 in del_states:
				m2.del_state_rcr(state2)
			return m1
		def del_state_rcr(self, state):
			"""
				删除自己和周围sub的双向联系, 若sub归零触发该sub的删除
				当某个方向没有sub时, 跳过(如刚开始的update, 或者中途sub的触发)
				操作

				"""
			#
			# assert state in self.states ##?
			if state not in self.states: return
			self.do_del_state(state)
			#
			del_subs = []
			for m2, inter_info in self.inter_info.items():
				state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = inter_info
				if state not in state_sub_map1: # 仅限首次update ??
					continue
				sub = state_sub_map1.pop(state)
				con_states1 = sub_states_map1[sub]
				flag_rcr = sub not in sub_states_map2 # 另一边已经没了
				if not flag_rcr: 
					counter_combine.count -= len( sub_states_map2[sub] )
				assert counter_combine.count >= 0
				if len(con_states1) == 1: # 触发sub删除
					# if flag_rcr: 
					# 	sub_states_map1.pop(sub)
					# else:
					del_subs.append((m2, sub))
					sub_states_map1.pop(sub)
				else:
					con_states1.remove(state)
			# del-subs
			for m2, sub in del_subs:
				self.del_sub_directed_rcr(m2, sub)
			self.net.check_list.add(self)
			return self

		def update_by(self, model, *, field) -> '<bool>modified':
			"""
				前提: 双方没有建立inter_info, self没有与关联model建立inter_info, 
				利用model更新自己, 不反向进行
				若更新成功, 加入checkList
				pc:
					提取model在inter上的子状态
					比对自己的所有状态
				inter: 
				"""
			assert model not in self.inter_info
			assert model.field_set.issubset(self.field_set)
			mf = False
			sub_Lmodel = model.sub_Lmodel(field) # set
			del_states = []
			# debug
			assert not self.field_set.issubset(model.field_set)
			if 0 and self.net.verbose_text >= 5:
				ori_debug_inter = self.get_inter_field_map_debug(model)
			#
			for state in self.states:
				sub_hash = self.sub_hash(state, field)
				if sub_hash in sub_Lmodel: pass
				else:
					mf = True
					del_states.append(state)
			#
			for state in del_states: ##? 循环
				self.do_del_state(state) # 不连续触发
				1
			# self.check_possible()
			# debug
			if 0 and self.net.verbose_text >= 5 and mf:
				summary1, map1, bound_combine1 = ori_debug_inter
				summary2, map2, bound_combine2 = debug_inter = self.get_inter_field_map_debug(model)
				#
				# print(f'before: {mystr(summary1)} {mystr(map1)}')
				# print(f'after: {mystr(summary2)} {mystr(map2)}')
				overlap = [ len(self.field), len(field), len(model.field) ]
				print(f'update-edge[{mf}]: {overlap}')
				print(f'    {mystr(summary1)} {bound_combine1} -> {mystr(summary2)} {bound_combine2}')
			# return
			if mf: self.net.check_list.add(self)
			return mf
		# draw
		def draw(self, **ks):
			# assert self.check_count_map()
			self.graph.draw(hl_edges=self.edges(), hl_nodes=self.anodes, **ks)
			self.graph.draw(hl_edges=self.assert0_edges(), title='assert0')
			self.graph.draw(hl_edges=self.assert1_edges(), title='assert1')
		# map
		def set_map_filter0(self, e, items):
			"""
				说明
					True/False: 不需要考虑内部的, 和完全在外部的
				pc:
					True
						完全外部: 无视
						内部: 删除
						外部相邻: 
				"""
			if items == True:
				pass
			elif items == False:
				pass
			else:
				assert not isinstance(items, set)
				assert len(items) == 1 and items[0][1] == 1
				e_ = items[0][0]
				self.set_rmap( (e, 1), e_ )
			return self
		def set_map_map(self, e, items, *, false_exist=None):
			"""
				false_exist:
					可能出现false存在的情况:
						与assert1形成循环 ( assert1 在field外）
						map重叠时都有(不论权重)
					,需要false_exist=True
				背景
					e可能是临时的(assert1的邻边)
				arg:
					用ei代替i
				说明: 只映射, 在之后统一过滤
				分析-重叠:
					只需考虑重叠前后两条边权相同时
					选择其中一条边删除, 若状态包含这条边, 删除该状态(items==False)
				操作
					e在内部
						1/0: 删除
						e_: 修改
					e在边界, 外部
						无视
				过滤flag
					1: 不需要 (循环由e_判断)
					0: 外边界需要
					e_: 内边界需要
				"""
			#
			i_e_map = self.i_e_map
			e_i_map = self.e_i_map
			i = self.solver.tmp_e_i_map[e]

			self.net.map_update_set.add(self)
			if i not in self.field_set:
				return 
			else:
			#
				if items == True:
					self.field_set.remove(i)
					self.field.remove(i)
					for state in self.states:
						# assert state.check_oddWeight()
						state.remove_iedge(i)	
				elif items == False:
					self.field_set.remove(i)
					self.field.remove(i)
					if false_exist == True:
						del_states = []
						for state in self.states:
							if i in state.iedges:
								del_states.append(state)
						for s in del_states:
							# 会破坏model之间的关系
							self.do_del_state(s)
					elif false_exist == False:
						if de.debug and 1:
							for state in self.states:
								assert i not in state.iedges, (i, state.iedges)
					else: raise Exception(f'false_exist={false_exist}')
								
					if 0:
						for state in self.states:
							# assert state.check_oddWeight()
							if i in state.iedges:
								# raise
								d(i)
								d(state.iedges)
								d( self.anodes )
								# d(len(self.graph.edges))
								# d(state.is_possible())
								
								raise
							# .map导致的False?
							# if i in state.iedges:
							# 	# state.remove_iedge(i)
							# 	state.weight = my.inf
							# 	state.iedges.remove(i)
							1
				else:
					assert not isinstance(items, set)
					assert len(items) == 1 and items[0][1] == 1
					e_ = items[0][0]
					# for state in self.states:
					# 	if i in state.iedges:
					# 		state.remove_iedge(i)
					# 		state.add_iedge(i_)
			return self
		def updated(self) -> 'new Model':
			"""
				背景
					在map之后
					field已更新
				说明
					model
						更新anodes,
					state:
						检测内部循环, 孤立并删除
						更新groupMap
				"""
			r = Model(field=self.field, solver=self.solver)
			# states
			ghash_weight_map = {}
			ghash_states_map = {}

			for s in self.states:
				# if s.match_trace:
				# 	flag = s.try_update(model=r)
				# 	s.draw()
				# 	assert flag
				# 	self.draw()
				# 	1
				res = s.try_update(model=r)
				if res == False: pass
				else: 
					ghash = s.group.hash()
					w = s.weight
					if ghash not in ghash_weight_map:
						ghash_weight_map[ghash] = w
						ghash_states_map[ghash] = {s}
					else:
						w_ = ghash_weight_map[ghash]
						if w < w_:
							ghash_weight_map[ghash] = w
							ghash_states_map[ghash] = {s}
							# d(w, w_)
							# raise
						elif w > w_:
							# d(w, w_)
							# raise
							continue
						else:
							ghash_states_map[ghash].add(s)
			states = my.set.unionm(ghash_states_map.values())
			#
			r.set_states(states)
			# d( len(self.states) - len(states) )
			if 0:
				if not self.is_possible():
					1
					dels = self.states.difference(states)
					for state in dels:
						if state.is_possible():


							1
							raise
					raise
			return r
		# info
		def var(self):
			return len(self.states)
		def size(self):
			return len(self.field)
		def assertion_iedge(self, e) -> '0 1 2':
			count = self.count_map[e]
			assert not empty(self.states)
			if count == 0: return 0
			elif count == len(self.states): return 1
			else: return 2
		def iedges_list(self):
			return [ ig.iedges for ig in self.states ]
		def edges(self):
			return [ self.i_e_map[i] for i in self.field ]
			return self._edges
		def relation(self, m):
			field = self.field_set
			f = m.field_set
			return my.set.relation(field, f)
		def get_anodes(self):
			return self.graph.get_anodes_by_edges(self.edges())
			
		#
		def assert0_edges(self):
			return [ self.i_e_map[i] for i in self.field if self.assertion_iedge(i) == 0 ]
		def assert1_edges(self):
			return [ self.i_e_map[i] for i in self.field if self.assertion_iedge(i) == 1 ]
		# judge
		def has_iedge1(self, i):
			"""
				存在一个state包含i

				"""
			for s in self.states:
				if i in s.iedges: return True
			return False
		# debug
		def is_igroup_possible(self, igroup, **ks):
			return igroup.is_possible(edges_used=self.edges(), i_e_map=self.net.i_e_map)
		def get_inter_field_map(self, model, *, field=None) -> '{ istate: [states1, states2] }':
			r = defaultdict(lambda: ([],[]))
			if field == None: field = sorted(self.field_set & model.field_set)
			for state in self.states:
				sub_hash = self.sub_hash(state, field)
				r[sub_hash][0].append(state)
			for state in model.states:
				sub_hash = model.sub_hash(state, field)
				r[sub_hash][1].append(state)
			return r
		def get_inter_field_map_debug(self, model) -> '[self inter model] print_count_map bound_combine':
			map = self.get_inter_field_map(model)
			print_list = [ sorted2( (len(l1), len(l2)) ) for l1, l2 in map.values() ]
			print_count_map = { tu : print_list.count(tu) for tu in print_list }
			#
			summary = [ len(self.states), len(map), len(model.states) ]
			bound_combine = sum( size1 * size2 * count for (size1, size2), count in print_count_map.items() )
			return summary, print_count_map, bound_combine
		def debug_state(self, s):
			for m2, inter_info in self.inter_info.items():
				state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = inter_info
				sub = state_sub_map1[s]
				states2 = sub_states_map2[sub]
				d(sub_len2=len(states2))
		def get_summary_complex(self, m2) -> 'states1, sub, states2(len)':
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = self.inter_info[m2]
			l1 = len(self.states)
			l2 = len(m2.states)
			l_inter = len(sub_states_map1)
			return l1, l_inter, l2
		def guess_combine_count(self, m2):
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = self.inter_info[m2]
			return counter_combine.count
		def debug_info(self):
			info = f'size={self.size()} var={self.var()}'
			print(f'<Model> {info}')
			self.draw(title=info)
		def debug_draw_states(self):
			# hg = self.graph
			# HyperGraph.prepare_draw()
			for i, s in enumerate(self.states):
				s.draw(title=f'<{s.weight}> state[{i}]')
		# trace
		def check_trace(self):
			trace = self.solver.trace
			return self.match_graph(trace)
		def match_graph(self, trace):
			iedges = self.get_sub_iedges(trace)
			for s in self.states:
				if iedges == s.iedges: return s
			return False
		def get_sub_iedges(self, graph) -> set:
			"""
				graph在model内的状态
				"""
			r = set()
			for i in self.field:
				e = self.i_e_map[i]
				if graph.has_edge(e): r.add(i)
			return r
		# misc
		def asserted_edges(self):
			return {ei for ei in self.field if self.assertion_iedge(ei) != 2}
		def setup_inter_info(m1, m2, field):
			assert not my.set.one_contain_another(m1.field_set, m2.field_set)
			state_sub_map1 = {}
			sub_states_map1 = {} ###
			state_sub_map2 = {}
			sub_states_map2 = {}
			for state in m1.states:
				sub_hash = m1.sub_hash(state, field)
				state_sub_map1[state] = sub_hash
				if sub_hash not in sub_states_map1:
					sub_states_map1[sub_hash] = set()
				sub_states_map1[sub_hash].add(state)
			for state in m2.states:
				sub_hash = m2.sub_hash(state, field)
				state_sub_map2[state] = sub_hash
				if sub_hash not in sub_states_map2:
					sub_states_map2[sub_hash] = set()
				sub_states_map2[sub_hash].add(state)
			#
			counter_combine = Name()
			#
		
			inter_info1 = state_sub_map1, sub_states_map1
			inter_info2 = state_sub_map2, sub_states_map2
			m1.inter_info[m2] = *inter_info1, *inter_info2, counter_combine
			m2.inter_info[m1] = *inter_info2, *inter_info1, counter_combine
			# return inter_info1, inter_info2

		def set_field(self, field:'iter'):
			self.field_set = set(field)
			self.field = sorted(self.field_set)
			# node
			self._edges = [ self.i_e_map[i] for i in self.field ]
			self.nodes = set(self.graph.nodes)
			self.anodes = self.graph.get_anodes_by_edges(self.edges())
			self.used_nodes = my.set.unionm(self.edges())
			self.inodes = self.used_nodes.difference(self.anodes)
			self.unused_nodes = self.nodes.difference(self.used_nodes)
			return self
		def set_field_by_edges(self, edges):
			field_set = { self.e_i_map[e] for e in edges }
			return self.set_field(field_set)
		def set_states(self, states):
			"""
				要求: states无主, 自己空
				"""
			assert isinstance(states, set)
			assert isinstance(my.pick(states), Igroup), states
			#
			self.states = states
			assert empty(self.inter_info), len(self.inter_info)
			# count-map
			self.count_map = { e:0 for e in self.field }
			for state in states:
				# assert state.check_oddWeight()
				for n in state.iedges:
					self.count_map[n] += 1
		# build
		def empty_model(*, solver):
			r = Model(field=[], solver=solver)
			states = { Igroup(weight=0, model=r) }
			r.set_states(states)
			return r
		# check
		def check_possible(self):
			if not de.check_possible: return True
			igroups = self.states
			edges_used = [ self.net.i_e_map[i] for i in self.field]
			flag = Igroup.is_possible_igroups(igroups, edges_used=edges_used, i_e_map=self.net.i_e_map, hg=self.net.solver.hg)
			assert flag
			return flag
		def is_possible(self, *, mst=None, mst_len=None):
			if not de.check_possible: return True
			igroups = self.states
			edges_used = [ self.net.i_e_map[i] for i in self.field]
			flag = Igroup.is_possible_igroups(igroups, edges_used=edges_used, i_e_map=self.net.i_e_map, 
				hg=self.net.solver.hg, mst=mst, mst_len=mst_len)
			return flag	# data-oper
		def check_count_map(self):
			map = { i:0 for i in self.field }
			for s in self.states:
				for i in s.iedges:
					map[i] += 1
			#
			flag = map == self.count_map
			return flag
		def check(self):
			"""
				count_map states anodes..
				"""
			if not self.check_count_map(): raise
			# states
			if not self.check_states(): raise
			if not self.anodes == self.get_anodes(): raise
			return True
		def check_states(self):
			"""
				不空
				set
				state:
					iedges符合field
					model is self
					group_map
					循环
					同型一样大
					不孤立
					weight
				"""
			graph = self.graph
			ghash_states_map = defaultdict(set)
			anodes = self.anodes
			if empty(self.states): raise
			if not isinstance(self.states, set): raise
			for s in self.states:
				if not s.iedges.issubset(self.field_set): raise
				if not s.model is self: raise
				if not s.graph() is graph: raise
				if not s.group.elements() == anodes: raise
				# assert s.anodes() == self.anodes
				group_map = graph.try_get_groupMap_by_edgesNodesAnodes_checkIsolateCycle(s.edges(), s.anodes())
				if not group_map == s.group: 
					d( my.hypergraph.checkIsolateCycle_byEdgesAnodes( s.edges(), s.anodes() ) )
					d(group_map)
					d(s.group)
					s.draw()
					myplt.show()
					raise
				# weight
				w_sum = sum( self.iweight[i] for i in s.iedges )
				if isinstance(s.weight, float): 
					if not abs(s.weight - w_sum) < 0.5: raise 
				else:
					if not w_sum == s.weight: raise
				ghash = group_map.hash()
				ghash_states_map[ghash].add(s)
			for states in ghash_states_map.values():
				if not my.all_equal( s.weight for s in states ):
					d(model=self)
					d( [s.iedges for s in states] )
					d( [s.group for s in states ] )
					raise Exception( [ s.weight for s in states ] )
			return True

		# operation-core
		def sub_Lmodel(self, field) -> '':
			"""
				
				"""
			assert isinstance(field, list)
			r = set()
			for state in self.states:
				Lstate = self.sub_hash(state, field)
				r.add(Lstate)
			return r
		def sub_hash(self, state:set, field:list) -> int:
			"""
				0b10001010011
				左边代表field前面的
				state {2 3 4}
				field [1 3 4 5 6]
				"""
			assert isinstance(field, list)
			# assert sorted(field), field
			iedges = state.iedges
			r = 0
			for i in field:
				if i in iedges:
					r = r * 2 + 1
				else:
					r = r * 2
			return r
		def walk_empty(model, start=None, order_mode=None, cut_mode=0, state_threshold=0):
			"""
				说明:
					对指定边集提取模式
				"""
			if "pre":
				i_e_map = model.i_e_map
				e_i_map = model.e_i_map
				self = hg = model.graph
				solver = model.solver
				debug = model.debug
				verbose_text = model.verbose_text
				verbose_pic = model.verbose_pic
				no_cycle = model.no_cycle
				best1 = solver.best1
				#
				pos = self.pos
				weight = self.get_weight_dict()
				nodes = sorted(self.nodes)
				all_edges = list(i_e_map.values()) # 不需要deepcopy， 因为edge不会改变
				edges_r = all_edges.copy()
				edges_used = []
				n_edges_map = {n: self.adj_n_e[n].copy() for n in self.nodes} # 未使用边
				igroups = set() # 幻组
				anodes = set() # 导点
				anodes_degree_n_n = my.SortedDict(key_v=lambda v:v) # 按未使用邻居点数排序，仅包含导点， 用于选点
				inodes = set()
				used_nodes = set() # 活跃 + 内点
				unused_nodes = set(nodes)
				new_nodes = set() # tmp
				new_anodes = set()
				min_igs = set()
				min_weight = my.inf
				assert cut_mode in range(3)
				# get_ru = hg.Ru_getter_depth(depth=0)
				# order, edges
				edge_order = list(self.get_edge_order(nodes, all_edges, mode=order_mode, start=start)) # [ e ..]
				iedge_order = [ e_i_map[e] for e in edge_order ]
				# debug
				count_equal_span = 0
				count_cut = 0
				list_count_state = []
				list_count_anode = []
				possible_msts = []
				b_connect_delta_map = defaultdict(lambda: 0)
				u_connect_delta_map = defaultdict(lambda: 0)
				count_assert_edges_list = []
				if debug and 0:
					mst_len = self.mst_len()
			if "methods":
				def react_new_anode(n):
					anodes.add(n)
					anodes_degree_n_n[n] = self.degree_n_n(n)
					new_anodes.add(n)
					# anodes_degree_n_e[n] = 
				def react_del_anode(n):
					anodes.remove(n)
					del anodes_degree_n_n[n]
				def react_new_node(n):
					new_nodes.add(n)
					used_nodes.add(n)
					unused_nodes.remove(n)
				def draw_edges_r():
					Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
					HyperGraph._draw_edges([edge_adding], pos=pos, edge_look=dict(color='orange'))
					Graph._draw_nodes(unused_nodes, pos=pos, look=dict(color='grey', alpha=0.5))
					myplt.title(f'i={len(igroups)} a={len(anodes)}')
				def draw_igroup(ig, **ks):
					ig.draw(inodes, anodes, used_nodes, pos, **ks)
					
				def debug_draw(i=debug):
					cond2 = 0
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
							ig.draw(inodes, anodes, used_nodes, pos)
					1
				def check_possible():
					if debug and 0:
						flag = any(ig.is_possible(edges_used, mst_len=mst_len) for ig in igroups_)
						flag |= min_ig != None and min_weight == mst_len
						assert flag, igroups
						return flag
				def get_model_fieldSet00() -> 'states, field_set':
					# model = []
					# for ig in igroups:
						# model.append(ig.state())
					#
					states = igroups
					field_set = { e_i_map[e] for e in edges_used }
					return states, field_set
			if "first":
				ig0 = Igroup(weight=0, model=model)
				if len(edge_order) != 0:
					n0 = my.pick(edge_order[0])
					ig0.add_anode(n0)
					react_new_node(n0)
					react_new_anode(n0)
				else:
					min_ig =ig0
				igroups.add(ig0)
			# main
			for ei in iedge_order: # e
				edge_adding = i_e_map[ei]
				new_inodes = set()
				new_anodes = set()
				new_nodes = set()
				degree_minus = len(edge_adding) - 1
				w = weight[edge_adding]
				edges_used.append(edge_adding)
				# 预处理节点 ( edge_adding =  new_anodes new_inodes non-change ) ( new_nodes = new_anodes + new_inodes部分 )
				# new_anodes: 新增加的anode <=> 新增的点去掉e后还有边
				# new_inodes: <=> 去掉e后一条边都不剩（所有新增inode）
				# new_nodes:  new_anodes + borni
				for n in edge_adding:
					if n not in anodes: # new-nodes
						react_new_node(n)
					n_edges_map[n].remove(edge_adding)
					if len(n_edges_map[n]) == 0: # new-inodes
						new_inodes.add(n)
						if n in anodes: # a -> i
							react_del_anode(n)
						else: # born i
							pass
					else:
						if n not in anodes: # new-anodes
							react_new_anode(n)
						else: # non-change
							pass
						anodes_degree_n_n[n] = len(my.set.unionm(n_edges_map[n])) - 1
						assert anodes_degree_n_n[n] >= 0
				# pre
				1
				inodes |= new_inodes
				igroups_ = set()
				flag_terminate = len(inodes) == len(nodes) # 绝对终止
				flag_terminate2 = len(used_nodes) == len(nodes) # 可能终止
				# 过滤 循环 孤立
				for ig in igroups:
					#
					not_add, add = ig.judge_add_e(edge_adding, new_anodes, new_inodes, flag_terminate2, no_cycle=no_cycle)
					if not_add:
						if add:
							ig1 = ig
							ig2 = ig.copy()
						else:
							ig1 = ig
					else:
						if add:
							ig2 = ig
						else: pass
					#
					if not_add:
						ig1.add_anodes(new_anodes)
						igroups_.add(ig1.not_add_e(new_inodes))
					if add:
						ig2.add_anodes(new_anodes) # 此时ig中包含除了borni的所有点
						ig2.add_e(edge_adding, ei, w, new_inodes)
						if flag_terminate2 and ig2.is_terminated(): # terminated
							if min_weight > ig2.weight: # min_weight放前面, inf优先
								min_igs = {ig2}
								min_weight = ig2.weight
							elif min_weight < ig2.weight: pass
							else:
								assert not best1
								min_igs.add(ig2)
							continue
						else:
							igroups_.add(ig2)
				edges_r.remove(edge_adding)
				assert not empty(igroups_) or len(min_igs) != 0
				#同型 过滤
				if cut_mode == 1:
					# equal
					raise
					count_cut_e = 0
					ghash_ig_map = {}
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_ig_map: ghash_ig_map[ghash] = ig
						else:
							count_cut_e += 1
							ig0 = ghash_ig_map[ghash]
							if ig.weight < ig0.weight:
								ghash_ig_map[ghash] = ig
					igroups_ = set(ghash_ig_map.values())
					# Lu
					"""
						考虑每一对I1 < I2 
						L: { F1 - F2 } 的变化值 ( 越大的组F值越小)

						ugraph: (越小越好)
							anodes之间的分部完全瓶颈图
						"""
					hg_remain = HyperGraph.from_edges_weight(edges_r, self.weight, pos=pos)
					ngraph = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_ru = hg_remain.seperate_Ru_getter_depth(depth=0)
					ugraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in ugraph.std_edges():
						ugraph.set_edge_weight(e1, get_ru(set(e1)))
					
					def get_Lu(g1, g2):
						"""
							g1欠缺的部分连接起来 需要的上限
							二元完全图: 二元瓶颈图(分立部分用inf边连接)
							? 孤立点, 分立部分
							算法: 上限完全图的部分mst
								根据g2的每个组和对应的g1的小组
									将g1的小组连接成大组的上限
								求和

							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							dta = ugraph.group_mst_len(subs, fail=None)
							if dta == None:
								return my.inf
								
							r += dta
						return r
					# Lb
					"""
						bgraph: (越大越好)
							anodes之间的分布完全断开瓶颈图
						"""
					
					ngraph2 = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_rb = hg_remain.seperate_Rb_getter_depth(depth=0, get_u=get_ru)
					bgraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in bgraph.std_edges():
						bgraph.set_edge_weight(e1, get_rb(set(e1)))
					def get_Lb(g1, g2):
						"""
							g2的部分断开到g1, 能得到的下限
							g2的各个组断开的得到的之和
							算法
								m组完全瓶颈图(取max), 取最大和m-2个最小的
								断开记为inf
							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							group_graph = bgraph.group_graph(subs)
							if not group_graph.is_span():
								return my.inf
							weights = sorted(group_graph.weight.values())
							dta = weights[-1] + sum(weights[:m-2])
								
							r += dta
						return r

					# filter
					"""
						对每个(g1,g2)对
							排除g1 is g2
							仅考虑g1 <= g2时 
						"""
					igroups_order = sorted(igroups_, key=lambda ig: ig.weight)
					# debug
					count_total = len(igroups_order) ** 2
					count_contain = 0
					count_u = count_b = 0
					#
					for ig1 in igroups_order: # ig1 <= ig2
						if ig1 not in igroups_: continue
						if ig1.weight >= min_weight:
							igroups_.remove(ig1)
							continue
						for ig2 in igroups_order:
							if ig2 not in igroups_: continue
							if ig1 is ig2: continue
							if ig2.cover_span(ig1): # cope
								count_contain += 1
								g1 = ig1.group
								g2 = ig2.group
								dw = ig2.weight - ig1.weight
								if 1: # Lu
									Lu = get_Lu(g1, g2)
									if dw > Lu:
										if 1:
											# draw_edges_r()
											# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ugraph.draw(edge_label=1, title='ugraph')
											# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
											1
											count_u += 1
											u_connect_delta = g2.connect_count() - g1.connect_count()
											u_connect_delta_map[u_connect_delta] += 1
											if 0:
												draw_igroup(ig1, title='ig1')
												draw_igroup(ig2, title='ig2')
												myplt.show()
											if verbose_text >= 3:
												1
												# print(f'connect-u {g1} {g2} delta={u_connect_delta}')
										igroups_.remove(ig2)
										continue
								#
								if 1: # Lb
									Lb = get_Lb(g1, g2)
									if dw <= Lb:
										if 1:
											# draw_edges_r()
											# debug_draw(6)
											# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ugraph.draw(edge_label=1, title='bgraph')
											# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
											1
											count_b += 1
											b_connect_delta = g2.connect_count() - g1.connect_count()
											b_connect_delta_map[b_connect_delta] += 1
											if verbose_text >= 3:
												1
												# print(f'connect-b {g1} {g2} delta={b_connect_delta}')
										igroups_.remove(ig1)
										break

					igroups = igroups_
					count_u_total += count_u
					count_b_total += count_b
					count_e_total += count_e
					# assert not empty(igroups_)
				elif cut_mode == 0:
					igroups = set()
					ghash_w_map = {}
					ghash_ig_map = defaultdict(set)
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_w_map: 
							ghash_ig_map[ghash].add(ig)
							ghash_w_map[ghash] = ig.weight
						else:
							count_cut += 1
							w0 = ghash_w_map[ghash]
							if ig.weight < w0:
								ghash_ig_map[ghash] = {ig}
								ghash_w_map[ghash] = ig.weight
							elif ig.weight > w0:
								pass
							else:
								assert not best1
								ghash_ig_map[ghash].add(ig)

					igroups = my.set.unionm(ghash_ig_map.values())
				else: raise Exception(f'{cut_mode}')
				1
				# debug
				if verbose_text >= 3:
					edges_count_map = DictOfSet( (e1, 0) for e1 in edges_used )
					for ig in igroups_:
						for e1 in ig.iedges:
							edges_count_map[i_e_map[e1]] += 1
					assert0_edges = [ e0 for e0, count in edges_count_map.items() if count == 0 ]
					assert1_edges = [ e0 for e0, count in edges_count_map.items() if count == len(igroups_) ]
					assert_edges = assert0_edges + assert1_edges
					count_assert0_edges = list(edges_count_map.values()).count(0)
					count_assert1_edges = list(edges_count_map.values()).count(len(igroups_))
					count_assert_edges = count_assert0_edges + count_assert1_edges
					count_assert_edges_list.append(count_assert_edges)
					# print
					# print(f'assert-edges 0:1:01:walked: {count_assert0_edges} / {count_assert1_edges} / {count_assert_edges} / {len(edges_used)}')
					if cut_mode == 1: 
						print(f'valid / contain / total {count_u + count_b} / {count_contain} / {count_total}')
						print(f'states={len(igroups)} e[{count_cut_equal}] u[{count_u}] b[{count_b}]')
						print(f'')
					if 0:
						myplt.cap(1)
						self.draw(hl_edges=my.setLike.difference(edges_used, assert_edges), hl_edges1=assert_edges)
						myplt.show()
				if verbose_text >= 2:
					list_count_state.append(len(igroups))
					list_count_anode.append(len(anodes))
				debug_draw()
				check_possible()
				# 判断是否终结
				if len(igroups) > state_threshold:
					break
			if "terminate":
				if len(min_igs) != 0:
					igroups = min_igs
					# assert0_edges = my.setLike.difference(self.edges, min_ig.edges)
					# assert1_edges = min_ig.edges
					# solver.assert_edges_0(assert0_edges)
					# solver.assert_edges_1(assert1_edges)
				else:
					assert not empty(igroups)
				# debug
				edges_count_map = DictOfSet( (e1, 0) for e1 in edges_used )
				for ig in igroups:
					for e1 in ig.iedges:
						edges_count_map[i_e_map[e1]] += 1
				assert0_edges = [ e0 for e0, count in edges_count_map.items() if count == 0 ]
				assert1_edges = [ e0 for e0, count in edges_count_map.items() if count == len(igroups) ]
				assert_edges = assert0_edges + assert1_edges
				count_assert0_edges = list(edges_count_map.values()).count(0)
				count_assert1_edges = list(edges_count_map.values()).count(len(igroups))
				count_assert_edges = count_assert0_edges + count_assert1_edges
				count_assert_edges_list.append(count_assert_edges)
				count_ori_edges = len(solver.ori_hg.edges)
				count_base_edges = len(hg.edges)
				count_edges_remained = count_base_edges - count_assert_edges
				if verbose_text >= 2:
					# print(f'dynamic_filter: assert-edges 0:1:01:walked: {count_assert0_edges} / {count_assert1_edges} / {count_assert_edges} / {len(edges_used)}')
					# print(f'    problem-state[{count_iter}]: {count_base_edges} - {count_assert_edges} = {count_edges_remained} / {count_ori_edges}')
					if len(min_igs) != 0:
						print(f'HgMstSolver: mst solved in walk-empty')
				if verbose_pic >= 2 and 0: # 仅当这次有效时显示
					if count_assert_edges == 0:
						pass
					else:

						myplt.cap(12)
						self.draw(hl_edges=edges_used, hl_edges1=assert_edges)
						if myplt.ax().index == 12: myplt.show()
				# return: update-info
				model.set_field_by_edges(edges_used)
				model.set_states(igroups)
				return model
				# debug
				if verbose_text >= 3:
					print(f'assert-edges: {mystr(count_assert_edges_list)}')
					if cut_mode == 1: print(f'u-connect-delta: {my.dict.str_sorted(u_connect_delta_map)}')
					if cut_mode == 1: print(f'b-connect-delta: {my.dict.str_sorted(b_connect_delta_map)}')
					print(f'state-count: {mystr(list_count_state)}')
					print(f'\taverage={my.average(list_count_state):.2} max={max(list_count_state)}')
					print(f'anode-count: {mystr(list_count_anode)}')
					print(f'\taverage={my.average(list_count_anode):.2} max={max(list_count_anode)}')
		def walk(model, order_mode=None, cut_mode=0, state_threshold=0, start=None) -> 'None':
			"""
				说明:
				"""
			if "pre":
				# simple
				i_e_map = model.i_e_map
				e_i_map = model.e_i_map
				self = hg = model.graph
				# assert hg.is_span(), hg.show()
				solver = model.solver
				debug = model.debug
				verbose_text = model.verbose_text
				verbose_pic = model.verbose_pic
				no_cycle = model.no_cycle
				best1 = solver.best1
				pos = hg.pos
				if start is not None: assert model.size() == 0
				# misc
				nodes = sorted(hg.nodes)
				weight = hg.get_weight_dict()
				# edges
				all_edges = list(i_e_map.values()) # 不需要deepcopy， 因为edge不会改变
				edges_used = model.edges().copy()
				edges_r = my.set_like.difference(all_edges, edges_used)
				##
				n_edges_map = {} # hg.node: 未使用边
				for n in nodes:
					adj_edges = [ e for e in hg.adj_n_e[n] if e not in edges_used ]
					n_edges_map[n] = adj_edges
				# nodes
				anodes = model.anodes.copy() # 导点
				# anodes_degree_n_n = my.SortedDict(key_v=lambda v:v) # 按未使用邻居点数排序，仅包含导点， 用于选点
				inodes = model.inodes.copy()
				used_nodes = model.used_nodes.copy() # 活跃 + 内点
				unused_nodes = model.unused_nodes.copy()
				# tmp
				new_nodes = set()
				new_anodes = set()
				# min
				min_igs = set()
				min_weight = my.inf
				assert cut_mode in range(3)
				# get_ru = hg.Ru_getter_depth(depth=0)
				# order, edges
				edge_order = list(hg.get_edge_order_half(nodes, edges_used, all_edges, mode=order_mode, start=start)) # [ e ..]
				# debug
				count_equal_span = 0
				count_cut = 0
				list_count_state = []
				list_count_anode = []
				possible_msts = []
				b_connect_delta_map = defaultdict(lambda: 0)
				u_connect_delta_map = defaultdict(lambda: 0)
				count_assert_edges_list = []
				if debug and 0:
					mst_len = self.mst_len()
			if "methods":
				def react_new_anode(n):
					anodes.add(n)
					new_anodes.add(n)
				def react_del_anode(n):
					anodes.remove(n)
				def react_new_node(n):
					new_nodes.add(n)
					used_nodes.add(n)
					unused_nodes.remove(n)
				def draw_edges_r():
					Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
					HyperGraph._draw_edges([edge_adding], pos=pos, edge_look=dict(color='orange'))
					Graph._draw_nodes(unused_nodes, pos=pos, look=dict(color='grey', alpha=0.5))
					myplt.title(f'i={len(igroups)} a={len(anodes)}')
				def draw_igroup(ig, **ks):
					ig.draw(inodes, anodes, used_nodes, pos, **ks)
					
				def debug_draw(i=debug):
					cond2 = 0
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
							ig.draw(inodes, anodes, used_nodes, pos)
					1
				def check_possible():
					if debug and 0:
						flag = any(ig.is_possible(edges_used, mst_len=mst_len) for ig in igroups_)
						flag |= min_ig != None and min_weight == mst_len
						assert flag, igroups
						return flag
				def get_model_fieldSet00() -> 'states, field_set':
					# model = []
					# for ig in igroups:
						# model.append(ig.state())
					#
					states = igroups
					field_set = { e_i_map[e] for e in edges_used }
					return states, field_set
			if "first":
				# ig0 = Igroup(weight=0, model=model)
				# if len(edge_order) != 0:
				# 	n0 = my.pick(edge_order[0])
				# 	ig0.add_anode(n0)
				# 	react_new_node(n0)
				# 	react_new_anode(n0)
				# else:
				# 	min_ig =ig0
				# igroups.add(ig0)
				if hasattr(model, 'states'):
					igroups = model.states
				else:
					raise
					igroups = [ Igroup(weight=0, model=model) ]
			# main
			for edge_adding in edge_order: # e
				ei = e_i_map[edge_adding]
				new_inodes = set()
				new_anodes = set()
				new_nodes = set()
				degree_minus = len(edge_adding) - 1
				w = weight[edge_adding]
				edges_used.append(edge_adding)
				# 预处理节点 ( edge_adding =  new_anodes new_inodes non-change ) ( new_nodes = new_anodes + new_inodes部分 )
				# new_anodes: 新增加的anode <=> 新增的点去掉e后还有边
				# new_inodes: <=> 去掉e后一条边都不剩（所有新增inode）
				# new_nodes:  new_anodes + borni
				for n in edge_adding:
					if n not in anodes: # new-nodes
						react_new_node(n)
					n_edges_map[n].remove(edge_adding)
					if len(n_edges_map[n]) == 0: # new-inodes
						new_inodes.add(n)
						if n in anodes: # a -> i
							react_del_anode(n)
						else: # born i
							pass
					else:
						if n not in anodes: # new-anodes
							react_new_anode(n)
						else: # non-change
							pass
						# anodes_degree_n_n[n] = len(my.set.unionm(n_edges_map[n])) - 1
						# assert anodes_degree_n_n[n] >= 0
				# pre
				1
				inodes |= new_inodes
				igroups_ = set()
				flag_terminate = len(inodes) == len(nodes) # 绝对终止
				flag_terminate2 = len(used_nodes) == len(nodes) # 可能终止
				# 过滤 循环 孤立
				for ig in igroups:
					#
					not_add, add = ig.judge_add_e(edge_adding, new_anodes, new_inodes, flag_terminate2, no_cycle=no_cycle)
					if not_add:
						if add:
							ig1 = ig
							ig2 = ig.copy()
						else:
							ig1 = ig
					else:
						if add:
							ig2 = ig
						else: pass
					#
					if not_add:
						ig1.add_anodes(new_anodes)
						igroups_.add(ig1.not_add_e(new_inodes))
					if add:
						ig2.add_anodes(new_anodes) # 此时ig中包含除了borni的所有点
						ig2.add_e(edge_adding, ei, w, new_inodes)
						if flag_terminate2 and ig2.is_terminated(): # terminated
							if min_weight > ig2.weight: # min_weight放前面, inf优先
								min_igs = {ig2}
								min_weight = ig2.weight
							elif min_weight < ig2.weight: pass
							else:
								assert not best1
								min_igs.add(ig2)
							continue
						else:
							igroups_.add(ig2)
				edges_r.remove(edge_adding)
				assert not empty(igroups_) or len(min_igs) != 0
				#同型 过滤
				if cut_mode == 1:
					# equal
					raise
					count_cut_e = 0
					ghash_ig_map = {}
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_ig_map: ghash_ig_map[ghash] = ig
						else:
							count_cut_e += 1
							ig0 = ghash_ig_map[ghash]
							if ig.weight < ig0.weight:
								ghash_ig_map[ghash] = ig
					igroups_ = set(ghash_ig_map.values())
					# Lu
					"""
						考虑每一对I1 < I2 
						L: { F1 - F2 } 的变化值 ( 越大的组F值越小)

						ugraph: (越小越好)
							anodes之间的分部完全瓶颈图
						"""
					hg_remain = HyperGraph.from_edges_weight(edges_r, self.weight, pos=pos)
					ngraph = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_ru = hg_remain.seperate_Ru_getter_depth(depth=0)
					ugraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in ugraph.std_edges():
						ugraph.set_edge_weight(e1, get_ru(set(e1)))
					
					def get_Lu(g1, g2):
						"""
							g1欠缺的部分连接起来 需要的上限
							二元完全图: 二元瓶颈图(分立部分用inf边连接)
							? 孤立点, 分立部分
							算法: 上限完全图的部分mst
								根据g2的每个组和对应的g1的小组
									将g1的小组连接成大组的上限
								求和

							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							dta = ugraph.group_mst_len(subs, fail=None)
							if dta == None:
								return my.inf
								
							r += dta
						return r
					# Lb
					"""
						bgraph: (越大越好)
							anodes之间的分布完全断开瓶颈图
						"""
					
					ngraph2 = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_rb = hg_remain.seperate_Rb_getter_depth(depth=0, get_u=get_ru)
					bgraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in bgraph.std_edges():
						bgraph.set_edge_weight(e1, get_rb(set(e1)))
					def get_Lb(g1, g2):
						"""
							g2的部分断开到g1, 能得到的下限
							g2的各个组断开的得到的之和
							算法
								m组完全瓶颈图(取max), 取最大和m-2个最小的
								断开记为inf
							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							group_graph = bgraph.group_graph(subs)
							if not group_graph.is_span():
								return my.inf
							weights = sorted(group_graph.weight.values())
							dta = weights[-1] + sum(weights[:m-2])
								
							r += dta
						return r

					# filter
					"""
						对每个(g1,g2)对
							排除g1 is g2
							仅考虑g1 <= g2时 
						"""
					igroups_order = sorted(igroups_, key=lambda ig: ig.weight)
					# debug
					count_total = len(igroups_order) ** 2
					count_contain = 0
					count_u = count_b = 0
					#
					for ig1 in igroups_order: # ig1 <= ig2
						if ig1 not in igroups_: continue
						if ig1.weight >= min_weight:
							igroups_.remove(ig1)
							continue
						for ig2 in igroups_order:
							if ig2 not in igroups_: continue
							if ig1 is ig2: continue
							if ig2.cover_span(ig1): # cope
								count_contain += 1
								g1 = ig1.group
								g2 = ig2.group
								dw = ig2.weight - ig1.weight
								if 1: # Lu
									Lu = get_Lu(g1, g2)
									if dw > Lu:
										if 1:
											# draw_edges_r()
											# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ugraph.draw(edge_label=1, title='ugraph')
											# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
											1
											count_u += 1
											u_connect_delta = g2.connect_count() - g1.connect_count()
											u_connect_delta_map[u_connect_delta] += 1
											if 0:
												draw_igroup(ig1, title='ig1')
												draw_igroup(ig2, title='ig2')
												myplt.show()
											if verbose_text >= 3:
												1
												# print(f'connect-u {g1} {g2} delta={u_connect_delta}')
										igroups_.remove(ig2)
										continue
								#
								if 1: # Lb
									Lb = get_Lb(g1, g2)
									if dw <= Lb:
										if 1:
											# draw_edges_r()
											# debug_draw(6)
											# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
											# ugraph.draw(edge_label=1, title='bgraph')
											# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
											1
											count_b += 1
											b_connect_delta = g2.connect_count() - g1.connect_count()
											b_connect_delta_map[b_connect_delta] += 1
											if verbose_text >= 3:
												1
												# print(f'connect-b {g1} {g2} delta={b_connect_delta}')
										igroups_.remove(ig1)
										break

					igroups = igroups_
					count_u_total += count_u
					count_b_total += count_b
					count_e_total += count_e
					# assert not empty(igroups_)
				elif cut_mode == 0:
					igroups = set()
					ghash_w_map = {}
					ghash_ig_map = {}
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_w_map: 
							ghash_ig_map[ghash] = {ig}
							ghash_w_map[ghash] = ig.weight
						else:
							# count_cut += 1
							w0 = ghash_w_map[ghash]
							if ig.weight < w0:
								ghash_ig_map[ghash] = {ig}
								ghash_w_map[ghash] = ig.weight
							elif ig.weight > w0:
								pass
							else:
								assert not best1
								ghash_ig_map[ghash].add(ig)

					igroups = my.set.unionm(ghash_ig_map.values())
				else: raise Exception(f'{cut_mode}')
				1
				# debug
				if verbose_text >= 3:
					edges_count_map = DictOfSet( (e1, 0) for e1 in edges_used )
					for ig in igroups_:
						for e1 in ig.iedges:
							edges_count_map[i_e_map[e1]] += 1
					assert0_edges = [ e0 for e0, count in edges_count_map.items() if count == 0 ]
					assert1_edges = [ e0 for e0, count in edges_count_map.items() if count == len(igroups_) ]
					assert_edges = assert0_edges + assert1_edges
					count_assert0_edges = list(edges_count_map.values()).count(0)
					count_assert1_edges = list(edges_count_map.values()).count(len(igroups_))
					count_assert_edges = count_assert0_edges + count_assert1_edges
					count_assert_edges_list.append(count_assert_edges)
					# print
					# print(f'assert-edges 0:1:01:walked: {count_assert0_edges} / {count_assert1_edges} / {count_assert_edges} / {len(edges_used)}')
					if cut_mode == 1: 
						print(f'valid / contain / total {count_u + count_b} / {count_contain} / {count_total}')
						print(f'states={len(igroups)} e[{count_cut_equal}] u[{count_u}] b[{count_b}]')
						print(f'')
					if 0:
						myplt.cap(1)
						self.draw(hl_edges=my.setLike.difference(edges_used, assert_edges), hl_edges1=assert_edges)
						myplt.show()
				if verbose_text >= 2:
					list_count_state.append(len(igroups))
					list_count_anode.append(len(anodes))
				debug_draw()
				# check_possible()
				# 判断是否终结
				if len(igroups) > state_threshold:
					break
			if "terminate":
				if len(min_igs) != 0:
					igroups = min_igs
					# assert0_edges = my.setLike.difference(self.edges, min_ig.edges)
					# assert1_edges = min_ig.edges
					# solver.assert_edges_0(assert0_edges)
					# solver.assert_edges_1(assert1_edges)
				else:
					assert not empty(igroups)
				# debug
				edges_count_map = DictOfSet( (e1, 0) for e1 in edges_used )
				for ig in igroups:
					for e1 in ig.iedges:
						edges_count_map[i_e_map[e1]] += 1
				assert0_edges = [ e0 for e0, count in edges_count_map.items() if count == 0 ]
				assert1_edges = [ e0 for e0, count in edges_count_map.items() if count == len(igroups) ]
				assert_edges = assert0_edges + assert1_edges
				count_assert0_edges = list(edges_count_map.values()).count(0)
				count_assert1_edges = list(edges_count_map.values()).count(len(igroups))
				count_assert_edges = count_assert0_edges + count_assert1_edges
				count_assert_edges_list.append(count_assert_edges)
				count_ori_edges = len(solver.ori_hg.edges)
				count_base_edges = len(hg.edges)
				count_edges_remained = count_base_edges - count_assert_edges
				if verbose_text >= 2:
					# print(f'dynamic_filter: assert-edges 0:1:01:walked: {count_assert0_edges} / {count_assert1_edges} / {count_assert_edges} / {len(edges_used)}')
					# print(f'    problem-state[{count_iter}]: {count_base_edges} - {count_assert_edges} = {count_edges_remained} / {count_ori_edges}')
					if len(min_igs) != 0:
						print(f'HgMstSolver: mst solved in walk-empty')
				if verbose_pic >= 2 and 0: # 仅当这次有效时显示
					if count_assert_edges == 0:
						pass
					else:

						myplt.cap(12)
						self.draw(hl_edges=edges_used, hl_edges1=assert_edges)
						if myplt.ax().index == 12: myplt.show()
				# return: update-info
				field = { e_i_map[e] for e in edges_used }
				model.set_field(field)
				model.set_states(igroups)
				# r = Model(field=field, solver=solver)
				# r.set_states(igroups)
				# d([e_i_map[e] for e in edge_order if e in edges_used])
				return None
				# debug

				if verbose_text >= 3:
					print(f'assert-edges: {mystr(count_assert_edges_list)}')
					if cut_mode == 1: print(f'u-connect-delta: {my.dict.str_sorted(u_connect_delta_map)}')
					if cut_mode == 1: print(f'b-connect-delta: {my.dict.str_sorted(b_connect_delta_map)}')
					print(f'state-count: {mystr(list_count_state)}')
					print(f'\taverage={my.average(list_count_state):.2} max={max(list_count_state)}')
					print(f'anode-count: {mystr(list_count_anode)}')
					print(f'\taverage={my.average(list_count_anode):.2} max={max(list_count_anode)}')
	class ModelNet:
		"""
			attr
				net<Graph>: model-net 边是相交关系
				_assert0_edges, _assert1_edges: { ei .. }
				_models <list>: 按照加入顺序
				i_models_map
				inter_map: [(m1, m2)] -> inter_info1
					inter_info= field, state_sub_map1, sub_count_map1
			合并标准:
				预估状态值小于阈值
			"""
		def __init__(self,  *, solver, ):
			# debug
			self
			self.debug = solver.debug
			self.verbose_text = solver.verbose_text
			self.verbose_pic = solver.verbose_pic
			self._show = solver._show
			self._print = solver._print
			#
			self.i_e_map = solver.i_e_map
			self.e_i_map = solver.e_i_map
			self.iedges = set(self.i_e_map)
			self._models = []
			self.solver = solver
			self.hg = self.graph = solver.hg
			# weight
			hg = self.solver.hg
			self.weight = {}
			for i, e in self.i_e_map.items():
				self.weight[i] = hg.weight[e]
			# net
			self.net = Graph()
			# self.inter_map = DictHash(hash=lambda s: my.set.hash_hashe(s, hashe=id)) # {m1,m2} -> field
			self.inter_map = {}
			def connect(m1, m2):
				field = sorted(m1.field_set & m2.field_set)
				assert not empty(field)
				#inter
				m1.setup_inter_info(m2, field)
				Graph.connect(self.net, m1, m2)
			self.net.connect = connect
			def disconnect(m1, m2):
				del m1.inter_info[m2]
				del m2.inter_info[m1]
				Graph.disconnect(self.net, m1, m2)
			self.net.disconnect = disconnect
			#
			self.i_models_map = { e: set() for e in self.iedges } # e: models
			self.check_list = set() # { model_not_checked_assert }
			self.map_update_set = set()
			self.count_continuous_subset = 0
		# info
		def size(self):
			return len(self.i_e_map)
		# net-info
		def edge_count_connect(self, e):
			m1, m2 = e
			return len(m1.states) + len(m2.states)
		def edge_count_sub(self, e):
			m1, m2 = e
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
			return len(sub_states_map1)
		def edge_weight_average(self, e):
			"""
				connect / sub / 2
				"""
			m1, m2 = e
			count_connect = self.edge_count_connect(e)
			count_sub = self.edge_count_sub(e)
			return count_connect / count_sub / 2
		# deubg
		def is_possible(self):
			mst = self.solver.hg.mst()
			mst_len = mst.len()
			for m in self.models():
				if not m.is_possible(mst=mst, mst_len=mst_len):
					return my.false_wrap(m)
			return True
		def draw(self, **ks):
			func = self.edge_weight_average
			labels = { e: f'{math.floor(func(e)):d}' for e in self.net.std_edges() }
			self.net.draw(**ks, edge_label=labels)
			return self
		# check
		def check_trace(self) -> 'bad-model':
			for m in self.models():
				if not m.check_trace():
					return my.false_wrap(m)
			return True
		def check_net(self):
			"""
				每个中间节点与周围节点的连接都是双向的
				没有单边0的中间节点
				"""
			for m1, m2 in self.net.edges:
				state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
				subs = set(sub_states_map1)
				# sub相同
				assert set(sub_states_map1) == set(sub_states_map2)
				for sub in subs:
					states1 = sub_states_map1[sub]
					states2 = sub_states_map2[sub]
					# 单边0
					assert not empty(states1)
					assert not empty(states2)
					# 双向
					for s1 in states1:
						assert state_sub_map1[s1] == sub
					for s2 in states2:
						assert state_sub_map2[s2] == sub
				# 双向
				for s1, sub in state_sub_map1.items():
					assert s1 in sub_states_map1[sub]
				for s2, sub in state_sub_map2.items():
					assert s2 in sub_states_map2[sub]
			return True
			...
		def check_assert(self):
			if not de.debug: return True
			for i, models in self.i_models_map.items():
				flags = [ m.assertion_iedge(i) for m in models ]
				if not my.all_equal(flags):
					return False
				if empty(flags): continue
				flag = flags[0]
				if flag == 0:
					for m in models:
						for s in m.states:
							if i in s.iedges: return False
				elif flag == 1:
					for m in models:
						for s in m.states:
							if i not in s.iedges: return False
				elif flag == 2:
					for m in models:
						syms = [ i in s.iedges for s in m.states ]
						if my.all_equal(syms): return False
				else: raise Exception(f'{flag}')
				
			return True
		def check(self):
			"""
				model.check()
				i_models_map
				"""
				
			if not self.check_assert(): raise
			# attr
			if not self.iedges == set(self.i_e_map): raise
			if not { i: e for e, i in self.e_i_map.items() } == self.i_e_map: raise
			#  _models
			models = set(self.net.nodes)
			if models != set(self._models): raise
			# models
			for m in self.models():
				if not m.i_e_map is self.i_e_map: raise
				if not m.field_set.issubset(self.iedges): raise
				if not m.check(): raise
			# i_models_map
			for m in models:
				for i in m.field:
					if not m in self.i_models_map[i]: raise
			for i, models in self.i_models_map.items():
				for m in models:
					if i not in m.field: raise
			return True
		# map
		def set_map0(self, e, items):
			"""
				assert1_group:
					map(1)
					map(0, )

				操作
					修改所有相关model中state（删改）
					False
						孤立的删除
					True
						循环的删除
					map(e_ 1)
						1. 在map前map(True),
							前提：是在assert1时将e_中的一个悬空点映射到现存点
							分析：不会产生孤立，循环在assert1已经处理了，不需要处理
							实现：不操作
						2. 一般情况
				pc(False)
					找到包含e的model，删除e
					找到e是待死边的model，删除死状态(
				pc(True)
					找到包含e的model，删除e
					找到e中有两个以上导点的model，删除循环状态(
				pc(map)
					找到包含e的model，用e_替换
				
				"""
			if items == True: ...
		def set_rmap0(self, items1, e2):
			"""
				说明
					和solver右推左的map相反，这里需要左推右。
				操作
					
				"""
			assert len(items1) == 1 and items1[0][1] == 1
			e1 = items1[0][0]

		def set_map(self, e, items, *, false_exist=None):
			"""
				items

				"""
			# e_i_map = self.solver.old_e_i_map
			# i = e_i_map[e]
			for model in self.models():
				model.set_map_map(e,items, false_exist=false_exist)
			return self
		def update_map(self):
			"""
				
				"""
			pairs = []
			if 0:
				self.clear()

			if 0 and not self.is_possible():
				for m in self.models():
					if not m.is_possible():
						d(m)
						d(m.states)
						print(f'not possible before update')
						raise
			models =[]
			assert self.map_update_set == set(self.models())
			for m in self.map_update_set:
				m_ = m.updated()
				models.append(m_)
				pairs.append((m, m_))
			self.map_update_set.clear()
			# pre
			# self.i_models_map.clear()
			# self.net = Graph()
			self.__init__(solver=self.solver)
			#
			self._show().mask(0)
			self._print().mask(0)
			for i, m in enumerate(models):
				if i == len(models) - 1:
					self._show().unmask()
					self._print().unmask()
				self.add_update_model(m, description='update_map')
			assert not empty(models)
			# 
			if 0 and not self.is_possible():
				for m2 in self.models():
					if not m2.is_possible():
						m1 = [ ma for (ma, mb) in pairs if mb is m2 ][0]
						del_states = m1.states.difference(m2.states)
						# d(del_states)
						# d(m1.is_possible())
						good_s = [ s for s in m1.states if s.is_possible() ][0]
						# print( mystr( [s.iedges for s in del_states], split='\n' ) )
						d(good_s=good_s)(good_s.iedges)
						d(good_s.try_update(anodes=m2.anodes))
						d(m1=m1.states)
						d(m2=m2.states)
						d(m1_iedges=[s.iedges for s in m1.states])
						d(m2_iedges=[s.iedges for s in m2.states])
						print(f'not possible after update')
						raise
			return self
		# oper
		def add_update_model(self, model, *, description='none' ) -> 'finish assert fail continue': 
			"""
				todo: 包含别人
				关系处理:
					被包含/相等: 返回
					包含其他: 用子集过滤删除子集
					相交: 相关
				update:
					先用相邻节点更新自己
					再用自己扩散式更新周围
				check-assert:
					等更新完成, 对所有待检查的元素进行检查
				return:
					更新完成后存在(所有)model为全范围时, 返回
				"""
			sub=None
			subs=None

			def debug():
				flag = self.check_trace()
				if flag: return
				else:
					trace = self.solver.trace
					# raise my.Exception
					bm = flag.gs[0]
					d(model_is_bm=model is bm)
					d(assert1_good=my.set_like.issubset(bm.assert1_edges(), trace.edges))
					d(assert0_good=all( not trace.has_edge(e) for e in bm.assert0_edges()))
					model.debug_info()
					bm.debug_info()
					# bm.debug_draw_states()
					self.hg.draw(node_label=0, title='hg')
					self.solver.trace.draw(node_label=0, title='mst')
					self.solver.trace.draw(node_label=1, title='mst')
					d(possible=bm.is_possible(mst=trace))
					myplt.show()
					raise my.Exception
				
				if empty(model.states):
					# if sub == None:
					# 	d(subs)
					# 	raise
					# d(_dict)
					d(sub_iedges_list=sub.iedges_list())
					d(model_iedges_list_before=[s.iedges for s in _dict.states])
					d(model_iedges_list_after=model.iedges_list())
					d(sub)
					d(model)
					# d(sub.match)
					d(sub.field)
					d(model.field)
					d(sub.field_set.issubset(model.field_set))
					# d(set(self.i_e_map))
					self.hg.draw(edge_label=1, hl_edges=model.edges())
					myplt.show()
					subs.clear()
					# return 0
					raise
				return True
			# pre
			assert not empty(model.states)
			field_set = model.field_set
			# relation
			relates = []
			subs = []
			for m in self.models():
				relation = my.set.relation(field_set, m.field_set)
				# d(model.field, m.field, relation)
				if relation in ('sub', 'equal'):
					self.count_continuous_subset += 1
					if self._print.update_net:
						print(f'[add fail] continuous = {self.count_continuous_subset}')
					return 'fail'
				elif relation == 'inter':
					relates.append(m)
				elif relation == 'hyper':
					subs.append(m)
				elif relation == 'seperate':
					pass
				else: raise Exception(f'{relation}')
			self.count_continuous_subset = 0
			# add-graph
			# add-node
			self.add_model(model)
			# debug
			if 0:
				ori_asserted_edges = model.asserted_edges()
				self.ori_assert_edges_count = len(ori_asserted_edges)
			# sub
			for sub in subs:
				if 0:
					_dict = Name(
						states = set(model.states),
						sub = sub,
						subs=subs,
					)
				model.update_by(sub, field=sub.field)
				# del-node
				self.del_model(sub)
			#
			
			for m1 in relates:
				self.net.connect( m1, model)
			if self.solver._show.models or my.average((m.size() for m in self.models()), default=0) > 30000:
				# if self.solver.ishow:
				myplt.cap(self.solver.ishow)
				myplt.new_figure()
				for i, m in enumerate(self.models()):
					self.solver.hg.draw(hl_edges=m.edges(), title=f'model[{i}]')
				if self.solver.ishow:
					myplt.show()
			if self._show.net:
				if self.solver.ishow:
					myplt.cap(self.solver.ishow)
				# for i, m in enumerate(self.models()):
				self.draw(title=f'net')
				if self.solver.ishow:
					myplt.show_on_full()

			if self._print.update_net:
				model_size_list = [ len(m.states) for m in self.models() ]
				model_size_list = [ f'{m.size()}:{m.var()}' for m in self.models() ]
				print(f'[{description}] size={len(self.models())} relation={len(self.net.edges)} {self.size()}:{mystr(model_size_list)}')
			# update
			self.update_from_model(model)
			self.check_list.add(model)
			assert self.hg.is_span()
			assert not empty(model.states)
			flag_assert = self.update_assert()
			if 0:
				asserted_edges = self._assert0_edges | self._assert1_edges
				if not ori_asserted_edges.issubset(asserted_edges):
					((ori_asserted_edges, asserted_edges), model.states)
					diff = ori_asserted_edges.difference(asserted_edges)
					e = my.pick(diff)
					if all( e in iedges for iedges in model.iedges() ):
						for m in self.i_models_map[e]:
							if not all( e in iedges for iedges in m.iedges() ):
								print(m.iedges())
					elif all( e not in iedges for iedges in model.iedges() ):
						for m in self.i_models_map[e]:
							if any( e in iedges for iedges in m.iedges() ):
								print(m.iedges())
					else: raise Exception(f'{0}')
					raise
			# combine
			if not flag_assert:
				self.update_combine()
			#
			flag_finish = self.check_finish()
			# return
			if flag_finish:
				return 'finish'
			elif flag_assert:
				return 'assert'
			else:
				#
				hg = self.solver.hg
				if 0:
					for n in hg.nodes:
						if hg.degree(n) <= 1:
							assert hg.degree(n) == 1
							e = hg.adj_n_e[n][0]
							i = self.e_i_map[e]
							assert self.i_e_map[i] == e
							assert i not in model.field
							d(hg.degree(n))
							d(e, i)
							# d(self.i_models_map)
							# 1
							# pause()
							if not empty(self.i_models_map[i]):
								1
								models = self.i_models_map[i]
								d(models)
								raise
				return 'continue'
		def update_from_model(self, model):
			"""
				pc
					对所有相邻节点发动更新命令
				"""
			model.update()
			return self
			# adjs = self.net.adj[model]
			# for adj in adjs:
			# 	self.update_model_rcr_by(adj, model)
		def check_finish(self):
			for m in self.models():
				if m.size() == len(self.i_e_map):
					assert len(self.models()) == 1
					self._finish = m
					assert isinstance( my.pick(m.states).weight, float ) or my.all_equal( s.weight for s in m.states )
					return True
			else:
				return False
		def update_assert(self) -> '<bool>has-assert':
			"""
				对每个元素, 随意选择一个包含的model进行检查(效率一样)
				"""
			check_field = my.set.unionm(m.field_set for m in self.check_list)
			self._assert0_edges = assert0_edges = set()
			self._assert1_edges = assert1_edges = set()
			for e in check_field:
				model = my.pick(self.i_models_map[e])
				assertion = model.assertion_iedge(e)
				if assertion == 2: pass
				elif assertion == 1:
					assert1_edges.add(e)
				elif assertion == 0:
					assert0_edges.add(e)
				else: raise Exception(f'{assertion}')
			# check
			if 0:
				for i in assert0_edges:
					for m in self.models():
						for s in m.states:
							if i in s.iedges:


								ms_has_i = [ m0 for m0 in self.models() if m0.has_iedge1(i) ]
								ms_not_has_i = [ m0 for m0 in self.models() if not m0.has_iedge1(i) ]
								d(ms_has_i)
								# d(ms_not_has_i)
								1
								d(i=i)
								d(len(self.models()))
								bad_states = [s0 for s0 in m.states if i in s0.iedges ]
								d( [s0.iedges for s0 in m.states ] )
								# networkx.draw_networkx_nodes(self.net, node_color={m:'red'})
								d(self.i_models_map[i])
								for m1 in self.i_models_map[i]:
									# d(rela=my.set.relation(m1.field_set, m.field_set))
									# d( (m, m1) in self.net.edges )
									d(m1.field)
									...
								# networkx.draw(self.net, nodelist=[m], node_color='red', edgelist=[])
								m.debug_state( bad_states[0] )
								plt.show()
								# d(s)
								d(s.iedges)
								# d(s.match())
								raise
			#
			self.check_list.clear()
			if not empty(assert0_edges) or not empty(assert1_edges):
				return True
			else:
				return False
		# combine
		def update_combine(self):
			if not self.solver.flag_combine: return
			while 1:
				for m1, m2 in self.net.edges:
					if not self.judge_combine(m1, m2): continue
					if (m1, m2) in self.net.edges:
						self.combine(m1, m2)
						break
				else:
					break
		def combine(self, m1, m2):
			"""
				删除节点, 建立新节点
				过滤:
					循环, 同型
				"""
			def debug():
				return
				flag = model.check_trace()
				if flag: return 1
				# model.debug_print_states()
				# d(model.states)
				assert self.check_net()
				s1 = m1.check_trace()
				s2 = m2.check_trace()
				state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
				
				sub = state_sub_map1[s1]
				states2 = sub_states_map2[sub]
				assert s2 in states2
				iedges, edges, common_weight = self.extract_sub(sub, inter_field)
				ig = s1.try_combine(s2, self.i_e_map, anodes, common_weight, model)
				1
				raise
			# get-new
			assert m1.field != m2.field
			ghash_igs_map = {}
			ghash_weight_map = {}
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
			assert len(sub_states_map1) == len(sub_states_map2)
			hg = self.solver.hg
			# 
			inter_field_set = m1.field_set & m2.field_set
			inter_field = sorted(inter_field_set)
			union_field_set = m1.field_set | m2.field_set
			union_field = sorted(union_field_set)
			union_edges = [ self.i_e_map[i] for i in union_field ]
			anodes = hg.get_anodes_by_edges(union_edges)
			# model
			model = Model(field=union_field_set, solver=self.solver)
			# debug
			# summary, print_count, bound = m1.get_inter_field_map_debug(m2)
			#
			h_match = None
			for sub, states1 in sub_states_map1.items():
				states2 = sub_states_map2[sub]
				iedges, edges, common_weight = self.extract_sub(sub, inter_field)
				for s1 in states1:
					assert s1.model is m1
					for s2 in states2:
						ig = s1.try_combine(s2, common_weight, model)
						
						# flag_match =  s1.match_trace() and s2.match_trace()
							
						# if flag_match: 
						# 	assert ig
						# 	assert ig.match_trace()
						if ig:
							h = ig.group.hash()
							w = ig.weight
							if h not in ghash_igs_map:
								ghash_igs_map[h] = {ig}
								ghash_weight_map[h] = w
							else:
								w_ = ghash_weight_map[h]
								if w < w_:
									ghash_igs_map[h] = {ig}
									ghash_weight_map[h] = w
								elif w == w_:
									ghash_igs_map[h].add(ig)
								else:
									pass
			#					
			igroups = my.set.unionm(ghash_igs_map.values())
			#debug
			# pause()
			if self._print.combine:
				
				summary_size = f'{m1.size()} {len(m1.field_set & m2.field_set)} {m2.size()}'
				summary_complex = m1.get_summary_complex(m2)
				bound = m1.guess_combine_count(m2)
				print(f'<combine> [{summary_size}] {summary_complex} {bound} -> {len(igroups)}')
			if 0:
				if not Igroup.is_possible_igroups(igroups, i_e_map=self.i_e_map, edges_used=union_edges, hg=hg):
					flag1 = m1.check_possible()
					flag2 = m2.check_possible()
					d(mystr(m1.states, split='\n'))
					d(mystr(m2.states, split='\n'))
					d(mystr(igroups, split='\n'))
					s1_min = []
					s2_min = []
					for s1 in m1.states:
						if m1.is_igroup_possible(s1):
							s1_min.append(s1)
							break 
					for s2 in m2.states:
						if m2.is_igroup_possible(s2):
							s2_min.append(s2)
							break
					m1.is_igroup_possible(flag1)
					d(flag1, flag2)
					# d( flag1.try_combine(flag2, self.i_e_map, anodes, common_weight, hg) )
					d(m1.is_igroup_possible(flag1))
					d(s1_min=s1_min)
					d(s2_min=s2_min)
					1
					raise
			# do
			model.set_states(igroups)
			self.del_model(m1)
			self.del_model(m2)
			if empty(igroups):
				1
				flag1 = m1.check_possible()
				flag2 = m2.check_possible()
				# l1 = [ s for s in m1.states if d.mst.match_state(s) ]
				# l2 = [ s for s in m2.states if d.mst.match_state(s) ]
				# d(l1, l2)
				d.expand(m1, m2)
				d.expand(flag1=flag1, flag2=flag2)
				edges1 = flag1.get_edges(i_e_map=self.i_e_map)
				edges2 = flag2.get_edges(i_e_map=self.i_e_map)
				d(edges1=edges1)
				d(edges2=edges2)
				raise
			self.add_update_model(model, description='combine') ###
		def judge_combine(self, m1, m2):
			combine_count = self.combine_count(m1, m2)
			if combine_count <= self.combine_threshold():
				return True
			else:
				return False
		def combine_count(self, m1, m2):
			state_sub_map1, sub_states_map1, state_sub_map2, sub_states_map2, counter_combine = m1.inter_info[m2]
			count = counter_combine.count
			assert count > 0
			return count
		def combine_threshold(self):
			return self.solver.combine_threshold()
		# net-oper
		def clear(self):
			self.__init__(solver=self.solver)
			return self
		# lib
		def add_model(self, model):
			for e in model.field:
				self.i_models_map[e].add(model)
			self.net.add_node(model)
			self._models.append(model)
			return model
		def del_model(self, m):
			
			self.net.del_node_clear(m)
			self._models.remove(m)
			for i in m.field:
				self.i_models_map[i].remove(m)
		def models(self):
			return self._models
		def extract_sub(self, sub, field) -> 'iedges edges weight':
			"""
				sub: sub-node<hash>
				"""
			weight = 0
			iedges = set()
			edges = []
			for i in reversed(field):
				bit = sub % 2
				sub //= 2
				if bit:
					e = self.i_e_map[i]
					w = self.weight[i]
					weight += w
					iedges.add(i)
					edges.append(e)
			return iedges, edges, weight
		def get_sub_weight(self, sub, field):
			r = 0
			for i in reversed(field):
				bit = sub % 2
				sub //= 2
				if bit:
					# e = self.i_e_map[i]
					w = self.weight[i]
					r += w
			return r
		def assert0_edges(self):
			return [ self.i_e_map[i] for i in self._assert0_edges ]
		def assert1_edges(self):
			return [ self.i_e_map[i] for i in self._assert1_edges ]
		# judge
			
	class HgMstSolver:
		"""
			mode
				filter<int>
					0: 无
					1: 简单快速
					2: 测试
			attr
				hg: 过滤前的
				hg_: 过滤后的
				asserted_edges <list>
				edge_map<DictOfSet>:
					True: assert=1
					False: assert=0
				complete_hg: 一个同mst的冗余hg
				debug: 0 1 2
				restore<bool>
				shrink: 缩减值
				<int>flag_dynamic_filter
				trace<HG>: 解
			net
				attr:
					tgraph #through-graph
					Bweight Wweight
				说明：
			说明：
				正向操作
					确认黑边：删除节点，与删除节点相连的边映射到新边，删除边
				比较遵循绝对不等原则，以hash(set)排序, 0.1 0.01, 0.001
			要求
				hg中有一个2元边完全连通图
			"""
		"""map
			usage
				set_map(e, bool)
				set_map(e, )
			mapper<MstMapper>
			"""
		"""oldmap
			usage
				set_map(e, [ e_ : +-1 ] )
			edge_map<DictOfSet>: e : { e_ : +-1 } | bool
			tail_map: { e_ : {e .. } }
			说明：
				按顺序映射
				每一个映射的前者都是当前存活的
				每一时刻不会同时存在两个相同边
			"""
		def __init__(self, hg, *, debug=0, verbose_text=0, verbose_pic=0, ishow=0, 
			_print=dict(), _show=dict(),
			restore=0, filter=0, cacu_v=2, dynamic_filter=0, 
			state_threshold=1000, iter_threshold=100, expand_rate_threshold=0.7, threshold_addState_edgeRate=0.2,
			best1=True, no_cycle=1, combine=True, order_mode=None, cut_mode=0, trace=None, pick_start=None,
			filter_mode=0,
			):
			# debug
			self.debug = de.debug and debug
			self.verbose_text = debug and verbose_text
			self.verbose_pic = debug and verbose_pic
			self._print = my.DebugSetting(_print, expand_state=1, set_map=0, update_net=0, combine=0 ).base(debug and verbose_text)()
			self._show = my.DebugSetting(_show, models=0, net=0, valid_add=0, invalid_add=0, set_map=0).base(debug and verbose_pic)()
			# if not debug:
			# 	for k in self.print: self.print[k] = 0
			# 	for k in self.show: self.show[k] = 0
			#
			self.restore = restore
			if trace is None: self.trace = None
			else: self.trace = trace.copy()
			# if complete_hg == None:
			# 	self.complete_hg = hg
			# else:
			# 	self.complete_hg = complete_hg
			self.ori_hg = hg
			self.hg = hg.copy()
			self.shrink = 0
			self.best1 = best1
			self.flag_filter = filter
			# walk
			if pick_start == None: self.pick_start = 'auto1'
			else: self.pick_start = pick_start
			self.order_mode = order_mode
			self.cut_mode = cut_mode
			self.no_cycle = no_cycle
			self.assert_no_cycle = no_cycle
			assert no_cycle
			self.state_threshold = state_threshold
			self.iter_threshold = iter_threshold
			self.threshold_addState_edgeRate = threshold_addState_edgeRate
			assert 0 <= expand_rate_threshold < 5
			self.expand_rate_threshold = expand_rate_threshold
			if self.restore:
				self.edge_map = my.DictOfSet([( e, DictOfSet([(e,1)]) ) for e in hg.edges])
				# self.edge_map = my.Inspector(self.edge_map, 'self.edge_map', print_self=1, before=1, after=0, breakhere=0, inspect=None,
				# 	tostr=lambda se: f'{se.sub_from_keys([d.e1, d.e2, d.e3], default=None)}',
				# 	)
				self.tail_map = my.DictOfSet([(e, SetOfSet( [e] )) for e in hg.edges]) # tail -> root
				# self.tail_map = my.Inspector(self.tail_map, 'self.tail_map', print_self=1, before=1, after=0, breakhere=1, inspect=None)
			self.record = Name(contain01_pairs=[], ru_edges=[], rb_edges=[], hang_edges=[]) # assert0, assert1, 
			self.cacu_v = cacu_v
			self.flag_dynamic_filter = dynamic_filter
			self.flag_combine = combine
			self.ishow = ishow
			# best1
			if best1:
				self.hg.set_odd_weight_OddWeight()
			# filter-mode
			self.filter_mode = filter_mode
		# lib
		# setting
		def combine_threshold(self):
			return self.state_threshold * 2
		# dynamic_filter
		def dynamic_filter2(self) -> '<bool>solved':
			"""
				attr
					i_e_map
					e_i_map
					iweight
				注意:
					提取模式时不能过滤同价值的
				说明-模式识别
					对每两个相交的模式进行兼容测试
					被包含的模式删除
					相关网:
						相交关系
					模式更新:
						一个模式更新时, 尝试带因更新周围的模式, 若成功更新, 重复以上过程
						带因更新: 既是更新的基准, 同时防止反哺循环

				arg
					state_threshold:  state上限(过滤后)
					iter_threshold: 迭代次数阈值
					pick_start: random | auto1
				说明
					找到一个点, 幻延展, 清理延展过程中确认的边, 直到states达到阈值
				起始点搜索顺序:
					random: 
				
				"""
			"""自动
				walk:
					expand_rate_threshold: 有model的var低于这个比率时walk
				addState: 每次增加倍数, 刷新尝试的edges
					当没有可以walk的, 只能新加入时
						当尝试的edges比率大于一定比率
						当model数量大于一定值
				"""
			# debug = self.debug
			verbose_text =self.verbose_text
			verbose_pic =self.verbose_pic
			#
			pick_start = self.pick_start
			count_iter = 0
			hg = self.hg
			solver = self
			best1 = self.best1
			state_threshold = self.state_threshold
			iter_threshold = self.iter_threshold
			expand_rate_threshold = self.expand_rate_threshold
			expand_state_rate = 2
			threshold_addState_edgeRate = self.threshold_addState_edgeRate
			flag_reject_add = False
			add_fail_count = 0
			#
			def debug():
				return
				if hg.check_span(): return
				print(0)
				hg.draw(edge_label=e_i_map)
				hg.draw(edge_label=1, title='weight')
				myplt.show()

				raise
			def debug():
				# model_net.check()
				for m in model_net.models():
					if d.e2 in m.edges() and d.e1 in m.edges():
						for s in m.states:
							assert d.e2 in s.iedges
							assert d.e1 not in s.iedges
			def model_net_assert_edges():
				# pre
				assert1_edges = model_net.assert1_edges()
				assert0_edges = model_net.assert0_edges()
				assert_edges = assert1_edges + assert0_edges
				model_size_list = [ len(m.states) for m in model_net.models() ]
				# assert model_net.ori_assert_edges_count <= len(assert_edges)
				# debug
				if verbose_text >= 3:
					print(f'ModelNet: size={len(model_net.models())} relations={len(model_net.net.edges)} independent={model_net.ori_assert_edges_count} / {len(assert_edges)} {mystr(model_size_list)}')
					print(f'    assert {len(edges)} - {len(assert_edges)} = {len(edges)-len(assert_edges)} / {len(self.ori_hg.edges)}')
					# print(f'    add model: size={assert_edges}')
					print(f'')
				if self._show.valid_add:
					if self.ishow: myplt.cap(self.ishow)
					hg.draw(hl_edges1=assert_edges, hl_edges=edges_used)
					if self.ishow: 
						myplt.show_on_full()
				# do.solver.hg ..
				if self._print.set_map:
					d(i_e_map=self.i_e_map)
					d(assert0=assert0_edges)
					d(assert1=assert1_edges)
				# assert model_net.check()
				if self._print.set_map:
					print(f'begin assert0')
				solver.assert_edges_0(assert0_edges)
				if d.e2 in assert1_edges: 
					debug()
				if self._print.set_map:
					print(f'begin assert1')
				solver.assert_edges_1(assert1_edges)
				self.hg.clear_isolated_nodes()
				if self.trace:
					self.trace.clear_isolated_nodes()
				# assert hg.check_span(), (print(1), hg.show())
				my.dict.copy_from( self.i_e_map, self.tmp_i_e_map )
				my.dict.copy_from( self.e_i_map, self.tmp_e_i_map )
				my.dict.copy_from( self.iweight, self.tmp_iweight )
				self.model_net.update_map()
				# do.model_net
				# model_net.assert_edges(edges0=assert0_edges, edges1=assert1_edges)
				# i_e_map, e_i_map
				# for e in assert_edges:
			def return_False():
				nonlocal state_threshold
				state_threshold = my.inf
			def expand_state():
				nonlocal state_threshold, iedges_to_pick, add_fail_count, flag_reject_add
				self.state_threshold = state_threshold = math.floor(state_threshold * expand_state_rate)
				iedges_to_pick = iedges.copy()
				add_fail_count = 0
				flag_reject_add = False
				#
				if self._print.expand_state:
					print(f'expand state to {state_threshold}')
				return 
			def try_expand_model():
				nonlocal model, res
				
				# expand
				for m in model_net.models():
					if m.var() <= expand_rate_threshold * state_threshold:
						# d(model_net.net.degree(m))
						model_net.del_model(m)
						# assert model_net.net.degree(m) == 0, model_net.net.degree(m)
						assert empty(m.inter_info), list(m.inter_info)
						m.walk(state_threshold=state_threshold, order_mode=self.order_mode)
						res = model_net.add_update_model(m, description='expand')
						model = m
						return True
				return False
			def add_new_model():
				nonlocal model, res
				cover_total = sum( m.size() for m in model_net.models() )
				# start
				if pick_start == 'auto1':
					"""
						在models覆盖度最小的点中随机选择
						"""
					min_cover = my.inf
					for i, models in model_net.i_models_map.items():
						if i not in iedges_to_pick: continue
						cover = len(models)
						if cover < min_cover:
							if cover > 4: continue
							min_cover = cover
							picks = [i]
						elif cover > min_cover:
							continue
						else:
							picks.append(i)
					if min_cover is my.inf: return False
					istart = my.random.pick(picks)
					# d(min_cover)
				elif pick_start == 'node0':
					"""
						node=0
						"""
					adj_edges = hg.adj_n_e[0]
					start = min(adj_edges, key=my.set.hash)
					istart = e_i_map[start]
				elif pick_start == 'random':
					raise
					istart = my.random.pick(iedges_to_pick)
				else: raise Exception(f'{pick_start}')
				iedges_to_pick.remove(istart)
				start = i_e_map[istart]
				#
				model = Model.empty_model(solver=solver)
				model.walk(start=start, state_threshold=state_threshold, order_mode=self.order_mode)
				assert not empty(model.states)
				res = model_net.add_update_model(model, description='add')
				return True
			#
			def step():
				nonlocal model, res
				while 1:
					# add
					flag_no_add = flag_reject_add or empty(iedges_to_pick)
					if not flag_no_add:
						flag = add_new_model()
						if flag: return
					# expand
					flag = try_expand_model()
					if flag: return
					# add-state
					expand_state()
					continue

					# flag1 = sum( m.size() for m in model_net.models() ) <= 100 * len(i_e_map) # 覆盖度不够
					# if flag1:
					# else:
					# flag2 = len(iedges_to_pick) < ( 1 - threshold_addState_edgeRate ) * len(iedges) # 可能选择的边少
					# if flag2: 
					# 	expand_state()
					# 	continuemodel(model)
					# break
					# if res == 'continue': continue
				
			#
			edges = hg.edges
			self.i_e_map = i_e_map = { i : e for i, e in enumerate(hg.edges) }
			self.e_i_map = e_i_map = DictOfSet( (e, i) for i, e in i_e_map.items() )
			self.iweight = iweight = { i: hg.weight[i_e_map[i]] for i in self.i_e_map }
			self.tmp_i_e_map = self.i_e_map.copy()
			self.tmp_e_i_map = self.e_i_map.copy()
			self.tmp_iweight = self.iweight.copy()
			id_i_e_map = id(i_e_map)
			
			self.model_net = model_net = ModelNet(solver=self)
			# tmp
			model = None
			res = None
			# main- loop
			while 1:
				"""
					i_e_map 和 e_i_map id不变
					"""
				# assert not empty(self.i_e_map), self.hg.show()
				iedges = set(i_e_map)
				assert id(i_e_map) == id_i_e_map
				#
				iedges_to_pick = set(iedges)
				while 1: # until assert or finish
					# pick-start
					# pre
					# main
					step()
					# debug
					edges_used = [ i_e_map[i] for i in model.field ]
					assert not empty(model.states)
					if not flag_reject_add and res != 'fail':
						add_fail_count = 0
					if res == 'assert':
						model_net_assert_edges()
						break
					elif res == 'finish':
						self.final_model = model_net._finish
						self.final_hgs = [ s.to_hg_by_edges(i_e_map) for s in self.final_model.states ]
						return True
					elif res == 'continue':
						pass
					elif res == 'fail':
						add_fail_count += 1
						if add_fail_count >= 6:
							flag_reject_add = True
					else: raise Exception(f'{0}')
					
					if self._show.invalid_add:
						if self.ishow: myplt.cap(self.ishow)
						# d.count()
						hg.draw(hl_edges=edges_used, title=d.count())
						# d(hg.len())
						if self.ishow: 
							myplt.show_when_full()
							# a = my.kb.wait('F6')
							# print(a)
							# myplt.close()
					#
					# post
						# count_iter += 1
						# if count_iter == iter_threshold:
						# 	return_False()
		def solve_filter_mode(self) -> '<bool>solved':
			"""
				attr
					i_e_map
					e_i_map
					iweight
				注意:
					提取模式时不能过滤同价值的
				说明-模式识别
					对每两个相交的模式进行兼容测试
					被包含的模式删除
					相关网:
						相交关系
					模式更新:
						一个模式更新时, 尝试带因更新周围的模式, 若成功更新, 重复以上过程
						带因更新: 既是更新的基准, 同时防止反哺循环

				arg
					state_threshold:  state上限(过滤后)
					iter_threshold: 迭代次数阈值
					pick_start: random | auto1
				说明
					找到一个点, 幻延展, 清理延展过程中确认的边, 直到states达到阈值
				起始点搜索顺序:
					random: 
				
				"""
			"""自动
				walk:
					expand_rate_threshold: 有model的var低于这个比率时walk
				addState: 每次增加倍数, 刷新尝试的edges
					当没有可以walk的, 只能新加入时
						当尝试的edges比率大于一定比率
						当model数量大于一定值
				"""
			# debug = self.debug
			verbose_text =self.verbose_text
			verbose_pic =self.verbose_pic
			#
			pick_start = self.pick_start
			count_iter = 0
			hg = self.hg
			solver = self
			best1 = self.best1
			state_threshold = self.state_threshold
			iter_threshold = self.iter_threshold
			expand_rate_threshold = self.expand_rate_threshold
			expand_state_rate = 2
			threshold_addState_edgeRate = self.threshold_addState_edgeRate
			flag_reject_add = False
			add_fail_count = 0
			#
			def debug():
				return
				if hg.check_span(): return
				print(0)
				hg.draw(edge_label=e_i_map)
				hg.draw(edge_label=1, title='weight')
				myplt.show()

				raise
			def debug():
				# model_net.check()
				for m in model_net.models():
					if d.e2 in m.edges() and d.e1 in m.edges():
						for s in m.states:
							assert d.e2 in s.iedges
							assert d.e1 not in s.iedges
			def model_net_assert_edges():
				# pre
				assert1_edges = model_net.assert1_edges()
				assert0_edges = model_net.assert0_edges()
				assert_edges = assert1_edges + assert0_edges
				model_size_list = [ len(m.states) for m in model_net.models() ]
				# assert model_net.ori_assert_edges_count <= len(assert_edges)
				# debug
				if verbose_text >= 3:
					print(f'ModelNet: size={len(model_net.models())} relations={len(model_net.net.edges)} independent={model_net.ori_assert_edges_count} / {len(assert_edges)} {mystr(model_size_list)}')
					print(f'    assert {len(edges)} - {len(assert_edges)} = {len(edges)-len(assert_edges)} / {len(self.ori_hg.edges)}')
					# print(f'    add model: size={assert_edges}')
					print(f'')
				if self._show.valid_add:
					if self.ishow: myplt.cap(self.ishow)
					hg.draw(hl_edges1=assert_edges, hl_edges=edges_used)
					if self.ishow: 
						myplt.show_on_full()
				# do.solver.hg ..
				if self._print.set_map:
					d(i_e_map=self.i_e_map)
					d(assert0=assert0_edges)
					d(assert1=assert1_edges)
				# assert model_net.check()
				if self._print.set_map:
					print(f'begin assert0')
				solver.assert_edges_0(assert0_edges)
				if d.e2 in assert1_edges: 
					debug()
				if self._print.set_map:
					print(f'begin assert1')
				solver.assert_edges_1(assert1_edges)
				self.hg.clear_isolated_nodes()
				if self.trace:
					self.trace.clear_isolated_nodes()
				# assert hg.check_span(), (print(1), hg.show())
				my.dict.copy_from( self.i_e_map, self.tmp_i_e_map )
				my.dict.copy_from( self.e_i_map, self.tmp_e_i_map )
				my.dict.copy_from( self.iweight, self.tmp_iweight )
				self.model_net.clear()
				# self.model_net.update_map()
				# do.model_net
				# model_net.assert_edges(edges0=assert0_edges, edges1=assert1_edges)
				# i_e_map, e_i_map
				# for e in assert_edges:
			def return_False():
				nonlocal state_threshold
				state_threshold = my.inf
			def expand_state():
				nonlocal state_threshold, iedges_to_pick, add_fail_count, flag_reject_add
				self.state_threshold = state_threshold = math.floor(state_threshold * expand_state_rate)
				iedges_to_pick = iedges.copy()
				add_fail_count = 0
				flag_reject_add = False
				#
				if self._print.expand_state:
					print(f'expand state to {state_threshold}')
				return 
			def try_expand_model():
				nonlocal model, res
				
				# expand
				for m in model_net.models():
					if m.var() <= expand_rate_threshold * state_threshold:
						# d(model_net.net.degree(m))
						model_net.del_model(m)
						# assert model_net.net.degree(m) == 0, model_net.net.degree(m)
						assert empty(m.inter_info), list(m.inter_info)
						m.walk(state_threshold=state_threshold, order_mode=self.order_mode)
						res = model_net.add_update_model(m, description='expand')
						model = m
						return True
				return False
			def add_new_model():
				nonlocal model, res
					# cover_total = sum( m.size() for m in model_net.models() )
					# # start
					# if pick_start == 'auto1':
					# 	"""
					# 		在models覆盖度最小的点中随机选择
					# 		覆盖 <= 4
					# 		"""
					# 	min_cover = my.inf
					# 	for i, models in model_net.i_models_map.items():
					# 		if i not in iedges_to_pick: continue
					# 		cover = len(models)
					# 		if cover < min_cover:
					# 			if cover > 4: continue
					# 			min_cover = cover
					# 			picks = [i]
					# 		elif cover > min_cover:
					# 			continue
					# 		else:
					# 			picks.append(i)
					# 	if min_cover is my.inf: return False # 所有点覆盖度 > 4
					# 	istart = my.random.pick(picks)
					# 	# d(min_cover)
					# elif pick_start == 'node0':
					# 	"""
					# 		node=0
					# 		"""
					# 	adj_edges = hg.adj_n_e[0]
					# 	start = min(adj_edges, key=my.set.hash)
					# 	istart = e_i_map[start]
					# elif pick_start == 'random':
					# 	raise
					# 	istart = my.random.pick(iedges_to_pick)
					# else: raise Exception(f'{pick_start}')
					# iedges_to_pick.remove(istart)
					# start = i_e_map[istart]
				start = my.random.pick(edges)
				#
				model = Model.empty_model(solver=solver)
				model.walk(start=start, state_threshold=state_threshold, order_mode=self.order_mode)
				assert not empty(model.states)
				res = model_net.add_update_model(model, description='add')
				return True
			#
			def step():
				nonlocal model, res
				while 1:
					# add
					flag_no_add = flag_reject_add or empty(iedges_to_pick)
					if not flag_no_add:
						flag = add_new_model()
						if flag: return
					# add-state
					expand_state()
					continue
				
			#
			edges = hg.edges
			self.i_e_map = i_e_map = { i : e for i, e in enumerate(hg.edges) }
			self.e_i_map = e_i_map = DictOfSet( (e, i) for i, e in i_e_map.items() )
			self.iweight = iweight = { i: hg.weight[i_e_map[i]] for i in self.i_e_map }
			self.tmp_i_e_map = self.i_e_map.copy()
			self.tmp_e_i_map = self.e_i_map.copy()
			self.tmp_iweight = self.iweight.copy()
			id_i_e_map = id(i_e_map)
			
			self.model_net = model_net = ModelNet(solver=self)
			# tmp
			model = None
			res = None
			# main- loop
			while 1:
				"""
					i_e_map 和 e_i_map id不变
					"""
				# assert not empty(self.i_e_map), self.hg.show()
				iedges = set(i_e_map)
				assert id(i_e_map) == id_i_e_map
				#
				iedges_to_pick = set(iedges)
				while 1: # until assert or finish
					# pick-start
					# pre
					# main
					step()
					# debug
					edges_used = [ i_e_map[i] for i in model.field ]
					assert not empty(model.states)
					if not flag_reject_add and res != 'continue':
						add_fail_count = 0
					if res == 'assert':
						model_net_assert_edges()
						break
					elif res == 'finish':
						self.final_model = model_net._finish
						self.final_hgs = [ s.to_hg_by_edges(i_e_map) for s in self.final_model.states ]
						if self._show.valid_add:
							hg.draw(hl_edges1=hg.edges)
						return True
					elif res == 'continue':
						add_fail_count += 1
						if add_fail_count >= 5:
							flag_reject_add = True
						model_net.del_model(model)
					elif res == 'fail':
						raise
					else: raise Exception(f'{0}')
					if self._show.invalid_add:
						if self.ishow: myplt.cap(self.ishow)
						# d.count()
						hg.draw(hl_edges=edges_used)
						# d(hg.len())
						if self.ishow: 
							myplt.show_when_full()
							# a = my.kb.wait('F6')
							# print(a)
							# myplt.close()
					#
					# post
						# count_iter += 1
						# if count_iter == iter_threshold:
						# 	return_False()
		# info
		def mst_len(self):
			return self.mst.len() + self.shrink
		# debug
			
		# getter
		def get_u(self):
			return self._get_u
		def set_get_u(self, v=None):
			get_u = self._get_u = self.hg.Ru_getter(v)
			return get_u
		def del_get_u(self):
			r = self._get_u
			del self._get_u
			return self
		# assert, map

		def set_map(self, e, items, *, false_exist=None):
			"""
				edge-map含有e的添加items, 为items设置tail-map
				tail_map删除e
				"""
			"""
				items: bool | edge | [ (e_, sym) .. ]
				"""
			"""dynamic-fileter
				说明
					修改相关信息
					map(e_) 不改变i和weight
				items=True/False/(e_, 1)
				pc(True/False)
					在i_e_map和e_i_map中删除该边
				pc(e_, 1)
					将map中e替换成e_
				"""
			if self.flag_dynamic_filter >= 2:
				if self._print.set_map:
					print(f'map {e} {items}')
				if 0: 
					if items == True:
						self.hg.draw(hl_edges=[e], title='True')
					elif items == False:
						self.hg.draw(hl_edges=[e], title='False')
					else:
						e_ =items[0][0]
						self.hg.draw(hl_edges=[e], hl_edges1=[e_], title='map')
					# myplt.show()
				self.model_net.set_map(e, items, false_exist=false_exist) # 必要, 需要用到tmp
				assert self.restore
				if items == True or items == False:
					i = self.tmp_e_i_map.pop(e)
					e1 = self.tmp_i_e_map.pop(i)
					del self.tmp_iweight[i]
					# assert e1 is e, (e1, e)
				else:
					assert not isinstance(items, set)
					assert len(items) == 1 and items[0][1] == 1, items
					e_ = items[0][0]
					i = self.tmp_e_i_map.pop(e)
					#
					self.tmp_i_e_map[i] = e_
					self.tmp_e_i_map[e_] = i
					# self.iweight[i] = ... # 不变
			if not self.restore: return
			#
			roots = self.tail_map.pop(e)
			if isinstance(items, bool):
				flag = 2 * items - 1
				for root in roots:
					map = self.edge_map[root]
					sym = map.pop(e)
					match flag * sym:
						case 1:
							if len(map) == 0:
								self.edge_map[root] =True
						case -1:
							self.edge_map[root] = False
							for e_, sym_ in map.items():
								self.tail_map[e_].remove(root)
						case _: raise Exception(f'{flag, sym}')
			else:
				assert not isinstance(items, set)
				for e1, val1 in items:
					self.tail_map.set_default(e1, SetOfSet())
				for root in roots:
					map = self.edge_map[root]
					sym = map.pop(e)
					for e_, val_ in items:
						assert e_ not in map
						assert val_ in {1, -1}
						map[e_] = val_ * sym
						self.tail_map[e_].add(root)
			return self
			assert root in self.edge_map
			target_ = self.edge_map[root]
			self.edge_map[root] = target
			# del root
			del self.tail_map[target_]
			if isinstance(target, set):
				self.tail_map[target] = root
			elif target in [False, True]:
				pass
			else: raise Exception(f'{0}')
		def transform(self, e, target, *, false_exist=None, map=Pass):
			"""
				map: 
					None: 无
					Pass: 默认
				"""
			hg = self.hg
			match target:
				case True:
					self.hg.disconnect(e)
					if self.trace:
						assert self.trace.has_edge(e)
						self.trace.disconnect(e)
				case False:
					self.hg.disconnect(e)
					if self.trace:
						if self.trace.has_edge(e):
							d((e, target))
							self.trace.draw(hl_edges=[e], title='trace')
							self.hg.draw(hl_edges=[e], title='hg')
							myplt.show()
							raise
				case t if isinstance(t, set):
					w = hg.weight[e]
					self.hg.disconnect(e)
					self.hg.connectw(target, w)
					if self.trace:
						if self.trace.has_edge(e):
							self.trace.disconnect(e)
							self.trace.connectw(target, w)
						else:
							pass
					target = [( target, 1 )]
				case _:
					raise Exception(f'{target}')
			match map:
				case my.Pass:
					self.set_map(e, target, false_exist=false_exist)
				case None: pass
				case _: raise Exception(f'{map}')
				
			return self
		def get_reserved_node(self, nodes):
			hg = self.hg
			return max( nodes, key=lambda n: hg.degree(n) )
		def get_compressed_edge(self, e, inter, reserved):
			"""
				压缩多个点
				允许有重复
				"""
			assert reserved in e
			r = e.difference(inter)
			r.add(reserved)
			return r
		def combine_nodes(self, nodes,*, exclude=[], mapper=[], reserved=None):
			
			"""
				说明
					处理hg的边 以assert=1为标准进行映射（除了exculded中的）
					连接两个点以上的删除
				arg
					mapper: 设置映射值
					exclude: 不进行压缩\重复删除\映射, 返回压缩操作
					return：强制压缩的压缩后的边
				"""
			hg = self.hg
			if reserved == None: reserved = self.get_reserved_node(nodes)
			del_nodes = my.set.removed(nodes, reserved)
			mapper = DictOfSet(mapper)
			# setup state map
			state_map = DictOfSet()
			for n in nodes:
				for e in hg.adj_n_e[n]:
					if e in state_map: state_map[e] = None
					else:
						state_map[e] = n
			# cope adj-state
			for adje, n in state_map.items():
				if adje in exclude: continue
				map = mapper.get(adje, Pass)
				if n == None: 
					self.transform(adje, False, map=map)
					continue
				if n == reserved: continue
				adje_ = my.set.changed(adje, n, reserved)
				if adje_ in hg.edges:
					new_w = hg.weight[adje]
					old_w = hg.weight[adje_]
					if new_w >= old_w:
						self.transform(adje, False, map=map)
					else:
						self.transform(adje_, False, map=map)
						self.transform(adje, adje_, map=map)
				else:
					self.transform(adje, adje_, map=map)
			hg.del_nodes(del_nodes)
		def combine_nodes_assert1_no_cycle(self, nodes, group):
			"""
				说明:
					处理map和connect
				"""
			"""pc

				找到相邻的所有边state_map e:state
					None: 删除（有两个以上交点）
					n: 交点
				对state_map中的每个边进行处理
					None：删除
					n: 若目标位置有边，留下权重较小的，
						否则留下
				"""
			assert self.assert_no_cycle
			hg = self.hg
			reserved = max( nodes, key=lambda n: hg.degree(n) )
			del_nodes = my.set.removed(nodes, reserved)
			# setup state map
			state_map = DictOfSet()
			for n in nodes:
				for e in hg.adj_n_e[n]:
					if e in state_map: state_map[e] = None
					else:
						state_map[e] = n
			## 剔除在group中的边
			for e in group:
				del state_map[e]
				self.transform(e, True)
			# cope adj-state
			for adje, n in state_map.items():
				if n == None: 
					self.transform(adje, False, false_exist=True)
					continue
				if n == reserved: continue
				adje_ = my.set.changed(adje, n, reserved)
				if adje_ in hg.edges:
					new_w = hg.weight[adje]
					old_w = hg.weight[adje_]
					if new_w > old_w:
						self.transform(adje, False, false_exist=False)
					elif new_w == old_w:
						self.transform(adje, False, false_exist=True)
					else:
						self.transform(adje_, False, false_exist=False)
						self.transform(adje, adje_)
				else:
					self.transform(adje, adje_)
			
			hg.del_nodes(del_nodes)
		def combine_nodes_assert1_cycle(self, nodes, group):
			raise
			"""pc
				找到相邻的所有边state_map e:state
					n: 交点
				对state_map中的每个边进行处理
					None：删除
					n: 若目标位置有边，留下权重较小的，
						否则留
				算法
					计算所有相邻边的相交集合，合并到一个点 （除了完全在nodes中的）
				说明
					不需要group
				pc

				"""
			hg = self.hg
			reserved = max( nodes, key=lambda n: hg.degree(n) )
			del_nodes = my.set.removed(nodes, reserved)

			# inter map
			inter_map = DictOfSet()
			for n in nodes:
				for e in hg.adj_n_e[n]:
					if e not in inter_map:
						inter_map[e] = set()
					inter_map[e].add(n)
			# cope
			for adje, ns in inter_map.items():
				if len(ns) == len(adje): # in nodes
					self.transform(adje, True)
				elif len(ns) == 1 and reserved in ns: # 只与reserved有交集
					continue
				else:
					adje_ = adje.difference(ns)
					adje_.add(reserved)
					if adje_ in hg.edges:
						new_w = hg.weight[adje]
						old_w = hg.weight[adje_]
						if new_w >= old_w:
							self.transform(adje, False)
						else:
							self.transform(adje_, False)
							self.transform(adje, adje_)
					else:
						self.transform(adje, adje_)
			
			hg.del_nodes(del_nodes)
		def combine_nodes_assert1(self, *gs, **ks):
			if self.assert_no_cycle:
				return self.combine_nodes_assert1_no_cycle(*gs, **ks)
			else:
				return self.combine_nodes_assert1_cycle(*gs, **ks)

		def assert_edges_1(self, edges):
			"""
				将相连的edge组合，缩小成一个点（取连接总边数最多的）
				"""
			edges = SetOfSet(edges)
			hg = self.hg
			group_hg = HyperGraph.from_edges(edges)
			groups = group_hg.edgeSubs()
			if not self.restore:
				for e in edges:
					self.declare_shrink(hg.weight[e])
			for group in groups:
				# cope group edges
				nodes = my.set.unionm(group)
				self.combine_nodes_assert1(nodes, group)
			# d
			# for e in edges:
			# 	if e in d.mst.edges:
			# 		d.mst.disconnect(e)

		def assert_edges_0(self, edges):
			for e in edges:
				self.assert_edge_0(e)
		def assert_edge_0(self, e):
			self.transform(e, False, false_exist=False)
		def assert_edge_1(self, e):
			self.assert_edges_1([e])
			return self
		def assert_edge0880(self, e):
			"""
				保留最多边相连的节点
				与e有两个以上相交节点的删除
				与删除节点相邻边映射，重复的保留最小
				"""
			hg = self.hg
			reserved_node = max(e, key=lambda n: hg.degree(n))
			del_nodes = {n for n in e if n != reserved_node}
			# adj_edges
			adj_edge_map = DictOfSet() # e : n   None:矛盾
			for n in del_nodes:
				es = hg.adj_n_e[n]
				for e1 in es:
					if e is e1: continue
					if e1 in adj_edge_map: 
						adj_edge_map[e1] = None
						continue
					adj_edge_map[e1] = n
			for e2 in hg.adj_n_e[reserved_node]:
				if e2 is e: continue
				if e2 in adj_edge_map:
					adj_edge_map[e2] = None

			adj_edges2 = []
			for adje, n in adj_edge_map.items():
				if n == None: # del_edge
					self.assert_edge_0(adje)
					continue
				adje_ = adje.copy()
				adje_.remove(n)
				adje_.add(reserved_node)
				if adje_ in hg.edges:
					new_w = hg.weight[adje]
					old_w = hg.weight[adje_]
					if new_w >= old_w:
						self.assert_edge_0(adje)
					else:
						self.assert_edge_0(adje_)
						self.transform_to_edge(adje, adje_)
				else:
					self.transform_to_edge(adje, adje_)
			#
			self.set_map(e, True)
			hg.disconnect(e)
			hg.del_nodes(del_nodes)
		# contrdictory pairs
		def pairs_not_11(self) -> list:
			"""
				1.共用多于一个点的
				"""
			assert self.assert_no_cycle
			hg = self.hg
			pairs = []
			for e in hg.edges:
				adj_state = DictOfSet()
				for n in e:
					for e1 in hg.adj_n_e[n]:
						if e1 in adj_state: adj_state[e1] = True
						else: adj_state[e1] = False
			#
				adj_state.pop(e)
				pairs += [  (e, e_) for e_,state in adj_state.items() if state and id(e) < id(e_) ]
			return pairs
		def pairs_contro_Ru(self) -> 'SetOfSetOfSet':
			"""
				1.至少有一个共同交点 && sum > Ru0

				"""
			hg = self.hg
			pairs = SetOfSetOfSet()
			get_u = self.get_u()
			for n in hg.nodes:
				for e1, e2 in my.comb( hg.adj_n_e[n], 2 ):
					nodes = e1 | e2
					u0 = get_u(nodes)
					w1 = hg.weight[e1]
					w2 = hg.weight[e2]
					delta = w1 + w2 - u0
					if delta > 0:
						pairs.add( (e1, e2) )
			return pairs
		def pairs_01(self) -> 'SetOfSetOfSet':
			"""
				1.一个点仅连接两条边且两条边有2点以上重叠
				"""
			hg = self.hg
			pairs = SetOfSetOfSet()
			for n in hg.nodes:
				es = hg.adj_n_e[n]
				if len(es) != 2: continue
				e1, e2 = es
				if len(e1 & e2) == 1: continue
				pairs.add( (e1, e2) )
			return pairs
		def only1_groups(self):
			"""
				一个点n连接的所有边且两两矛盾
				矛盾：

				"""
			hg = self.hg
			groups = []
			pairs_contro = self.pairs_contro_Ru()
			def try_group(group):
				if len(group) <= 1: return
				for e1, e2 in my.comb( group, 2 ):
					if (e1, e2) not in pairs_contro:
						return
				groups.append(group)
			for n in hg.nodes:
				group = hg.adj_n_e[n]
				try_group(group)
			return groups
		# filter
		def filter0(self):
			pass
		def filter1(self):
			"""
				steps:
					清除悬挂边
					建立BW-net
					B-net清除3元以上边
				"""
			hg = self.hg
			ori_hg = self.ori_hg
			while 1:
				mf = False
				#
				mf_ = self.filter_tgraph()
				mf |= mf_
				if mf_ and 5 <= self.debug < 6:
					self.draw(title='BW')
				# #
				# mf_ = self.filter_contain01_pair()
				# mf |= mf_
				# if mf_ and 5 <= self.debug < 6:
				# 	self.draw(title='contain01')
				# #
				mf_ = self.filter_hang()
				mf |= mf_
				if mf_ and 5 <= self.debug < 6:
					self.draw(title='hang')
				# #
				# if not self.restore:
				# 	mf_ = self.filter_only1()
				# 	mf |= mf_
				# 	if mf_ and 5 <= self.debug < 6:
				# 		self.draw(title='only1', edge_label=1)
				#
				if not mf: break
			if self.debug > 0:
				before_len = len(ori_hg.edges)
				after_len = len(hg.edges)
				print(f'filter-summary: remained: {after_len} / {before_len} {after_len/before_len:.3}')
			if self.debug >= 1:
				l_hang = self.record.hang_edges
				l_ru = self.record.ru_edges
				l_rb = self.record.rb_edges
				l_contain = self.record.contain01_pairs
				c_hang = len(l_hang)
				c_ru = len(l_ru)
				c_rb = len(l_rb)
				c_contain = len(l_contain)
				print(f'hang: {c_hang} ru: {c_ru} rb: {c_rb} contain: {c_contain}')
				if self.debug >= 2:
					print(f'hang: {mystr(l_hang)}')
					print(f'ru: {mystr(l_ru)}')
					print(f'rb: {mystr(l_rb)}')
					print(f'contain: {mystr(l_contain)}')
			return self

		def filter2(self):
			"""
				steps:
					清除悬挂边
					建立BW-net
					B-net清除3元以上边	
				"""
			hg = self.hg
			ori_hg = self.ori_hg
			while 1:
				mf = False
				#
				mf_ = self.filter_tgraph()
				mf |= mf_
				if mf_ and 5 <= self.debug < 6:
					self.draw(title='BW')
				#
				mf_ = self.filter_contain01_pair()
				mf |= mf_
				if mf_ and 5 <= self.debug < 6:
					self.draw(title='contain01')
				#
				mf_ = self.filter_hang()
				mf |= mf_
				if mf_ and 5 <= self.debug < 6:
					self.draw(title='hang')
				#
				if not self.restore:
					mf_ = self.filter_only1()
					mf |= mf_
					if mf_ and 5 <= self.debug < 6:
						self.draw(title='only1', edge_label=1)
				
				if not mf: break
			if self.debug > 0:
				before_len = len(ori_hg.edges)
				after_len = len(hg.edges)
				print(f'filter-summary: remained: {after_len} / {before_len} {after_len/before_len:.3}')
			if self.debug >= 1:
				l_hang = self.record.hang_edges
				l_ru = self.record.ru_edges
				l_rb = self.record.rb_edges
				l_contain = self.record.contain01_pairs
				c_hang = len(l_hang)
				c_ru = len(l_ru)
				c_rb = len(l_rb)
				c_contain = len(l_contain)
				print(f'hang: {c_hang} ru: {c_ru} rb: {c_rb} contain: {c_contain}')
				if self.debug >= 2:
					print(f'hang: {mystr(l_hang)}')
					print(f'ru: {mystr(l_ru)}')
					print(f'rb: {mystr(l_rb)}')
					print(f'contain: {mystr(l_contain)}')
			return self
		def filter_hang(self):
			"""
				一个节点只与一条边相连
				"""
			hg = self.hg
			filter_list = []
			mf = False
			while 1:
				modified = False
				for n in list(hg.nodes):
					if n not in hg.nodes: continue
					if hg.degree(n) == 1:
						e = hg.adj_n_e[n][0]
						filter_list.append(e)
						self.assert_edge_1(e)
						modified = True
						mf = True
				if not modified: break
			if self.debug:
				self.record.hang_edges += filter_list
			if self.debug >= 2:

				print(f'{len(filter_list)} hang-edges filtered')
			return mf
		def filter_tgraph000(self):
			"""
				tgraph: 每个超边完全扩展后的图
				Bweight：临界值
				Wvalweight: tgraph中每两点之间的val值
				Weight: 
				算法
					Wweight: 
						二元：Wvalweight的瓶颈
					Bweight:
						二元：二元weight的瓶颈
						多元：min（自身边值，二元完全B的mst）
				过滤算法：
					1.根据Bweight删除值不同的超边
					2.根据Wweight删除值不同的超边
				"""
			def get_u(s:set):
				"""
					算法：二元上限最小树 / in-complete
					"""
				assert isinstance(s, set)
				assert len(s) >= 2
				if s in Bweight: return Bweight[s]
				Bvals = []
				# complete_hg
				# if s in complete_hg.edges:
				# 	Bvals.append(complete_hg.weight[s])
				# 2 mst
				Bgraph = Graph.from_edges( my.comb.comb2(s) )
				Bval2 = Bgraph.mst_len(weight=Bweight2)
				Bvals.append(Bval2)
				Bval = min(Bvals)
				Bweight[s] = Bval
				return Bval
				#

			def get_sup_n_val(sup, n):
				if len(sup) == 2: return hg.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = hg.weight[sup]
				r = w - B_oppos
				return max(r, 0) 
			debug = self.debug
			hg = self.hg
			complete_hg = self.complete_hg
			pos = self.ori_hg.get_pos()
			modified = False
			# tgraph
			# tedges = []
			# for e in hg.edges:
			# 	for e2 in my.comb.comb2(e):
			# 		tedges.append(sorted2(e2))
			# edges2 = [ sorted2(e) for e in hg.edges if len(e) == 2 ]
			# weight_edge2 = { sorted2(e): w for e, w in hg.wedges() if len(e) == 2}
			# graph2 = Graph.from_wedges(weight_edge2.items())
			# bone = graph2.mst()
			# tgraph = Graph.from_edges(tedges, pos=hg.get_pos())
			self.tgraph = hg.tgraph_pos()

			# Bweight
			# Bweight2 = tgraph.get_bottle_neck_from_mst(bone, weight=weight_edge2, mode='v')
			Bweight2 = hg.get_Ru_dict1_normal()
			Bweight = DictOfSet([ (set(e2), v) for e2, v in Bweight2.items() ])
			# Wweight
			#. e2sup_val
			sup_n_val = DictOfSet()
			for sup in hg.edges:
				sup_n_val[sup] = map_ = {}
				for n in sup:
					map_[n] = get_sup_n_val(sup, n)

			#. Wvalweight
			Wvalweight = {}
			for sup in hg.edges:
				for e2 in my.comb.comb2(sup):
					a, b = e2 = sorted2(e2)
					v = max( sup_n_val[sup][a], sup_n_val[sup][b] )
					if e2 not in Wvalweight or Wvalweight[e2] > v:
						1
						Wvalweight[e2] = v
			Wweight2 = tgraph.get_bottle_neck(weight=Wvalweight, mode='v') # dict
			Wweight = DictOfSet([ (set(e2), v) for e2, v in Wweight2.items() ])
			# debug
			if self.debug >= 2:
				tgraph.draw(edge_label=Bweight2, node_label=0, title='Bweight2')
				tgraph.draw(edge_label=Wweight2, node_label=0, title='Weight2')
				# tgraph.draw(edge_label=Wvalweight, node_label=0, title='Wvaleight')
				hg.draw(edge_label=[(e, get_u(e)) for e in hg.edges ], node_label=0, title='Bweight')
				hg.draw(edge_label=[ (e, Wweight.get(e, '')) for e in hg.edges], node_label=0, title='Wweight')

			# Bweight-filter
			ufilter_conflict_map = {} # len: e
			ufilter_list = []
			for e in hg.edges:
				B = get_u(e)
				w = hg.weight[e]
				if B < w: 
					ufilter_list.append(e)
				elif B == w:
					# ufilter_conflict_map[w] = e
					...
				else: pass
			ufilter_list += list(ufilter_conflict_map.values())

			# Wweight-filter
			bfilter_conflict_map = {} # len: e
			bfilter_list = []
			for e in hg.edges:
				if len(e) != 2: continue
				w = hg.weight[e]
				Wval = Wweight(e)
				if Wval > w:
					raise
					bfilter_list.append(e)
				elif Wval == w:
					bfilter_conflict_map[w] = e
				else: pass
			bfilter_list += list(bfilter_conflict_map.values())
			
			# do-filter
			for e in ufilter_list:
				modified = True
				self.transform(e, False)
			self.assert_edges_1(bfilter_list)
			if not empty(bfilter_list): modified = True
			if debug:
				print(f'{len(ufilter_list)} edges assert=0 by Bweight')
				print(f'{len(bfilter_list)} edges assert=0 by Wweight')
			return modified
		def filter_tgraph(self):
			"""
				tgraph: 每个超边完全扩展后的图
				Bweight：临界值
				Wvalweight: tgraph中每两点之间的val值
				Weight: 
				算法
					Wweight: 
						二元：Wvalweight的瓶颈
					Bweight:
						二元：二元weight的瓶颈
						多元：min（自身边值，二元完全B的mst）
				过滤算法：
					1.根据Bweight删除值不同的超边
					2.根据Wweight删除值不同的超边
				"""

			def get_sup_n_val(sup, n):
				if len(sup) == 2: return hg.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = hg.weight[sup]
				r = w - B_oppos
				return max(r, 0) 
			debug = self.debug
			hg = self.hg
			pos = self.ori_hg.get_pos()
			modified = False
			tgraph = hg.tgraph_pos()
			# get_u get_b
			get_u = hg.Ru_getter()
			get_u2 = lambda ne: get_u(set(ne))
			get_b = hg.Rb_getter()
			get_b2 = lambda e: get_b(set(e))
			get_b_ignore = hg.Rb_getter_ignore(get=get_b)
				
			# debug
			if self.debug >= 6 and 1:
				tgraph.draw(edge_label=get_u2, node_label=0, title='u-tgraph')
				tgraph.draw(edge_label=get_b2, node_label=0, title='b-tgraph')
				# tgraph.draw(edge_label=Wvalweight, node_label=0, title='Wvaleight')
				hg.draw(edge_label=[(e, get_u(e)) for e in hg.edges ], node_label=0, title='Ru')
				hg.draw(edge_label=[ (e, get_b_ignore(e)) for e in hg.edges], node_label=0, title='Rb')

			# u-filter
			ufilter_conflict_map = {} # len: e
			ufilter_list = []
			for e in hg.edges:
				u = get_u(e)
				w = hg.weight[e]
				if u < w: 
					ufilter_list.append(e)
				elif u == w:
					# ufilter_conflict_map[w] = e
					...
				else: pass
			ufilter_list += list(ufilter_conflict_map.values())
			# get_b-filter
			bfilter_conflict_map = {} # len: e
			bfilter_list = []
			for e in hg.edges:
				if len(e) != 2: continue
				w = hg.weight[e]
				b = get_b(e)
				# if b > get_u(e):
				# 	get_r = hg.R_getter()
				# 	re = get_r(e)
				# 	mst = hg.cacu_mst()
				# 	flag = e not in mst.edges
				# 	1
					
				if b > w:
					raise
					bfilter_list.append(e)
				elif b == w:
					1
					bfilter_conflict_map[w] = e
				else: pass
			bfilter_list += list(bfilter_conflict_map.values())
			
			li = d(my.setLike.inter(ufilter_list, bfilter_list))
			# do-filter
			# filter-u
			if debug >= 6:
				if len(ufilter_list) > 0:
					hg.draw(title='Ru-one', hl_edges1=(ufilter_list), edge_label=1)
			for e in ufilter_list:
				modified = True
				self.transform(e, False)
			# filter-b
			if debug >= 6:
				if len(bfilter_list) > 0:
					hg.draw(title='Rb-one', hl_edges1=(bfilter_list), edge_label=1)
			self.assert_edges_1(bfilter_list)
			#
			if not empty(bfilter_list) or not empty(ufilter_list): modified = True

			if self.debug >= 1:
				self.record.ru_edges += ufilter_list
				self.record.rb_edges += bfilter_list
			if debug >= 2:
				print(f'{len(ufilter_list)} edges assert=0 by Ru')
				print(f'{len(bfilter_list)} edges assert=0 by Rb')
			return modified
		def filter_contain01_pair(self):
			"""
				说明：
					包含且矛盾关系的两条边
					小边合并掉
				相关：
					内含性：只要相关点还在就，相关边不被改变，就不影响
					没有共同端点则不相关
				若压缩的位置有边：
					。。。
				"""
			hg = self.hg
			pairs_01 = self.pairs_01() 
			pairs = []
			modified = False
			count = 0
			# filter subset
			for pair in pairs_01:
				e1, e2 = pair
				if len(e1) > len(e2): pair = e1, e2 = e2, e1
				if not e1.issubset(e2): continue
				pairs.append(pair)
			#
			ir_pairs = my.hypergraph.irrelavant_subs(pairs)
			#
			for pair in ir_pairs:
				e1, e2 = pair
				w1 = hg.weight[e1]
				w2 = hg.weight[e2]
				w_ = w2 - w1
				if w_ <= 0: continue
				modified = True
				if not self.restore:
					self.declare_shrink(w1)
				assert w_ > 0, w_
				inter = e1
				reserved = self.get_reserved_node(inter)
				e2_ = self.get_compressed_edge(e2, inter, reserved)
				#
				if self.debug >= 1:
					self.record.contain01_pairs.append((e1, e2))
				self.hg.disconnect(e1)
				self.hg.disconnect(e2)
				if e2_ in hg.edges:
					if hg.weight[e2_] <= w_: # 不更新e2_
						self.set_map(e1, True)
						self.set_map(e2, False)
					else:
						hg.set_edge_weight(e2_, w_)
						self.set_map(e2_, False)
						self.set_map(e1, [(e2_, -1)])
						self.set_map(e2, [(e2_, 1)])
				else:
					self.hg.connectw(e2_, w_)
					self.set_map(e1, [(e2_, -1)])
					self.set_map(e2, [(e2_, 1)])

				self.combine_nodes(inter, reserved=reserved)
				count += 1
			# summary
			if self.debug >= 2:
				print(f'{count} edges compressed by contain01-pair')
			return modified
		def filter_only1(self):
			"""
				算法
					每组矛盾的上限假设 s-u0
					取最小上限
				操作
					每条边的距离减少
				后处理
					0距离边合并
					其他达到上限的组合边重映射到两条边
					pc
						对每队非归0组合
							删除e0，将e0映射到e1+e2
							e1->
							e2->
						只考虑只有一对归0的情况
						对每条归0组合
							一定只有一条归0
							合并+重映射
				附加要求：所有上限中两条边的组合实在存在, du计算方式为sum-u0, dw=sum-w0
					要求：所有du >= dw > 0
						delta = min(dw) <= min(du)
						所有du==min(dw)值的组合都有dw
					一条边归0 <=> 是包含关系
				假设：
					若归0：只有一条边归0，且合并点后所有矛盾消失
					不归0：
				pc
					归0
						合并
					不归0
						删除并重映射所有e0
				"""
			"""
				破坏模式
					减法
					交给别人
				ps
				"""
			hg = self.hg
			weight = hg.weight
			get_u = self.set_get_u()
			only1_groups = self.only1_groups()
			mf = False
			def try_pairs(pairs):
				min_dw = my.inf
				min_dws = [] # 只记录最小的 (e1, e2)
				min_no_w_du = my.inf
				min_du = my.inf
				for e1, e2 in pairs:
					s = weight[e1] + weight[e2]
					e0 = e1 | e2
					u0 = get_u(e0)
					du = s - u0
					if du <= 0:
						return False
					if du < min_du:
						min_du = du
						
					# w
					flag_w = hg.has_edge(e0)
					if flag_w:
						w0 = weight[e0]
						dw = s - w0
						if dw <= 0 or dw > du: return False
						if dw < min_dw:
							min_dw = dw
							min_dws.clear()
							min_dws.append((e1, e2))
						elif dw == min_dw:
							min_dws.append((e1, e2))
						else: pass
					else:
						if du < min_no_w_du:
							min_no_w_du = du
				if min_no_w_du <= min_dw: return False
				if min_du < min_dw: return False
				for e1, e2 in min_dws:
					e0 = e1 | e2
					if not hg.has_edge(e0):
						return False
				return min_dws, min_dw
			# get valid groups
			group_infos = DictHash(hash=id)
			for group in only1_groups:
				if len(group) <= 1: continue
				# cap
				pairs = my.comb.comb(group, 2)
				res = try_pairs(pairs)
				if res == False: continue
				else:
					min_dws, delta = res
					assert delta > 0
					group_infos[group] = res
			# irrelavant groups
			groups_ = my.hypergraph.irrelavant_subs(group_infos.keys())
			for group in groups_:
				min_dws, delta = group_infos[group]
				mf = True
				if self.debug >= 6:
					hg.draw(title='only1-one', edge_label=1, hl_edges1=group)
				#
				# weight
				flag_0 = False
				for e in group:
					w = weight[e]
					w_ = w - delta
					if self.restore:
						assert w_ >= 0
					hg.set_edge_weight(e, w_) # 更新权重
					if self.restore:
						if w_ == 0:
							assert flag_0 == False
							flag_0 = True
				
				if self.restore:
					raise Exception(f'{0}')
				else:
					self.declare_shrink(delta)
			if self.debug >= 2:
				print(f'{len(groups_)} group shrinked by only1')
			self.del_get_u()
			return mf
		# map
		def declare_shrink(self, v):
			self.shrink += v
			return self
		def map_mst(self, mst_):
			"""
				restore
				"""
			if not self.restore: return mst_
			if not (self.flag_filter or self.flag_dynamic_filter): return mst_
			edges = []
			ori_hg = self.ori_hg
			for e in ori_hg.edges:
				if e not in self.edge_map: # 自己
					raise
					if e in mst_.edges: edges.append(e)
					continue
				mapping = self.edge_map[e]
				match mapping:
					case True: flag_exist = True
					case False: flag_exist = False
					case map if isinstance(map, DictOfSet):
						flag_exist = all( (e1 in mst_.edges) == (val1 == 1) for e1, val1 in map.items() )
					case _: raise Exception(f'{mapping}')
				if flag_exist:
					edges.append(e)
			mst = ori_hg.sub_from_edges(edges)
			return mst
		# main
		def solve(self, return_solver=0, **ks):
			"""
				attr
					mst_ mst 
				"""
			hg = self.hg
			assert hg.is_span()
			if len(hg.edges) == 0:
				self.mst_ = self.mst = hg
				return self
			# filter
			if self.flag_filter > 0:
				method_name = f'filter{self.flag_filter}'
				if self.debug >= 4:
					cap = myplt.cap()
					myplt.cap(6)
					myplt.window_title('filter')
					self.ori_hg.draw(title='ori', node_label=1, edge_label=1)
				getattr(self, method_name)()
				if self.debug >= 4:
					self.draw(title='filtered', edge_label=1)
			# dynamic-filter
			if self.filter_mode:
				solved = self.solve_filter_mode()
			else:
				if self.flag_dynamic_filter > 0:
					name = f'dynamic_filter{self.flag_dynamic_filter}'
					call = getattr(self, name)
					solved = call()
				else: raise
			# cacu
			assert solved
			if solved:
				hg = my.pick(self.final_hgs)
				self.mst_ = mst_ = hg
			else:
				method_name = f"cacu_mst{self.cacu_v}"
				mst_ = self.mst_ = getattr(self.hg, method_name)(**ks)
				if self.debug >= 4:
					mst_.draw(title='mst_', edge_label=1)
			# map
			mst = self.mst = self.map_mst(mst_)
			if return_solver: return self
			else: return mst
		# draw
		def get_fake_edges(self):
			"""
				原本不存在的边（考虑权重）
				"""
			hg = self.hg
			ori_hg = self.ori_hg
			r = []
			
			for e in hg.edges:
				if e not in ori_hg.edges or ori_hg.weight[e] != hg.weight[e]:
					r.append(e)
			return r
		def draw(self, **ks):
			fake_edges = self.get_fake_edges()
			self.hg.draw(hl_edges=fake_edges, **ks)
			return self
	class Igroup:
		"""
			attr
				group (anodes)
				iedges: set<int>
				graph
				weight
				matched: bool
			use
				get_edges()
			"""
		"""性质
			born-inode：只与一条边相连
			a-inodes：从anode转换来的inode
			new-inodes = born-inode + a-inode
			new-anodes = 新增的anode
			e = new_inodes(1-0) + a-inodes(0-1) + non-change(-)
			#
			aborted-inode <=> 不与其他活跃点相连 <=> 所在组只有inode
				<=> e只与该组一个点相连： new-inodes & (所在group只有自己 | 是born)
					e可能与多个点相连：new-inodes & (所在group全是new-inode | 是born）
			不加边导致孤立 <=> new-inodes中有aborted-inode
			加边导致孤立 <=> e中全部是aborted且除了e相邻组之外还有其他组
			终结 <=> 组数小于等于1
			"""
		def __init__(self, *, weight, model, iedges=[], group=None):
			if group is None: self.group = my.Group()
			else: self.group = group
			if 0: self.group = my.Inspector(self.group, 'group', print_self=True, before=True, after=True, breakhere=1, inspect='connectm_allownew')
			# self.best1 = best1
			self.iedges = set(iedges)
			# if best1:
			# 	self.weight = OddWeight(weight, iedges)
			# else:
			self.weight = weight
			self.model = model
			if 0: self.edges = Inspector(self.edges, 'edges', print_self=1, before=0, after=1, breakhere=0)
		def __str__(self):
			return f'{self.weight}: {self.group}'
		__repr__ = __str__
		def copy(self):
			r = object.__new__(Igroup)
			r.group = self.group.copy()
			r.iedges = self.iedges.copy()
			if not hasattr(self.weight, 'copy'): ###
				r.weight = self.weight
			else:
				r.weight = self.weight.copy()
			if 0: self.iedges = Inspector(self.iedges, 'edges', print_self=1, before=1, after=1, breakhere=0)
			r.model = self.model
			return r
		# info
		def edges1(self,):
			i_e_map = self.i_e_map()
			# return [ i_e_map[i] for i in self.iedges ]
			# try:
			return [ i_e_map[i] for i in self.iedges ]
			# except KeyError as exc:
			# 	i_list = [ i for i in self.iedges if i not in i_e_map ]
			# 	d(i_list=i_list) 
			# 	raise my.Exception
		
		def edges0(self):
			i_e_map = self.i_e_map()
			edges1 = [ i_e_map[i] for i in self.iedges ]
			return my.set_like.difference(self.edges_field(), edges1)
		def edges_field(self):
			return self.model.edges()
		def to_hg_by_edges(self, i_e_map, **ks):
			edges = self.edges()
			hg = HyperGraph.from_edges(edges, **ks)
			return hg
		def graph(self):
			return self.model.graph
		hg = graph
		edges = edges1
		def i_e_map(self):
			return self.model.i_e_map
		def anodes(self):
			return self.model.anodes
		def inodes(self):
			return self.model.inodes
		def used_nodes(self):
			return self.model.used_nodes
		def unused_nodes(self):
			return self.model.unused_nodes
		# oper
		def add_anode(self, node):
			self.group[node] = set()
		def add_anodes(self, new_anodes):
			for n in new_anodes:
				self.group[n] = set()
		def not_add_e(self, new_inodes):
			for n in new_inodes:
				if n in self.group:
					del self.group[n]
			return self
		def add_e(self, e, ei, w, new_inodes):
			"""
				connectm: e 中除了borni的其他点 (
				"""
			self.iedges.add(ei)
			self.weight += w
			# self.group.check()
			to_connect = {n for n in e if n in self.group}
			self.group.connectm(to_connect)
			# del-included
			for n in new_inodes:
				if n in self.group:
					del self.group[n]
			# if self.best1:
			# 	self.weight._val += w
			# else:
			return self
		# judge
		def judge_add_e(self, e, new_anodes, new_inodes, flag_terminate2, *, no_cycle=1) -> 'not_add, add, terminated':
			
			# not add e
			if self.is_isolated_not_add(new_anodes, new_inodes): not_add = False
			else: not_add = True
			# add-e
			terminated = False
			if no_cycle:
				if self.cause_cycle_edge(e): add = False
				elif self.cause_isolated_edge(e, new_inodes): add = False
				else:
					add = True
			else:
				if self.cause_isolated_edge_noAssertNoCycle(e, new_inodes): add = False
				else:
					add = True
			return not_add, add
		def cause_cycle_edge(self, e):
			ids = set()
			for n in e:
				if n in self.group:
					s = self.group[n]
					id_ = id(s)
					if id_ in ids: return True
					else: ids.add(id_)
				else: continue
			return False
		def is_isolated_not_add(self, new_anodes, new_inodes):
			"""
				前提：不循环
				e相邻的一个点集全部是内点
				说明
					e可能连接一组的多个点
				伪码
					对每个new-inode
						若n不在self.group中（即n是天生inode）: True
						若n在self.group中: 
							组内全部inode
							否则：continue
				"""
			for n in new_inodes:
				if n not in self.group: return True
				s = self.group[n]
				if all( n2 in new_inodes for n2 in s ): return True
			return False
		def cause_isolated_edge(self, e, new_inodes):
			"""
				前提：不循环
				e没有活跃点且连接后集合数量大于1
				说明
					需要检查所有内点
					要求：连接后每个内点必须连接到一个活跃点
				判断：
					e的每个端点都是inode
					e的每个端点要么不在group中，要么自己成一组 (a型）
					且连接前组数 > a型组数
				"""
			if len(e) > len(new_inodes): return False
			#
			count_a = 0
			for n in e:
				if n in self.group:
					if len(self.group[n]) == 1: 
						count_a += 1
						continue
					else: return False
				else: continue
			#
			if len(self.group) > count_a: return True
			else: return False
		def cause_isolated_edge_noAssertNoCycle(self, e, new_inodes):
			"""
				前提：无
				e没有活跃点且连接后集合数量大于1
				说明
					需要检查所有内点
					要求：连接后每个内点必须连接到一个活跃点
				判断：
					e的每个端点都是死的
					且连接后组数<=1
				"""
			raise NotImplemented
			if len(e) > len(new_inodes): return False
			#
			count_a = 0
			for n in e:
				if n in self.group:
					if len(self.group[n]) == 1: 
						count_a += 1
						continue
					else: return False
				else: continue
			#
			if len(self.group) > count_a: return True
			else: return False
		def is_terminated(self):
			"""
				前提：没有未使用点
				说明：只有0/1组活跃点
				伪码：
					组数 <= 1

				"""
			# if not len(new_inodes) == len(e): return False
			return len(self.group) <= 1
		def cover_span(ig1, ig2):
			"""
				g1 > g2
				"""
			return ig1.group.covering(ig2.group)
		def equal_span(ig1, ig2):
			return ig1.group == ig2.group
		def can_be_replaced_by_cover(ig1, ig2):
			return ig2.group.covering(ig1.group) and ig2.weight <= ig1.weight
		def can_be_replaced_by_equal(ig1, ig2):
			return ig2.group == ig1.group and ig2.weight <= ig1.weight
		# check
		def is_possible(self, *, mst=None):
			"""
				出现ms型会出现判断错误
				"""
			return self.graph().state_in_mst(edges1=self.edges(), edges0=self.edges0(), mst=mst)
		def is_possible_igroups(igroups, *, edges_used, i_e_map, hg, mst=None, mst_len=None):
			if mst is None: mst = hg.mst()
			if mst_len is None: mst_len = mst.len()
			for ig in igroups:
				edges1 = ig.edges()
				edges0 = ig.edges0()
				if mst.match_state(edges1=edges1, edges0=edges0): 
					assert ig.is_possible()
					return ig
			for ig in igroups:
				edges1 = ig.edges()
				edges0 = ig.edges0()
				if hg.state_in_mst(edges1=edges1, edges0=edges0, mst=mst, mst_len=mst_len, check_in_provided=False): return True
			return False
		def check_oddWeight(self):
			if isinstance(self.weight, int) and self.weight == 0:
				assert empty(self.iedges)
				return True
			assert isinstance(self.weight, OddWeight)
			assert self.iedges == set(self.weight._li)
			return True
		def match_trace(self):
			trace = self.model.solver.trace
			assert trace
			return self.match_graph(trace)
		def match_graph(self, graph):
			
			edges1 = self.edges1()
			edges0 = self.edges0()
			flag = graph.match_state(edges1=edges1, edges0=edges0)
			return flag
		# model
		def state(self):
			return self.iedges
		def try_combine(ig1, ig2, common_weight, model):
			"""
				pc
				说明
					排除循环,孤立
				"""
			union_iedges = ig1.iedges | ig2.iedges
			union_edges = [ model.i_e_map[i] for i in union_iedges ]
			# main
			# nodeSubs = my.hypergraph.try_nodeSubs_by_edges_no_cycle(union_edges)
			# if nodeSubs == False: 
			# 	assert not model.graph.try_get_groupMap_by_edgesNodesAnodes_checkIsolateCycle(union_edges, anodes)
			# 	return False
			# anodeGroups = my.set.group_by_sets_isolate_overflow(anodes, nodeSubs)
			# group_map = MstGroupMap(anodeGroups)
			group_map = model.graph.try_get_groupMap_by_edgesNodesAnodes_checkIsolateCycle(union_edges, model.used_nodes, model.anodes)
			if group_map == False:
				return False
			w = ig1.weight + ig2.weight - common_weight
			r = Igroup(weight=w, group=group_map, iedges=union_iedges, model=model)
			return r
		# map
		def remove_iedge(self, i):
			"""
				减权重
				删除边
				不检查有效性
				"""
			self.iedges.remove(i)
			self.weight -= self.model.iweight[i]
			return self
		def add_iedge(self, i):
			self.iedges.add(i)
			self.weight += self.model.iweight[i]
			return self
		def try_update(self, *, model) -> 'self | False':
			"""
				检测内部循环, 孤立并删除 -> False
				更新groupMap
				不更新weight
				前提: hg稳定
				"""
			no_cycle = model.no_cycle
			self.model = model
			i_e_map = self.i_e_map()
			hg = self.hg()
			edges = self.edges()
			if no_cycle:
				group_map = hg.try_get_groupMap_by_edgesNodesAnodes_checkIsolateCycle( edges, model.used_nodes, model.anodes )
				if group_map == False: return False
				#
				else:
					self.group = group_map
					return self
			else:
				raise
		if "debug":
			def match_trace_add(self, hg, e) -> bool:
				if not self.matched: return False
				else:
					if e in hg.edges: 
						return True
					else:
						raise
						self.matched = False
						return False
		# draw
		def draw(self,  title=None, **ks):
			inodes = self.inodes()
			anodes = self.anodes()
			used_nodes = self.used_nodes()
			edges = self.edges()
			graph = self.graph()
			ks = HyperGraph.prepare_draw(**ks)
			ks = graph._draw_edges(edges, **ks)
			graph._draw_nodes(inodes, look=dict(color='blue'), **ks)
			graph._draw_nodes(anodes, look=dict(color='red'), **ks)
			myplt.title(f'<{self.weight}>')
			if title != None: myplt.title(title)
			return self
		def draw_(self,inodes, anodes, used_nodes, pos, *, title=Pass,**ks):
			edges = self.edges()
			if title is Pass: title = f'<{self.weight}>'
			ks = Graph.prepare_draw(title=title, **ks)
			ks = HyperGraph._draw_edges(edges, pos=pos, **ks)
			Graph._draw_nodes(inodes, pos=pos, look=dict(color='blue'), **ks)
			Graph._draw_nodes(anodes, pos=pos, look=dict(color='red'), **ks)
		@classmethod
		def cls_draw(cls, edges, inodes, anodes, used_nodes, pos, **ks):
			ks = Graph.prepare_draw(**ks)
			ks = HyperGraph._draw_edges(edges, pos=pos, **ks)
			Graph._draw_nodes(inodes, pos=pos, look=dict(color='blue'), **ks)
			Graph._draw_nodes(anodes, pos=pos, look=dict(color='red'), **ks)
	#
class HyperGraph:
	"""
		edges: { set() } <SetHash>
		nodes:
		adj_n_e: { n: [e ..] }
		#weight
		attrs: 
			weight: DictOfSet | callable | False
			interface: weight(node)
		#pos:
			interface: get_pos(nodes) -> dict
			attrs:
				pos : dict | call(nodes)->dict | None
			3种模式
				dict模式：
					独立性 删除点不会删除
				get模式：
					_get_pos(nodes) -> dict
				False模式
		#algo:
			span: 完全覆盖
			spantree：完全覆盖节点且是树
			tree：每个节点仅连接一条边
			reduced: 无法精简
		"""
	def __init__(self, *, pos=None, nodes=None, edges=None, weight=False):
		...
		"""
			weight: dict|callable|None|False|g|hg
				None: dict
				默认False
				在connectw时若weight==False且edges为空会自动改变模式为dict
			pos: list|dict|callable|None|g|hg
				None: 默认get
			"""
		self.nodes = set()
		self.edges = SetHash(hash=my.set.hash)
		self.adj_n_e = {}
		#
		self.set_weight(False)
		if nodes == None: 
			assert edges == None
		else:
			self.add_nodes(nodes)
			self.connectm(edges)
		# weight pos
		self.set_weight(weight)
		self.set_pos(pos)
	if "pos weight":
		def set_pos(self, pos):
			if pos == None:
				self.pos = pos
			elif isinstance(pos, PosDict):
				self.pos = pos
			elif isinstance(pos, dict):
				self.pos = PosDict(pos)
			elif isinstance(pos, (Graph, HyperGraph)):
				self.copy_pos_from(pos)
			elif isinstance(pos, list):
				self.pos = {i:p for i,p in enumerate(pos)}
			elif callable(pos):
				self.pos = pos
			else: raise Exception(f'{pos}')
			
			# if pos == False:
			# 	self.pos_mode = False
			# elif pos == None:
			# 	self.pos_mode = 'get'
			# elif isinstance(pos, dict):
			# 	self.pos_mode = 'dict'
			# 	self.pos_dict = pos
			# elif isinstance(pos, list):
			# 	self.pos_mode = 'dict'
			# 	self.pos_dict = { i: p for i, p in enumerate(pos) }
			# elif callable(pos):
			# 	self.pos_mode = 'get'
			# 	self._get_pos = pos
			# elif isinstance(pos, HyperGraph):
			# 	self.copy_pos_from(pos)
			# else: raise Exception(f'{pos}')
		@dynamicmethod
		def get_pos(self, *, nodes=None, edges=None, pos=None) -> 'dict|None':
			if pos == None: pos = self.pos
			if pos == None: 
				return self.default_pos(nodes=nodes,edges=edges)
			if callable(pos):
				r = pos(nodes=nodes, edges=edges)
			elif isinstance(pos, dict):
				r = pos
			else:
				raise Exception(f'{pos}')
				
			assert isinstance(r, dict)
			return r

		def get_pos_by_edges(self, edges):
			if self.pos_mode == False: raise
			elif self.pos_mode == 'dict':
				return self.pos_dict
			elif self.pos_mode == 'get':
				nodes = my.set.unionm(edges)
				return self._get_pos(nodes)
			else: raise Exception(f'unexpected [{self.pos_mode}], expecting[{'dict'} {'get'}')
		def copy_pos_from(self, hg):
			
			# pos
			pos = hg.pos
			if pos == None:
				self.pos = None
			elif isinstance(pos, dict):
				self.pos = pos.copy()
			elif callable(pos):
				self.pos = pos
			else: raise Exception(f'{pos}')
			return self
		def default_pos(self, nodes=None, edges=None):
			assert nodes is not None or edges is not None
			nodes_ = set(nodes)
			nodes_ |= my.set.unionm(edges)
			return Graph.default_pos(nodes=nodes)
			
		#
		def _weight_by_DictOfSet(self, e):
			"""
				weight dict模式
				"""
			return self.weight[e]
		def _weight_by_call(self, e):
			"""
				weight call模式
				"""
			return self.weight[e]
		def _weight_by_False(self, e):
			"""
				weight False模式
				"""
			raise Exception(f'weight==False {e}')
		def _weight_react_disconnect_by_DictOfSet(self, e):
			"""
				weight dict模式
				"""
			self.weight.try_del(e)
		def _weight_react_disconnect_by_call(self, e):
			"""
				weight call模式
				"""
			return 
		def _weight_react_disconnect_by_False(self, e):
			"""
				weight False模式
				"""
			return
		#
		def copy_weight_from(self, g):
			"""
				g: Graph | HyperGraph
				"""	
			return self.set_weight(g.weight)
			if isinstance(g, Graph):
				self.set_weight(g.weight)
			elif isinstance(g, HyperGraph):
				self.set_weight(g.weight)
			else: raise Exception(f'{g}')
			return self
		def set_weight(self, weight):
			if isinstance(weight, DictOfSet):
				self.weight = weight.sub_by_keys(self.edges)
				self.weight_react_disconnect =  self._weight_react_disconnect_by_DictOfSet
			elif callable(weight):
				self.weight = WeighterCall(weight)
				self.weight_react_disconnect = self._weight_react_disconnect_by_call
			elif weight == False:
				self.weight = False
				self.weight_react_disconnect = self._weight_react_disconnect_by_False
			elif weight == None:
				self.weight = DictOfSet()
				self.weight_react_disconnect =  self._weight_react_disconnect_by_DictOfSet
			elif isinstance(weight, (Graph, HyperGraph)):
				self.copy_weight_from(weight)
			else: raise Exception(f'{weight} {type(weight)}')
			return self
			

			
			return self
			self.get_weight = None
			if weight == False or weight == None:
				self.weighted = False
				self._update_weight = False
			else: # weighted
				if isinstance(weight, DictOfSet):
					self.weighted = 'dict'
					self.weight = DictOfSet(weight)
					self._update_weight = False
				elif callable(weight):
					assert len(self.nodes) == 0
					self.weighted = 'get'
					self.get_weight = weight
					self.weight = DictOfSet()
					self._update_weight = True
				elif weight in {True, 'w'}:
					assert len(self.nodes) == 0
					self.weighted = 'w'
					self.weight = DictOfSet()
					self._update_weight = True
				else: raise Exception(f'{weight}')
		def set_edge_weight(self, e, w):
			self.weight[e] = w
			return self
		def get_weight_dict(self, edges=None):
			if edges == None: edges = self.edges
			items = [ (e, self.weight[e]) for e in edges ]
			r = DictOfSet(items)
			return r
	if "info":
		def adj(self, n) -> '{n .. }':
			es = self.adj_n_e[n]
			if len(es) == 0: return set()
			r = my.set.unionm(es)
			r.remove(n)
			return r
		adj_n_n = adj
		def adj_e_ne(self, e) -> '[ (n, es) .. ]':
			"""
				不包括e自己
				"""
			r = [] # n, es
			for n in e: # 点
				es = []
				for e2 in self.adj_n_e[n]: # 点上的边
					if e2 == e: continue
					es.append(e2)
				r.append( (n, es) )
			return r
		def degree_n_n(self, n):
			return len(self.adj(n))
		def degree_n_e(self, n):
			return len(self.adj_n_e[n])
		degree = degree_n_e
		def adj_ns_es(self, nodes) -> 'SetOfSet':
			r = SetOfSet()
			for n in nodes:
				for e in self.adj_n_e[n]:
					r.add(e)
			return r
		#
		def edges_weight_sum(self, edges):
			try: r = sum( self.weight[e] for e in edges )
			except KeyError as exc:
				e, es = exc.args

				raise KeyError(e, es)
				# assert sorted(es) == sorted(self.edges), (sorted(es), sorted(self.edges))
				raise Exception(*exc.args, e in self.edges, self.edges)
			return r
		def len(self):
			return self.edges_weight_sum(self.edges)
		# judge-basic
		def has_node(self, n):
			return n in self.nodes
		def has_edge(self, e):
			return e in self.edges
		def is_span(self):
			subs = self.nodeSubs()
			return len(subs) <= 1
		def is_subgraph(self, g):
			"""
				nodes和edges都是sub
				"""
			if not self.nodes.issubset(g.nodes): return False
			if not self.edges.issubset(g.edges): return False
			return True
		# path
		def path(self, n1, n2):
			"""
				伪码
					while 延长一段
						若当前没路：返回直到有路
						向前走
						若发现目标：返回
						waiting拿出一个
						path, node_path +1
						waiting加入新边的子边
				len(waiting) = len(path) + 1

				"""
			assert n1 != n2
			path = [] # edges
			node_path = [] # 对应边前面的点
			#
			waiting = [ [ (n1, list(self.adj_n_e[n1]) ) ] ] # [ [n,es ..] ]
			while 1: # w
				# 没路， 返回，直到有路
				while 1:
					if len(waiting[-1]) == 0:
						waiting.pop()
						if len(path) == 0: raise Exception(f'path not found')
						path.pop()
						# if len(waiting[-1]) > 0: break
						continue
					else:
						v, es = waiting[-1][-1]
						if len(es) == 0:
							waiting[-1].pop()
							continue
						else:
							w = es.pop()
							break
				# 选择一条路
				# mother = path[-1]
				#
				new_waiting = []
				for n, es in self.adj_e_ne(w): # 下个点
					if n == v: continue # 避免返回上一级
					if n == n2:
						path.append(w)
						return path
					for e in es: # 下条边
						assert e != w
					if len(es) != 0: new_waiting.append( (n, es) )
				if not empty(new_waiting):
					waiting.append(new_waiting)
					path.append(w)
				#
		# graph
		def wedges(self):
			return [ (e, self.weight[e]) for e in self.edges ]
	if "oper":
		def add_node(self, n):
			assert n not in self.nodes
			self.nodes.add(n)
			self.adj_n_e[n] = []
			return self
		def add_nodes(self, nodes):
			for n in nodes:
				self.add_node(n)
			return self
		def del_node(self, n):
			"""
				要求：孤立
				"""
			assert self.degree(n) == 0, (self.degree(n), self.adj_n_e[n], n)
			self.nodes.remove(n)
			del self.adj_n_e[n]
			return self
		def del_nodes(self, ns):
			for n in ns:
				self.del_node(n)
			return self
		def del_node_clear(self, n):
			"""
				移除相连边
				"""
			for e in list(self.adj_n_e[n]):
				self.disconnect(e)
			return self.del_node(n)
		def del_nodes_clear(self, ns):
			for n in ns:
				self.del_node_clear(n)
			return self
		# edge
		def connect(self, e):
			assert self.weight == False, self.weight
			return self._connect(e)
		def _connect(self, e):
			e = set(e)
			assert not self.edges.has(e)
			self.edges.add(e)
			for n in e:
				self.adj_n_e[n].append(e)
			return self
			
		def connectm(self, edges):
			for e in edges:
				self.connect(e)
			return self
		def connectw(self, e, w):
			if self.weight == False:
				if empty(self.edges):
					self.set_weight(None)
				else:
					raise Exception(f'{self.edges}')
					
			self._connect(e)
			self.weight[e] = w
			return self
		def disconnect(self, e):
			assert isinstance(e, set)
			# e = set(e)
			self.edges.remove(e)
			for n in e:
				self.adj_n_e[n].remove(e)
			self.weight_react_disconnect(e)
			return self
		
		# add_edge
		def add_edges(self, edges):
			for e in edges:
				self.add_edge(e)
			return self
		def add_edge(self, e):
			e = set(e)
			for n in e:
				if n not in self.nodes:
					self.add_node(n)
			self.connect(e)
			return self
		def add_edgew(self, e, w):
			e = set(e)
			for n in e:
				if n not in self.nodes:
					self.add_node(n)
			self.connectw(e, w)
			return self
		def add_wedge(self, ew):
			e, w = ew
			self.add_edgew(e, w)
			return self
		def add_wedges(self, wedges):
			for e, w in wedges:
				self.add_edgew(e, w)
			return self
	if "oper-misc":
		def set_layer(self, *, edges1, edges0):
			for e1 in edges1:
				self.set_edge_weight(e1, 0)
			for e0 in edges0:
				self.disconnect(e0)
			return self
		def clear_isolated_nodes(self):
			"""
				degree == 0
				"""
			for n in list(self.nodes):
				if self.degree(n) == 0:
					self.del_node(n)
			return self
	if "oper-temp":
		def set_wedge_temp(self, wedge):
			e, w = wedge
			if self.has_edge(e):
				w_ = self.weight[e]
				self.set_edge_weight(e, w)
				def goback():
					self.set_edge_weight(e, w_)
					return self
			else:
				self.connectw(e, w)
				def goback():
					self.disconnect(e)
					return self
			return goback
		def disconnect_temp(self, e):
			assert self.has_edge(e)
			if e in self.weight:
				w = self.weight[e]
				self.disconnect(e)
				def goback():
					self.connectw(e, w)
			else:
				self.disconnect(e)
				def goback():
					self.connect(e)
			return goback

	if "algo":
		'''
			def reduced_spantrees00(self) -> '[ edges ]':
			"""
				要求
				reduce: 无法更精简
				
				算法：
					对每条边的存在二叉树进行广度搜索
					合并同型
					孤立或成环时删除节点
				伪码
					for e in edges

				结构
					node_cover_count记录每个节点的覆盖值
					active_connectivity记录连通性
				"""
			state = [0]
			edges = list(self.edges)
			nodes = list(self.nodes)
			size = len(edges)
			states = []
			#
			connectivity = my.Group()
			edges_remain = {n: set() for n in nodes }
			#

			def save():
				states.append(tuple(state))
			def settle_new_node():
				"""
					说明：
						若back==True，不会修改状态
					死点：e_remain == 1 && subgroup == 1
					tail=0
						孤立：某个节点是死点
					tail=1
						孤立：所有节点是死点
						成环：包含同一活跃组的节点
					"""
				tail = state[-1]
				if tail == 0:
					if any(len(n_edges_r[n]) == 0
				else:
					...
			def go_back():
				"""
					往右或往回
					"""
			def go_down():
				"""
					
					"""
				state.append(0)
				if len(state) == size: back = True
				i = len(state) - 1
				e = edges[i]
				back = settle_new_node()

					connectivity = 

			def funcName(self):
				
			def judge_conflict():
				"""
					重复点
					孤立点
					"""
			#
			back = False
			while 1: # 一步一条边，有可能走到走过的节点
				if back:
					go_back()
				else:
					go_down()


				if len(state) == size: # leaf
					if conflict:
						go_back_next_state()
					else:
						sava()
						go_back_next_state()
				else:
					if conflict:
						go_back_next_state()
					else:
						go_down()
			'''
	if "tree":
		def tree_subtree_from_nodes(self, nodes) -> 'edges': ###
			"""
				nodes 生成的子树
				"""
			# 要求是树
			nodes = list(nodes)
			n0 = nodes[0]
			paths = [ self.path(n, n0) for n in nodes[1:] ]
			tree = my.list.unionm(paths)
			return tree
		def subtree_expand_nodes(self, sub:'edges', nodes):
			"""
				self is tree
				"""
			if len(sub) == 0:
				nodes_ = nodes
			else:
				n = my.pick( my.pick(sub) )
				nodes_ = {n} | nodes
			sub2 = self.tree_subtree_from_nodes( nodes_ )
			tree = my.list.union(sub, sub2)
			return tree
	class test:
		def wedges_from_string(s):
			"""
				w e \n ..
				"""
			r = []
			for line in my.str.nonblank_lines(s):
				nums = [ int(i) for i in line.split() ]
				w, e = nums[0], set(nums[1:])
				assert len(e) > 1, line
				r.append((e, w))
			return r
		def pos_from_string(s):
			"""
				"""
			li = [int(i) for i in s.split()]
			groups = my.tuple.group_by_len(li, 2)
			return { i: groups[i] for i in range(len(groups)) }

		def h1(): # 正方形
			wedges = HyperGraph.test.wedges_from_string('''
				1 0 1
				1 1 2
				1 2 3
				1 3 0
			''')
			pos = HyperGraph.test.pos_from_string('''
				0 0
				0 1
				1 0
				1 1
			''')
			h = HyperGraph(pos=pos)
			h.add_wedges(wedges)
			return h
		def h2(): # 菱形
			wedges = HyperGraph.test.wedges_from_string('''
				3 0 1 2
				4 1 2 3
				1 0 2
				1 2 3
			''')
			pos = HyperGraph.test.pos_from_string('''
				0 1
				1 2
				1 0
				2 1
			''')
			h = HyperGraph(pos=pos)
			h.add_wedges(wedges)
			return h
		def h3(): # 经典rsmt5
			wedges = HyperGraph.test.wedges_from_string('''
				1 0 1
				2 1 2
				3 0 4
				2 2 3
				6 1 3 4
				4 3 4
			''')
			pos = HyperGraph.test.pos_from_string('''
				0 0
				0 1
				0 3
				2 3
				4 0
			''')
			h = HyperGraph(pos=pos)
			h.add_wedges(wedges)
			return h
		def h4(): 
			wedges = HyperGraph.test.wedges_from_string('''
				3 0 1 2
				4 1 2 3
				1 0 2
				1 2 3
				1 0 1
			''')
			pos = HyperGraph.test.pos_from_string('''
				0 1
				1 2
				1 0
				2 1
			''')
			h = HyperGraph(pos=pos)
			h.add_wedges(wedges)
			return h
		def h4(): 
			wedges = HyperGraph.test.wedges_from_string('''
				3 0 1 2
				4 1 2 3
				1 0 2
				1 2 3
				1 0 1
			''')
			pos = HyperGraph.test.pos_from_string('''
				0 1
				1 2
				1 0
				2 1
			''')
			h = HyperGraph(pos=pos)
			h.add_wedges(wedges)
			return h
		
		def hg_fsts(k=10, seed=0):
			import rsmt2
			hg = rsmt2.fsts_hg_by_key( (k,seed) )
			return hg
		def hg_pruned(k=10, seed=0):
			import rsmt2
			hg = rsmt2.pruned_hg_by_key( (k,seed) )
			return hg
			match (k,i):
				case (10,0):
					wedges = [({0, 1, 2, 3}, 7), ({8, 3, 7}, 8), ({8, 4, 7}, 8), ({2, 3}, 2), ({2, 4}, 2), ({5, 6}, 2), ({9, 6}, 2), ({0, 2}, 3), ({1, 2}, 4), ({6, 7}, 4), ({8, 7}, 4), ({1, 5}, 5)]
					pos = {0: (0, 6), 1: (2, 3), 2: (2, 7), 3: (3, 6), 4: (3, 8), 5: (5, 1), 6: (7, 1), 7: (7, 5), 8: (7, 9), 9: (8, 0)}
				case _:
					raise Exception(f'{i}')
					
			h = HyperGraph.from_wedges(wedges=wedges, pos=pos)
			return h
		# Rgraph
	if "test":
		def test_Rgraph_tri_le00(self):
				"""
					r1 + r2 <= r3
					r3是1.2的并
					说明
						对存在的所有的超边的并
					"""
				edges = list(self.edges)
				count = 0
				count_fail = 0
				for ecomb in my.comb.comb_range(edges, (2, -1)):
					nodes = my.set.unionm(ecomb)
					if not self.has_edge(nodes): continue
					w_sum = sum( self.weight[e] for e in ecomb )
					w = self.weight[nodes]
					count += 1
					if w_sum > w:
						print(f'Rgraph_tri_le: fail: {ecomb} > {nodes}  {w_sum} > {w}')
						count_fail += 1
				if count_fail == 0:
					print(f'Rgraph_tri_le: succeed tested:{count}')
		def test_r000(self, cap=3):
				"""
					r1 + r2 + .. <= r3
					r3是1.2的并
					arg:
						cap: k1, k2的cap
					说明
						对存在的所有的超边，任意多个组合，且组合后仍然是存在超边
						由递推性，只需证明r1 + r2 <= r3 
					"""
				edges = list(self.edges)
				count = 0
				count_fail = 0
				get_r = self.R_getter()
				# r1 + r2
				kpair_list = { (k1, k2) for k1 in range(2, cap) for k2 in range(k1, cap) }
				for k1, k2 in kpair_list:
					edges_k1 = [ e for  e in self.edges if len(e) == k1 ]
					edges_k2 = [ e for  e in self.edges if len(e) == k2 ]
					assert len(edges_k1) * len(edges_k2) <= 10000
					for e1 in edges_k1:
						for e2 in edges_k2:
							e0 = e1 | e2
							if len(e0) == len(e2): continue
							r0 = get_r(e0)
							r1 = get_r(e1)
							r2 = get_r(e2)
							count += 1
							d(r1 + r2 - r0)
							if r1 + r2 <= r0: pass
							else:
								print(f'Rgraph_tri_le: fail: r1 + r2 > r0 {e1} {e2} {e0} {r1} {r2} {r0}')
								count_fail += 1
				if count_fail == 0:
					print(f'Rgraph_tri_le: succeed tested:{count}')
				else:
					print(f'Rgraph_tri_le: fail tested:{count} fail:{count_fail}')

		def test_r(self):
				"""
					r1, r2, r3, r0
					size: nodes
					"""
				edges = list(self.edges)
				count = 0
				count_fail = 0
				get_r = self.R_getter()
				weight = self.weight
				# pattern
				size = 4
				var_count = (my.math.comb(size, 2))
				pattern = [ True ] * (var_count - 1) # i == i+1
				def get_pattern(li):
					if not 0:
						return
					for i in range(var_count-1):
						if li[i] != li[i+1]:
							pattern[i] = False
							#update pattern_
					pattern_ = [1]
					for flag in pattern:
						if flag:
							pattern_[-1] += 1
						else: pattern_.append(1)
					print(f'pattern{var_count}: {mystr(pattern_)}')
				# nodes=size
				if 1: groups = [ e for e in self.edges if len(e) == size ]
				else: groups = my.comb(self.nodes, size, typ=set)
				for nodes in groups:
					if 0: # -m
						hg_ = self.copy().disconnect(nodes)
						get_r = hg_.R_getter()
					count += 1
					nedges = my.comb(nodes, 2, typ=set)
					e0 = nodes
					r0 = get_r(nodes)
					rs = []
					for ne in nedges:
						rs.append(get_r(ne))
					rs.sort()
					get_pattern(sorted(rs))
					flag = 1
					if 0: #mst
						g = Graph.from_edges(nedges, weight=lambda e: get_r(set(e)))
						mst_r = g.mst_len()
						flag = mst_r <= r0
					if 0:
						m1, m2 = my.max_multi( rs, 2 )
						flag &= m1 == m2
					if 0:
						m1, m2 = my.min_multi( rs, 2 )
						flag = m1 + m2 <= r0
					if 1: # delta-exist
						flag = 1
						w0 = weight[e0]
						for a in nodes:
							sub = nodes.difference({a})
							rsub = get_r(sub)
							r0 = get_r(e0)
							hg_ = self.copy().disconnect(nodes)
							get_r_ = hg_.R_getter()
							r_ab = [ get_r_({a,b}) for b in sub ]
							flag &= rsub <= w0 - min(r_ab)
							guesses = [ r0 - rab - rsub for rab in r_ab ]
							print(f'{mystr(guesses)}')
							# if r0 < w0: pause()
					if 0: # delta-non-exist
						if not self.has_edge(nodes): continue
						flag = 1
						for a in nodes:
							sub = nodes.difference({a})
							rsub = get_r(sub)
							r0 = get_r(e0)
							hg_ = self.copy().disconnect(nodes)
							get_r_ = hg_.R_getter()
							r_ab = [ get_r_({a,b}) for b in sub ]
							flag &= rsub <= r0 - min(r_ab)
							guesses = [ r0 - rab - rsub for rab in r_ab ]
							print(f'{mystr(guesses)}')
							# if r0 < w0: pause()
					print(f' {r0} {mystr(sorted(rs))} {bool(flag)}')
					if count_fail > 0: print(f'fail {count_fail}')
					if not flag:
						print(f'test_R: fail: e0 es  {e0} {mystr(nedges)}')
						if 1:
							self.show(hl_nodes=nodes)
						count_fail += 1
				if count_fail == 0:
					print(f'test_R: succeed tested:{count}')
				else:
					print(f'test_R: fail tested:{count} fail:{count_fail}')
		def test_Ru_tri(self, v=None):
			"""
				超边的三元子集中 u123 - min(u12, u23) >= r13
				"""
			count = 0
			count_eq = 0
			count_gt = 0
			count_fail = 0
			flags = []
			delta_u = []

			get_r = self.R_getter()
			get_u = self.Ru_getter(v)

			for sup in self.edges:
				if len(sup) == 2: continue
				for nodes in my.comb(sup, 3):
					nedges = my.comb.comb_set(nodes, 2)
					u_3 = get_u(nodes)
					if 0:
						e1, e2, e3 = nedges
						u1 = get_u(e1)
						u2 = get_u(e2)
						u3 = get_u(e3)
						r1 = get_r(e1)
						r2 = get_r(e2)
						r3 = get_r(e3)
						# d( (u1, u2, u3) )
						d( (r1, r2, r3) )
					for (e1,), (e2, e3) in my.comb.comb(nedges, 1, 2):
						count += 1
						r1 = get_r(e1)
						u2 = get_u(e2)
						u3 = get_u(e3)
						guess_u1 = u_3 - min(u2, u3)
						flag = guess_u1 - r1
						flags.append(flag)
						u1 = get_u(e1)
						delta_u.append(guess_u1 - u1)
						if flag < 0:
							count_fail += 1
							print(f'test_Ru_tri: fail {nodes} {e1}')
						elif flag == 0:
							count_eq += 1
						else:
							count_gt += 1
						
					# n1, n2, n3 = nodes
			if count_fail == 0:
				print(f'test_Ru_tri: succeed')
			else:
				print(f'test_Ru_tri: fail={count_fail}')

			print(f'tested:{count}')
			print(f'=:{count_eq} >:{count_gt}')
			print(f'delta(guess_u - r): {flags}')
			print(f'delta(guess_u - u1): {delta_u}')
		def compare_Ru(self, v=1+0):
			"""
				对存在边
				"""
			ran = (1, v+1)
			indexs = list(my.slice.range(my.slice.inter(ran, (1,None) )))
			get = {}
			mst = self.cacu_mst()
			ru_map = { i: DictOfSet() for i in indexs }
			get_r = self.R_getter()
			#
			for i in indexs:
				get[i] = self.Ru_getter(i)
			#
			size = 2
			if 1: tested_edges = self.edges
			else: tested_edges = my.comb.comb(self.nodes, size, typ=set)
			#
			for e in tested_edges:
				for i in indexs:
					ru = get[i](e)
					r = get_r(e)
					delta = ru - r
					ru_map[i][e] = delta
			# show
			last_li = None
			for i in indexs:
				print(f'Ru-getter{i}: {list(ru_map[i].values())}')
				if last_li == None:
					last_li = ru_map[i]
				else:
					improve = [ ru_map[i][e] - last_li[e] for e in tested_edges ]
					if not any(improve):
						print(f'Ru-getter{i} got no improve')
					else:
						1
						print(f'improve{i} {improve}')
					last_li = ru_map[i]
				# check delta >= 0
				neg_list = [ (e, dt) for e, dt in ru_map[i].items() if dt < 0 ]
				if len(neg_list) != 0:
					print(f'!!!!!!!!!!!!!!!!!')
					print(f'Ru_getter{i} error: {neg_list}')
				for e, dt in neg_list:
					# d(self.has_edge(e))
					r = get_r(e)
					ru = r + dt
					w = self.weight[e]
					print( f'{ru - w} {mst.has_edge(e)}' )
					# assert rb <= w
					# assert not mst.has_edge(e)
					# if self.weight[e] == rb:
					# 	print(f'eq')
					# else:
		def compare_Rb(self, v=0+0):
			"""
				对存在边
				"""
			ran = (0, v+1)
			# if ran == None: ran = HyperGraph.newest_Rb_version + 1
			indexs = list(my.slice.range(ran))
			get = {}
			rb_map = { i: DictOfSet() for i in indexs } # r - rb
			mst = self.cacu_mst()
			get_r = self.R_getter(ms_len=mst.len())
			#
			for i in indexs:
				get[i] = self.Rb_getter(i)
			#
			if 1: tested_edges = [e for e in self.edges if len(e) == 2]
			else: tested_edges = my.comb.comb(self.nodes, 2, typ=set)
			for e in tested_edges:
				for i in indexs:
					rb = get[i](e)
					r = get_r(e)
					delta = r - rb
					rb_map[i][e] = delta
			# show
			last_li = None
			for i in indexs:
				print(f'Rb-getter{i}: {list(rb_map[i].values())}')
				if last_li == None:
					last_li = rb_map[i]
				else:
					improve = [ rb_map[i][e] - last_li[e] for e in tested_edges ]
					if not any(improve):
						print(f'Rb-getter{i} got no improve')
					else:
						1
						print(f'improve{i} {improve}')
					# changed 
					for e in tested_edges:
						if rb_map[i][e] - last_li[e] == 0: continue
						print(f'changed-existence: {rb_map[i][e] >= 0} {self.edge_in_mst_state_str(e, mst=mst)}')
					last_li = rb_map[i]
				# check delta >= 0
				neg_list = [ (e, dt) for e, dt in rb_map[i].items() if dt < 0 ]
				if len(neg_list) != 0:
					print(f'!!!!!!!!!!!!!!!!!')
					print(f'Rb_getter{i} error: {neg_list}')
					for e, dt in neg_list:
						r = get_r(e)
						rb = r - dt
						w = self.weight[e]
						print( f'{rb - w} {self.edge_in_mst_state(e, mst=mst)}' )
						assert rb <= w
						# assert self.edge_in_mst_state(e, mst=mst) == 0
						# if self.weight[e] == rb:
						# 	print(f'eq')
						# else:
				for e in tested_edges:
					r = get_r(e)
					w = self.weight[e]
					dt = rb_map[i][e]
					rb = r - dt
					if rb == w:
						print(f'==weight: {e} {self.edge_in_mst_state(e, mst=mst)}')
		def test_print_rb(self, depth=0):
			get_u = self.Ru_getter(depth+1)
			
			def get_sup_n_val(sup, n):
				if len(sup) == 2: return self.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = self.weight[sup]
				r = w - B_oppos
				return max(r, 0)
			
			tgraph = self.tgraph()
			#. v(n:sup)
			sup_n_val = DictOfSet()
			for sup in self.edges:
				sup_n_val[sup] = map_ = {}
				for n in sup:
					map_[n] = get_sup_n_val(sup, n)

			#. v(ne)
			val_tedge = {}
			for sup in self.edges:
				for e2 in my.comb.comb2(sup):
					a, b = e2 = sorted2(e2)
					v = max( sup_n_val[sup][a], sup_n_val[sup][b] )
					if e2 not in val_tedge or val_tedge[e2] > v:
						1
						val_tedge[e2] = v
			map_ne = tgraph.get_bottle_neck(weight=val_tedge, mode='v') # dict
			map = DictOfSet([ (set(e2), v) for e2, v in map_ne.items() ])
			# get_r = self.R_getter()
			def get(nodes):
				# assert len(nodes) == 2
				rb = map[nodes]
				if 0:
					r = get_r(nodes)
					assert rb <= r
				return rb
			tgraph.draw(title='v(e)', edge_label=val_tedge)
			self.draw(title='rb', edge_label=lambda e: get(e) if len(e) == 2 else '')
		#
		def test_r_del_edges(self):
			self = self.copy()
			mst = self.cacu_mst()
			white_edges = [ e for e in self.edges if not mst.has_edge(e) ]
			#
			rgraph = last_r = self.Rgraph()
			last_r.draw(edge_label=1)
			changed = []
			for e in [e for e in self.edges if len(e) >= 3]:
				self.disconnect(e)
				rgraph = self.Rgraph()
				# changed
				changed = SetOfSet()
				for e1, w in rgraph.wedges():
					w_ = last_r.weight[e1]
					if w != w_:
						changed.add(e1)
						# assert w < w_
						assert w < w_
				rgraph.draw(edge_label=1, hl_edges=[e], hl_edges1=changed)
				last_r = rgraph
			return self
		def test_rb_del_edges(self):
			self = self.copy()
			mst = self.cacu_mst()
			white_edges = [ e for e in self.edges if not mst.has_edge(e) ]
			#
			rgraph = last_r = self.copy(weight=self.Rb_getter_str())
			last_r.draw(edge_label=1)
			changed = []
			for e in white_edges:
				if len(e) == 2: continue
				self.disconnect(e)
				rgraph = self.copy(weight=self.Rb_getter_str())
				# changed
				changed = SetOfSet()
				for e1, w in rgraph.wedges():
					w_ = last_r.weight[e1]
					if w != w_:
						changed.add(e1)
						# assert w < w_
				rgraph.draw(edge_label=1, hl_edges=[e], hl_edges1=changed)
				last_r = rgraph
			return self
		def test_ru_del_edges(self):
			self = self.copy()
			mst = self.cacu_mst()
			white_edges = [ e for e in self.edges if not mst.has_edge(e) ]
			#
			rgraph = last_r = self.copy(weight=self.Ru_getter())
			last_r.draw(edge_label=1, node_label=1)
			for e in white_edges:
				if len(e) == 2: continue
				self.disconnect(e)
				rgraph = self.copy(weight=self.Ru_getter())
				# changed
				changed = SetOfSet()
				for e1, w in rgraph.wedges():
					w_ = last_r.weight[e1]
					1
					if w != w_:
						changed.add(e1)
						# assert w < w_
				rgraph.draw(edge_label=1, hl_edges=[e], hl_edges1=changed)
				last_r = rgraph
			return self
	if "check":
		def check_span(self):
			if self.is_span(): return True
			else:
				nodeSubs = self.nodeSubs()
				d(subs=nodeSubs)
				return False
	if "debug":
		def getDelNodes_delNodesClear_cutSmallerSubs(self, nodes):
			"""
				剩下的部分,将较小的连通部分删掉, 只留下最大的 (依据点数)
				返回所有delClear的点
				"""
			if not isinstance(nodes, set): nodes = set(nodes)
			r = set(nodes)
			#
			h = self.copy()
			h.del_nodes_clear(nodes)
			subs = h.nodeSubs()
			sub_max = max(subs, key=len)
			for sub in subs:
				if sub is not sub_max:
					r |= sub
			return r
		def getDelNodes_delNodesClear_reserveNode(self, nodes, reserve):
			"""
				arg:
					nodes: 删除的nodes
					
				剩下的部分,将较小的连通部分删掉, 只留下最大的 (依据点数)
				返回所有delClear的点
				"""
			if not isinstance(nodes, set): nodes = set(nodes)
			assert reserve in self.nodes
			assert reserve not in nodes
			r = set(nodes)
			#
			h = self.copy()
			h.del_nodes_clear(nodes)
			subs = h.nodeSubs()
			sub_reserve = [s for s in subs if reserve in s][0]
			for sub in subs:
				if sub is not sub_reserve:
					r |= sub
			return r
	if "differ":
		"""
			f: 整（对应节点相同）
				最小整图对
			gen: 生成对, 不包括重复的
			pair: edges1-edges2
			说明
				要求是树
			概念
				整图对：节点相同，连通分量相同（若1两点相连 => 2两点相连）
				整树对：节点相同，都是树
				生成整树对：由一个相异边生成
			定理
				生成整树对之间可能相交、包含
				有共同节点的整树对之并仍是整树对
				整数对之交仍是整树对（树交树=树）
			"""
		def fdiffer_gen1_pair_nodes(g0, g1, e0) -> (list,list,set):
			g = [ g0, g1 ]
			nodes = [ set(e0), set() ]
			edges = [[e0], []]
			more = 0
			less = 1
			#
			while 1: # 直到一边反超
				diff = nodes[more].difference( nodes[less] )
				tree = g[less].subtree_expand_nodes(edges[less], diff) # edges
				#
				nodes[less] = my.set.unionm(tree)
				edges[less] = tree
				more, less = less, more
				#
				if len(nodes[less]) == len(nodes[more]):
					assert nodes[less] == nodes[more], nodes
					break
			return (edges[0], edges[1]), nodes[0]

		#public
		def differ(g1, g2) -> 'edges1, edges2':
			edges1 = g1.edges.difference(g2.edges)
			edges2 = g2.edges.difference(g1.edges)
			return edges1, edges2
		def fdiffer_gen_pairs(g1, g2)-> '[edges1, edges2]':
			"""
				伪码
					穷举每一个不同边
				"""
			assert g1.nodes == g2.nodes
			self = HyperGraph
			edges1, edges2 = HyperGraph.differ(g1, g2)

			pairs = []
			node_groups = []
			for e1 in edges1: ###
				(es1, es2), nodes = self.fdiffer_gen1_pair_nodes(g1, g2, e1)
				assert isinstance(nodes, set)
				if nodes in node_groups:	continue
				pairs.append((es1, es2))
				node_groups.append(nodes)
			for e2 in edges2:
				(es2, es1), nodes = self.fdiffer_gen1_pair_nodes(g2, g1, e2)
				assert isinstance(nodes, set)
				if nodes in node_groups:	continue
				pairs.append((es1, es2))
				node_groups.append(nodes)
			
			return pairs
		def fdiffer_gen_pairs_weight_nonweight(g1, g2)-> '相异的 （不等权 等权）':
			"""
				伪码
					穷举每一个不同边
				"""
			assert g1.nodes == g2.nodes
			self = HyperGraph
			edges1, edges2 = HyperGraph.differ(g1, g2)

			pairs = []
			eq_pairs = []
			node_groups = []
			for e1 in edges1: ###
				(es1, es2), nodes = self.fdiffer_gen1_pair_nodes(g1, g2, e1)
				assert isinstance(nodes, set)
				if nodes in node_groups: continue
				node_groups.append(nodes)
				if g1.edges_weight_sum(es1) == g2.edges_weight_sum(es2):
					eq_pairs.append((es1, es2))
				else:
					pairs.append((es1, es2))
			for e2 in edges2:
				(es2, es1), nodes = self.fdiffer_gen1_pair_nodes(g2, g1, e2)
				assert isinstance(nodes, set)
				if nodes in node_groups: continue
				if self.edges_weight_sum(es1) == self.edges_weight_sum(es2):
					eq_pairs.append((es1, es2))
				else:
					pairs.append((es1, es2))
				node_groups.append(nodes)
			return pairs, eq_pairs
		def fdiffer_gen_pairs_weight(g1, g2) -> '相异的 （不等权）':
			ne, eq = g1.fdiffer_gen_pairs_weight_nonweight(g2)
			return ne
		def fdiffer(g1, g2) -> 'edges1, edges2':
			assert g1.nodes == g2.nodes
			self = HyperGraph
			pairs = self.fdiffer_gen_pairs(g1, g2)
			groups1, groups2 = zip(*pairs)
			edges1 = my.list.unionm(groups1)
			edges2 = my.list.unionm(groups2)
			return edges1, edges2
		def fdiffer_weight(g1, g2) -> 'edges1, edges2':
			"""
				算法：
					穷举生成对，排除等权的
				"""
			assert g1.nodes == g2.nodes
			self = HyperGraph
			pairs = self.fdiffer_gen_pairs_weight(g1, g2)
			groups1, groups2 = zip(*pairs)
			edges1 = my.list.unionm(groups1)
			edges2 = my.list.unionm(groups2)
			return edges1, edges2
	if "build":
		@classmethod
		def from_edges(cls, edges, **ks):
			nodes = my.set.unionm_iterable(edges)
			self = cls(nodes=nodes, edges=edges, **ks)
			return self
		@classmethod
		def from_wedges(cls, wedges, **ks):
			self = cls(**ks)
			self.add_wedges(wedges)
			return self
		@classmethod
		def from_edges_weight(self, edges, weight, **ks):
			r = HyperGraph(**ks)
			r.add_edges(edges)
			r.set_weight(weight)
			return r
		def copy(self, weight=None, pos=None):
			cls = type(self)
			r = cls(nodes=self.nodes, edges=self.edges)
			# pos weight
			if weight == None: weight = self
			if pos == None: pos = self
			r.set_pos(pos)
			r.set_weight(weight)
			#
			return r
		def sub_from_edges(self, edges):
			cls = type(self)
			r = cls()
			# pos
			r.copy_pos_from(self)
			# weight
			r.copy_weight_from(self)
			#
			if isinstance(self.weight, DictOfSet):
				for e in edges:
					r.add_wedge( (e, self.weight[e] ) )
			else: r.add_edges(edges)
			return r
	if "normal 2-graph":
		def tgraph(self, *, pos=None) -> 'ngraph':
			if pos == None: pos = self
			nedges = SetHash(hash=lambda ne: hash(sorted2(ne)))
			for e in self.edges:
				nedges |= my.comb.comb2_tuple(e)
			g = Graph.from_edges(nedges, pos=pos)
			return g
		def tgraph_pos(self) -> 'ngraph':
			r = self.tgraph(pos=self)
			return r
		def weighted_subngraph(self):
			wedges = [ (e, self.weight[e] ) for e in self.edges if len(e) == 2 ]
			g = Graph.from_wedges(wedges)
			return g
		extract_weighted_ngraph = weighted_subngraph
		def subngraph_from_edges(self, edges):
			"""
				edge<set>
				"""
			g = Graph(edges=[sorted2(e) for e in edges])
			g.copy_pos_from(self)
			g.copy_weight_from(self)
			return g
		def subngraph(self): # weight, pos
			g = Graph.from_edges(edges=[sorted2(e) for e in self.edges if len(e) ==2])
			g.copy_pos_from(self)
			g.copy_weight_from(self)
			return g
		def seperate_sub_full_ngraph_from_nodes(self, nodes, *, pos=Pass):
			"""
				根据自己的连通性分组nodes
				"""
			if pos == Pass: pos = self
			groups = self.group_nodes_by_connectivity(nodes)
			edges = []
			for group in groups:
				edges += my.comb.comb(group, 2, typ=tuple)
			return Graph.from_edges(edges, pos=pos)
	if "hg 2-graph":
		def thgraph(self, *, pos=None) -> 'hg':
			if pos == None: pos = self.pos
			nedges = SetOfSet()
			for e in self.edges:
				for ne in my.comb.comb(e, 2, typ=set):
					nedges.add(ne)
			assert my.check.unique(nedges, hash=my.set.hash)
			hg = HyperGraph.from_edges(nedges, pos=self)
			return hg
		def nhgraph(self) -> 'hg':
			nedges = [ sorted2(e) for e in self.edges if len(e) == 2 ]
			g = self.subgraph_from_edges(nedges)
			return g		
		def subgraph_from_edges(self, edges):
			g = HyperGraph.from_edges(edges)
			g.copy_pos_from(self)
			g.copy_weight_from(self)
			return g
	if "misc":
		def get_verbose_edges(self) -> '<sos>edges':
			"""
				去掉后不影响连通性
				"""
			
			span = self.get_rspan()
			r = self.edges.difference(span)
			return r
		def get_rspan(self) -> '<sos>edges':
			
			"""
				rspan: reduced-span
				要求: 单连通, 不多余
				算法: 依次加入相邻边, 只要能引入新节点
				"""
			walked_nodes = set()
			r = SetOfSet()
			for e in self.walk_edges():
				if e.issubset(walked_nodes): pass
				else:
					r.add(e)
					walked_nodes |= e
			assert len(walked_nodes) == len(self.nodes), self.show()
			return r
		def group_nodes_by_connectivity(self, nodes):
			subs = self.nodeSubs()
			groups = my.set.group_by_sets(nodes, subs)
			return groups
		def match_state(self, *, edges1, edges0):
			for e in edges1:
				assert isinstance(e, set)
				if not self.has_edge(e): return False
			for e in edges0:
				assert isinstance(e, set)
				if self.has_edge(e): return False
			return True
	if "anode":
		def get_anodes_by_edges(self, edges) -> set:
			"""
				前提: edges不重复, 都是存在的
				定义: 同时连接黑白两边的node
				"""
			n_count_map = defaultdict(lambda: 0)
			for e in edges:
				for n in e:
					n_count_map[n] += 1
			#
			anodes = set()
			for n, count in n_count_map.items():
				if count < self.degree(n):
					anodes.add(n)
			return anodes
	if "sub":
		# sub
		def nodeSub_by_node(self, n):
			anodes = {n}
			walked = {n}
			while not empty(anodes):
				anode = anodes.pop()
				adjs = self.adj(anode)
				for adj in adjs:
					if adj in walked: continue
					else:
						anodes.add(adj)
						walked.add(adj)
			return walked
		def edgeSubs_by_node(self, n): ###
			nodes = self.nodeSubs_by_node(n)
			return self.adj_ns_es(nodes)
		def nodeSubs(self):
			r = []
			nodes = self.nodes.copy()
			while 1:
				if empty(nodes): break
				n = nodes.pop()
				sub = self.nodeSub_by_node(n)
				r.append(sub)
				nodes = nodes.difference(sub)
			return r

		def edgeSubs(self):
			"""
				深度搜索
				"""
			nodeSubs = self.nodeSubs()
			return [ self.adj_ns_es(sub) for sub in nodeSubs ]
		def nodeEdgeSubs(self) -> '[ (nodes, edges) ..]':
			nodeSubs = self.nodeSubs()
			nodeEdgeSubs = [ (nsub, self.adj_ns_es(nsub)) for nsub in nodeSubs]
			return nodeEdgeSubs
		# subgraph
		def subgraph_from_nodes_edges(self, nodes, edges):
			hg = HyperGraph(nodes=nodes, edges=edges, weight=self, pos=self)
			return hg
		def graphSubs(self) -> 'hg':
			nodeSubs = self.nodeSubs()
			r = [ self.deduced_subgraph_by_nodes(nsub) for nsub in nodeSubs]
			return r
		def deduced_subgraph_by_nodes(self, nodes):
			"""
				所有与nodes相连的边, 节点是nodes
				"""
			edges = self.adj_ns_es(nodes)
			hg = self.subgraph_from_nodes_edges(nodes, edges)
			return hg
		
		# misc
		# def try_nodeSubs_by_edgesNodes_no_cycle(self, edges, nodes): ###
		# 	"""
		# 		说明
		# 			nodes: 所有需要考虑的node
		# 		循环 -> False
				
		# 		"""
		# 	subs = my.hypergraph.try_nodeSubs_by_edges_no_cycle(edges)
			# return subs
	if "walk":
		def walk_edges(self):
			"""
				要求:单连通
				算法:
					每次取出一个等待点,加入相连的所有边
				"""
			r = []
			walked_edges = set() # id
			waited_nodes = [my.pick(self.nodes)]
			walked_nodes = set()
			while 1:
				n0 = waited_nodes.pop()
				edges = [ e for e in self.adj_n_e[n0] if id(e) not in walked_edges ]
				for e in edges:
					walked_edges.add(id(e))
					r.append(e)
					waited_nodes += list(e.difference(walked_nodes))
					walked_nodes |= e
				if len(waited_nodes) == 0: break
			assert len(walked_nodes) == len(self.nodes), self.draw(edges=r).show()
			return r
	if "odd-weight":
		def set_odd_weight_OddWeight(self):
			for i, (e, w) in enumerate(self.wedges()):
				self.set_edge_weight(e, OddWeight(w, [i]) )
			return self
	if "R":
		#
		def get_R(self, nodes, *, ms_len=None) -> int:
			"""
				算法：加入虚拟0边前后计算mst_
					R = mst - mst_
				"""
			if ms_len == None: ms_len = self.ms_len()
			goback = self.set_wedge_temp( (nodes, 0 ))
			#
			mst_len_ = self.ms_len()
			r = ms_len - mst_len_
			goback()
			return r
		def Rgraph_from_groups(self, groups) -> 'weighted_hg':
			wedges = []
			ms_len = self.ms_len()
			for group in groups:
				group = set(group)
				w = self.get_R(group, ms_len=ms_len)
				wedges.append( (group, w) )
			r = HyperGraph.from_wedges(wedges, pos=self)
			return r
		def full_Rgraph(self, *, ran=None) -> 'HyperGraph': 
			"""
				ran: 子集长度
				"""
			groups = my.comb.comb_range(self.nodes, my.slice.inter((2,None), ran))
			r = self.Rgraph_from_groups(groups)
			return r
		def Rgraph(self) -> 'hg':
			"""
				设置权重为r
				"""
			assert self.check_span()
			get_r = self.R_getter()
			hg = self.copy(weight=get_r)
			return hg

			
		def R_getter(self, *, ms_len=None) -> 'getter(nodes) -> int':
			map = DictOfSet()
			if ms_len == None: ms_len = self.ms_len()
			def getter(nodes):
				assert isinstance(nodes, set)
				if nodes in map: return map[nodes]
				#
				r = self.get_R(nodes, ms_len=ms_len)
				map[nodes] = r
				return r
			return getter
		# K
		def get_k_exist(self, nodes):
			hg_ = self.copy().disconnect(nodes)
			if not hg_.is_span():
				return 'inf'
			k = hg_.get_R(nodes)
			return k
		def K_getter(self):
			"""
				算法
					白边或不存在的边返回R
					黑边删去e后计算R
				"""
			ms = self.ms()
			# ms_len = self.ms_len()
			get_r = self.R_getter(ms_len=ms.len())

			def get(nodes):
				assert isinstance(nodes, set)
				if ms.has_edge(nodes):
					return self.get_k_exist(nodes)
				else:
					return get_r(nodes)
			return get
		def Kgraph(self) -> 'hg':
			"""
				设置权重为k
				"""
			assert self.check_span()
			get_k = self.K_getter()
			hg = self.copy(weight=get_k)
			return hg

		# Ru
		newest_Ru_version = 1 + 1
		default_Ru_version = 1 + 0
		def Ru_getter(self, v=None, **ks):
			"""
				2以后是depth
				1: depth=0
				"""
			if v == None: v = self.default_Ru_version
			if v >= 2:
				return self.Ru_getter_depth(depth=v-1)
			name = f'Ru_getter{v}'
			call = getattr(self, name)
			if de.print_getter_created: print(f'Ru-getter{v} created')
			return call( **ks)
		def Ru_getter0(self) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst -> 多元Ru
				"""
			raise
			sub_ngraph = self.extract_weighted_ngraph()
			sub_nmst = sub_ngraph.mst()
			tgraph = self.tgraph()
			map2 = tgraph.get_bottle_neck_from_mst(mst=sub_nmst)
			map = DictOfSet( [set(e), w] for e, w in map2.items() )
			def getter(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 3
				edges_ = my.comb.comb2_tuple(nodes)
				graph_ = Graph.from_edges(edges_)
				v = graph_.mst_len(weight=map2)
				map[nodes] = v
				return v
			return getter
		def Ru_getter100(self) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
				实现：
					先计算连通普通图的mst
					需要时扩展
				"""
			sub_ngraph = self.extract_weighted_ngraph()
			get2 = sub_ngraph.R_getter()
			map = DictOfSet()
			def getter(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			return getter
		def Ru_getter1(self) -> 'getter(nodes) -> Ru1':
			"""
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：

					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
				实现：
					先计算连通普通图的mst:包括包含的超边的完全tgraph
					需要时扩展
				"""
			# tgraph
			tgraph = self.tgraph()
			for e in self.edges:
				w = self.weight[e]
				for ne in my.comb.comb(e, 2, typ=tuple):
					w_ = tgraph.weight.get(ne, None)
					if w_ == None or w < w_:
						tgraph.set_edge_weight(ne, w)
			
			# sub_ngraph = self.extract_weighted_ngraph()
			get2 = tgraph.R_getter()
			map = DictOfSet()
			def getter(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			return getter
		def Ru_getter299(self, vrb=0) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
					利用公式 r(ab) <= r(abc) - r(bc)|r(ac) 
						u(ab) := u(abc) - max( b(bc) b(ac) )
						(存在的超边）
				"""

			sub_ngraph = self.extract_weighted_ngraph()
			sub_nmst = sub_ngraph.mst()
			tgraph = self.tgraph()
			map2 = tgraph.get_bottle_neck_from_mst(mst=sub_nmst)
			map = DictOfSet( [set(e), w] for e, w in map2.items() )
			get_rb = self.Rb_getter(vrb)
			def getter(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 3
				vs = []
				# bottle2-mst
				edges_ = my.comb.comb2_tuple(nodes)
				graph_ = Graph.from_edges(edges_)
				v1 = graph_.mst_len(weight=map2)
				vs.append(v1)
				# exist
				if self.has_edge(nodes):
					v2 = self.weight[nodes]
					vs.append(v2)
				#
				v = min(vs)
				map[nodes] = v
				return v
			# v2
			get_r  = self.R_getter()
			for sup in self.edges:
				if len(sup) != 3: continue
				u0 = getter(sup)
				nedges = my.comb.comb2_set(sup)
				for (e1,), (e2, e3) in my.comb.comb(nedges, 1, 2):
					b2 = get_rb(e2)
					b3 = get_rb(e3)
					u1_ = u0 - min(b2, b3)
					if u1_ < map[e1]:
						map[e1] = u1_
						if 0:
							r1 = get_r(e1)
							if not u1_ >= r1:
								r0 = get_r(sup)
								r2 = get_r(e2)
								r3 = get_r(e3)
								raise
			return getter
		def Ru_getter200(self) -> 'getter(nodes) -> Ru1': # 循环使用
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
					差
						r(b..) <= m - min( r[-m](ab) .. )
				实现：
					先计算连通普通图的mst
					需要时扩展
				说明-差
					每一个超边需要独立的一个get_b
					先用默认方式实现一个get_u，
						在对每个超边进行更新
						更新时使用最新的get_u？
				算法
					对所有大于2超边，计算每个小一子集的差Ru，与getter1的Ru进行比较取最小
				"""
			sub_ngraph = self.extract_weighted_ngraph()
			sub_ngraph.update_nodes(self.nodes)
			# add 0 edges
			# subs = sub_ngraph.nodeSubs(isolated=True)
			# reprs = [ my.pick(sub) for sub in subs ]
			# arrows = my.misc.get_arrow_by_nodes(reprs)
			# sub_ngraph.connectmw( [ (arrow, 0) for arrow in arrows ] )
			assert sub_ngraph.check_span(self.nodes)
			#
			weight = self.weight
			get2 = sub_ngraph.R_getter()
			map = DictOfSet()
			#
			def get(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			# 差
			for e0 in self.edges: 
				if len(e0) <= 2: continue
				w0 = weight[e0]
				hg_ = self.copy().disconnect(e0) ###
				get_b_e0 = hg_.Rb_getter(get_u=get)
				# print(f'a b-getter created')
				for a in e0:
					sub = my.set.removed(e0, a)
					rb_ab_list = [ get_b_e0( {a, b} ) for b in sub ]
					min_rb = min(rb_ab_list)
					v = w0 - min_rb
					# compare with v_
					v_ = get(sub)
					if v < v_:
						# if sub in map:
						# 	print(f'update-delta: {map[sub]} -> {v}  {sub}')
						map[sub] = v

			return get
		def Ru_getter_depth000(self, depth=1) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
					差
						r(b..) <= m - min( r[-m](ab) .. )
				实现：
					先计算连通普通图的mst
					需要时扩展
				说明-差
					每一个超边需要独立的一个get_b
					先用默认方式实现一个get_u，
						在对每个超边进行更新
						更新时使用最新的get_u？
						循环往复，直到所有超边都无法更新
				算法
					对所有大于2超边，计算每个小一子集的差Ru，与getter1的Ru进行比较取最小
				"""
			if depth == 0: return self.Ru_getter1()
			sub_ngraph = self.extract_weighted_ngraph()
			weight = self.weight
			get2 = sub_ngraph.R_getter()
			map = DictOfSet()
			# get_b = self.Rb_getter()
			#
			def get(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			# 差
			big_edges = [e for e in self.edges if len(e) >= 3]
			len_big_edges = len(big_edges)
			# non_update_count = 0
			for e0 in big_edges:
				w0 = weight[e0]
				hg_ = self.copy().disconnect(e0) ###
				get_b_e0 = hg_.Rb_getter_depth(depth=depth-1)
				update = False
				for a in e0:
					sub = my.set.removed(e0, a)
					rb_ab_list = [ get_b_e0( {a, b} ) for b in sub ]
					min_rb = min(rb_ab_list)
					v = w0 - min_rb
					# compare with v_
					v_ = get(sub)
					if v < v_:
						# print(f'update-delta: {map[sub]} -> {v}  {sub}')
						map[sub] = v
						update = True
				# count
				# if update:
				# 	non_update_count = 0
				# else:
				# 	non_update_count += 1
				# 	if non_update_count == len_big_edges: break

			return get
		def Ru_getter300(self) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
					差
						r(b..) <= m - min( r[-m](ab) .. )
				实现：
					先计算连通普通图的mst
					需要时扩展
				说明-差
					每一个超边需要独立的一个get_b
					先用默认方式实现一个get_u，
						在对每个超边进行更新
						更新时使用最新的get_u？
						循环往复，直到所有超边都无法更新
				算法
					对所有大于2超边，计算每个小一子集的差Ru，与getter1的Ru进行比较取最小
				"""
			sub_ngraph = self.extract_weighted_ngraph()
			weight = self.weight
			get2 = sub_ngraph.R_getter()
			map = DictOfSet()
			#  = self.Rb_getter()
			#
			def get(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			# 差
			big_edges = [e for e in self.edges if len(e) >= 3]
			len_big_edges = len(big_edges)
			non_update_count = 0
			for e0 in my.iter.loop(big_edges):
				w0 = weight[e0]
				hg_ = self.copy().disconnect(e0) ###
				get_b_e0 = hg_.Rb_getter(get_u=hg_.Ru_getter2())
				update = False
				for a in e0:
					sub = my.set.removed(e0, a)
					rb_ab_list = [ get_b_e0( {a, b} ) for b in sub ]
					min_rb = min(rb_ab_list)
					v = w0 - min_rb
					# compare with v_
					v_ = get(sub)
					if v < v_:
						# print(f'update-delta: {map[sub]} -> {v}  {sub}')
						map[sub] = v
						update = True
				# count
				if update:
					non_update_count = 0
				else:
					non_update_count += 1
					if non_update_count == len_big_edges: break

			return get
		def Ru_getter_depth(self, depth=0) -> 'getter(nodes) -> Ru1':
			"""
				要求：hg中包含一个连通普通图
				返回：getter(nodes), nodes 不要求是self某个超边的子集
				算法：
					普通子图的瓶颈算法 -> 二元Ru
					二元瓶颈的mst | 存在的超边 -> 多元Ru
					差
						r(b..) <= m - min( r[-m](ab) .. )
				实现：
					先计算连通普通图的mst
					需要时扩展
				说明-差
					每一个超边需要独立的一个get_b
					先用默认方式实现一个get_u，
						在对每个超边进行更新
						更新时使用最新的get_u？
						循环往复，直到所有超边都无法更新
				算法
					对所有大于2超边，计算每个小一子集的差Ru，与getter1的Ru进行比较取最小
				"""
			if depth == 0: return self.Ru_getter1()
			tgraph = self.tgraph()
			for e in self.edges:
				w = self.weight[e]
				for ne in my.comb.comb(e, 2, typ=tuple):
					w_ = tgraph.weight.get(ne, None)
					if w_ == None or w < w_:
						tgraph.set_edge_weight(ne, w)
			#
			weight = self.weight
			get2 = tgraph.R_getter()
			map = DictOfSet()
			# get_b = self.Rb_getter()
			#
			def get(nodes):
				if nodes in map:
					return map[nodes]
				assert len(nodes) >= 2
				if len(nodes) == 2:
					v = get2(tuple(nodes))
				else:
					vs = []
					# bottle2-mst
					nedges_ = my.comb.comb2_tuple(nodes)
					graph_ = Graph.from_edges(nedges_, weight=get2)
					v1 = graph_.mst_len()
					vs.append(v1)
					# exist
					if self.has_edge(nodes):
						v2 = self.weight[nodes]
						vs.append(v2)
					v = min(vs)
				map[nodes] = v
				return v
			# 差
			big_edges = [e for e in self.edges if len(e) >= 3]
			len_big_edges = len(big_edges)
			# non_update_count = 0
			for e0 in big_edges:
				w0 = weight[e0]
				hg_ = self.copy().disconnect(e0) ###
				if not hg_.is_span(): # e0断开树, k=inf, r=e0
					assert e0 not in map or map[e0] == w0
					continue
				get_b_e0 = hg_.Rb_getter_depth(depth=depth-1)
				# d.count()
				update = False
				for a in e0:
					sub = my.set.removed(e0, a)
					rb_ab_list = [ get_b_e0( {a, b} ) for b in sub ]
					min_rb = min(rb_ab_list)
					v = w0 - min_rb
					# compare with v_
					v_ = get(sub)
					if v < v_:
						# print(f'update-delta: {map[sub]} -> {v}  {sub}')
						map[sub] = v
						update = True
				# count
				# if update:
				# 	non_update_count = 0
				# else:
				# 	non_update_count += 1
				# 	if non_update_count == len_big_edges: break

			return get
		def seperate_Ru_getter_depth(self, depth=0, fail=Pass):
			"""
				当nodes横跨不同部分时返回fail
				"""
			subs = self.graphSubs()
			n_i_map = {}
			getters = []
			for i, sub in enumerate(subs):
				getter = sub.Ru_getter_depth(depth=depth)
				getters.append(getter)
				for n in sub.nodes:
					n_i_map[n] = i
			map = DictOfSet()
			def get(nodes):
				assert isinstance(nodes, set)
				v = map.get(nodes, None)
				if v != None:
					return v
				# get
				li = [ n_i_map[n] for n in nodes ]
				i = li[0]
				if not my.all_equal(li):
					if fail == Pass: raise Exception(f'{nodes}')
					v = fail
				else:
					getter = getters[i]
					v = getter(nodes)
				map[nodes] = v
				return v
			return get
		# Rb
		newest_Rb_version = 0 + 0
		default_Rb_version = 0 + 0
		def Rb_getter_str(self, *gs, get=None, **ks):
			if get == None:
				get = self.Rb_getter(*gs, **ks)
			def getter(nodes):
				if len(nodes) == 2:
					return get(nodes)
				else:
					return ''
			return getter
		Rb_getter_ignore = Rb_getter_str
		def Rb_getter(self, v=None, **ks):
			if v == None: v = self.default_Rb_version
			if v >= 1:
				return self.Rb_getter_depth(depth=v)
			name = f'Rb_getter{v}'
			call = getattr(self, name)
			if de.print_getter_created: print(f'Rb-getter{v} created')
			return call(**ks)
		def Rb_getter00(self, *, get_u=None):
			"""
				use:
					只允许tgraph中二元边
				算法：
					计算tgraph的单元距离值val
					tgraph的瓶颈图
				"""
			if get_u == None: get_u = self.Ru_getter(vru)
			
			def get_sup_n_val(sup, n):
				if len(sup) == 2: return self.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = self.weight[sup]
				r = w - B_oppos
				return max(r, 0)
			# tgraph
			tgraph = self.tgraph()
			#. v(n:sup)
			sup_n_val = DictOfSet()
			for sup in self.edges:
				sup_n_val[sup] = map_ = {}
				for n in sup:
					map_[n] = get_sup_n_val(sup, n)

			#. v(ne)
			val_ne_in_sup = {}
			for sup in self.edges:
				for e2 in my.comb.comb2(sup):
					a, b = e2 = sorted2(e2)
					v = max( sup_n_val[sup][a], sup_n_val[sup][b] )
					if e2 not in val_ne_in_sup or val_ne_in_sup[e2] > v:
						1
						val_ne_in_sup[e2] = v
			map_ne = tgraph.get_bottle_neck(weight=val_ne_in_sup, mode='v') # dict
			map = DictOfSet([ (set(e2), v) for e2, v in map_ne.items() ])
			# get_r = self.R_getter()
			def get(nodes):
				# assert len(nodes) == 2
				rb = map[nodes]
				if 0:
					r = get_r(nodes)
					assert rb <= r
				return rb
			return get
		def Rb_getter0(self, *, get_u=None):
			"""
				use:
					只允许二元边
				算法：
					val根据Ru1计算
					计算tgraph的单元距离值val
					tgraph的瓶颈图
				"""
			if get_u == None: get_u = self.Qu_getter(1)
			
			def get_sup_n_val(sup, n):
				if len(sup) == 2: return self.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = self.weight[sup]
				r = w - B_oppos
				return max(r, 0)
			# tgraph
			tgraph = self.tgraph()
			#. v(n:sup)
			sup_n_val = DictOfSet()
			for sup in self.edges:
				sup_n_val[sup] = map_ = {}
				for n in sup:
					map_[n] = get_sup_n_val(sup, n)

			#. v(ne)
			val_ne_in_sup = {}
			for sup in self.edges:
				for e2 in my.comb.comb2(sup):
					a, b = e2 = sorted2(e2)
					v = max( sup_n_val[sup][a], sup_n_val[sup][b] )
					if e2 not in val_ne_in_sup or val_ne_in_sup[e2] > v:
						1
						val_ne_in_sup[e2] = v
			get_b2 = tgraph.R_getter(weight=val_ne_in_sup) # dict
			# map = DictOfSet([ (set(e2), v) for e2, v in map_ne.items() ])
			# get_r = self.R_getter()
			map = DictOfSet()
			def get(nodes):
				assert len(nodes) == 2
				nodes = set(nodes)
				b = map.get(nodes, None)
				if b == None:
					b = get_b2(sorted2(nodes))
					map[nodes] = b
					return b
				else:
					return b 
			return get
		def Rb_getter_depth(self, *, depth=0, get_u=None):
			"""
				use:
					只允许二元边
				算法：
					val根据Ru1计算
					计算tgraph的单元距离值val
					tgraph的瓶颈图
				"""
			if get_u == None: get_u = self.Ru_getter_depth(depth=depth)
			
			def get_sup_n_val(sup, n):
				if len(sup) == 2: return self.weight[sup]
				oppos = my.set.removed(sup, n)
				B_oppos = get_u(oppos)
				w = self.weight[sup]
				r = w - B_oppos
				return max(r, 0)
			# tgraph
			tgraph = self.tgraph()
			#. v(n:sup)
			sup_n_val = DictOfSet()
			for sup in self.edges:
				sup_n_val[sup] = map_ = {}
				for n in sup:
					map_[n] = get_sup_n_val(sup, n)

			#. v(ne)
			val_ne_in_sup = {}
			for sup in self.edges:
				for e2 in my.comb.comb2(sup):
					a, b = e2 = sorted2(e2)
					v = max( sup_n_val[sup][a], sup_n_val[sup][b] )
					if e2 not in val_ne_in_sup or val_ne_in_sup[e2] > v:
						1
						val_ne_in_sup[e2] = v
			get_b2 = tgraph.R_getter(weight=val_ne_in_sup) # dict
			# map = DictOfSet([ (set(e2), v) for e2, v in map_ne.items() ])
			# get_r = self.R_getter()
			map = DictOfSet()
			def get(nodes):
				assert len(nodes) == 2
				nodes = set(nodes)
				b = map.get(nodes, None)
				if b == None:
					b = get_b2(sorted2(nodes))
					map[nodes] = b
					return b
				else:
					return b 
			return get
		def seperate_Rb_getter_depth(self, depth=0, get_u=None, fail=Pass):
			"""
				当nodes横跨不同部分时返回fail
				fail==Pass -> raise
				"""
			subs = self.graphSubs()
			n_i_map = {}
			getters = []
			for i, sub in enumerate(subs):
				getter = sub.Rb_getter_depth(depth=depth, get_u=get_u)
				getters.append(getter)
				for n in sub.nodes:
					n_i_map[n] = i
			map = DictOfSet()
			def get(nodes):
				assert isinstance(nodes, set)
				v = map.get(nodes, None)
				if v != None:
					return v
				# get
				li = [ n_i_map[n] for n in nodes ]
				i = li[0]
				if not my.all_equal(li):
					if fail == Pass: raise Exception(f'{nodes}')
					v = fail
				else:
					getter = getters[i]
					v = getter(nodes)
				map[nodes] = v
				return v
			return get
	# Qu
		newest_Qu_version = 0
		def Qu_getter(self, v=None, **ks):
			if v == None: v = self.newest_Qu_version
			name = f'Qu_getter{v}'
			call = getattr(self, name)
			return call(**ks)
		def Qu_getter1(self):
			return self.Ru_getter1()
	if "draw":		
		# fit
		appropriate_node_size = Graph.appropriate_node_size
		appropriate_edge_width = Graph.appropriate_edge_width
		# draw
		@dynamicmethod
		def view(self, edges, *, pos) -> '<list>edges, vnodes(pos), vedges(pos)':
			"""
				点是各边的中心
				边是中心到点
				"""
			edges = list(edges)
			vnodes = []
			vedges = []
			for e in edges:
				center = my.geo.average_center( { pos[n] for n in e })
				vnodes.append(center)
				for n in e:
					vedges.append( (pos[n], center) )
			return edges, vnodes, vedges
		@dynamicmethod
		def prepare_draw(self, **ks):
			return Graph.prepare_draw(**ks)
		def draw(self, *, edges=None, nodes=None, hl_nodes=[], hl_edges=[], hl_edges1=[],
				edge_label=False, node_label=False, 
				node_look={}, enode_look={}, edge_look={}, 
				pos=None, **ks):
			hl_edges = list(hl_edges)
			hl_edges1 = list(hl_edges1)
			hl_nodes = list(hl_nodes)
			if edges == None: edges = self.edges
			if nodes == None: nodes = self.nodes
			#
			pos = self.get_pos(nodes=nodes, pos=pos)
			ks = self.prepare_draw(**ks)
			node_look = default.HyperGraph.node | node_look
			edge_look = default.HyperGraph.edge | edge_look
			enode_look = default.HyperGraph.enode | enode_look
			#
			if not myplt.flag_axis_set(): 
				myplt.set_axis_by_nodes(self.get_pos().values())
			# get-edges
			normal_edges = my.unhashableSet.difference(edges, hl_edges + hl_edges1)
			# assert my.unhashableSet.no_overlap(hl_edges, hl_edges1)
			# main
			self._draw_edges(normal_edges, pos=pos, 
				edge_look=edge_look, enode_look=enode_look, label=edge_label, **ks)
			self._draw_edges(hl_edges, pos=pos, 
				edge_look=default.HyperGraph.hl_edge, enode_look=default.HyperGraph.hl_enode, label=edge_label, **ks)
			self._draw_edges(hl_edges1, pos=pos, 
				edge_look=default.HyperGraph.hl_edge1, enode_look=default.HyperGraph.hl_enode1, label=edge_label, **ks)
			Graph._draw_nodes(my.unhashableSet.difference(nodes, hl_nodes), pos=pos, 
				look=node_look, label=node_label, **ks)
			Graph._draw_nodes(hl_nodes, pos=pos, 
				look=default.HyperGraph.hl_node, label=node_label, **ks)
			return self
		@dynamicmethod
		def _draw_nodes(self, *gs, **ks):
			return Graph.__dict__['_draw_nodes'].func(self, *gs, **ks)
		@dynamicmethod
		def _draw_edges(self, edges, *, pos=None, enode_look={}, edge_look={}, label=False):
			enode_look = default.HyperGraph.enode | enode_look
			edge_look =  default.HyperGraph.edge | edge_look
			# pos = self.get_pos_by_edges(edges)
			pos = self.get_pos(edges=edges, pos=pos)
			# label
			edges_, vnodes, vedges = self.view(edges, pos=pos)
			if label in [False, 0]:
				pass
			elif label in [True, 1]:
				label = { vnodes[i]: self.weight[edges_[i]] for i in range(len(edges_)) }
			elif isinstance(label, DictOfSet):
				label = { vnodes[i]: label[edges_[i]] for i in range(len(edges_)) }
			elif isinstance(label, list):
				di = DictOfSet(label)
				label = { vnodes[i]: di[edges_[i]] for i in range(len(edges_)) }
			elif callable(label):
				label = { vnodes[i]: label(edges_[i]) for i in range(len(edges_)) if len(edges_[i]) == 2 }
			else: raise Exception(f'{label}')
			
			Graph._draw_nodes(vnodes, pos=pos_get_pos, look=enode_look, label=label)
			Graph._draw_edges(vedges, pos=pos_get_pos, look=edge_look)
			return {}
		def show(self, **ks):
			self.draw(**ks)
			myplt.show()
	if "mst":
		# ms
		def ms_len(self):
			ms = self.ms()
			return ms.len()
		def ms(self, **ks):
			return self.cacu_mst()
		
		@classmethod
		def get_edge_order_half(cls, nodes:list, edges_start:list, edges_end:list, *, mode=None, start:'edge'=None) -> '<iter>edges':
			"""
				arg:
					start: 开始的节点 (仅当empty(edges_start))
					mode: 'x'
						'delta': 优先选择delta最小的
				要求：
					nodes 位置有序
					edges == list<set>
					连通
				return 
					edges : list<int>
				delta: 连接的外点-待死点 <=> 选择后活跃点数量的改变量
				死点：degree == 1
				内点：degree == 0

				算法：
					按照事先预定的顺序加入节点
					若存在非正增益的，将非正增益的边加入
				"""
			if len(edges_end) == 0:
				return []
			if mode == None: mode = 'delta'
			assert isinstance(edges_start, list)
			assert isinstance(edges_end, list)
			nodes = list(nodes)
			assert my.is_sorted(nodes)
			i_e_list = edges_end # ei -> e 不变 <list> 和外面的i_e_map不同
			e_i_map = DictOfSet( (e, i) for i, e in enumerate(i_e_list) ) # 不变
			iedges = list(range(len(edges_end))) # 不变
			iedges_by_n = { n: set() for n in nodes } # 不变
			for e, e_ in enumerate(i_e_list):
				for n in e_:
					iedges_by_n[n].add(e)
			class ReturnSignal(Exception): ...
			match mode:
				case 0: raise
				case 'delta':
					def append(i):
						"""
							处理sorted_edge_delta_map
							"""
						# edge_order.a ppend(i)
						# yield i # 必须在call前yield
						ex = i_e_list[i]
						for n in ex:
							if n not in sorted_anodes: # 外点
								sorted_anodes.add(n)
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1 # 少了一个外点
							n_edges_map[n].remove(i)
							n_degree_map[n] -= 1
							if n_degree_map[n] == 1: # 不定点(待死点)
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1
							elif n_degree_map[n] == 0: # 这次加入后变成内点
								sorted_anodes.remove(n)
						sorted_iedge_delta_map.pop(i)
						# if len(sorted_anodes) == 0:
						# 	raise ReturnSignal
					
					# pre
					sorted_anodes = set() # 变化
					n_degree_map = { n: len(iedges_by_n[n]) for n in nodes } # 变化, degree: 未使用边
					n_edges_map = { n: iedges_by_n[n].copy() for n in nodes } # 变化, edges: 未使用边
					edge_delta_map = [ len(ex) for ex in i_e_list ] # 变化
					for n in nodes:
						if n_degree_map[n] == 1:
							for e in iedges_by_n[n]:
								edge_delta_map[e] -= 1
					sorted_iedge_delta_map = my.SortedDict( { i: edge_delta_map[i] for i in iedges }, key_v=lambda v:v )
					# first
					if empty(edges_start):
						if start == None: 
							istart = my.pick( sorted_iedge_delta_map.keys() )
							start = i_e_list[istart]
						else: 
							istart = e_i_map[start]
						assert istart < len(i_e_list), istart
						yield start
						append(istart)
					else:
						assert start == None
						for e in edges_start:
							i = e_i_map[e]
							append(i)
					# main
					while 1: # n
						if len(sorted_iedge_delta_map) == 0: return
						adj_edges = my.set.unionm_iterable(n_edges_map[n] for n in sorted_anodes)
						for i in sorted_iedge_delta_map.keys(): ###
							if i in adj_edges:
								yield i_e_list[i]
								append(i)
								break

				case _: raise Exception(f"not match {mode}")
		
		@classmethod
		def get_edge_order(cls, nodes:list, edges:list, *, mode=None, start:'edge'=None) -> '<iter>edges':
			"""
				arg:
					start: 开始的节点
					mode: 'x'
						'delta': 优先选择delta最小的
				要求：
					nodes 位置有序
					edges == list<set>
					连通
				return 
					edges : list<int>
				delta: 连接的外点-待死点 <=> 选择后活跃点数量的改变量
				死点：degree == 1
				内点：degree == 0

				算法：
					按照事先预定的顺序加入节点
					若存在非正增益的，将非正增益的边加入
				"""
			if len(edges) == 0:
				return []
			if mode == None: mode = 'delta'
			assert isinstance(edges, list)
			nodes = list(nodes)
			assert my.is_sorted(nodes)
			i_e_list = edges # ei -> e 不变 <list> 和外面的i_e_map不同
			e_i_map = DictOfSet( (e, i) for i, e in enumerate(i_e_list) )
			iedges = list(range(len(edges)))
			iedges_by_n = { n: set() for n in nodes } # 不变
			# edge_order = [] # 不变
			for e, e_ in enumerate(i_e_list):
				for n in e_:
					iedges_by_n[n].add(e)
			class ReturnSignal(Exception): ...
			match mode:
				case 0: raise
				case 'delta':
					def append(i):
						"""
							处理sorted_edge_delta_map
							"""
						# edge_order.a ppend(i)
						# yield i # 必须在call前yield
						ex = i_e_list[i]
						for n in ex:
							if n not in sorted_anodes: # 外点
								sorted_anodes.add(n)
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1 # 少了一个外点
							n_edges_map[n].remove(i)
							n_degree_map[n] -= 1
							if n_degree_map[n] == 1: # 不定点(待死点)
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1
							elif n_degree_map[n] == 0: # 这次加入后变成内点
								sorted_anodes.remove(n)
						sorted_iedge_delta_map.pop(i)
						# if len(sorted_anodes) == 0:
						# 	raise ReturnSignal
					
					#
					sorted_anodes = set()
					n_degree_map = { n: len(iedges_by_n[n]) for n in nodes }
					n_edges_map = { n: iedges_by_n[n].copy() for n in nodes } # 变化
					edge_delta_map = [ len(ex) for ex in i_e_list ]
					for n in nodes:
						if n_degree_map[n] == 1:
							for e in iedges_by_n[n]:
								edge_delta_map[e] -= 1
					sorted_iedge_delta_map = my.SortedDict( { i: edge_delta_map[i] for i in iedges }, key_v=lambda v:v )
					# first
					if start == None: 
						istart = my.pick( sorted_iedge_delta_map.keys() )
						start = i_e_list[istart]
					else: 
						istart = e_i_map[start]
					assert istart < len(i_e_list), istart
					yield start
					append(istart)

					while 1: # n
						if len(sorted_iedge_delta_map) == 0: return
						adj_edges = my.set.unionm_iterable(n_edges_map[n] for n in sorted_anodes)
						for i in sorted_iedge_delta_map.keys(): ###
							if i in adj_edges:
								yield i_e_list[i]
								append(i)
								break

				case 'x': # 
					raise
					def append(e):
						"""
							处理sorted_edge_delta_map
							"""
						# edge_order.a ppend(e)
						# yield e # 必须在call前yield
						ex = edges_map[e]
						for n in ex:
							if n not in sorted_anodes: # 外点
								sorted_anodes.add(n)
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1 # 少了一个外点
							n_edges_map[n].remove(e)
							n_degree_map[n] -= 1
							if n_degree_map[n] == 1: # 不定点
								for e1 in n_edges_map[n]:
									sorted_iedge_delta_map[e1] -= 1
							elif n_degree_map[n] == 0: # 死点
								sorted_anodes.remove(n)
						sorted_iedge_delta_map.pop(e)
						if len(sorted_anodes) == 0:
							raise ReturnSignal
					def try_append_neg():
						while 1:
							e, delta = sorted_iedge_delta_map.index_item(0)
							if delta <= 0:
								yield e
								append(e)
							else: break
					#
					sorted_anodes = SortedList()
					n_degree_map = { n: len(iedges_by_n[n]) for n in nodes }
					n_edges_map = { n: iedges_by_n[n].copy() for n in nodes } # 变化
					edge_delta_map = [ len(ex) for ex in edges_map ]
					for n in nodes:
						if n_degree_map[n] == 1:
							for e in iedges_by_n[n]:
								edge_delta_map[e] -= 1
					sorted_iedge_delta_map = my.SortedDict( { i: edge_delta_map[i] for i in edges }, key_v=lambda v:v )
					# first
					if start == None: start = nodes[0]
					sorted_anodes.add(start)
					try:
						while 1: # n
							try_append_neg()
							n = sorted_anodes[0]
							for e in list(n_edges_map[n]):
								if e in n_edges_map[n]:
									yield e
									append(e)
									try_append_neg()
					except ReturnSignal:
						return 

				case 'y': raise
				
				case _: raise Exception(f"not match {mode}")
		
		# misc
		def edge_in_mst(self, e, *, mst=None):
			"""
				存在一个包含e的mst
				"""
			if mst == None: mst = self.mst_quick()
			if mst.has_edge(e): return True
			hg = self
			goback = hg.set_wedge_temp( (e, 0 ) )
			if not hg.is_span(): 
				r = False
			else:
				mst_len_ = hg.mst_len()
				r = hg.mst_len() == mst.len()
			goback()
			return r
		def edge_not_in_mst(self, e, *, mst=None):
			"""
				存在一个不包含e的mst
				"""
			if mst == None: mst = self.mst_quick()
			if not mst.has_edge(e): return True
			hg = self
			goback = hg.disconnect_temp( e )
			if not hg.is_span():
				r = False
			else:
				mst_len_ = hg.mst_len()
				r = hg.mst_len() == mst.len()
			goback()
			return r
		def edge_in_mst_state(self, e, *, mst=None) -> int:
			"""
				0: not exist in any
				1: exist in any
				2: exist in some and not in others
				"""
			exist = None
			if mst == None: mst = self.mst_quick()
			if mst.has_edge(e):
				not_exist = self.edge_not_in_mst(e, mst=mst)
				if not_exist: return 2
				else: return 1
			else:
				exist = self.edge_in_mst(e, mst=mst)
				if exist: return 2
				else: return 0
		def edge_in_mst_state_str(self, *gs, **ks):
			state = self.edge_in_mst_state(*gs, **ks)
			match state:
				case 0: return 'not-exist-in-any'
				case 1: return 'exist-in-any'
				case 2: return 'both'
				case _: raise Exception(f"not match {state}")
		def state_in_mst(self, *, edges1, edges0, mst=None, mst_len=None, check_in_provided=True):
			"""
				当前层可能在一个mst中
				"""
			
			if mst is not None and check_in_provided:
				if mst.match_state(edges1=edges1, edges0=edges0):
					return True
			w0 = self.edges_weight_sum(edges1)
			hg = self.copy().set_layer(edges1=edges1, edges0=edges0)
			le = hg.mst_len(fail=None)
			# if le is None:
			# 	# d(hg.is_span())
			# 	# d('fail').count()
			# 	# self.draw()
			# 	# hg.show()
			# 	return False
			if mst_len is not None: pass
			elif mst is not None: mst_len = mst.len()
			else: mst_len = self.mst_len()
			# assert mst_len <= le + w0
			if isinstance(mst_len, float):
				# d(abs(mst_len - (le + w0)))
				return abs(mst_len - (le + w0)) <= 0.5
			else:
				return mst_len == le + w0
		# mst
		def mst_len(self, fail=Pass): ###
			"""
				当自身不连通时
				"""
			if fail is Pass:
				assert self.check_span()
				return self.mst().len()
			else:
				if self.is_span():
					mst = self.mst(fail=None)
					if mst == None:
						return fail
					else:
						return mst.len()
				else:
					return fail
			
		def mst(self, *, debug=0, pos:dict=None, trace:'HyperGraph'=None, cut_mode=0, no_cycle=1, cond=0):
			"""
				扩展方式：
					选择一个点，一次选择该点连接的所有边
					优先级：
						优先选择选择完边后新增节点最少的, 
				伪码
					找到下一个点
						将这个点的所有邻边依次加入
							排除循环，包含
				debug 0|1|2
					0: 无
					1：全部
					2：不包括幻组
				cut_mode: 0: cover 1:equal
				
				"""
			# pre
			debug = de.mst and debug
			if pos == None: pos = self.get_pos(self.nodes)
			weight = self.weight
			nodes = self.nodes
			edges_r = self.edges.copy() # 不需要deepcopy， 因为edge不会改变
			edges_used = []
			n_edges_map = {n: self.adj_n_e[n].copy() for n in self.nodes} # 未使用边
			igroups = set() # 幻组
			anodes = set() # 导点
			anodes_degree_n_n = my.SortedDict(key_v=lambda v:v) # 按未使用邻居点数排序，仅包含导点， 用于选点
			inodes = set()
			used_nodes = set() # 活跃 + 内点
			unused_nodes = set(nodes)
			new_nodes = set() # tmp
			new_anodes = set()
			min_ig = None
			min_weight = math.inf
			# debug
			count_equal_span = 0
			count_cut = 0
			list_count_state = []
			list_count_anode = []
			#
			if cut_mode == 0:
				cut_judge = Igroup.can_be_replaced_by_cover
			elif cut_mode == 1:
				cut_judge = Igroup.can_be_replaced_by_equal
			else: raise Exception(f'{0}')
			
			# anodes_degree_n_e = {} # 用于计算
			def react_new_anode(n):
				anodes.add(n)
				anodes_degree_n_n[n] = self.degree_n_n(n)
				new_anodes.add(n)
				# anodes_degree_n_e[n] = 
			def react_del_anode(n):
				anodes.remove(n)
				del anodes_degree_n_n[n]
			def react_new_node(n):
				new_nodes.add(n)
				used_nodes.add(n)
				unused_nodes.remove(n)
			def draw_edges_r():
				Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
				HyperGraph._draw_edges([e], pos=pos, color='orange')
				Graph._draw_nodes(unused_nodes, pos=pos, color='grey', alpha=0.5)
				myplt.title(f'i={len(igroups)} a={len(anodes)}')
			def debug_draw():
				cond2 = cond and len(igroups) >= 12
				cond1 = cond2
				if debug == 2 or cond2:
					myplt.new_figure()
				# edges-remained
				if debug >= 1 or cond1:
					draw_edges_r()
				if debug == 2 or cond2:
					# igs
					matched_found = 0
					for ig in igroups:
						ig.draw(inodes, anodes, used_nodes, pos)
				
			# first
			# n0 = newCountMap.popIndex_key(0)
			n0 = min( self.nodes, key=lambda n: self.degree_n_n(n) )
			react_new_node(n0)
			react_new_anode(n0)
			ig0 = Igroup(weight=0, graph=self)
			ig0.add_anode(n0)
			igroups.add(ig0)
			
			# main
			while 1:
				n_include = anodes_degree_n_n.index_key(0)
				edges = n_edges_map[n_include]
				for e in list(edges): # e
					new_inodes = set()
					new_anodes = set()
					new_nodes = set()
					degree_minus = len(e) - 1
					w = weight[e]
					edges_used.append(e)
					# 预处理节点 ( e =  new_anodes new_inodes non-change ) ( new_nodes = new_anodes + new_inodes部分 )
					# new_anodes: 新增加的anode <=> 新增的点去掉e后还有边
					# new_inodes: <=> 去掉e后一条边都不剩（所有新增inode）
					# new_nodes:  new_anodes + borni
					for n in e:
						if n not in anodes: # new-nodes
							react_new_node(n)
						n_edges_map[n].remove(e)
						if len(n_edges_map[n]) == 0: # new-inodes
							new_inodes.add(n)
							if n in anodes: # a -> i
								react_del_anode(n)
							else: # born i
								pass
						else:
							if n not in anodes: # new-anodes
								react_new_anode(n)
							else: # non-change
								pass
							anodes_degree_n_n[n] = len(my.set.unionm(n_edges_map[n])) - 1
							assert anodes_degree_n_n[n] >= 0
					#
					1
					inodes |= new_inodes
					igroups_ = set()
					flag_terminate = len(inodes) == len(nodes) # 绝对终止
					flag_terminate2 = len(used_nodes) == len(nodes) # 可能终止
					if trace:
						match_add = e in trace.edges
					# 过滤 循环 孤立
					for ig in igroups:
						#
						not_add, add = ig.judge_add_e(e, new_anodes, new_inodes, flag_terminate2, no_cycle=no_cycle)
						if not_add:
							if add:
								ig1 = ig
								ig2 = ig.copy()
							else:
								ig1 = ig
						else:
							if add:
								ig2 = ig
							else: pass
						#
						if not_add:
							ig1.add_anodes(new_anodes)
							igroups_.add(ig1.not_add_e(new_inodes))
						if add:
							ig2.add_anodes(new_anodes) # 此时ig中包含除了borni的所有点
							ig2.add_e(e, w, new_inodes)
							if flag_terminate2 and ig2.is_terminated(): # terminated
								if min_ig == None:
									min_ig = ig2
									min_weight = ig2.weight
								else:
									if ig2.weight < min_weight:
										min_ig = ig2
										min_weight = ig2.weight
								continue
							else:
								igroups_.add(ig2)
					#同型 过滤
					if 1:
						ghash_ig_map = {}
						for ig in igroups_:
							ghash = hash(ig.group)
							if ghash not in ghash_ig_map: ghash_ig_map[ghash] = ig
							else:
								count_cut += 1
								ig0 = ghash_ig_map[ghash]
								if ig.weight < ig0.weight:
									ghash_ig_map[ghash] = ig
						igroups = set(ghash_ig_map.values())
					elif 1:
						for ig1 in list(igroups_):
							if ig1.weight >= min_weight:
								igroups_.remove(ig1)
								continue
							for ig2 in igroups_:
								if ig1 is ig2: continue
								if cut_judge(ig1, ig2):
									if debug and de.cut_equal_cover:
										count_cut += 1
										if ig1.equal_span(ig2):
											count_equal_span += 1
									igroups_.remove(ig1)
									break
						igroups = igroups_
					edges_r.remove(e)
					1
					if debug:
						list_count_state.append(len(igroups))
						list_count_anode.append(len(anodes))
					debug_draw()
				if 1: ###
					for ig in igroups:
						ig.group.check()
				if flag_terminate2 and len(igroups) == 0: # terminate
				
					edges = min_ig.edges
					if debug and de.cut_equal_cover:
						match cut_mode:
							case 0: cut_mode_str = 'cover'
							case 1: cut_mode_str = 'equal'
							case _: raise
						print(f'cut-mode: {cut_mode_str}')
						if cut_mode == 0:
							print(f'equal/cover: {count_equal_span} / {count_cut}')
						else:
							print(f'equal: {count_equal_span}')
					if debug:
						print(f'state-count: {mystr(list_count_state)}')
						print(f'\taverage={my.average(list_count_state)} max={max(list_count_state)}')
						print(f'anode-count: {mystr(list_count_anode)}')
						print(f'\taverage={my.average(list_count_anode)} max={max(list_count_anode)}')
					r = HyperGraph.from_edges(edges, pos=self.get_pos, weight=self.weight)
					return r
				if flag_terminate:
					raise
				# pause(len(igroups))
				1
		def cacu_mst1(self, *, debug=0, pos:dict=None, trace:'HyperGraph'=None, cut_mode=0, no_cycle=1, cond=0, order_mode=None, **ks):
			"""
				要求：
					nodes按照顺序编号
				扩展方式：
					选择一个点，一次选择该点连接的所有边
					优先级：
						优先选择选择完边后新增节点最少的, 
				伪码
					找到下一个点
						将这个点的所有邻边依次加入
							排除循环，包含
				debug 0|1|2
					0: 无
					1：全部
					2：不包括幻组
				cut_mode: 0: cover 1:equal
				order_mode: 0: default 'x' 'y'
				"""
			# pre
			debug = de.mst and debug
			if pos == None: pos = self.get_pos(self.nodes)
			weight = self.get_weight_dict()
			nodes = sorted(self.nodes)
			edges_r = self.edges.copy() # 不需要deepcopy， 因为edge不会改变
			edges_used = []
			n_edges_map = {n: self.adj_n_e[n].copy() for n in self.nodes} # 未使用边
			igroups = set() # 幻组
			anodes = set() # 导点
			anodes_degree_n_n = my.SortedDict(key_v=lambda v:v) # 按未使用邻居点数排序，仅包含导点， 用于选点
			inodes = set()
			used_nodes = set() # 活跃 + 内点
			unused_nodes = set(nodes)
			new_nodes = set() # tmp
			new_anodes = set()
			min_ig = None
			min_weight = math.inf
			# order
			edge_map = list(self.edges)
			edge_order = self.get_edge_order(nodes, edge_map, mode=order_mode)
			# debug
			count_equal_span = 0
			count_cut = 0
			list_count_state = []
			list_count_anode = []
			# cut-mode
			if cut_mode == 0:
				cut_judge = Igroup.can_be_replaced_by_cover
			elif cut_mode == 1:
				cut_judge = Igroup.can_be_replaced_by_equal
			else: raise Exception(f'{0}')
			
			# anodes_degree_n_e = {} # 用于计算
			def react_new_anode(n):
				anodes.add(n)
				anodes_degree_n_n[n] = self.degree_n_n(n)
				new_anodes.add(n)
				# anodes_degree_n_e[n] = 
			def react_del_anode(n):
				anodes.remove(n)
				del anodes_degree_n_n[n]
			def react_new_node(n):
				new_nodes.add(n)
				used_nodes.add(n)
				unused_nodes.remove(n)
			def draw_edges_r():
				Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
				HyperGraph._draw_edges([e], pos=pos, edge_look=dict(color='orange'))
				Graph._draw_nodes(unused_nodes, pos=pos, look=dict(color='grey', alpha=0.5))
				myplt.title(f'i={len(igroups)} a={len(anodes)}')
			def debug_draw():
				cond2 = cond and len(igroups) >= 12
				cond1 = cond2
				if debug >= 6 or cond2:
					myplt.new_figure()
				# edges-remained
				if debug >= 5 or cond1:
					draw_edges_r()
				if debug >= 6 or cond2:
					# igs
					matched_found = 0
					for ig in igroups:
						ig.draw(inodes, anodes, used_nodes, pos)
				1
			# first
			# n0 = newCountMap.popIndex_key(0)
			ig0 = Igroup(0, self)
			if len(edge_order) != 0:
				n0 = my.pick(edge_map[edge_order[0]])
				ig0.add_anode(n0)
				react_new_node(n0)
				react_new_anode(n0)
			else:
				min_ig =ig0
			igroups.add(ig0)
			
			# main
			for ei in edge_order: # e
				e = edge_map[ei]
				new_inodes = set()
				new_anodes = set()
				new_nodes = set()
				degree_minus = len(e) - 1
				w = weight[e]
				edges_used.append(e)
				# 预处理节点 ( e =  new_anodes new_inodes non-change ) ( new_nodes = new_anodes + new_inodes部分 )
				# new_anodes: 新增加的anode <=> 新增的点去掉e后还有边
				# new_inodes: <=> 去掉e后一条边都不剩（所有新增inode）
				# new_nodes:  new_anodes + borni
				for n in e:
					if n not in anodes: # new-nodes
						react_new_node(n)
					n_edges_map[n].remove(e)
					if len(n_edges_map[n]) == 0: # new-inodes
						new_inodes.add(n)
						if n in anodes: # a -> i
							react_del_anode(n)
						else: # born i
							pass
					else:
						if n not in anodes: # new-anodes
							react_new_anode(n)
						else: # non-change
							pass
						anodes_degree_n_n[n] = len(my.set.unionm(n_edges_map[n])) - 1
						assert anodes_degree_n_n[n] >= 0
				#
				1
				inodes |= new_inodes
				igroups_ = set()
				flag_terminate = len(inodes) == len(nodes) # 绝对终止
				flag_terminate2 = len(used_nodes) == len(nodes) # 可能终止
				if trace:
					match_add = e in trace.edges
				# 过滤 循环 孤立
				for ig in igroups:
					#
					not_add, add = ig.judge_add_e(e, new_anodes, new_inodes, flag_terminate2, no_cycle=no_cycle)
					if not_add:
						if add:
							ig1 = ig
							ig2 = ig.copy()
						else:
							ig1 = ig
					else:
						if add:
							ig2 = ig
						else: pass
					#
					if not_add:
						ig1.add_anodes(new_anodes)
						igroups_.add(ig1.not_add_e(new_inodes))
					if add:
						ig2.add_anodes(new_anodes) # 此时ig中包含除了borni的所有点
						ig2.add_e(e, w, new_inodes)
						if flag_terminate2 and ig2.is_terminated(): # terminated
							if min_ig == None:
								min_ig = ig2
								min_weight = ig2.weight
							else:
								if ig2.weight < min_weight:
									min_ig = ig2
									min_weight = ig2.weight
							continue
						else:
							igroups_.add(ig2)
				#同型 过滤
				if 1:
					ghash_ig_map = {}
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_ig_map: ghash_ig_map[ghash] = ig
						else:
							count_cut += 1
							ig0 = ghash_ig_map[ghash]
							if ig.weight < ig0.weight:
								ghash_ig_map[ghash] = ig
					igroups = set(ghash_ig_map.values())
				elif 1:
					for ig1 in list(igroups_):
						if ig1.weight >= min_weight:
							igroups_.remove(ig1)
							continue
						for ig2 in igroups_:
							if ig1 is ig2: continue
							if cut_judge(ig1, ig2):
								if debug and de.cut_equal_cover:
									count_cut += 1
									if ig1.equal_span(ig2):
										count_equal_span += 1
								igroups_.remove(ig1)
								break
					igroups = igroups_
				edges_r.remove(e)
				1
				if debug >= 2:
					list_count_state.append(len(igroups))
					list_count_anode.append(len(anodes))
				debug_draw()
			if 0: ### check
				for ig in igroups:
					ig.group.check()
			if "terminate":
				edges = min_ig.edges
				if debug >= 2 and de.cut_equal_cover:
					match cut_mode:
						case 0: cut_mode_str = 'cover'
						case 1: cut_mode_str = 'equal'
						case _: raise
					print(f'cut-mode: {cut_mode_str}')
					if cut_mode == 0:
						print(f'equal/cover: {count_equal_span} / {count_cut}')
					else:
						print(f'equal: {count_equal_span}')
				if debug >= 2:
					print(f'state-count: {mystr(list_count_state)}')
					print(f'\taverage={my.average(list_count_state):.2} max={max(list_count_state)}')
					print(f'anode-count: {mystr(list_count_anode)}')
					print(f'\taverage={my.average(list_count_anode):.2} max={max(list_count_anode)}')
				return HyperGraph.from_edges(edges, pos=self.get_pos, weight=self.weight)
			# pause(len(igroups))
			1
		def cacu_mst2(self, *, debug=0, pos:dict=None, cut_mode=0, 
			no_cycle=1, cond=0, verbose_text=0, verbose_pic=0,  order_mode=None, start=None, fail=Pass, best1=True):
			"""
				要求：
				伪码
					找到下一个点
						将这个点的所有邻边依次加入
							排除循环，包含
				说明
					列出状态包含关系表
					对每个包含关系进行排除
				arg:
					order_mode: 0: default 'x' 'y'
					cut_mode:
						0: 同型
						1: bu
				"""
			# pre
			debug = de.mst and debug
			if len(self.nodes) == 1:
				return self.copy()
			elif len(self.nodes) == 0:
				return self.subgraph_from_nodes_edges(nodes=[], edges=[])
			if pos == None: pos = self.get_pos(nodes=self.nodes)
			weight = self.get_weight_dict()
			nodes = sorted(self.nodes)
			edges = i_e_map = list(self.edges)
			e_i_map = DictOfSet( (e, i) for i,e in enumerate(edges) )
			edges_r = edges.copy() # 不需要deepcopy， 因为edge不会改变
			edges_used = []
			n_edges_map = {n: self.adj_n_e[n].copy() for n in self.nodes} # 未使用边
			igroups = set() # 幻组
			anodes = set() # 导点
			anodes_degree_n_n = my.SortedDict(key_v=lambda v:v) # 按未使用邻居点数排序，仅包含导点， 用于选点
			inodes = set()
			used_nodes = set() # 活跃 + 内点
			unused_nodes = set(nodes)
			new_nodes = set() # tmp
			new_anodes = set()
			min_ig = None
			min_weight = math.inf
			# order
			edge_map = list(self.edges)
			edge_order = list(self.get_edge_order(nodes, edge_map, mode=order_mode, start=start))
			iedge_order = [ e_i_map[e] for e in edge_order ]
			# debug
			count_equal_span = 0
			count_cut = 0
			list_count_state = []
			list_count_anode = []
			possible_msts = []
			b_connect_delta_map = defaultdict(lambda: 0)
			u_connect_delta_map = defaultdict(lambda: 0)
			count_assert_edges_list = []
			if debug and 0:
				mst_len = self.mst_len()
			
			if "model":
				model = object.__new__(Model)
				model.i_e_map = i_e_map
				model.e_i_map = e_i_map
				model.graph = self
				def update_model():
					model.set_field_by_edges(edges_used)
				update_model()
			# anodes_degree_n_e = {} # 用于计算
			def react_new_anode(n):
				anodes.add(n)
				anodes_degree_n_n[n] = self.degree_n_n(n)
				new_anodes.add(n)
				# anodes_degree_n_e[n] = 
			def react_del_anode(n):
				anodes.remove(n)
				del anodes_degree_n_n[n]
			def react_new_node(n):
				new_nodes.add(n)
				used_nodes.add(n)
				unused_nodes.remove(n)
			def draw_edges_r():
				Igroup.cls_draw(edges_r, inodes, anodes, used_nodes, pos)
				HyperGraph._draw_edges([edge_adding], pos=pos, edge_look=dict(color='black', width_rate=2))
				HyperGraph._draw_edges(my.list.removed(edges_used, edge_adding), pos=pos, edge_look=dict(color='black', width_rate=2))
				Graph._draw_nodes(unused_nodes, pos=pos, look=dict(color='grey', alpha=0.2))
				myplt.title(f's={len(igroups)} a={len(anodes)}')
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
					myplt.new_figure()
					
					for ig in list(igroups_):
						if ig.match_graph(d.mst0):
							ig00 = ig
							ig.draw_(inodes, anodes, used_nodes, pos, title=None)
					for ig in list(igroups_)[:7]:
						if ig is ig00: continue
						ig.draw_(inodes, anodes, used_nodes, pos, title=None)
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
			def draw_igroup(ig):
				ig.draw_(inodes, anodes, used_nodes, pos)
				
			# first
			# n0 = newCountMap.popIndex_key(0)
			ig0 = Igroup(weight=0, model=model)
			if len(edge_order) != 0:
				n0 = my.pick(edge_order[0])
				ig0.add_anode(n0)
				react_new_node(n0)
				react_new_anode(n0)
			else:
				min_ig =ig0
			igroups.add(ig0)
			
			# main
			for ei in iedge_order: # e
				edge_adding = edge_map[ei]
				new_inodes = set()
				new_anodes = set()
				new_nodes = set()
				degree_minus = len(edge_adding) - 1
				w = weight[edge_adding]
				edges_used.append(edge_adding)
				# 预处理节点 ( edge_adding =  new_anodes new_inodes non-change ) ( new_nodes = new_anodes + new_inodes部分 )
				# new_anodes: 新增加的anode <=> 新增的点去掉e后还有边
				# new_inodes: <=> 去掉e后一条边都不剩（所有新增inode）
				# new_nodes:  new_anodes + borni
				for n in edge_adding:
					if n not in anodes: # new-nodes
						react_new_node(n)
					n_edges_map[n].remove(edge_adding)
					if len(n_edges_map[n]) == 0: # new-inodes
						new_inodes.add(n)
						if n in anodes: # a -> i
							react_del_anode(n)
						else: # born i
							pass
					else:
						if n not in anodes: # new-anodes
							react_new_anode(n)
						else: # non-change
							pass
						anodes_degree_n_n[n] = len(my.set.unionm(n_edges_map[n])) - 1
						assert anodes_degree_n_n[n] >= 0
				# pre
				1
				inodes |= new_inodes
				igroups_ = set()
				flag_terminate = len(inodes) == len(nodes) # 绝对终止
				flag_terminate2 = len(used_nodes) == len(nodes) # 可能终止
				update_model()
				# 过滤 循环 孤立
				for ig in igroups:
					#
					not_add, add = ig.judge_add_e(edge_adding, new_anodes, new_inodes, flag_terminate2, no_cycle=no_cycle)
					if not_add:
						if add:
							ig1 = ig
							ig2 = ig.copy()
						else:
							ig1 = ig
					else:
						if add:
							ig2 = ig
						else: pass
					#
					if not_add:
						ig1.add_anodes(new_anodes)
						igroups_.add(ig1.not_add_e(new_inodes))
					if add:
						ig2.add_anodes(new_anodes) # 此时ig中包含除了borni的所有点
						ig2.add_e(edge_adding, ei, w, new_inodes)
						if flag_terminate2 and ig2.is_terminated(): # terminated
							if min_ig == None:
								min_ig = ig2
								min_weight = ig2.weight
							else:
								if ig2.weight < min_weight:
									min_ig = ig2
									min_weight = ig2.weight
							continue
						else:
							igroups_.add(ig2)
				edges_r.remove(edge_adding)
				if empty(igroups_) and min_ig == None: # fail
					if fail == Pass:
						raise Exception(f'invalid hg for mst')
						
					return fail
				# debug()
				if len(edges_used) == 4:
					...
				#同型 过滤
				if cut_mode == 1:
					# Lu
					"""
						考虑每一对I1 < I2 
						L: { F1 - F2 } 的变化值 ( 越大的组F值越小)

						ugraph: (越小越好)
							anodes之间的分部完全瓶颈图
						"""
					hg_remain = HyperGraph.from_edges_weight(edges_r, self.weight, pos=pos)
					ngraph = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_ru = hg_remain.seperate_Ru_getter_depth(depth=0)
					ugraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in ugraph.std_edges():
						ugraph.set_edge_weight(e1, get_ru(set(e1)))
					
					def get_Lu(g1, g2):
						"""
							g1欠缺的部分连接起来 需要的上限
							二元完全图: 二元瓶颈图(分立部分用inf边连接)
							? 孤立点, 分立部分
							算法: 上限完全图的部分mst
								根据g2的每个组和对应的g1的小组
									将g1的小组连接成大组的上限
								求和

							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							dta = ugraph.group_mst_len(subs, fail=None)
							if dta == None:
								return my.inf
								
							r += dta
						return r
					# Lb
					"""
						bgraph: (越大越好)
							anodes之间的分布完全断开瓶颈图
						"""
					
					ngraph2 = hg_remain.subngraph().update_nodes(anodes) # 有可能有孤立的anode
					get_rb = hg_remain.seperate_Rb_getter_depth(depth=0, get_u=get_ru)
					bgraph = hg_remain.seperate_sub_full_ngraph_from_nodes(anodes , pos=pos)
					for e1 in bgraph.std_edges():
						bgraph.set_edge_weight(e1, get_rb(set(e1)))
					def get_Lb(g1, g2):
						"""
							g2的部分断开到g1, 能得到的下限
							g2的各个组断开的得到的之和
							算法
								m组完全瓶颈图(取max), 取最大和m-2个最小的
								断开记为inf
							"""
						# pre
						r = 0
						for s2 in g2:
							if len(s2) == 1: continue
							subs = SetHash(hash=id)
							for n2 in s2:
								s1 = g1[n2]
								subs.add(s1)
							m = len(subs)
							if m == 1: continue
							group_graph = bgraph.group_graph(subs)
							if not group_graph.is_span():
								return my.inf
							weights = sorted(group_graph.weight.values())
							dta = weights[-1] + sum(weights[:m-2])
								
							r += dta
						return r

					# filter
					"""
						对每个(g1,g2)对
							排除g1 is g2
							仅考虑g1 <= g2时 
						"""
					igroups_order = sorted(igroups_, key=lambda ig: ig.weight)
					# debug
					count_total = len(igroups_order) ** 2
					count_contain = 0
					count_u = count_b = 0
					#
					for ig1 in igroups_order: # ig1 <= ig2
						if ig1 not in igroups_: continue
						if ig1.weight >= min_weight:
							igroups_.remove(ig1)
							continue
						for ig2 in igroups_order:
							if ig2 not in igroups_: continue
							if ig1 is ig2: continue
							if ig2.cover_span(ig1): # cope
								count_contain += 1
								g1 = ig1.group
								g2 = ig2.group
								dw = ig2.weight - ig1.weight
								Lu = get_Lu(g1, g2)
								if dw >= Lu:
									if 1:
										# draw_edges_r()
										# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
										# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
										# ugraph.draw(edge_label=1, title='ugraph')
										# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
										1
										count_u += 1
										u_connect_delta = g2.connect_count() - g1.connect_count()
										u_connect_delta_map[u_connect_delta] += 1
										if verbose_text >= 3:
											1
											# print(f'connect-u {g1} {g2} delta={u_connect_delta}')
									igroups_.remove(ig2)
									continue
								#
								Lb = get_Lb(g1, g2)
								if dw <= Lb:
									if 1:
										# draw_edges_r()
										# debug_draw(6)
										# ig1.draw(inodes, anodes, used_nodes, pos, title='ig')
										# ig2.draw(inodes, anodes, used_nodes, pos, title='ig')
										# ugraph.draw(edge_label=1, title='bgraph')
										# ngraph.draw(pos=pos, edge_label=1, title='ngraph')
										1
										count_b += 1
										b_connect_delta = g2.connect_count() - g1.connect_count()
										b_connect_delta_map[b_connect_delta] += 1
										if verbose_text >= 3:
											1
											# print(f'connect-b {g1} {g2} delta={b_connect_delta}')
									igroups_.remove(ig1)
									break
					if verbose_text >= 3:
						edges_count_map = DictOfSet( (e1, 0) for e1 in edges_used )
						for ig in igroups_:
							for e1 in ig.edges:
								edges_count_map[e1] += 1
						assert0_edges = [ e0 for e0, count in edges_count_map.items() if count == 0 ]
						assert1_edges = [ e0 for e0, count in edges_count_map.items() if count == len(igroups_) ]
						assert_edges = assert0_edges + assert1_edges
						count_assert0_edges = list(edges_count_map.values()).count(0)
						count_assert1_edges = list(edges_count_map.values()).count(len(igroups_))
						count_assert_edges = count_assert0_edges + count_assert1_edges
						count_assert_edges_list.append(count_assert_edges)
						# print
						print(f'assert-edges 0:1:01:walked: {count_assert0_edges} / {count_assert1_edges} / {count_assert_edges} / {len(edges_used)}')
						print(f'valid / contain / total {count_u + count_b} / {count_contain} / {count_total}')
						print(f'states={len(igroups)} u[{count_u}] b[{count_b}]')
						print(f'')
						if 0:
							myplt.cap(1)
							self.draw(hl_edges=my.setLike.difference(edges_used, assert_edges), hl_edges1=assert_edges)
							myplt.show()
					igroups = igroups_
					# assert not empty(igroups_)
				elif cut_mode == 0:
					ghash_ig_map = {}
					for ig in igroups_:
						ghash = hash(ig.group)
						if ghash not in ghash_ig_map: ghash_ig_map[ghash] = ig
						else:
							count_cut += 1
							ig0 = ghash_ig_map[ghash]
							# draw_edges_r()
							# draw_igroup(ig)
							# draw_igroup(ig0)
							if ig.weight < ig0.weight:
								ghash_ig_map[ghash] = ig
					igroups_ = igroups = set(ghash_ig_map.values())
				1
				if verbose_text >= 2:
					list_count_state.append(len(igroups))
					list_count_anode.append(len(anodes))
				if ei == 10 and 0:
					debug_draw()
				if verbose_pic:
					draw_edges_r()
				check_possible()
			if "terminate":
				edges = [i_e_map[i] for i in min_ig.iedges]
				if verbose_text >= 2:
					print(f'assert-edges: {mystr(count_assert_edges_list)}')
					if cut_mode == 1: print(f'u-connect-delta: {my.dict.str_sorted(u_connect_delta_map)}')
					if cut_mode == 1: print(f'b-connect-delta: {my.dict.str_sorted(b_connect_delta_map)}')
					print(f'state-count: {mystr(list_count_state)}')
					print(f'\taverage={my.average(list_count_state):.2} max={max(list_count_state)}')
					print(f'anode-count: {mystr(list_count_anode)}')
					print(f'\taverage={my.average(list_count_anode):.2} max={max(list_count_anode)}')
				return HyperGraph.from_edges(edges, pos=self.get_pos, weight=self.weight)
			# pause(len(igroups))
			1

		cacu_mst = cacu_mst2
		def mst_quick(self):
			"""
				前提: 输入连通, 满足mst条件

				"""
			return self.cacu_mst()
		def mst(self, fail=Pass, **ks):
			if fail is Pass:
				assert self.check_span()
				return self.cacu_mst(**ks)
			else:
				if self.is_span(): return self.cacu_mst(**ks, fail=fail)
				else: return fail
		def mst_test(self, *, solver_args={}, solve_args={}):
			solver = HgMstSolver(self, **solver_args,)
			return solver.solve(**solve_args)
	if "mst-lib":
		def try_get_groupMap_by_edgesNodesAnodes_checkIsolateCycle(self, edges, nodes, anodes):
			"""
				isolate判断
					存在一个连通分量不包含任何anodes. (除了已经完成且总共只有一个连通分量的情况)
						完成 <=> len(anodes) == 0
				"""
			nodeSubs = my.hypergraph.try_nodeSubs_byEdgesNodes_checkCycle(edges, nodes)
			if nodeSubs == False: return False
			# isolate
			anodeGroups, notOcuppiedCount = my.set.groupBySets_returnNotOcuppiedCount(anodes, nodeSubs)
			if len(anodes) == 0:
				if notOcuppiedCount > 1: return False
				else: anodeGroups = []
			else:
				if notOcuppiedCount > 0: return False
				else: pass
			group_map = my.GroupMap(anodeGroups)
			return group_map
		def checkIsolateCycle_byEdgesAnodes0(self, edges, anodes):
			nodeSubs = my.hypergraph.try_nodeSubs_by_edges_no_cycle(edges)
			if nodeSubs == False: return my.false_wrap('cycle')
			# isolate
			anodeGroups, notOcuppiedCount = my.set.groupBySets_isolateOverflow_returnNotOcuppiedCount(anodes, nodeSubs)
			if len(anodes) == 0:
				if notOcuppiedCount > 1: return my.false_wrap('isolated')
				else: pass
			else:
				if notOcuppiedCount > 0: return my.false_wrap('isolated')
				else: pass
			return True
			group_map = my.GroupMap(anodeGroups)
			return group_map

class PosHyperGraph(HyperGraph):
	def get_pos(self, nodes=None) -> dict:
		if nodes == None: nodes = self.nodes
		return {n:n for n in nodes}
	def random(self, *, nodes_count, edges_count, span=None):
		"""
			span: inclusive (a, b)
			"""
		if span == None: span = [2, min( len(nodes_count), max(3, math.floor(math.sqrt(nodes_count)))) ]
		assert isinstance(nodes_count, int) and isinstance(edges_count, int)
		assert 2 ** nodes_count - nodes_count - 1 >= edges_count
		assert span[1] >= span[0]
		# pre
		cap = nodes_count
		#
		nodes = my.random.sample_tuple2(cap, cap, k=nodes_count)
		span_len = span[1] - span[0] + 1
		span_dist = my.random.dist_choice(k=edges_count, var=span_len)
		edges = my.set.unionm( my.random.sample_subset(nodes, size=span0+i, k=span_dist[i]) for i in range(span_len) )
		return HyperGraph(nodes=nodes, edges=edges)
def test(): # PosGraph
	# help(nx.draw_networkx)
	g = PosGraph()
	a = (0, 0)
	b = (1, 1)
	edge_adding = (a, b)
	g.add_edges( [(a, b)] )
	myplt.set_cap(1)
	g.draw(hl=[a, e])
	plt.show()

def test0():
	g = PosGraph()
	nodes = nodes_random(10, cap = 100)
	g.add_nodes(nodes)
	myplt.set_cap(10)
	myplt.new()
	g.draw_nodes(size_rate=1)
	plt.show()

def test0(): # debug-mode
	myplt.cap(6)
	g = Graph()
	g.add_node(0)
	# myplt.new()
	1
	g.show()
	
def test5(): # debug-mode
	myplt.cap(6)
	g = Graph()
	myplt.new()
	g.show()
	
def test0():
	myplt.cap(6)
	g = Graph()
	1
def test0(): # HyperGraph.path
	h = HyperGraph()
	edges = e0, e1, e2 = [
		( 1, 2, 3 ),
		( 3 ,4 ),
		( 2, 5 ),
	]
	h.add_edges(edges)
	#
	path = h.path(1, 5)
	d(path)
def test0(): # HyperGraph.differ
	h1 = HyperGraph()
	edges = e0, e1, e2 = [
		{ 1, 2, 3 },
		{ 3 ,4, 6 },
		{ 2, 5 },
	]
	h1.add_edges(edges)
	#
	h2 = HyperGraph()
	edges = e0, e1, e2 = [
		{ 1, 2, 3 },
		{ 3 ,6 },
		{ 2, 4, 5 },
	]
	h2.add_edges(edges)
	#
	r = h1.fdiffer(h2)
	d(r)
def test(): # hyper mst
	# random
	# h2 = PosHyperGraph.random(10, 10)
	#
	h = HyperGraph.test.h3()
	myplt.cap(12)
	myplt.share_axis_by_nodes(h.get_pos().values())
	solver = h.mst_test(
			solver_args=dict(debug=4, verbose_text=2, verbose_pic=1, filter=0, dynamic_filter=2, restore=1, cacu_v=2),
			dynamic_filter_args=dict(debug=1, verbose_text=2, verbose_pic=1, pick_start=None, state_threshold=100, iter_threshold=10),
			return_solver=1,
			debug=5, cut_mode=0, no_cycle=1, order_mode='delta', cond=0, verbose_text=3, verbose_pic=2, start=None,
			)
	mst = solver.mst
	d(mst.edges)
	mst.show(title=f'{ solver.mst_len()}')
def test0():
	edges = [{0, 2}, {0, 1}]
	d(HyperGraph.get_edge_order(list(range(3)), edges, order_mode='x',))
def test0(): # filter 
	
	wedges, pos = [({2, 4, 6}, 4), ({8, 3, 5}, 8), ({8, 9, 6, 7}, 10), ({0, 1}, 1), ({1, 2}, 1), ({0, 4}, 2), ({3, 4}, 2), ({8, 9}, 2), ({2, 6}, 3), ({3, 5}, 5), ({8, 3}, 5), ({6, 7}, 5)], {0: (1, 5), 1: (1, 6), 2: (2, 6), 3: (3, 3), 4: (3, 5), 5: (5, 0), 6: (5, 6), 7: (7, 9), 8: (8, 3), 9: (9, 4)}
	hg = HyperGraph.from_wedges(wedges, pos=pos)
	c_map = hg.cacu_c()
	d(c_map)
	hg.show()
def test0(): # hg.bottle
	hg = HyperGraph.test.hg_pruned(10, 9)
	# hg = HyperGraph.test.h1()
	# hg = HyperGraph.test.hg_pruned(30, 2)
	# hg = hg.nhgraph()
	# hg.del_nodes_clear((0, 1, 2, 7, 9, 3))
	if 0:
		# Rgraph = hg.full_Rgraph(ran=4)
		Rgraph.draw(edge_label=True)
	if 0:
		hg.test_r()
	if 0:
		hg.test_Ru_tri()
	if 1:
		myplt.cap(6)
		# get = hg.Rb_getter()
		# hg.test_r_del_edges()
		if 1:
			hg.compare_Ru(1)
		else:
			hg.compare_Rb(1)
			hg.test_print_rb(1)
			hg.Rgraph().draw(title='r', edge_label=1)
			hg.Kgraph().draw(title='k', edge_label=1)
			hg.cacu_mst().draw()
	# draw`
	# myplt.cap(2)
	hg.draw(node_label=1, edge_label=True)
	myplt.show()
def test0():
	nodes = list(range(3))
	hg = HyperGraph(nodes=nodes, edges=edges)
def test0(): # g.bottle
	g = Graph.test.pruned_graph(20, 0)
	# draw
	myplt.cap(2)
	d(g.edges)
	g.test_R()
	# g.draw(node_label=1, edge_label=1)
	myplt.show()
def test0():
	nodes = {1, 2, 3}
	edges = [{1, 2}]
	h = HyperGraph(nodes = nodes, edges=edges)
	d(h.is_span())
def test():
	hg = HyperGraph.test.h2()
	edges = list(hg.edges)
	hg.show(edges=[edges[0], edges[1]])
if __name__ == '__main__':
	test()