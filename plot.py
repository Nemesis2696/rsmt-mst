import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import PathCollection
import numpy as np
from base import *
# import nty
# import structure
import PIL
import mplcursors
__all__ = '''
	myplt
'''.split()

'''
plt size 是面积
event
	artist
'''
present_path = 'ground'
point_limit = 1000000
def really_small(i):
	return abs(i) < 0.0001
def almost_int(f):
	return really_small(f % 1)
class default:
	alpha = 0.5
	grid_alpha = 0.4
	spine_alpha = 0.1

	def hover(i, j): return f'{i}, {j}'

	class color:
		dot = 'blue'
class limit:
	"""
		"""
	dot_shown = int(1e5)
	line_shown = int(2e3)
class prompt:
	"""
		"""
	compress = True
def set_hover(hover=default.hover):
	#要在图画完后调用
	if hover == None: return
	crs = mplcursors.cursor(hover=True, highlight=False)
	def reply(sel):
		#d(sel.artist)
		if isinstance(sel.artist, Line2D):
			crs.remove_selection(sel)
			return
		
		
		i, j = sel.target[0], sel.target[1]
		if almost_int(i): i = round(i)
		if almost_int(j): j = round(j)
		
		sel.annotation.set_text(hover(i ,j))
	crs.connect("add", reply)
if "lib":
	# title
	def parse_title(title=None, *, title_a=None, ori_title) -> 'None | string':
		"""
			inst:
				a: append
				i: insert
			"""
		if title == None and title_a == None: return None
		else:
			r = ori_title
			#
			if title != None:
				r = title
			if title_a != None:
				r += title_a
			return r
class MyPlt:
	"""
		rn cn
		cap <= rn * cn
		cap_info: (rn, cn, cap_)
		attr:
			flag_newfig 
			flag_ion
		用法
			cap(12)
			cap() -> int
			share_axis:
				让之后的图全部共享第一个的坐标，直到share_axis(0|False)
				每次建立新的ax时读取上一个的axis
				flag_share_axis 
				shared_axis: 
					None: 没有上一个
					ax: 上一个ax
					axis: 
		struct:
			axis:(xlim, ylim, xticks, yticks)
		"""
	def __init__(self):
		self.ratio = 5/3
		self.last_ytick_info = None
		self.figures = []
		self.flag_ion = False
		# axis
		self.flag_share_axis = False
		self.shared_axis = None
		self.flag_block_share_axis = False
		self._cap_info = None
		self.set_cap(1, 1) # flag_newfig
		plt.rcParams['font.sans-serif']=['Microsoft YaHei']
		plt.plot()
		plt.close()
	class fonts:
		label = matplotlib.font_manager.FontProperties(family='SimHei', size=12)
		legend = label
	if "oper":
		def new(self):
			if self.flag_newfig:
				rn, cn, cap = self._cap_info
				myplt.add_figure(rn=rn, cn=cn, cap=cap)
				self.flag_newfig = False
			elif self.figure().full():
				rn, cn, cap = self._cap_info
				myplt.add_figure(rn=rn, cn=cn, cap=cap)
			else: pass
			ax = self.figure().add_ax()
			# share_axis
			if self.flag_share_axis and not self.flag_block_share_axis:
				if self.shared_axis == None:
					self.shared_axis = ax
				else:
					if isinstance(self.shared_axis, Ax):
						self.shared_axis = self.shared_axis.axis()
					ax.set_axis(self.shared_axis)
			#return plt.subplot(self.rn, self.cn, self.index)
		def new_figure(self, **ks):
			self.flag_newfig = False
			return self.add_figure(**ks)
		def ion(self):
			plt.ion()
			self.flag_ion = True
		def ioff(self):
			plt.ioff()
			self.flag_ioff = False
		def set_cap(self, *gs, cap=None):
			"""
				11 -> 3, 4, 12
				5, 4 -> 5, 4, 20
				5, 4, cap=19 -> 5, 4, 19
				cap=19 -> 5, 4, 19
				"""
			if cap == None:
				if len(gs) == 1:
					n = gs[0]
					r, c = self.get_rows_cols(n)
					cap_info = r, c, r*c
				elif len(gs) == 2:
					r, c = gs
					cap_info = r, c, r*c
				else: raise Exception(f'{0}')
			else:
				assert cap >= 1
				if len(gs) == 0:
					r, c = self.get_rows_cols(cap)
					cap_info = r, c, cap
				elif len(gs) == 2:
					r, c = gs
					assert r * c >= cap, f'{0}'
					cap_info = r, c, cap
				else: raise Exception(f'{0}')
			if cap_info == self._cap_info: pass
			else:
				self._cap_info = cap_info
				self.index = 0
				self.flag_newfig = True
		def show(self):
			plt.show()
			return self
		def close(self):
			plt.close()
			return self
		def save(self, relpath, *, cover=False):
			# cover: False | 'ignore' | True
			path = f'{present_path}\\{relpath}.png'

			if os.path.exists(path): 
				if cover == 'ignore': pass
				elif cover == True:
					plt.savefig(path)
				elif cover == False:
					raise Exception(f'{path} exists')
			else:
				plt.savefig(path)
		# misc
		def show_on_full(self):
			if self.is_full():
				self.show()
		show_when_full = show_on_full
		# ax
		def set_xlim(self, *gs, **ks):
			self.ax().set_xlim(*gs, **ks)
		def set_ylim(self, *gs, **ks):
			self.ax().set_ylim(*gs, **ks)
	if "axis":
		
		def share_axis(self, flag=True):
			assert my.is_general_bool(flag)
			if flag:
				assert self.shared_axis == None
				self.flag_share_axis = True
			else:
				self.flag_share_axis = False
				self.shared_axis = None
			return self
		def share_axis_by_nodes(self, *gs, **ks):
			axis = self.get_axis_by_nodes(*gs, **ks)
			assert self.flag_share_axis == False
			self.flag_share_axis = True
			self.shared_axis = axis
			return self
		def get_axis_by_nodes(self, nodes, *, pad=0.05) -> 'xlim, ylim, None, None':
			"""
				pad: 上下左右各自的百分比（占全部）
				返回正方形
				"""
			assert 0 <= pad < 0.5
			expand_rate = pad / (1 - 2 * pad )
			x1, x2, y1, y2, dx, dy = my.geo.points.analyze_bound(list(nodes))
			dmax = max(dx, dy)
			if dmax == 0: 
				dpad = 1
			else:
				dpad = dmax * expand_rate
			centerx = (x1 + x2) / 2
			centery = (y1 + y2) / 2
			half = (dmax + dpad * 2) / 2
			x1_ = centerx - half
			x2_ = centerx + half
			y1_ = centery - half
			y2_ = centery + half
			axis = (x1_, x2_), (y1_, y2_), None, None
			return axis
		def set_axis_by_nodes(self, nodes, **ks):
			axis = self.get_axis_by_nodes(nodes, **ks)
			self.set_axis(axis)
			return self
		def set_axis(self, *gs, **ks):
			self.ax().set_axis(*gs, **ks)
			return self
		def block_share_axis(self, flag):
			"""
				block_share_axis(1)
				...
				block_share_axis(0)
				"""
			self.flag_block_share_axis = flag
		# judge
		def flag_axis_set(self):
			return self.ax().flag_axis_set
	if "attr":
		def figure(self):
			if len(self.figures) == 0:
				self.new_figure()
			return self.figures[-1]
		def ax(self):
			return self.figures[-1].axs[-1]
			#return plt.subplot(self.rn, self.cn, self.index)
	if "attr oper":
		def title(self, *gs, **ks):
			return self.ax().title(*gs, **ks)
		def window_title(self, *gs, **ks):
			return self.figure().window_title(*gs, **ks)
		def axis(self, *gs): return self.ax().axis(*gs)
		def cap(self, *gs):
			if len(gs) == 0:
				return self._cap_info[2]
			else:
				return self.set_cap(*gs)
		def xlabel(self, label):
			# font = self.fonts.label
			plt.xlabel(label)
			return self
		def ylabel(self, label):
			# font = self.fonts.label
			plt.ylabel(label)
			return self
		def legend(self, *gs, **ks):
			font = self.fonts.legend
			plt.legend(*gs, **ks)
			return self
	if "info":	
		def cap_info(self):
			return self._cap_info
		# judge
		def initialized(self): ##
			return len(self.figures) != 0 and len(self.figures[-1].axs) != 0
		def is_full(self):
			return self.cap() == self.ax().index + 1
	#basic	
	def add_figure(self, *gs, rn=None, cn=None, cap=None, figsize=(13, 8), title=None, window_title='', **ks): # 不会处理flag
		if self.flag_ion: input('myplt [Enter]')
		if rn == None and cn == None and cap == None:
			rn, cn, cap = self.cap_info()
		else:
			if cap == None:
				assert rn != None and cn != None
				cap = rn * cn
			else:
				if rn == None and cn == None:
					rn, cn = self.get_rows_cols(cap)
				else:
					assert rn != None and cn != None
		fig_ = plt.figure(*gs, figsize=figsize, **ks)
		fig = Figure(fig_, rn=rn, cn=cn, cap=cap, title=title, index=len(self.figures), window_title=window_title)
		self.figures.append(fig)
		return fig
	#private
	def get_rows_cols(self, cap):
		
		rn = 1
		cn = 1
		while rn * cn < cap:
			if rn * self.ratio > cn:
				cn += 1
			else: rn += 1
		return rn, cn
	def get_yticks_visible(self):
		return Ax.get_yticks_visible(self.ax())
	if "draw":
		#private
		def draw_base0(self, *, x=None, y=None, alpha=default.alpha, ytickline=None, newplot=True, title=None, color=None, axis=True, ytick=None, hover=default.hover, ylim=(None, None), xscale=None, yscale=None, fit=None, di=None, dire=None,
			_size=False, size=None, _linewidth=False, width=None,
			**ks):
			"""
				ytickline: None | list | 'tick' | 'dot'
				yaxis: None | list | 'auto_dot' | 'share'
					None: 自动
					list: ...
					auto_dot: 根据数据
					share: 上一个

				lim: None | int | 'tick'
				"""
			if x is not None:
				assert len(x) <= point_limit, f'{len(x)}'
				if y is not None:
					assert len(x) == len(y), f'{len(x), len(y)}'

			if newplot: ax = self.new()
			else: ax = self.ax()
			if title != None: plt.title(title)
			if not axis: plt.axis('off')
			for spine in ax.spines.values():
				spine.set_alpha(default.spine_alpha)
			plt.margins(0)
			#ticks
			if yaxis == 'auto_dot': 
				yticks = self.auto_yticks(y)
				ax.set_yaxis(yticks)
			elif yaxis == 'share':
				assert self.last_ytick_info != None
				yticks, floor, ceil = self.last_ytick_info
				ax.set_yaxis(yticks, floor=floor, ceil=ceil)
			elif isinstance(yaxis, list):
				yticks = yaxis
				ax.set_yaxis(yticks)
			else: assert yaxis == None
			#tickline
			if ytickline == None: pass
			else:
				if ytickline == 'tick': 
					ytickline = yticks
				elif ytickline == 'dot':
					ytickline = set(y)
				elif isinstance(ytickline, structure.Seq):
					ceil = math.ceil(max(y))
					ytickline = ytickline.get(ceil)
				assert is_iterable(ytickline), f'{ytickline}'
				assert len(ytickline) < 1000, f'{0}'
				
				linewidth = self.fit_grid_width(len(ytickline))
				for j in ytickline:
					if j in y: color = 'green'
					else: color = 'purple'
					plt.axhline(y=j, xmin=0, xmax=1, color=color, linestyle='-', linewidth=linewidth, alpha=default.grid_alpha)
			#scale
			if xscale != None: plt.xscale(xscale)
			if yscale != None: plt.yscale(yscale)
			#color
			if color == None: colorList = None
			elif callable(color):
				colorList = [Color.norm_plt(color(i,e), default=default.color.dot) for i, e in zip(x, y)]
			elif isinstance(color, list):
				colorList = color
			else: raise Exception(f'{color}')
			#size width
			if _size:
				if size == None:
					if y != None: n = len(y) - y.count(None)
					else: n = len(x)
					if di == None: di = 2
					size = self.fit_dot_size(n, di=di)
				ks.update(s=size)
			if _linewidth:
				if width == None:
					n = len(x)
					width = self.fit_line_width(n, dire=dire)
				ks.update(linewidth=width)
			#
			ks_ = dict(ax=ax, hover=hover, yaxis=yaxis, ylim=ylim)
			ks.update(color=colorList, alpha=alpha)
			return ks, ks_

		def draw_after(self, *, ax, yaxis, ylim, hover):
			if hover != None: set_hover(hover)
			if yaxis != 'share': self.last_ytick_info = ax.get_y_axis_info()
			#lim
			ax.set_ylim(*ylim)
		def prepare_draw(self, *, color=None, new=True, **ks):
			"""
				pc:
					处理new
					color
				"""
			if new: self.new()
			if isinstance(color, my.Color):
				color_ = color.norm_plt()
			ks['color'] = color_
			return ks
		#
		def scatter_test(self, n=10, size=None, **ks):
			x = np.random.randint(n, size=n)
			y = np.random.randint(n, size=n)
			ks, ks_ = self.draw_base(x=x, y=y, **ks)
			plt.scatter(x, y, s=size, **ks)
			self.draw_after(**ks_)
		def plot_test(self, n=10, **ks):
			ks, ks_ = self.draw_base(**ks)
			x = np.random.randint(n, size=n)
			y = np.random.randint(n, size=n)
			plt.plot(x, y, **ks)
			self.draw_after(**ks_)
		def color_rgb(self, rgb, **ks):
			ks, ks_ = self.draw_base(**ks)
			img = PIL.Image.new('RGB', (10, 10), rgb)
			ax = self.ax()
			plt.axis('off')
			ax.imshow(img)
			self.draw_after(**ks_)
		def color(self, color, **ks):
			self.color_rgb(color.rgb)
		def scatter(self, x, y, *, size=None, di=2, compress_ceil=limit.dot_shown, **ks):
			x, y = self.compress_xy(x, y, compress_ceil)
			# ks, ks_ = self.draw_base(x=x, y=y, **ks)
			if size == None: size = self.fit_dot_size(len(y) - y.count(None), di=di)
			ks = self.prepare_draw(**ks)
			# plt.scatter(x, y, **ks)
			plt.scatter(x, y, s=size, **ks)
			# self.draw_after(**ks_)
		def plot(self, x, y, *, linewidth=1, compress_ceil=limit.dot_shown, **ks):
			x, y = self.compress_xy(x, y, compress_ceil)
			# ks, ks_ = self.draw_base(x=x, y=y, **ks)
			ks = self.prepare_draw(**ks)
			# if markersize == None: markersize = self.fit_marker_size(len(y) - y.count(None))
			plt.plot(x, y, linewidth=linewidth, **ks)
			# self.draw_after(**ks_)
		def seq_line(self, x, *, width=None, dire='h', compress_ceil=limit.line_shown, **ks):
			x = self.compress(x, compress_ceil)
			ks, ks_ = self.draw_base(x=x, dire=dire, _linewidth=True, **ks)
			for i in x:
				if dire == 'v': plt.axhline(y=i, xmin=0, xmax=1, linestyle=None, **ks)
				elif dire == 'h': plt.axvline(x=i, ymin=0, ymax=1, linestyle=None, **ks)
				else: raise Exception(f'{0}')
				
			self.draw_after(**ks_)
		def _draw_yline(self, y, start=None, stop=None, *, width=None, linestyle=None):
			if start is None: start = self.ax().xlim()[1]
			if stop is None: stop = self.ax().xlim()[0]
			plt.axhline(y=y, xmin=start, xmax=stop, linestyle=linestyle, linewidth=width)
			return self
		def _draw_xline(self, x, start, stop, *, width=None, linestyle=None):
			plt.axvline(x=x, ymin=0, ymax=1, linestyle=linestyle, linewidth=width)
			return self
		def seq_dot(self, x, *, dire='h', compress_ceil=limit.dot_shown, **ks):
			x = self.compress(x, compress_ceil)
			ks, ks_ = self.draw_base(x=x, **ks, _size=True, di=1)
			y = [0] * len(x)
			for i in x:
				if dire == 'v': plt.scatter(x, y, **ks)
				elif dire == 'h': plt.scatter(x, y, **ks)
				else: raise Exception(f'{0}')
				
			self.draw_after(**ks_)
	#private: auto fit
	def fit_dot_size(self, n, *, di=2): #
		rn, cn, cap = self.cap_info()
		screen = 1 / (rn * cn)
		floor = 0.1
		ceil = 40 * (screen ** 1/2)
		return fit_size(n, space=screen, floor_n=5000, floor=0.2, ceil=1, space_dim=di, unit_dim=2)
	def fit_marker_size(self, n, *, di=2):
		screen = 1 / (self.rn * self.cn)
		floor = 0
		ceil = 40 * (screen ** 1/2)
		return fit_size(n, const=20, ratio=screen, floor=floor, ceil=ceil, space_di=di, size_di=2)
	def fit_line_width(self, n, *, dire):
		if dire == 'v': ratio = 1 / self.cn
		elif dire == 'h': ratio = 1 / self.rn
		else: raise Exception(f'{dire}')
		
		floor = 0
		ceil = 100 * ratio
		return fit_size(n, const=200, ratio=ratio, floor=floor, ceil=ceil, space_di=1, size_di=1)
	def fit_grid_width(self, n, *, di=1):
		ratio = 1 / self.rn
		floor = 0.4
		ceil = 1 * ratio
		return fit_size(n, const=5, ratio=ratio, floor=floor, ceil=ceil, space_di=di, size_di=1)
	def auto_yticks(self, y):
		ticks = norm_ticks(sorted(set(y)), 1/8)
		return ticks
	def compress(self, x, ceil):
		fold = compress_fold(len(x), ceil)
		if fold == None: return x
		if prompt.compress: print(f'compress {len(x)} -> {len(x) // fold} by {fold}   limit[{ceil}]')
		return x[::fold]
	def compress_xy(self, x, y, ceil):
		fold = compress_fold(len(x), ceil)
		if fold == None: return x, y
		else:
			if prompt.compress: print(f'compress {len(x)} -> {len(x) // fold} by {fold}    limit[{ceil}]')
			return x[::fold], y[::fold]
class Figure:
	"""
		"""
	def __init__(self, fig_, *, rn, cn, cap, index, title, window_title):
		self.fig_ = fig_
		self.index = index #从0开始
		self.axs = []
		self.rn = rn
		self.cn = cn
		self.cap_ = cap
		self.title_ = title
		self._window_title = window_title
		self.set_window_title(f'[{index}] {window_title}')
		assert rn > 0 and cn > 0
	def full(self):
		return len(self.axs) == self.cap_
	def add_ax(self):
		index = len(self.axs)
		ax_ = plt.subplot(self.rn, self.cn, index+1)
		self.index += 1
		ax = Ax(ax_, figure=self, r=index//self.rn, c=index%self.rn, index=index)
		self.axs.append(ax)
		return ax
	def window_title(self, title=None):
		if title == None: return self.get_window_title()
		else:
			self.set_window_title(title)
	def set_window_title(self, title):
		self.fig_.canvas.manager.set_window_title(title)
	def get_window_title(self, title):
		self.fig_.canvas.manager.get_window_title(title)
class Ax:
	"""
		axis: (xlim, ylim, xticks, yticks)
		lim
			floor, ceil: None | 'tick'
				tick: 最值
				None：不变（默认）
		tick: None|list
		attr:
			flag_axis_set:
				调用过set_axis
		"""
	def __init__(self, ax_, *, r, c, figure, index):
		self.figure = figure
		self.ax_ = ax_
		self.r = r
		self.c = c
		self.index = index
		self.yticks = None
		self.flag_axis_set = False
	#complex
	def set_yaxis(self, yticks, *, floor='tick', ceil='tick'):
		assert self.yticks is None, f'{self.yticks, yticks}'
		self.yticks = yticks
		if floor == None: floor = min(yticks)
		if ceil == None: ceil = max(yticks)
		self.ax_.set_yticks(yticks)
		self.set_ylim(floor, ceil)
	#tick lim
	def get_yticks_visible(self):
		if self.yticks is None: 
			r = list(self.ax_.get_yticks())
			return r[1: -1]
		else:
			return self.yticks
	def get_y_axis_info(self):
		yticks = self.get_yticks()
		floor, ceil = self.ax_.get_ylim()
		return yticks, floor, ceil
	def set_xlim(self, floor=None, ceil=None):
		floor_, ceil_ = self.get_xlim()
		if floor == 'tick': floor = None
		elif floor == None: floor = floor_
		
		if ceil == 'tick': ceil = None
		elif ceil == None: ceil = ceil_
		self.ax_.set_xlim(floor, ceil)
	def set_ylim(self, floor=None, ceil=None):
		floor_, ceil_ = self.get_ylim()
		if floor == 'tick': floor = None
		elif floor == None: floor = floor_
		
		if ceil == 'tick': ceil = None
		elif ceil == None: ceil = ceil_
		self.ax_.set_ylim(floor, ceil)
	def set_xticks(self, xticks):
		if xticks is None: return
		else:
			self.ax_.set_xticks(xticks)
	def set_yticks(self, yticks):
		if yticks is None: return
		else:
			self.ax_.set_yticks(yticks)
	def xlim(self, *gs):
		if len(gs) == 0:
			return self.get_xlim()
		else:
			self.set_xlim(*gs)
	def ylim(self, *gs):
		if len(gs) == 0:
			return self.get_ylim()
		else:
			self.set_ylim(*gs)
	#axis
	def axis(self, *gs):
		if len(gs) == 0: return self.get_axis()
		elif len(gs) == 1: return self.set_axis(gs[0])
		else: raise Exception(f'{gs}')
	def get_axis(self):
		xlim = self.get_xlim()
		ylim = self.get_ylim()
		xticks = self.get_xticks()
		yticks = self.get_yticks()
		return (xlim, ylim, xticks, yticks)
	def set_axis(self, axis:None):
		self.flag_axis_set = True
		if axis == None: raise
		(xlim, ylim, xticks, yticks) = axis
		self.set_xticks(xticks)
		self.set_yticks(yticks)
		self.set_xlim(*xlim)
		self.set_ylim(*ylim)
	#
	#
	def set_title(self, *gs, **ks):
		s = parse_title(*gs, ori_title=self.get_title(), **ks)
		if s == None: pass
		else:
			self.ax_.set_title(s)
	def title(self, *gs, **ks):
		if len(gs) == 0 and len(ks) == 0: return self.get_title()
		else: return self.set_title(*gs, **ks)
	def get_title(self):
		return self.ax_.title.get_text()
	def __getattr__(self, name):
		return getattr(self.ax_, name)
#init
myplt = MyPlt()

#compress
"""
	ceil: None
	"""
def compress_fold(n, ceil):
	if ceil == None or n <= ceil: return None
	fold = ceildiv(n, ceil)
	assert fold >= 1, f'{0}'
	return fold
	return 
def compress_index(n, ceil):
	if n <= ceil: return list(range(n))
	fold = ceildiv(n, ceil)
	assert fold >= 1, f'{0}'
	return list(range(0, n, fold))
def compress(li, ceil):
	n = len(li)
	if n <= ceil: return li
	fold = ceildiv(n, ceil)
	assert fold >= 1, f'{0}'
	return li[::fold]


#
def norm_ticks(ticks, spread_ratio):
	assert 0 < spread_ratio <= 1
	assert not empty(ticks), f'{0}'
	
	if len(ticks) == 1: return ticks
	l1 = []
	l2 = []
	i = 0
	j = len(ticks) - 1
	e1 = ticks[i]
	e2 = ticks[j]
	le = e2 - e1
	spread = spread_ratio * le
	l1.append(e1)
	l2.append(e2)
	flag_break = False
	while 1:
		while 1:
			i += 1
			if e2 - ticks[i] < spread:
				flag_break = True
				break
			if ticks[i] - e1 >= spread:
				e1 = ticks[i]
				l1.append(e1)
				break
		if flag_break: break
		while 1:
			j -= 1
			if ticks[j] - e1 < spread:
				flag_brreak = True
				break
			if e2 - ticks[j] >= spread:
				e2 = ticks[j]
				l2.append(e2)
				break
		if flag_break: break
	r = l1 + list(reversed(l2))
	return r
def autolabel00000000(rects):
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2.-0.08, 1.03*height, '%s' % int(height), size=10, family="Times new roman")
def table1(i, j):
	if i > j: return ''
	else: return i + j
def seq1(i):
	return nty.factor_count_opt(i)

#import
import structure
def test1():
	
	fig, ax = plt.subplots(1, 1)
	my.data = [[1, 2, 3], [5, 6, 7], [8, 9, 10]]
	column_labels = ["Column 1", "Column 2", "Column 3"]
	ax.axis("tight")
	ax.axis("off")
	ax.table(cellText=my.data, colLabels=column_labels, loc="center")
	plt.show()
def test():
	tab = Table(table1)
	tab.show()
def test():
	seq = Seq(seq1, index=2)
	seq.show(200000, max_=True, bar = True)
def test1():
	x = [1, 2]
	y = [3, 4]
	plt.figure()
	plt.subplot(1, 1, 1)
	plt.scatter(x, y)
	#fig.show()

	plt.figure()
	plt.subplot(1, 1, 1)
	plt.scatter(x, y)

	plt.show()
def test():
	for i in range(3):
		myplt.subplot(7)
		myplt.draw_test()
	plt.show()
def test():
	myplt.set_cap(4)
	myplt.draw_test(5)
	myplt.draw_test(50)
	myplt.draw_test(500)
	myplt.draw_test(5000)
	myplt.show()
	#help(plt.scatter)
def test():
	ticks = [0, 1.1, 2, 3, 4, 4.1, 4.5, 6, 6.1]
	ticks = [0, 2]
	t = norm_ticks(ticks, 1/3)
	print(t)
def test():
	myplt.set_cap(2)
	#myplt.scatter_test(10, ytick='auto_dot', ytickline='dot')
	#myplt.scatter_test(10, ytick='share', ytickline='dot')
	myplt.scatter_test(10)
	ax = myplt.ax()
	#myplt.plot_test()
	#plt.grid(xdata=[0, 1], ydata=[0, 1])
	myplt.show()
if __name__ == '__main__':
	test()

