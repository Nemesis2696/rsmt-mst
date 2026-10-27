import math
import sympy.ntheory as ntheory
import matplotlib.pyplot as plt
import prettytable
import pickle
import keyboard
import os
import random
import time as _time
import numpy as np
import sortedcontainers
from sortedcontainers import SortedSet
from collections import defaultdict
import cProfile
import sys
import builtins
import timeit
import ctypes
import threading
import multiprocessing
base = __this__ = __import__(__name__)
"""
	debug分级
		0: 无
		1：一两行总结
		2：关键步骤总结
		3：
		4：一两张图总结
		5：关键步骤图片
		6：详细图片
	"""
if "env":
	class _env_:
	
		if os.sep == '\\': os = 'Windows'
		else: os = 'Linux'
class setting:
	class str:
		splitLine_len_threshold = 20
		splitLine_rate_threshold = 0.4
	
if "d":
	debug = 1
	class de:
		debug = __debug__ and debug and 1
		class Group:
			check = debug and 1
		fix_random = debug and 1
	d_pause = 0
	# Inspector_idSet = {4}
	# d
	class d_class:
		"""
			d.count() -> count
			d.count(0) -> count, break, return bool
			"""
		e1 = {89, 82, 100, 87}
		e2 ={100, 89 ,114, 108}
		e3 = {2,4}
		def __init__(self):
			self._count = 0
		def __call__(self, *gs, pause=None, **ks):
			for a in gs:
				print(f'>>> d: {mystr(type(a))} = {mystr(a)}')
			for name, a in ks.items():
				print(f'>>> d: {mystr(type(a))} {name} = {mystr(a)}')
			
			if pause == None:
				if d_pause: base.pause()
			else:
				if pause: base.pause()
			return self
			# if len(gs) != 0: return gs[0]
			# elif len(ks.keys()) != 0: return ks[list(ks.keys())[0]]
			# else: return
		def count(self, *indexs) -> int:
			self._count += 1
			print(f'd.count: {self._count}')
			if self._count in indexs:
				breakhere()
			return self._count
		def _expand_one(self, a, name=None):
			attrs = my.object.normal_attributes(a)
			if name:
				print(f'd-expand: {mystr(type(a))} {name} = {mystr(a)}')
			else:
				print(f'd-expand: {mystr(type(a))} = {mystr(a)}')
			for name, val in attrs.items():
				print(f'    {name} = {val}')
		def expand(self, *gs, **ks):
			pairs = [ (None, a) for a in gs ] + list(ks.items())
			for name, a in pairs:
				self._expand_one(a, name=name)
			return self
			# if len(pairs) == 0: return pairs[0][1]
			# else: return gs
	d = d_class()
	def d_compare(a, b):
		print(f'>>> d_compare')
		print(f'a = {a}')
		print(f'b = {b}')
		print(f'a == b: {a == b}')
		print(f'a is b: {a is b}')
	def hello_world():
		print('Hello World')
	def return0(*gs):
		if len(gs) == 0: return
		else: return gs[0]
	def pdir(a, attr=None):
		
		if attr == None:
			print(dir(a))
		else: 
			print(dir(a))
			help(getattr(a, attr))
	def breakhere(cond=True):
		if cond:
			pass
if "lib":
	class _default_arg: pass
		
	#misc
	def pause(text='[Enter]'):
		input(text)
	class Name(): 
		"""
			Name(name)
			self.__attr__: <dict>
				ks name
			attr:
				<dict>__attr__

			"""
		def __init__(self, *gs, **ks):
			self.__dict__.update(ks)
			# __attr__
			assert '__attr__' not in ks
			self.__attr__ = {}
			self.__attr__['ks'] = ks
			# gs
			if len(gs) == 0: pass
			elif len(gs) == 1:
				name = gs[0]
				self.__attr__['name'] = name
		def __str__(self):
			if hasattr(self.__attr__, 'name'):
				return self.__attr__['name']
			else:
				return f'<Name> {mystr(self.__attr__, split="=", brace=None)}'
	def myprint(*gs, end='\n'):
		for a in gs:
			print(mystr(a), end='')
		print(end=end)
	def range_from_slice(s, *, stop=None):
		start = s.start if s.start != None else 0
		stop = s.stop if s.stop != None else stop
		step = s.step if s.step != None else 1
		return range(start, stop, step)
	def fit_size(n, *, space, ceil, floor, space_dim, unit_dim, used_dim=None, floor_n):
		# floor, ceil 以unit为单位
		# const 以unit为单位
		# space 以n元面（体）积为单位
		"""
			const: space = 1时的值

			args:
				space_dim: 总空间维度
				unit_dim: 结果单位维度
				floor_n: floor对应的个数
				used_dim(default=space_dim): 实际使用空间维度
			"""
		if used_dim == None: used_dim = space_dim
		assert 1 <= unit_dim <= used_dim <= space_dim
		assert space > 0
		assert 0 < floor < ceil, (floor, ceil)
		if n == 0: return ceil
		#
		const = floor * ( floor_n ** (unit_dim/used_dim) )
		#
		space_ = space ** (used_dim/space_dim)
		size = space_ / n
		res = size ** (unit_dim/used_dim)
		r = res * const
		#d(r)
		assert r > 0
		if r < floor: return floor
		elif r > ceil: return ceil
		else: return r
	#tostr
	def _need_split_str_units(units:'list<str>'):
		"""
			长度大于2 && >=splitLine_rate_threshold的比率>=splitLine_len_threshold 
			"""
		if len(units) <= 1: return False
		count = sum( [len(unit) >= setting.str.splitLine_len_threshold for unit in units] )
		if count / len(units) >= setting.str.splitLine_rate_threshold: return True
		else: return False
	def _str_items(self):
		...
	def mystr(a, split=_default_arg, brace=_default_arg, mapper=':'):
		"""
			arg
				brace: None
			"""
		if isinstance(a, str): return a
		if isinstance(a, type): return f'<{a.__name__}>'
		# list-like
		if brace is None:
			brace = ['','']
		if isinstance(a, list):
			if brace == _default_arg: brace = '[]'
			units = [mystr(e) for e in a]
			if split is _default_arg and _need_split_str_units(units): split = '\n'
			else: split = ' '
			return brace[0] + split.join(units) + brace[1]
		if isinstance(a, tuple):
			if brace == _default_arg: brace = '()'
			units = [mystr(e) for e in a]
			if split is _default_arg and _need_split_str_units(units): split = '\n'
			else: split = ' '
			return brace[0] + split.join(units) + brace[1]
		if isinstance(a, set):
			if brace == _default_arg: brace = '{}'
			units = [mystr(e) for e in a]
			if split is _default_arg and _need_split_str_units(units): split = '\n'
			else: split = ' '
			return brace[0] + split.join(units) + brace[1]
		if isinstance(a, dict):
			if brace == _default_arg: brace = '{}'
			units = [f'{mystr(k)}{mapper}{mystr(v)}' for k, v in a.items()]
			if split is _default_arg and _need_split_str_units(units): split = '\n'
			else: split = ' '
			return brace[0] + split.join(units) + brace[1]
		if is_iterable(a): return mystr(list(a))
		else: return str(a)

	#judge
	def empty(a):
		if isinstance(a, dict): return len(a.keys()) == 0
		return len(a) == 0
	def is_iterable(a) -> bool:
		return hasattr(a, '__iter__')
	def isnumber(a):
		return isinstance(a, int) or isinstance(a, float)
	#programming
	def list_from_indexs(*gs, default=Name('list_from_indexs_error')) -> list:
		"""
			(2, a, 0, b, 1, c)
			"""
		assert len(gs) % 2 == 0
		le = len(gs) // 2
		r = [ default ] * le
		for i in range(le):
			r[ gs[i * 2] ] = gs[ i * 2 + 1 ]
		return r
	#complex
	def map_range_to_nature(ran):
		"""
			(5, 15, 5)  10->1
			"""
		start, stop, step = norm_range_args(ran)
		if step == 1: return lambda i: i - start
		else:
			return lambda i: ( i - start ) // step
	def file_readlines(file): #除去末尾\n
		return file.read().split('\n')#struct
	#struct

	def ranged_index(seq, a, b): # -> i, j (实索引）
		#范围在右边外或左边外分别返回两个边界索引对
		max_ind = len(seq) - 1
		if a == None: i = 0
		else: 
			i = binary_find_min(seq, lambda e: e >= a)
			if i == None: return max_ind, -1
		if b == None: j = len(seq) - 1
		else: 
			j = binary_find_max(seq, lambda e: e <= b)
			if j == None: return 0, -1
		return i, j
	def ranged_seq_index(seq, a, b): # -> ind_rg, li
		if (a == None or a <= seq[0]) and (b == None or b >= seq[-1]): return (0, len(seq) - 1), seq
		else: 
			ind_rg = i, j = ranged_index(seq, a, b)
			return ind_rg, seq[i:j+1]
	def sliced_list(li, a, b):
		# python 传统索引
		if b != None and b >= len(li): b = None
		if a == 0 and b == None: return li
		elif b == None:
			return li[a:]
		else:
			return li[a:b]
	def sorted_dict(dic):
		r = {}
		keys = sorted(dic.keys())
		for key in keys:
			r[key] = dic[key]
		return r
	def sorted_tuple(tu):
		return tuple(sorted(tu))
	def copy_list2(list2) -> 'list2':
		r = []
		for row in list2:
			r.append(row.copy())
		return r
	list2_copy = copy_list2
	def locate(li, value):
		r = []
		for i in range(len(li)):
			if li[i] == value: r.append(i)
		return r
if "programming":
	def norm_list(arg) -> None:
		#to list
		if isinstance(arg, list): return arg
		else: return [arg]
	def norm_range_args(ran) -> 'start, stop, step':
		if isinstance(ran, int):
			return 0, ran, 1
		elif len(ran) == 1:
			return 0, ran[0], 1
		elif len(ran) == 2:
			return *ran, 1
		elif len(ran) == 3:
			return ran
		else: raise Exception(f'{ran}')
	def len_range(ran):
		start, stop, step = norm_range_args(ran)
		return exactdiv(stop - start, step)
	# des
	class dynamicmethod_caller:
		"""
			attr: func owner
			"""
		def __init__(self, func, owner):
			self.func = func

			self.owner = owner
		def __call__(self, *gs, **ks):
			return self.func(self.owner, *gs, **ks)
	class dynamicmethod:
		def __init__(self, func):
			assert callable(func)
			self.func = func
		def __get__(self, obj, cls):
			if obj == None:
				return dynamicmethod_caller(self.func, cls)
			else:
				return dynamicmethod_caller(self.func, obj)
	# metaclass
	class callable_class(type):
		def __call__(self, *gs, **ks):
			call = self.__dict__['__call__']
			return call(*gs, **ks)
	class operable_class(type):
		def __call__(self, *gs, **ks):
			call = self.__dict__['__call__']
			return call(*gs, **ks)
		def __getitem__(self, *gs, **ks):
			call = self.__dict__['__getitem__']
			return call(*gs, **ks)
if "bisect":
	def binary_find_max(seq, cond, *, value=False):
		i = binary_find_max_(seq, cond)
		if value:
			if i == None: return None
			else: return seq[i]
		else: return i
	def binary_find_max_(seq, cond):
		# 序列的前半部分满足条件
		# 不存在时返回None
		floor, ceil = 0, len(seq) - 1
		if cond(seq[ceil]): return ceil
		elif not cond(seq[floor]): return None

		while 1:
			if ceil - floor == 1: 
				return floor
			mid = (floor + ceil) // 2
			if cond(seq[mid]): floor = mid
			else: ceil = mid
	def binary_find_min(seq, cond, *, value=False):
		i = binary_find_min_(seq, cond)
		if value:
			if i == None: return None
			else: return seq[i]
		else: return i
	def binary_find_min_(seq, cond):
		# 序列的后半部分满足条件
		# 不存在时返回None
		floor, ceil = 0, len(seq) - 1
		if cond(seq[floor]): return 0
		elif not cond(seq[ceil]): return None

		while 1:
			if ceil - floor == 1: return ceil
			mid = (floor + ceil) // 2
			if cond(seq[mid]): ceil = mid
			else: floor = mid
if "sorted containers":
	class SortedList(sortedcontainers.SortedList):
		def __new__(cls, *gs, key=None, rkey=None, **ks):
			if key == None:
				self = super().__new__(cls, *gs, **ks)
			else:
				self = object.__new__(SortedKeyList)
			return self
		def __init__(self, *gs, rkey:'reverse key'=None, **ks):
			super().__init__(*gs, **ks)
			self.rkey = rkey
		def irange(self, a, b, *gs, keyed=(False,False), **ks):
			if keyed[0]: a = self.rkey(a)
			elif keyed[1]: b = self.rkey(b)
			return super().irange(self, a, b, *gs, **ks)
		def range(self, a, b) -> list:
			return list(self.irange(a,b))
	class SortedKeyList(sortedcontainers.SortedKeyList, SortedList):
		def __init__(self, *gs, key, rkey:'reverse key'=None, **ks):
			super().__init__(*gs, key=key, **ks)
			self.rkey = rkey
		def irange(self, a, b, *gs, keyed=(False,False), **ks):
			if keyed[0]: a = self.rkey(a)
			if keyed[1]: b = self.rkey(b)
			return super().irange(a, b, *gs, **ks)
		def range(self, a, b) -> list:
			return list(self.irange(a,b))
	class SortedDict():
		"""
			_keys
			key: func(item)
			说明
				默认按key排序
			"""
		def __init__(self, di={}, *, key_k=None, key_kv=None, key_v=None, rkey=None):
			if key_k != None:
				key = key_k
			elif key_kv != None:
				key = lambda k: key_item( k, self.map[k] )
			elif key_v != None:
				key = lambda k: key_v( self.map[k] )
			else: key = None # key
			self.map = dict(di)
			self._keys = SortedList(di, key=key, rkey=rkey)
			self.key = key
			self.rkey = rkey
		# dict-oper
		def __setitem__(self, k, v):
			if k in self.map:
				self._keys.remove(k)
			self.map[k] = v
			self._keys.add(k)
		def __getitem__(self, k):
			return self.map[k]
		def __delitem__(self, k):
			self._keys.remove( k)
			self.map.pop(k)
		def pop(self, k):
			self._keys.remove( k)
			r = self.map.pop(k)
			return r
		# info
		def __iter__(self):
			return iter(self._items)
		def __len__(self):
			return len(self.map)
		def __contains__(self, k):
			return k in self.map
		def __str__(self):
			return my.dictItems.tostr(self.items())
		__repr__ = __str__
		# dict-attr
		def keys(self):
			return self._keys
		def values(self):
			return [ self.map[v] for k in self._keys ]
		def items(self):
			return [ (k, self.map[k]) for k in self._keys ]
		# index
		def index_item(self, i):
			k = self._keys[i]
			return k, self.map[k]
		def index_key(self, i):
			k = self._keys[i]
			return k
		def index_value(self, i):
			return self._keys[i]
		index = index_value
		def popIndex_item(self, i):
			k = self._keys.pop(i)
			v = self.map.pop(k)
			return k, v
		def popIndex_key(self, i):
			k = self._keys.pop(i)
			v = self.map.pop(k)
			return k
		def popIndex_value(self, i):
			k = self._keys.pop(i)
			v = self.map.pop(k)
			return v
		popIndex = popIndex_value
		def delIndex(self, i):
			k = self._keys.pop(i)
			self.map.pop(k)
			return self
if "symbol":
	class Symbol:
		def __init__(self, name):
			self.name = name
		def __str__(self):
			return self.name
		def __bool__(self):
			raise Exception(f'{self}')
			
	Pass = Symbol('Pass')
class Tab: #{ rlabel: {clabel:} }
	"""
		说明：
			tab: dict<dict>
			tab[rlable][clable] = value
		order: None | list/tuple | 'sort'
		"""
	def str(tab, *, rorder=None, corder=None):
		mat, rlabel, clabel = Tab.parse(tab, rorder=rorder, corder=corder)
		return Mat.str(mat, rlabel=rlabel, clabel=clabel)
	def parse(tab, *, rorder=None, corder=None):
		if len(tab) == 0: return [], None, None
		rlabel = Tab.norm_label(tab.keys(), rorder)
		sample = my.dict.pickValue(tab)
		clabel = Tab.norm_label(sample.keys(), corder)
		mat = []
		for r in rlabel:
			row = []
			for c in clabel:
				row.append(tab[r][c])
			mat.append(row)
		return mat, rlabel, clabel
	def norm_label(label, order):
		if order == None: return list(label)
		elif order == 'sort': return sorted(label)
		elif isinstance(order, (list, tuple)): return list(order)
class Comb: ###
	def combine_ordered_index(n, k):
		return Comb.combine_ordered_index_exclude(n, k, set())
	def combine_ordered_index_exclude(n, k, exclude):
		assert k <= n, f'{0}'
		if k == 1: return [(i,) for i in range(n) if i not in exclude]
		combs = []
		for i in range(n):
			if i in exclude: continue
			combs_ = Comb.combine_ordered_index_exclude(n, k-1, exclude | {i})
			combs += [ (i,) + comb_ for comb_ in combs_ ]
		return combs
	def combine_ordered(array, k):
		n = len(array)
		raise

class Flag:
	"""
		0 1 True False
		"""
	accepted = {0, 1, True, False}
	def __init__(self, value):
		self.set(value)
	def check(self, value):
		assert value in self.accepted, f'{value}'
	def __str__(self):
		return f'<{self.value}>'
	def __bool__(self):
		return self.value
	#public
	def turnTo(self, value):
		assert self.value != value
		self.check(value)
		self.value = bool(value)
	def set(self, value):
		self.check(value)
		self.value = bool(value)
	turnto = turnTo
class enum:
	left, right, down, up = dires = tuple(range(4))
	x, y = dims = tuple(range(2))
	quas = qua0, qua1, qua2, qua3 = tuple(range(4))
	if "dire":
		center = Symbol('center')
		anti_dire = list_from_indexs(left, right, right, left, down, up, up, down)
		opposite_dire = anti_dire
		tostr_dire = list_from_indexs(up, 'up', left, 'left', down, 'down', right, 'right')
		key_dire = list_from_indexs( up, lambda a: a[1], left, lambda a: -a[0], down, lambda a: -a[1], right, lambda a: a[0] )
		keyv_dire = list_from_indexs( up, lambda a: a, left, lambda a: -a, down, lambda a: -a, right, lambda a: a )
		# rkey_dire = [ lambda a: a[1], -lambda a: a[0], lambda a: -a[1], lambda a: a[0] ]
		dires_x = [ left, right]
		dires_y = [ down, up ]
		dire_to_dires = list_from_indexs(left, dires_x, right, dires_x, down, dires_y, up, dires_y)
		dire_to_vertical_dires = list_from_indexs(left, dires_y, right, dires_y, down, dires_x, up, dires_x)
		# dire
		dire = list_from_indexs(
			left, Name('left', name='left', dim=0, key=lambda p: -p[0],
				keyv=lambda v: -v, is_pos=False, 
				),
			right, Name('right', name='right', dim=0, key=lambda p: p[0],
				keyv=lambda v: v, is_pos=True, 
				),
			down, Name('down', name='down', dim=1, key=lambda p: -p[1],
				keyv=lambda v: -v, is_pos=False, 
				),
			up, Name('up', name='up', dim=1, key=lambda p: p[1],
				keyv=lambda v: v, is_pos=True, 
				),
		)
	# dim
	dire_to_dim = list_from_indexs(left, x, right, x, down, y, up, y)
	key_dim = [ lambda a: a[0], lambda a: a[1] ]
	rkey_dim = [ lambda x: (x, 0), lambda y: (0, y) ]
	dim_to_dires = dim_to_dire_pos = [ [ left, right ], [ down, up ] ]
	if "quas":
		qua = [
			Name('qua0', name='qua0', dires=(right, up), ),
			Name('qua1', name='qua1', dires=(up, left), ),
			Name('qua2', name='qua2', dires=(left, down), ),
			Name('qua3', name='qua3', dires=(down, right), ),
		]
if "tostr":
	def str_list(lis, *, brace=None, sep=' '):
		if brace == True: brace = '[]'
		if brace == None: bl, br = '', ''
		else: bl, br = brace
		return bl + sep.join(str(e) for e in lis) + br
	def str_list2(lis2, *, brace1=None, brace2=None, sep1='\n', sep2=' '):
		return str_list([str_list(lis, brace=brace2, sep=sep2) for lis in lis2], brace=brace1, sep=sep1)
	def str_list_count(lis, *, sort=True, brace=None, sep=' ', repeat_symbol='*', show_1=False):
		set_ = set(lis)
		if sort: set_ = sorted(set_)
		lis2 = []
		for e in set_:
			count = lis.count(e)
			if (not show_1) and count == 1:
				lis2.append(str(e))
			else:
				lis2.append(str(e) + repeat_symbol + str(count))
		return str_list(lis2, brace=brace, sep=sep)
if "str operation":
	blank_chars = ('\n', ' ', '\t')
	def isblank_char(c):
		return c in blank_chars
	def isblank_str(string):
		for c in string:
			if not isblank_char(c): return False
		return True
	def list_find_all(lis, ele, * , start=0, stop=None):
		# list_0 count0
		if start == 0:
			if stop == None:
				r = [ i for i, value in emumerate(lis) if value == ele ]
			else:
				r = [ i for i, value in emumerate(lis) if i < stop and value == ele ]
		else:
			if stop == None:
				r = [ i for i, value in enumerate(lis) if start <= i and value == ele ]
			else:
				r = [ i for i, value in emumerate(lis) if start <= i < stop and value == ele ]
		return r
if "structure":
	class DictHash:
		"""
			DictHash(items, hash=)
			说明
				自带hash函数
			attr:
				hash<func>
				val_dict:
				key_dict:
			"""
		# builtin-dict-operations
		def __init__(self, items=[], *, hash=None):
			if isinstance(items, DictHash):
				self.hash = items.hash
				self.val_dict = items.val_dict.copy()
				self.key_dict = items.key_dict.copy()
			else:
				assert hash != None
				self.hash = hash
				self.val_dict = {}
				self.key_dict = {}
				for k, v in items:
					self[k] = v
		def __str__(self):
			return str(my.dictItems.tostr(self.items()))
		def __repr__(self):
			return f'DictHash: {self}'
		def __len__(self):
			return len(self.key_dict)
		def __iter__(self):
			return self.keys()
		def __getitem__(self, key):
			try: r = self.val_dict[ self.hash(key) ]
			except KeyError as exc:
				raise KeyError(key, list(self.keys()))
			return r
		def __setitem__(self, key, val):
			hash = self.hash(key)
			self.val_dict[hash] = val
			self.key_dict[hash] = key
		def __delitem__(self, key):
			hash = self.hash(key)
			del self.key_dict[hash]
			del self.val_dict[hash]
		def __contains__(self, e):
			return self.hash(e) in self.key_dict
		def keys(self):
			return self.key_dict.values()
		def values(self):
			return self.val_dict.values()
		def items(self):
			r = []
			for hash, key in self.key_dict.items():
				val = self.val_dict[hash]
				r.append( (key, val) )
			return r
		def get(self, k, default=None):
			hash = self.hash(k)
			return self.val_dict.get(hash, default)
		def pop(self, k):
			hash = self.hash(k)
			del self.key_dict[hash]
			return self.val_dict.pop(hash)
		def clear(self):
			self.key_dict.clear()
			self.val_dict.clear()
			return self
		def update(self, di):
			for k, v in di.items():
				self[k] = v
			return self
		#misc-oper
		def set_default(self, k, v):
			hash =self.hash(k)
			if hash not in self.key_dict:
				self.key_dict[hash] = k
				self.val_dict[hash] = v
			return self
		def try_del(self, k):
			h = self.hash(k)
			if h in self.key_dict:
				del self.key_dict[h]
				del self.val_dict[h]
			return self
		# misc
		def sub_from_keys(self, ks, *, default=Pass):
			r = self.empty_copy()
			for k in ks:
				if default is not Pass: v = self.get(k, default)
				else: v = self[k]
				r[k] = v
			return r
		sub_by_keys = sub_from_keys
			
		# build
			
		def empty_copy(self):
			"""
				前提: empty(self)
				"""
			if type(self) == DictHash:
				return DictHash(hash=self.hash)
			else:
				cls = type(self)
				return cls()
		def copy(self):
			return DictHash(self)
	class SetHash:
		"""
			SetHash(hash=)
			说明
				自带hash函数
			"""
		# builtin
		def __init__(self, s=set(), *, hash):
			self.hash = hash
			self.hash_set = set() # { hash .. }
			self.val_dict = {} # { hash : set }
			self |= s
		def __str__(self):
			return my.str(list(self), brace='{}')
		def __repr__(self):
			return f'SetHash: {self}'
		def __len__(self):
			return len(self.hash_set)
		def __iter__(self):
			return iter(self.val_dict.values())
		def __contains__(self, e):
			return self.hash(e) in self.hash_set
		def __ior__(self, s):
			for e in s:
				self.add(e)
			return self
		def __iand__(self, s):
			for e in list(self):
				if e not in s:
					self.remove(e)
			return self
		def __isub__(self, s):
			for e in s:
				self.try_remove(e)
			return self

		def add(self, a):
			hash = self.hash(a)
			self.hash_set.add(hash)
			self.val_dict[hash] = a
		def remove(self, a):
			hash = self.hash(a)
			try:
				self.hash_set.remove(hash)
			except KeyError:
				raise KeyError( f'{a} not found, self={self}' )
			del self.val_dict[hash]
		def difference(self, s2) -> list:
			hashs2 = {self.hash(b) for b in s2}
			hashs1 = {self.hash(a) for a in self}
			hashs_differ = hashs1.difference(hashs2)
			return [ self.val_dict[h] for h in hashs_differ ]
		def clear(self):
			self.val_dict.clear()
		def issubset(self, s):
			if len(self) > len(s): return False
			assert isinstance(s, SetHash)
			for h in self.val_dict:
				if h not in s.val_dict:
					return False
			return True
		# misc
		def has(self, a):
			hash = self.hash(a)
			return hash in self.hash_set
		if "build":
			def copy(self):
				r = object.__new__(SetHash)
				r.hash = self.hash
				r.hash_set = self.hash_set.copy()
				r.val_dict = self.val_dict.copy()
				return r
	class FuncDict(dict):
		"""
			不存在的元素通过func获得
			attr
				func
				assert_range<callable>: 范围
			说明：
				in: 返回确实存在的
				不允许setitem
			"""
		def __init__(self, di={}, *, func, assert_range=lambda k:True):
			super().__init__(di)
			self.func = func
			self.assert_range = assert_range
		def __getitem__(self, k):
			if k in self:
				r = super().__getitem__(k)
			else:
				assert self.assert_range(k)
				r = self.func(k)
				super().__setitem__(k, r)
			return r
		def __setitem__(self, k, v):
			raise Exception(f'{k, v}')

	# class Dict_Set_autoRemoveEmpty(dict):
	# 	"""
	# 		{ key : set() }
	# 		当value空时自动移除
	# 		"""
	class SetOfSet(SetHash):
		def __init__(self, *gs, **ks):
			super().__init__(*gs, hash=my.set.hash, **ks)
	class SetOfSetOfSet(SetHash):
		"""
			元素是set的列表或是元组或是其他任意容器
			setitem时会保留原有的容器类型
			顺序无关
			"""
		def __init__(self, *gs, **ks):
			super().__init__(*gs, hash=my.set_of_set.hash, **ks)
	class DictOfSet(DictHash):
		def __init__(self, *gs, **ks):
			super().__init__(*gs, hash=my.set.hash, **ks)
if "tree search":
	class TreeSearcherBase:
		#: overload search_iterator
		def list(self):
			r = []
			for result in self.search_iterator():
				r.append(result)
			return r
		def try_search_one(self, *, fail=None):
			for result in self.search_iterator():
				return result
			else:
				return fail
		def exist(self) -> bool:
			for result in self.search_iterator():
				return True
			else:
				return False
		def count(self): ###
			r = 0
			for result in self.search_iterator():
				r += 1
			return r
			
	class TreeSearcher(TreeSearcherBase):
		"""
			深度搜索树，返回部分节点
			use
				TreeSearcher(build_nodes=, root=)
			args
				build_nodes(node) → iter( (new_node, save) )
			todo:
				在列出一个节点后直接走到节点
			"""
		def __init__(self, *, build_nodes, get_keys, root):
			self.build_nodes = build_nodes
			self.root = root
		
		def search_iterator(self): ###
			build_nodes = self.build_nodes
			# node:=path[-1]
			active_nodes = [ root ] # 等待扩展的节点
			expands = [ get_keys(root) ] # [ [key .... ] ]
			while 1: # 每次迭代保证path不为空
				node = active_nodes.pop()
				for (new_node, save) in build_nodes(node, key): # 建立新节点
					if save: yield save
					if new_node == None: # 不加入新节点
						continue
					else: #加入新节点
						active_nodes.append(new_node)
				if len(active_nodes) == 0: break # 结束

	
	class TreeSearcherWithKey(TreeSearcherBase):
		"""
			深度搜索树，返回部分节点
			use
				TreeSearcher(build_node=, get_keys, root=)
			args
				build_node(node, key) → new_node, keys, save
				get_keys(node) -> keys
			misc
				key反序更快
			"""
		def __init__(self, *, build_node, get_keys, root):
			self.build_node = build_node
			self.root = root
			self.get_keys = get_keys
		
		def search_iterator(self): ###
			build_node = self.build_node
			root = self.root
			get_keys = self.get_keys
			path = [ root ] # 等待扩展的节点
			expands = [ get_keys(root) ] # [ [key .... ] ]
			while True: # 每次迭代保证keys不为空
				keys = expands[-1]
				key = keys.pop() # 取出下一个key
				new_node, save = build_node( path[-1], key) # 建立新节点
				if len(keys) == 0: # path中删除母节点 / 结束, 顺序重要（path[-1])
					path.pop()
					expands.pop()
				if save is not None:
					yield save
				if new_node is not None: # 新节点存在
					new_keys = get_keys(new_node)
					if len(new_keys) == 0: # 新节点是终点，等效于不存在
						if len(path) == 0: break # 若活跃点为空
					else:
						path.append(new_node)
						expands.append(new_keys)
				else: # 新节点不存在
					if len(path) == 0: break # 若活跃点为空


if "pre-my":
	def my_hex(n, bits=None):
		r = hex(n)[2:].upper()
		if bits == None: return r
		else: return '0' * (bits - len(r)) + r
class my:
	"""
		datas: name:data 
			dump成功时更新 或者手动更新
		groups:
			不在任何一组为None
		"""
	#misc
	if "inf":
		class Inf:
			def __init__(self):
				...
			# compare
			def __lt__(self, b):
				return False
			def __gt__(self, b):
				return True
			def __le__(self, b):
				if b is self: return True
				return False
			def __ge__(self, b):
				return True
			def __eq__(self, b):
				return self is b
			# misc
			def __neg__(self):
				return my.minusInf
			# binary-oper
			def __mul__(self, i):
				if isinstance(i, (float, int)):
					if i > 0: return self
					elif i < 0: return my.minusInf
					else: raise Exception(f'inf * 0')
				else: raise Exception(f'{i, type(i)}')
				
			def __rmul__(self, i):
				return self * i

		class MinusInf:
			def __init__(self):
				...
			def __lt__(self, b):
				return True
			def __gt__(self, b):
				return False
			def __le__(self, b):
				return True
			def __ge__(self, b):
				if b is self: return True
				return False
			def __eq__(self, b):
				return self is b
			def __neg__(self):
				return my.inf
		inf = Inf()
		minusInf = MinusInf()
	if "dynamic":
		def iter_dynamic_turn(li, cond):
			for a in list(li):
				if cond(a): yield a
		def iter_dynamic_cycle(li, cond):
			"""
				不自动停止
				"""
			while 1:
				#le = len(li)
				for a in list(li):
					if cond(a):
						yield a
				#if len(li) == 0: break
				#assert len(li) < le, li
		def iter_dynamic_tested(li, tested:set):
			"""
				说明
					产生元素时自动加入tested
					当tested和li相同时停止
					要求
				需要外面清空tested和删除tested的元素，当tested是整个集合时停止
				"""
			while 1:
				#le = len(li)
				for a in list(li):
					tested.add(a)
					yield a
					if len(tested) == len(li):
						assert tested == set(li)
						return
				else: return #empty(li)
		# def iter_dynamic_dead(li, cond):
		# 	"""
		# 		当所有元素都不满足条件时停止
		# 		"""
		# 	count = 0
		# 	le = len(li)
		# 	while 1:
		# 		for a in list(li):
		# 			if cond(a):
		# 				yield a
		# 				count = 0
		# 				le = len(li)
		# 			count += 1
		# 			if count == le:
		# 				return

		def iter_dynamic(li, *, cond='exist', mode):
			"""
				cond: func | 'exist'
				mode: None |turn | cycle | dead
				"""
			if cond == 'exist': cond = lambda a: a in li
			elif callable(cond): pass
			else: raise Exception(f'{cond}')
			#
			if mode == None: return li
			elif mode == 'turn':
				return my.iter_dynamic_turn(li, cond)
			elif mode == 'cycle':
				return my.iter_dynamic_cycle(li, cond)
			else: raise Exception(f'unexpected [{mode}], expecting[None turn cycle]')	
	if "programming":
		class false_wrap:
			"""
				use
					obj = my.false_wrap(*gs, **ks)
					bool(obj) -> False
					obj.gs obj.ks
				"""
			def __init__(self, *gs, **ks):
				self.gs = gs
				self.ks = ks
			def __bool__(self):
				return False
			def __str__(self):
				r = f'{my.tostr.gs_ks(self.gs, self.ks)}'
				return r
		class flag:
			"""
				"""
			# def __new__(cls, value):
			# 	self = object.__new__(Flag_)
			# 	Flag_.__init__(self, value)
			# 	return self
			def turnTo(flag, value):
				assert flag != value, f'{flag, value}'
				return value
			turnto = turnTo
			def mask(flag, value):
				return value, flag		
		class slice:
			"""
				<tuple> 所有符合range()的组合
					None -> all
				"""
			# basic
			def min_stop(b1, b2):
				"""
					None最大
					"""
				if b2 == None: return b1
				if b1 == None: return b2
				return min(b1, b2)
			def len(ran):
				a, b, step = stdran = my.slice.std(ran)
				le = ceildiv( b-a, step)
				return le
			#
			def std(ran, *, length=None) -> 'start, stop!=None, step':
				if isinstance(ran, int):
					start, stop, step = 0, ran, 1
				elif len(ran) == 1:
					start, stop, step = 0, ran[0], 1
				elif len(ran) == 2:
					start, stop, step = *ran, 1
				elif len(ran) == 3:
					start, stop, step = ran
				else: raise Exception(f'{ran}')
				#
				if stop == None: stop = length
				# assert stop != None
				return start, stop, step
			def range(ran, *, length=None):
				std = my.slice.std(ran, length=length)
				return range(*std)
			def inter(ran1, ran2):
				"""
					要求 step1 == step2 > 0
					"""
				a1, b1, c1 = my.slice.std(ran1)
				a2, b2, c2 = my.slice.std(ran2)
				assert c1 == c2 > 0
				a3 = max(a1, a2)
				b3 = my.slice.min_stop(b1, b2)
				assert a3 <= b3
				c3 = c1
				return a3, b3, c3
		class iter:
			def loop(ite):
				"""
					不会改变大小
					"""
				li = list(ite)
				le = len(li)
				if le == 0: return
				while 1:
					assert len(li) == le
					for a in li:
						yield a
			def loop_until_empty(con):
				"""
					每次迭代有可能删除元素
					"""
				while 1:
					if len(con) == 0: return
					e = next(iter(con))
					yield e
	if "misc":
		def timeit(*gs, **ks):
			t = timeit.timeit(*gs, **ks)
			print(t)
		def hex(n, bits=None):
			r = hex(n)[2:].upper()
			if bits == None: return r
			else: return '0' * (bits - len(r)) + r
		def average(ls, *, default=Pass):
			"""
				default: len==0 
					Pass(raise)
				"""
			if not isinstance(ls, list): ls = list(ls)
			if len(ls) == 0:
				if default is Pass: raise Exception(f'empty list')
				else: return default
			else:
				return sum(ls) / len(ls)
		class CompleteSet:
			def __contains__(self, a):
				return True
		completeSet = CompleteSet()
		# judge
		def isnumber(i):
			return isinstance(i, (int, float))
		def is_general_bool(flag):
			return flag in {1, 0, True, False}
		def all_equal(li):
			first = True
			for e in li:
				if first:
					first = False
					sample = e
					continue
				else:
					if sample == e: continue
					else: return False
			return True
	if "struct":
		# judge
		def is_unique(ite, hash=None):
			if hash == None:
				set_ = set()
				for e in ite:
					if e in set_: return False
					set_.add(e)
				return True
			else:
				set_ = set()
				for e in ite:
					h = hash(e)
					if h in set_: return False
					set_.add(h)
				return True
		unique = is_unique
		def is_sorted(ite):
			last = -my.inf
			for a in ite:
				if a < last: return False
				last = a
			return True
		# info
		def pick(ite):
			return next(iter(ite))
		def max_multi(ite, k, *, key=None):
			"""
				最大的k个值 -> SortedList()
				"""
			assert len(ite) >= k >= 0
			if key == None:
				r = SortedList()
				for e in ite:
					if len(r) < k:
						r.add(e)
					elif r[0] < e:
						r.pop(0)
						r.add(e)
					else: pass
				return r
			else: raise Exception(f'{key}')
		def min_multi(ite, k, *, key=None):
			"""
				最大的k个值 -> SortedList()
				"""
			assert len(ite) >= k >= 0
			if key == None:
				r = SortedList()
				for e in ite:
					if len(r) < k:
						r.add(e)
					elif r[-1] > e:
						r.pop()
						r.add(e)
					else: pass
				return r
			else: raise Exception(f'{key}')
		# oper
		def to_unique(li):
			if not isinstance(li, list): li = list(li)
			r = []
			for a in li:
				if a not in r:
					r.append(a)
			return r
	if "symbol":
		Pass = Pass
	class unit:
		class Time:
			def __init__(self, val):
				self._val = val
			unit_val_map = dict(s=1000000000, ms=1000000, us=10000, ns=1)
			# str
			def __str__(self):
				val = self._val
				for unit, val_ in self.unit_val_map.items():
					if val >= val_:
						return self.tostr(unit)
				return self.tostr(unit)
			def tostr(self, unit):
				val_ = self.unit_val_map[unit]
				r = f'{self._val/val_:g}{unit}'
				return r
			
			# val
			def s(self):
				return self._val / 1000000000
			def ns(self):
				return self._val
			#compare
			def __gt__(self, t):
				if isinstance(t, int):
					return self._val > t
				elif isinstance(t, my.unit.Time):
					return self._val > t._val
				else: raise Exception(f'{t}')
				
			def __ge__(self, t):
				if isinstance(t, int):
					return self._val >= t
				elif isinstance(t, my.unit.Time):
					return self._val >= t._val
				else: raise Exception(f'{t}')
			def __lt__(self, t):
				if isinstance(t, int):
					return self._val < t
				elif isinstance(t, my.unit.Time):
					return self._val < t._val
				else: raise Exception(f'{t}')
				
			def __le__(self, t):
				if isinstance(t, int):
					return self._val <= t
				elif isinstance(t, my.unit.Time):
					return self._val <= t._val
				else: raise Exception(f'{t}')
			def __eq__(self, t):
				if isinstance(t, int):
					return self._val == t
				elif isinstance(t, my.unit.Time):
					return self._val == t._val
				else: raise Exception(f'{t}')
				
			# oper
			def __iadd__(self, t):
				if isinstance(t, int):
					self._val += t
				elif isinstance(t, my.unit.Time):
					self._val += t._val
				else: raise Exception(f'{t}')
				
				return self
			def __itruediv__(self, a):
				self._val /= a
				return self
			val = ns
		class time:
			#build
			def s(val):
				return my.unit.Time(val * 1000000000)
			def ns(val):
				return my.unit.Time(val)
	if "color":
		def color_mix_func(a, b): ###
			a_, b_ = 1-a/255, 1-b/255
			m1 = a_ + b_
			m2 = (a_ + b_ - 2) ** 2 / 4
			r = math.floor(m2 * 255)
			if r < 0: return 0
			return r
		class Color():
			"""
				use:
					my.Color('white' | rgb)
					self.tostr_rgb() .tostr_rgb_with_numsym()
					my.Color.from_name(name), .from_rgb(rgb)
				attr:
					stdname: lower
					cname: 中文名
					_rgb_string: "5F0342"
					rgb<tuple>
				"""
			def __new__(self, arg=None):
				if arg is not None: 
					if isinstance(arg, Color): return arg
					elif isinstance(arg, str): return Color.from_name(arg)
					elif isinstance(arg, tuple): return Color.from_rgb(arg)
					else: raise Exception(f'{arg}')
					
				else:
					raise
			#
			def __str__(self):
				if self.stdname != None: return self.stdname
				elif self.cname != None: return self.cname
				else: return f'#{self.rgb_string}'
			def tostr_rgb(self):
				return self._rgb_string
			def tostr_rgb_with_numsym(self):
				return '#' + self._rgb_string
			def rgb_to_string(rgb):
				r, g, b = rgb
				rgb_string = my.hex(r,2) + my.hex(g,2) + my.hex(b,2)
				return rgb_string
			def __add__(self, color):
				return self.mix(color)
			def mix_cut(self, color, *, factor=1, anti=True):
				r1, g1, b1 = self.rgb
				r2, g2, b2 = color.rgb
				if anti:
					r = max(( 255-math.floor( (510-(r1+r2)) * factor ), 0 ))
					g = max(( 255-math.floor( (510-(g1+g2)) * factor ), 0 ))
					b = max(( 255-math.floor( (510-(b1+b2)) * factor ), 0 ))
				else:
					r = min(( math.floor( (r1+r2) * factor ), 255 ))
					g = min(( math.floor( (g1+g2) * factor ), 255 ))
					b = min(( math.floor( (b1+b2) * factor ), 255 ))
				c = Color.from_rgb((r,g,b))
				return c
			def mix(self, color):
				r1, g1, b1 = self.rgb
				r2, g2, b2 = color.rgb
				r = color_mix_func(r1, r2)
				g = color_mix_func(g1, g2)
				b = color_mix_func(b1, b2)
				c = Color.from_rgb((r,g,b))
				return c
			# oper
			def __eq__(self, color):
				if isinstance(color, my.Color): return self is color
				elif color is None: return False
				else:
					return self is my.Color(color)
			# build, get
			def from_name(name):
				name_ = name.lower()
				if name_ in Color.name_color_map: 
					color = Color.name_color_map[name]
				else:
					stdname, rgb, cname = Color.color_name_info_map[name_]
					color = Color.setup_new(rgb, stdname, cname)
				return color
			def from_rgb(rgb):
				if rgb in  Color.rgb_color_map: return rgb_color_map[rgb]
				elif rgb in  Color.color_rgb_info_map:
					name, rgb, cname =  Color.color_rgb_info_map[rgb]
					return Color.setup_new(rgb, name, cname)
				else:
					return Color.setup_new(rgb, None, None)
			def setup_new(rgb, stdname, cname):
				self = object.__new__(Color)
				r, g, b = self.rgb = rgb
				self.stdname = stdname
				self.cname = cname
				self._rgb_string = my_hex(r,2) + my_hex(g,2) + my_hex(b,2)
				if stdname != None: Color.name_color_map[stdname.lower()] = self
				Color.rgb_color_map[rgb] = self
				return self
			#norm
			def norm_plt(clr, *, default=None):
				"""
					得到适合plt的格式
					default：clr==None时使用
					"""
				if clr == None: clr = default
				if isinstance(clr, Color): return clr.tostr_rgb_with_numsym()
				elif isinstance(clr, str): return clr
				else: raise Exception(f'{clr}')
			#
			def show(self):
				plot.myplt.color_rgb(self.rgb)
				plt.title(str(self))
				plt.show()
			if "date":
				color_infos = [
					('LightPink', (255, 182, 193), '浅粉红'),
					('Pink', (255, 192, 203), '粉红'),
					('Crimson', (220, 20, 60), '猩红'),
					('LavenderBlush', (255, 240, 245), '脸红的淡紫色'),
					('PaleVioletRed', (219, 112, 147), '苍白的紫罗兰红色'),
					('HotPink', (255, 105, 180), '热情的粉红'),
					('DeepPink', (255, 20, 147), '深粉色'),
					('MediumVioletRed', (199, 21, 133), '适中的紫罗兰红色'),
					('Orchid', (218, 112, 214), '兰花的紫色'),
					('Thistle', (216, 191, 216), '蓟'),
					('plum', (221, 160, 221), '李子'),
					('Violet', (238, 130, 238), '紫罗兰'),
					('Magenta', (255, 0, 255), '洋红'),
					('Fuchsia', (255, 0, 255), '灯笼海棠(紫红色)'),
					('DarkMagenta', (139, 0, 139), '深洋红色'),
					('Purple', (128, 0, 128), '紫色'),
					('MediumOrchid', (186, 85, 211), '适中的兰花紫'),
					('DarkVoilet', (148, 0, 211), '深紫罗兰色'),
					('DarkOrchid', (153, 50, 204), '深兰花紫'),
					('Indigo', (75, 0, 130), '靛青'),
					('BlueViolet', (138, 43, 226), '深紫罗兰的蓝色'),
					('MediumPurple', (147, 112, 219), '适中的紫色'),
					('MediumSlateBlue', (123, 104, 238), '适中的板岩暗蓝灰色'),
					('SlateBlue', (106, 90, 205), '板岩暗蓝灰色'),
					('DarkSlateBlue', (72, 61, 139), '深岩暗蓝灰色'),
					('Lavender', (230, 230, 250), '熏衣草花的淡紫色'),
					('GhostWhite', (248, 248, 255), '幽灵的白色'),
					('Blue', (0, 0, 255), '纯蓝'),
					('MediumBlue', (0, 0, 205), '适中的蓝色'),
					('MidnightBlue', (25, 25, 112), '午夜的蓝色'),
					('DarkBlue', (0, 0, 139), '深蓝色'),
					('Navy', (0, 0, 128), '海军蓝'),
					('RoyalBlue', (65, 105, 225), '皇家蓝'),
					('CornflowerBlue', (100, 149, 237), '矢车菊的蓝色'),
					('LightSteelBlue', (176, 196, 222), '淡钢蓝'),
					('LightSlateGray', (119, 136, 153), '浅石板灰'),
					('SlateGray', (112, 128, 144), '石板灰'),
					('DoderBlue', (30, 144, 255), '道奇蓝'),
					('AliceBlue', (240, 248, 255), '爱丽丝蓝'),
					('SteelBlue', (70, 130, 180), '钢蓝'),
					('LightSkyBlue', (135, 206, 250), '淡蓝色'),
					('SkyBlue', (135, 206, 235), '天蓝色'),
					('DeepSkyBlue', (0, 191, 255), '深天蓝'),
					('LightBlue', (173, 216, 230), '淡蓝'),
					('PowDerBlue', (176, 224, 230), '火药蓝'),
					('CadetBlue', (95, 158, 160), '军校蓝'),
					('Azure', (240, 255, 255), '蔚蓝色'),
					('LightCyan', (225, 255, 255), '淡青色'),
					('PaleTurquoise', (175, 238, 238), '苍白的绿宝石'),
					('Cyan', (0, 255, 255), '青色'),
					('Aqua', (212, 242, 231), '水绿色'),
					('DarkTurquoise', (0, 206, 209), '深绿宝石'),
					('DarkSlateGray', (47, 79, 79), '深石板灰'),
					('DarkCyan', (0, 139, 139), '深青色'),
					('Teal', (0, 128, 128), '水鸭色'),
					('MediumTurquoise', (72, 209, 204), '适中的绿宝石'),
					('LightSeaGreen', (32, 178, 170), '浅海洋绿'),
					('Turquoise', (64, 224, 208), '绿宝石'),
					('Auqamarin', (127, 255, 170), '绿玉\\碧绿色'),
					('MediumAquamarine', (0, 250, 154), '适中的碧绿色'),
					('MediumSpringGreen', (0, 255, 127), '适中的春天的绿色'),
					('MintCream', (245, 255, 250), '薄荷奶油'),
					('SpringGreen', (60, 179, 113), '春天的绿色'),
					('SeaGreen', (46, 139, 87), '海洋绿'),
					('Honeydew', (240, 255, 240), '蜂蜜'),
					('LightGreen', (144, 238, 144), '淡绿色'),
					('PaleGreen', (152, 251, 152), '苍白的绿色'),
					('DarkSeaGreen', (143, 188, 143), '深海洋绿'),
					('LimeGreen', (50, 205, 50), '酸橙绿'),
					('Lime', (0, 255, 0), '酸橙色'),
					('ForestGreen', (34, 139, 34), '森林绿'),
					('Green', (0, 128, 0), '纯绿'),
					('DarkGreen', (0, 100, 0), '深绿色'),
					('Chartreuse', (127, 255, 0), '查特酒绿'),
					('LawnGreen', (124, 252, 0), '草坪绿'),
					('GreenYellow', (173, 255, 47), '绿黄色'),
					('OliveDrab', (85, 107, 47), '橄榄土褐色'),
					('Beige', (245, 245, 220), '米色(浅褐色)'),
					('LightGoldenrodYellow', (250, 250, 210), '浅秋麒麟黄'),
					('Ivory', (255, 255, 240), '象牙'),
					('LightYellow', (255, 255, 224), '浅黄色'),
					('Yellow', (255, 255, 0), '纯黄'),
					('Olive', (128, 128, 0), '橄榄'),
					('DarkKhaki', (189, 183, 107), '深卡其布'),
					('LemonChiffon', (255, 250, 205), '柠檬薄纱'),
					('PaleGodenrod', (238, 232, 170), '灰秋麒麟'),
					('Khaki', (240, 230, 140), '卡其布'),
					('Gold', (255, 215, 0), '金'),
					('Cornislk', (255, 248, 220), '玉米色'),
					('GoldEnrod', (218, 165, 32), '秋麒麟'),
					('FloralWhite', (255, 250, 240), '花的白色'),
					('OldLace', (253, 245, 230), '老饰带'),
					('Wheat', (245, 222, 179), '小麦色'),
					('Moccasin', (255, 228, 181), '鹿皮鞋'),
					('Orange', (255, 165, 0), '橙色'),
					('PapayaWhip', (255, 239, 213), '番木瓜'),
					('BlanchedAlmond', (255, 235, 205), '漂白的杏仁'),
					('NavajoWhite', (255, 222, 173), '纳瓦霍白'),
					('AntiqueWhite', (250, 235, 215), '古代的白色'),
					('Tan', (210, 180, 140), '晒黑'),
					('BrulyWood', (222, 184, 135), '结实的树'),
					('Bisque', (255, 228, 196), '(浓汤)乳脂,番茄等'),
					('DarkOrange', (255, 140, 0), '深橙色'),
					('Linen', (250, 240, 230), '亚麻布'),
					('Peru', (205, 133, 63), '秘鲁'),
					('PeachPuff', (255, 218, 185), '桃色'),
					('SandyBrown', (244, 164, 96), '沙棕色'),
					('Chocolate', (210, 105, 30), '巧克力'),
					('SaddleBrown', (139, 69, 19), '马鞍棕色'),
					('SeaShell', (255, 245, 238), '海贝壳'),
					('Sienna', (160, 82, 45), '黄土赭色'),
					('LightSalmon', (255, 160, 122), '浅鲜肉(鲑鱼)色'),
					('Coral', (255, 127, 80), '珊瑚'),
					('OrangeRed', (255, 69, 0), '橙红色'),
					('DarkSalmon', (233, 150, 122), '深鲜肉(鲑鱼)色'),
					('Tomato', (255, 99, 71), '番茄'),
					('MistyRose', (255, 228, 225), '薄雾玫瑰'),
					('Salmon', (250, 128, 114), '鲜肉(鲑鱼)色'),
					('Snow', (255, 250, 250), '雪'),
					('LightCoral', (240, 128, 128), '淡珊瑚色'),
					('RosyBrown', (188, 143, 143), '玫瑰棕色'),
					('IndianRed', (205, 92, 92), '印度红'),
					('Red', (255, 0, 0), '纯红'),
					('Brown', (165, 42, 42), '棕色'),
					('FireBrick', (178, 34, 34), '耐火砖'),
					('DarkRed', (139, 0, 0), '深红色'),
					('Maroon', (128, 0, 0), '栗色'),
					('White', (255, 255, 255), '纯白'),
					('WhiteSmoke', (245, 245, 245), '白烟'),
					('Gainsboro', (220, 220, 220), '亮灰色'),
					('LightGrey', (211, 211, 211), '浅灰色'),
					('Silver', (192, 192, 192), '银白色'),
					('DarkGray', (169, 169, 169), '深灰色'),
					('Gray', (128, 128, 128), '灰色'),
					('DimGray', (105, 105, 105), '暗淡的灰色'),
					('Black', (0, 0, 0), '纯黑'),
				]
				color_name_info_map = { name.lower() : (name, rgb, cname) for name, rgb, cname in color_infos }
				color_rgb_info_map = { rgb : (name, rgb, cname) for name, rgb, cname in color_infos }
				name_color_map = {} #lower
				rgb_color_map = {}
		globals()['Color'] = Color
		class color:
			def constract(count, *, background=Color('white')):
				if background == my.Color('white'):
					if count == 3:
						return [ my.color.set1.orange, my.color.set1.blue, my.color.set1.green ]
					else: raise Exception(f'{count}')
					
				else: raise Exception(f'{background}')
			class set1: # sci
				
				red = Color.from_rgb((164, 5, 69))
				orange = Color.from_rgb((244, 111, 68))
				skin = Color.from_rgb((253, 217, 133))
				yellow = Color.from_rgb((233, 245, 161))
				green = Color.from_rgb((127, 203, 164))
				blue = Color.from_rgb((75, 101, 175))
	if "process thread":
		def Process_target(target, queue, args):
			queue.put(target(*args))
		class Process(multiprocessing.Process):
			def __init__(self, target, *gs, args=[], **ks):
				self.queue = queue = multiprocessing.Queue()
				self._killed = False
				return super().__init__(target=my.Process_target, args=(target, queue, args), *gs, **ks)
			def try_get_res(self, *, fail=None):
				if self.is_alive() or self.killed(): 
					return fail
				else:
					return self.queue.get()
			def kill(self):
				self._killed = True
				super().kill()
			# info
			def killed(self):
				return self._killed
		class ThreadKilledSignal(Exception): ...
		class Thread(threading.Thread):
			"""
				attrs
					_func _ret
				"""
			def __init__(self, target, **ks):
				super().__init__(target=target, **ks)
				self._func = target
				self._killed = False
				self._terminated = False
			def kill(self):
				repeat_sec = 1
				while self.is_alive():
					ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident),
															ctypes.py_object(my.ThreadKilledSignal))
					# d('kill')
					self.join(repeat_sec)
					# assert not self.is_alive()
			def run(self):
				try:
					ret = self._func()
					self._terminated = True
					# d('finish')
				except my.ThreadKilledSignal:
					self._killed = True
				except Exception:
					# d('except')
					raise
				else:
					self._ret = ret
				# d('finish running')
				return self
			def ret(self):
				if not hasattr(self, '_ret'):
					d(killed=self.killed())
					d(_terminated=self.terminated())
					raise
				return self._ret
			# info
			def killed(self):
				return self._killed
			def terminated(self):
				return self._terminated
	if "Timer":
		class time:
			
			def time_timeout_main_call(call, args):
				timer = my.Timer().start()
				ret = call(*args)
				timer.stop()
				time = timer.time()
				r = ret, time
				return r
			def time_timeout(call, limit_s, *, args) -> ' ret|None time|False':
				assert my.isnumber(limit_s)
				r = None
				def limit_call():
					nonlocal r
					t.kill()
				limit_timer = threading.Timer( limit_s, limit_call,)
				t = my.Process(target=my.time_timeout_main_call, args=(call, args))
				# t = my.Thread(target=my.time_timeout_main_call, args=(call, args))
				t.start()
				limit_timer.start()
				t.join()
				fail = Name()
				r = t.try_get_res(fail=fail)
				if r is fail: r = None, False
				else: 
					r = r
				return r
			def time_timeout(call, timeout=None) -> ' ret|None time|False':
				assert my.isnumber(timeout) or timeout is None
				r = None
				def main_call():
					timer = my.Timer().start()
					ret = call()
					timer.stop()
					time = timer.time()
					r = ret, time
					return r
				t = my.Thread( main_call)
				t.start()
				if timeout is None:
					t.join()
					r = t.ret()
				else:
					timeout = my.unit.time.s(timeout)
					time = my.unit.Time(0)
					while 1:
						timer = my.Timer().start()
						t.join(timeout.s())
						time_det = timer.stop().time()
						time += time_det
						if t.is_alive():
							assert time_det > 0
							if time >= timeout:
								t.kill()
								r = None, False
								break
							else:
								continue
						else:
							r = t.ret()
							break
				return r
			def time(call, time_floor:'s'=0, timeout=None):
				ret, time = my.time.time_timeout(call ,timeout=timeout)
				if time is False: return ret, time
				#
				repeat = 1
				def func():
					# d(repeat)
					for i in range(repeat):
						call()
				floor = my.unit.time.s(time_floor).val()
				# time == 0
				# while 1:
				# 	if time.val() == 0: 
				# 		repeat *= 10
				# 		ret, time = my.time.time_timeout(func)
				# 	else:
				# 		break
				# time < time_floor
				while 1:
					if time.val() < floor:
						if time.val() <= 20 * 1000000:
							repeat *= 10
						else:
							repeat = math.ceil(repeat * floor / time.val() )
						ret_, time = my.time.time_timeout(func)
						# d((repeat, time))
					else: break
				#
				# d(repeat)
				# d(time=time)
				time /= repeat
				return ret, time
		class Timer: #程序运行时间
			"""
				usage:
					with Timer() as timer:
						...
					timer.time()
				method
					_time.perf_counter[_ns]: 计算sleep
					_time.process_time[_ns]: 不计算sleep (cpu时间）
					_time.time[_ns]: 现实时间
				"""
			def __new__(cls, *, split=False, **ks):
				if split:
					self = object.__new__(my.TimerSplit)
				else:
					self = object.__new__(my.TimerSingle)
				# self.__init__(**ks)
				return self
			def __init__(self, *, method=_time.process_time_ns):
				self.time_start = None
				self.time_stop = None
				self.method = method
			def __exit__(self, excType, exc, tb):
				#返回True则无视异常, 无异常则excType为None
				if excType == None: # 无异常
					self.stop()
					return True
				else: #有异常 
					return False
		class TimerSingle(Timer):
			def __init__(self, *, method=_time.process_time_ns, **ks):
				self.time_start = None
				self.time_stop = None
				self.method = method
			def __enter__(self):
				#进入执行, 返回值赋给as后的名称
				self.start()
				return self
			#public
			def start(self):
				assert self.time_start == None
				self.time_start = self.method()
				return self
			def stop(self):
				self.time_stop = self.method()
				return self
			def time(self):
				time_ns = self.time_stop - self.time_start
				return my.unit.time.ns(time_ns)
			def clear(self):
				self.time_start = None
				self.time_stop = None
		class TimerSplit(Timer):
			"""
				attr
					discard_tail: 计算时间时允许正在运行， 舍弃最后一段
				"""
			def __init__(self, *, method=_time.process_time_ns, discard_tail=False, **ks):
				self.times_start = []
				self.times_stop = []
				self.method = method
				self.discard_tail = discard_tail
			def __enter__(self):
				#进入执行, 返回值赋给as后的名称
				self.start()
				return self
			#public
			def start(self):
				assert len(self.times_start) == len(self.times_stop)
				time_start = self.method()
				self.times_start.append(time_start)
				return self
			def stop(self):
				time_stop = self.method()
				assert len(self.times_start) == len(self.times_stop) + 1
				self.times_stop.append(time_stop)
				return self
			def time(self):
				le = len(self.times_start)
				if len(self.times_start) == len(self.times_stop):
					times = [ self.times_stop[i] - self.times_start[i] for i in range(le) ]
				elif len(self.times_start) == len(self.times_stop) + 1:
					if self.discard_tail:
						times = [ self.times_stop[i] - self.times_start[i] for i in range(le-1) ]
					else: raise Exception(f'{0}')
				else: raise Exception(f'{0}')
				
				time_ns = sum(times)
				return my.unit.time.ns(time_ns)

			def clear(self):
				self.times_start = []
				self.times_stop = []
	class check:
		def is_unique(ite, hash=None):
			if hash == None:
				set_ = set()
				for e in ite:
					if e in set_: 
						print(f'check-unique: fail')
						print(f'repeated: {e}')
						print(f'{ite}')
						return False
					set_.add(e)
				return True
			else:
				set_ = set()
				for e in ite:
					h = hash(e)
					if h in set_:
						print(f'check-unique: fail')
						print(f'repeated: {e}')
						print(f'{ite}')
						return False
					set_.add(h)
				return True
		unique = is_unique
	if "rewrite pyton module":
		class keyboard:
			def wait(*gs, **ks):
				r= keyboard.wait(*gs, **ks)
				return r
		kb = keyboard
		class os:
			def ls(dir=None):
				if dir == None: return os.listdir()
				else: return os.listdir(dir)
			cwd = os.getcwd
			cd = os.chdir
	# misc
	class misc:
		def get_arrow_by_nodes(nodes:list):
			r = [ (nodes[i], nodes[i+1]) for i in range(len(nodes)-1) ]
			return r
	class geo:
		# rotate
		def rotateL(point):
			x, y = point
			return -y, x
		def rotateR(point):
			x, y = point
			return y, -x
		rotate = rotateL
		def rotateL_on_center(point, center):
			x, y = point
			x0, y0 = center
			return -y + y0 + x0, x - x0 + y0
		def rotateR_on_center(point, center):
			x, y = point
			x0, y0 = center
			raise
			# return -y + y0 + x0, x - x0 + y0
		def rotateL_on_center2_int(point, center2):
			x, y = point
			x2, y2 = center2
			return -y + (y2 + x2) // 2, x + (y2 - x2) // 2
		rotate_on_center2_int = rotateL_on_center2_int
		# mirror
		def mirror_on_center2(point, center2):
			x, y = point
			x2, y2 = center2
			return x2 - x, y2 - y
		def mirror(point):
			x, y = point
			return -x, -y
		def mirror_on_xline2_int(point, xline2):
			x, y = point
			return xline2 - x, y
		def mirror_on_yline2_int(point, yline2):
			x, y = point
			return x, yline2 - y
		# center
		def average_center(points):
			"""
				横纵坐标平均值
				"""
			xs, ys = list(zip(*points))
			x = my.average(xs)
			y = my.average(ys)
			return x, y
		class points:
			def skew(nodes, skew):
				dx, dy = skew
				r = { ( x + dx, y + dy ) for x , y in nodes }
				return r
			#rotate
			def rotate_on_center2_int(s, center2):
				cls = my.geo.points
				r = set()
				for n in s:
					r.add( my.geo.rotate_on_center2_int(n, center2) )
				return r
			def rotateL(s):
				cls = my.geo.points
				r = set()
				for x, y in s:
					r.add( (-y, x) )
				return r
			rotate = rotateL
			# mirror
			def mirror_on_center2(s, center2):
				cls = my.geo.points
				r = set()
				for n in s:
					r.add( cls.mirror_on_center2(n, center2) )
				return r
			def mirror(s):
				r = set()
				for x, y in s:
					r.add( (-x, -y) )
				return r
			# misc
			def analyze_bound(points) -> 'x1, x2, y1, y2, dx, dy':
				xs = []
				ys = []
				for x, y in points:
					xs.append(x)
					ys.append(y)
				x1 = min(xs)
				x2 = max(xs)
				dx = x2 - x1
				y1 = min(ys)
				y2 = max(ys)
				dy = y2 - y1
				return x1, x2, y1, y2, dx, dy
		class segs:
			def skew(edges, skew):
				dx, dy = skew
				r = { ((x1+dx,y1+dy),(x2+dx,y2+dy)) for ((x1, y1), (x2, y2)) in edges }
				return r
		nodes = points
		edges = segs
	class collect:
		class python:
			binaryOperation_rawNames = ''' 
				and or
				add sub 
				eq ne gt lt ge le'''.split()
			operation_rawNames = binaryOperation_rawNames + ''' 
				delitem setitem getitem contains '''.split()
			readonly_operation_rawNames = '''
				contains getitem len str iter gt lt ge le eq ne
				'''.split()
			#
			operation_names = { f'__{name}__' for name in operation_rawNames }
			readonly_operation_names = { f'__{name}__' for name in readonly_operation_rawNames }
		globals()['my_collect_python'] = python
		class type(metaclass=operable_class):
			def __getitem__(typ):
				return my.collect.type._type_to_ns_map[typ]
			class dict:
				readonly_method_names = {'get'} | my_collect_python.readonly_operation_names
			class list:
				readonly_method_names = my_collect_python.readonly_operation_names
			class set:
				readonly_method_names = my_collect_python.readonly_operation_names
			class int:
				...
			born_attrs = {'__module__', '__dict__', '__weakref__', '__doc__'}
			
			_type_to_ns_map = {
				builtins.int : int,
				builtins.dict : dict,
				builtins.list : list,
				builtins.set : set,
			}
			
		class char:
			number = set('0123456789')
			blank = set(' \n\t\r ')
			blank_inline = set(' \t')
	class des:
		def dict(cls):
			"""
				class -> dict
				"""
			di = my.type.defined_attributes(cls)
			return di
	class comb(metaclass=callable_class):
		"""
			return <list>
			"""
		
		#
		def igroups(*gs):
			"""
				use:
					igroups(2, 1, 3) -> list
						count(0) == 2
						count(1) == 1
						count(2) == 3
				算法：
					深度树路径枚举算法
					每一次循环从当前位置往下走一步（并记录状态）/往上走一步
				struct
					path<list>
					nexts[layer] -> <list>nexts
					remained<set> -> 剩下的
				"""
			r = []
			size = sum(gs)
			cap = len(gs)
			total_count_map = gs #
			count_map = list(gs) # changable
			path = []
			remained = set(range(cap)) #[ *([i] * count) for i, count in enumerate(total_count_map) ]
			nexts = [ [] for layer in range(size) ]
			# first
			nexts[0] = list(remained) # 当前层选择
			nextd = 0 # 下一步的层数
			flag_back = False
			while 1:
				1
				if flag_back: # 往上
					#
					if nextd == 0: break
					ele = path.pop()
					count_map[ele] += 1
					if count_map[ele] == 1: remained.add(ele)
					nextd -= 1
					if len(nexts[nextd]) == 0:
						flag_back = True
					else:
						flag_back = False
				else: # down
					next = nexts[nextd].pop()
					path.append(next)
					count_map[next] -= 1
					if count_map[next] == 0: remained.remove(next)
					nextd += 1
					if nextd == size: 
						r.append(path.copy())
						flag_back = True
					elif len(remained) == 0:
						flag_back = True
					else:
						flag_back = False
						nexts[nextd] = list(remained)
			return r
		def igroup_to_comb(li, igroup, group_count):
			comb = [ [] for i in range(group_count) ]
			for i in range(len(li)):
				comb[igroup[i]].append(li[i])
			return comb

		#comb
		def comb(li, *gs, typ=list):
			"""
				use
					comb(li, k)
					comb(li, k1, k2, ..):
						要求 sum(k) == len(li)
						返回所有组
				长度k
				"""
			if not isinstance(li, list): li = list(li)
			if len(gs) == 1:
				k = gs[0]
				size = len(li)
				if typ == list:
					if k == 1: r = [ [e] for e in li ]
					elif k == 2:
						r = [ [li[i], li[j]] for i in range(size) for j in range(i+1, size) ]
					else:
						assert len(li) >= k > 0, (li, k)
						if k == len(li): return [li]
						#
						r = []
						ele = li[0]
						sub_list = li[1:]
						r += [ [ele] + sub_comb for sub_comb in my.comb(sub_list, k-1) ] # include 0
						r += my.comb(sub_list, k) # not include 0
				elif typ == set:
					if k == 2:
						r = [ {li[i], li[j]} for i in range(size) for j in range(i+1, size) ]
					else:
						r = [ typ(c) for c in my.comb.comb(li, *gs) ]
				elif typ == tuple:
					if k == 2:
						r = [ (li[i], li[j]) for i in range(size) for j in range(i+1, size) ]
					else:
						r = [ typ(c) for c in my.comb.comb(li, *gs) ]
				else:
					r = [ typ(c) for c in my.comb.comb(li, *gs) ]
			elif len(gs) >= 2:
				assert typ == list
				assert len(li) == sum(gs)
				igroups = my.comb.igroups(*gs) # [0 0 1 0 1 2 3 3] len(li) == 4
				group_count = len(gs)
				r = []
				for igroup in igroups:
					comb = my.comb.igroup_to_comb(li, igroup, group_count)
					r.append(comb)
			else: raise Exception(f'{gs}')
			return r
		__call__ = comb
		def comb_set(*gs, **ks):
			combs = my.comb.comb(*gs, **ks)
			r = [set(c) for c in combs]
			return r
		def comb2_tuple(li) -> 'list<tuple>':
			if not isinstance(li, list): li = list(li)
			size = len(li)
			return [ (li[i], li[j])  for i in range(size) for j in range(i+1, size) ]
		def comb2_set(li) -> 'list<tuple>':
			if not isinstance(li, list): li = list(li)
			size = len(li)
			return [ {li[i], li[j]}  for i in range(size) for j in range(i+1, size) ]
		def comb2(li) -> 'list<list>':
			if not isinstance(li, list): li = list(li)
			size = len(li)
			return [ [li[i], li[j]]  for i in range(size) for j in range(i+1, size) ]
		def comb_range(li, ran):
			"""
				range: comb长度
				"""
			if not isinstance(li, list): li = list(li)
			size = len(li)
			r = []
			for k in my.slice.range(ran, length=len(li)):
				r += my.comb(li, k)
			return r
		def comb_ge2(li):
			return my.comb.comb_range(li, (2, None))
	class tostr:
		def gs_ks(gs, ks):
			li = []
			for a in gs:
				li.append(mystr(a))
			for n, v in ks.items():
				assert isinstance(n, str)
				li.append(f'{mystr(n)}={mystr(v)}')
			return ' '.join(li)
	# python
	"""
		attrs: set<str>
		attributes: dict<name:val>
		normal_attrs: not startswith '__' (不搜索）
		defined_attrs: not born (不搜索）
		borned_attrs: 自带的 (不搜索）
		"""
	class attr:
		def is_internal(name):
			return name.startswith('__') and name.endswith('__')
	class object:
		# judge
		def is_self_attr(obj, name):
			return name in obj.__dict__ or name in {'__class__'}
		def hasattr(obj, name): # 防止自定义__getattr__导致的误判
			try:
				object.__getattribute__(obj, name)
				return True
			except AttributeError:
				return False
		def isinstance_no_attr_dict(obj):
			return isinstance(obj, (int, float))
		# attrs
		def normal_attrs(obj):
			if my.object.isinstance_no_attr_dict(obj):
				return {}
			return { name for name in obj.__dict__ if not name.startswith('__') }
		def normal_attributes(obj):
			if my.object.isinstance_no_attr_dict(obj):
				return {}
			return { name:val for name,val in obj.__dict__.items() if not name.startswith('__') }
		def defined_attrs(obj):
			return set(obj.__dict__)
		def defined_attributes(obj):
			return dict(obj.__dict__)
		#
		def get_attrs_method(obj):
			"""
				判断
					是类的属性
				"""
			if isinstance(obj, dict):
				return dir(dict)
			names = [ na for na in dir(obj) if not my.object.is_self_attr(obj, na) and callable( getattr(obj, na) ) ]
			return names
		attrs_method = get_attrs_method
		def search_attr_source(obj, name):
			if name in {'__class__'}: raise
			if isinstance(obj, type): cls = obj
			else: cls = type(obj)
			for c in cls.__mro__:
				if name in c.__dict__:
					return c
			return None
	class type:
		def normal_attributes(self):
			return { name:val for name,val in self.__dict__.items() if not name.startswith('__') }
		def defined_attrs(self):
			born_attrs = my.collect.type.born_attrs
			return { name for name in obj.__dict__ if name not in born_attrs }
		def defined_attributes(self):
			born_attrs = my.collect.type.born_attrs
			return { name:val for name,val in self.__dict__.items() if name not in born_attrs }
	if "basic-struct":
		# python struct
		class iterable:
			def difference(s1, s2) -> set:
				raise
				r = set(s1)
				for a in s2: 
					r.remove(a)
				return r
		class str(metaclass=callable_class):
			number = '0123456789'
			def group(s, groups):
				li_groups = my.list.group(list(s), groups)
				groups = [''.join(group) for group in li_groups]
				return groups
			def from_lines(lines):
				return '\n'.join(lines) + '\n'
			__call__ = mystr
			#
			def nonblank_lines(s):
				lines = [ line for line in s.split('\n') if my.str.line_is_not_blank(line) ]
				return lines
			# judge
			def line_is_not_blank(line):
				blank_inline =  my.collect.char.blank_inline
				return any( c not in blank_inline for c in line )
		class dict:
			"""
				sort: None | True | 'value' | gt((i1, e1), (i2, e2))
				"""
		
			#
			def pick(dic):
				return next(iter(dic))
			def pickValue(dic):
				return next(iter(dic.values()))
			def pickItem(dic):
				return next(iter(dic.itemss()))
			# oper
			def set_default(di, **ks):
				"""
					usage: set_default(di, name1=val1, .. )
					"""
				for k, v in ks.items():
					if k not in di:
						di[k] = v
				return di
			# dict-oper
			def copy_from(di1, di2):
				"""
					不改变id
					"""
				di1.clear()
				di1.update(di2)
				return di1
			# misc
			def str_sorted(di, *, key=lambda item: item[0]): # sort by key
				items = list(di.items())
				items.sort(key=key)
				r = my.dict_items.str(items)
				return r
			def from_list(lis, *, sort=None):
				"""
					sort: None | 'value' | gt(e1, e2)
					"""
				tuples = list(enumerate(lis))
				if sort == None: pass
				elif sort == 'value': tuples = sorted(tuples, lambda t1, t2: t1[1] > t2[1])
				else: raise Exception(f'{0}')
				return { i:e for i,e in tuples }
			def sub_by_keys(di, keys):
				r = { k : di[k] for k in keys }
				return r
			# info
			def sorted_items_by_key(di):
				keys = sorted(di.keys())
				r = []
				for key in keys:
					r.append((key, di[key]))
				return r
		class set:
			def pick(s):
				return next(iter(s))
			# unit-oper
			def removed(s, e):
				r = s.copy()
				r.remove(e)
				return r
			def remove(s, e):
				s.remove(e)
				return s
			def changed(s, e1, e2):
				r = s.copy()
				r.remove(e1)
				r.add(e2)
				return r
			def change(s, e1, e2):
				s.remove(e1)
				s.add(e2)
				return s
				
			# set-oper
			def iunion_nonlap(s1, s2):
				assert empty(s1 & s2)
				s1 |= s2
			def union_nonlap(s1, s2):
				assert empty(s1 & s2)
				return s1 | s2
			def unionm(sets):
				r = set()
				for s in sets:
					r |= s
				return r
			union_m = unionm
			def unionm_iterable(iters):
				r = set()
				for ite in iters:
					for a in ite:
						r.add(a)
				return r
			#
			def differencem(s, sets):
				s2 = my.set.unionm(sets)
				r = s.difference(s2)
				return r
			# group
			def group_by_sets(s, sets) -> 'list-set':
				"""
					将属于相同set的元素分在一组
					"""
				if not isinstance(sets, list): sets = list(sets)
				map = {} # e: set-index
				for i, se in enumerate(sets):
					for e in se:
						map[e] = i
				#
				r = [ set() for s in sets ]
				for e in s:
					i = map[e]
					r[i].add(e)
				return r
			def groupBySets_isolateOverflow(s, sets):
				"""
					s中多出来的部分会单独成组
					"""
				if not isinstance(sets, list): sets = list(sets)
				map = {} # e: set-index
				for i, se in enumerate(sets):
					for e in se:
						map[e] = i
				#
				r = [ set() for s2 in sets ]
				for e in s:
					i = map.get(e, None)
					if i == None:
						r.append( {e} )
					else:
						r[i].add(e)
				return r
			group_by_sets_isolate_overflow = groupBySets_isolateOverflow
			def groupBySets_isolateOverflow_returnNotOcuppiedCount(s, sets):
				"""
					s中不在任何set中的单独成组
					返回不被使用sets
					"""
				if not isinstance(sets, list): sets = list(sets)
				map = {} # e: set-index
				occupied = set() # set-index
				for i, se in enumerate(sets):
					for e in se:
						map[e] = i
				#
				r = [ set() for s2 in sets ]
				for e in s:
					i = map.get(e, None)
					if i == None:
						r.append( {e} )
					else:
						occupied.add(i)
						r[i].add(e)

				#
				count_not_occuppied = len(sets) - len(occupied)
				return r, count_not_occuppied
			def groupBySets_returnNotOcuppiedCount(s, sets):
				"""
					返回不被使用sets数量
					r包括不被使用的sets(空集)
					"""
				if not isinstance(sets, list): sets = list(sets)
				map = {} # e: set-index
				occupied = set() # set-index
				for i, se in enumerate(sets):
					for e in se:
						map[e] = i
				#
				r = [ set() for s2 in sets ]
				for e in s:
					i = map[e]
					occupied.add(i)
					r[i].add(e)

				#
				count_not_occuppied = len(sets) - len(occupied)
				return r, count_not_occuppied
			# misc
			def hash(s):
				return hash(tuple(sorted(s)))
			def hash_hashe(s, hashe=hash):
				return hash(tuple(sorted( hashe(e) for e in s )))
				# return hash(tuple(sorted(s)))
			def relation(s1, s2) -> 'equal hyper sub inter seperate':
				"""
					相等空集 -> equal
					"""
				l1 = len(s1)
				l2 = len(s2)
				if l1 == l2:
					if s1 == s2:
						return 'equal'
					else:
						for e1 in s1:
							if e1 in s2:
								return 'inter'
						else:
							return 'seperate'
				elif l1 > l2:
					if l2 == 0: return 'hyper'
					ite2 = iter(s2)
					first2 = next(ite2)
					if first2 in s1:
						for e2 in ite2:
							if e2 not in s1: return 'inter'
						else: return 'hyper'
					else:
						for e2 in ite2:
							if e2 in s1: return 'inter'
						else: return 'seperate'
				else:
					if l1 == 0: return 'sub'
					ite1 = iter(s1)
					first1 = next(ite1)
					if first1 in s2:
						for e1 in ite1:
							if e1 not in s2: return 'inter'
						else: return 'sub'
					else:
						for e1 in ite1:
							if e1 in s2: return 'inter'
						else: return 'seperate'
			# judge
			def one_contain_another(s1, s2):
				if len(s1) > len(s2):
					return s2.issubset(s1)
				else:
					return s1.issubset(s2)
		class list:
			def find_max(li, *, value=False) -> 'index (,value)':
				index = max( range(len(li)), key=lambda i: li[i] )
				if value: return index, li[index]
				else: return index
			def find_min(li, *, value=False) -> 'index (,value)':
				index = min( range(len(li)), key=lambda i: li[i] )
				if value: return index, li[index]
				else: return index
			def is_unique(li):
				return my.is_unique(li)
			# union inter
				# def unionm(lists): ###
				# 	r = []
				# 	for li in lists:
				# 		for a in li:
				# 			if a not in r:
				# 				r.append(a)
				# 	return r
				# union_m = unionm
				# def iunion(l1, l2):
				# 	# 要求两者原本就unique
				# 	for b in l2:
				# 		if b not in l1:
				# 			l1.append(b)
				# 	return l1
				# def union(l1, l2):
				# 	r = list(l1)
				# 	my.list.iunion(r, l2)
				# 	return r
			"""
				union, inter: 堆算法
				"""
			# misc
			def compare_lt(l1, l2):
				"""
					前提: 元素可比较
					按li前面的大小比较
					不够长的补最小的
					"""	
				if len(l1) >= len(l2):
					for i in range(len(l2)):
						e1 = l1[i]
						e2 = l2[i]
						if e1 == e2: continue
						else: return e1 < e2
					else:
						return False
				else:
					for i in range(len(l2)):
						e1 = l1[i]
						e2 = l2[i]
						if e1 == e2: continue
						else: return e1 < e2
					else:
						return True
			def compare_gt(l1, l2):
				"""
					前提: 元素可比较
					按li前面的大小比较
					不够长的补最小的
					"""	
				return my.list.compare_lt(l2, l1)
			# unit-oper
			def removed(li, e):
				r = li.copy()
				r.remove(e)
				return r
			#group
			def group_by_len(li, le):
				li = list(li)
				assert len(li) % le == 0
				count = len(li) // le
				r = [ li[i:i+le] for i in range(0, count*le, le) ]
				return r
			def group(li, arg):
				if isinstance(arg, int):
					return my.list.group_by_len(li, arg)
				elif is_iterable(arg):
					groups = arg
					assert len(groups) > 0
					r = []
					i_ = Pass
					for a in li:
						i = my.groups.find_priority(groups, a, priority=i_)
						if i != i_:
							g = [a]
							r.append(g)
							i_ = i
						else:
							g.append(a)
					return r
				else: raise Exception(f'{arg}')
			def split_by_index(li, indexs): # 去除空
				flag_sub_created = 0
				r = []
				for i, ele in enumerate(li):
					if i in indexs: 
						if flag_sub_created:
							flag_sub_created = 0
						else: pass
					else:
						if flag_sub_created:
							sub.append(ele)
						else:
							sub = [ele]
							r.append(sub)
							flag_sub_created = 1
					# if flag_sub_created:
					# 	#flag_sub_created = 0
				return r
			def group_by_brace(li, brace, *, inclusive=True):
				"""
					只看最外层
					"""
				if isinstance(inclusive, tuple): raise
				elif inclusive:
					inclusive1 = inclusive2 = True
				else:
					inclusive1 = inclusive2 = False
					
				b1, b2 = brace
				r = []
				
				b1_indexs = [ i for i, a in enumerate(li) if a == b1 ]
				b2_indexs = [ i for i, a in enumerate(li) if a == b2 ]
				assert len(b1_indexs) == len(b2_indexs)

				i1_ = i2_ = -math.inf

				for i1, i2 in zip(b1_indexs, b2_indexs):
					assert i2 > i1, li
					assert i1 > i2_, li
					i1_ = i1
					i2_ = i2
					#
					i2 += 1
					if not inclusive1: i1 = i1 + 1
					if not inclusive2: i2 = i2 - 1
					r.append( li[i1:i2] )
				return r
		class tuple:
			
			def group_by_len(li, le):
				groups = my.list.group_by_len(li, le)
				return [ tuple(g) for g in groups ]
		# non-std struct
		class set_like:
			"""
				list
				前提：无重复
				"""
			def difference(s1, s2):

				r = []
				s2 = list(s2)
				for a in s1:
					if a not in s2:
						r.append(a)
				return r
			def inter(s1, s2):
				r = []
				for a in s1:
					if a in s2:
						r.append(a)
				return r
			def issubset(s1, s2):
				if len(s1) > len(s2): return False
				for e1 in s1:
					if e1 not in s2:
						return False
				return True
		unhashableSet = set_like
		setLike = set_like
		# struct-misc
		class list2:
			def sorted_by_len(lis2):
				return sorted(lis2, key=lambda l: len(l))
		class dictItems:
			def tostr(items, *, mapper=':', brace='{}', split=' '):
				if brace == None: brace = '{}'
				return brace[0] + split.join(f'{mystr(k)}{mapper}{mystr(v)}' for k,v in items) + brace[1]
			str = tostr
		dict_items = dictItems
		class bisect:
			find_max = binary_find_max
			find_min = binary_find_min
		# complex struct
		class dict_set:
			def remove_clear_empty(di, key, ele):
				s = di[key]
				s.remove(ele)
				if len(s) == 0:
					del di[key]
				return di
		class set_set:
			def hash(ss):
				return my.set.hash_hashe(ss, hashe=my.set.hash)
		set_of_set = set_set
		class list_of_set:
			def is_unique(li):
				raise
	# real-struct
	class hypergraph:
			
		def irrelavant_subs(subs) -> '[ edges ]':
			"""
				返回一组互不相连的部分
				返回的是原有的object
				"""
			#
			subs = list(subs)
			if empty(subs): return []
			nodes_walked = set()
			#
			def cope_sub(sub):
				nonlocal nodes_walked
				nodes_sub = set()
				for e in sub:
					for n in e:
						if n in nodes_walked: 
							return False
						nodes_sub.add(n)
				nodes_walked |= nodes_sub
				r.append(sub)
				return True
			#
			r = []
			for sub in subs: ## sub
				cope_sub(sub)
			return r

		def try_nodeSubs_byEdgesNodes_checkCycle(edges, nodes): ###
			"""
				循环 -> False
				
				"""
			id_sub_map = {}
			n_sub_map = {}
			for e in edges:
				ite = iter(e)
				for n in ite:
					if n in n_sub_map:
						sub = n_sub_map[n]
						
						for m in ite:
							if m in n_sub_map: # 有另外的交点
								subm = n_sub_map[m]
								if subm is sub: return False #与同一个组有两个交点
								else: # 交于不同组,合并组
									sub |= subm
									for m1 in subm:
										n_sub_map[m1] = sub
									id_sub_map.pop(id(subm))
							else: continue
						else:
							sub |= e
							for k in e:
								n_sub_map[k] = sub
							break
				else:
					sub = set(e)
					id_sub_map[id(sub)] = sub
					for k in e:
						n_sub_map[k] = sub
			subs = list(id_sub_map.values())
			for n in nodes:
				if n not in n_sub_map:
					subs.append({n})
			return subs
		def checkIsolateCycle_byEdgesAnodes(edges, anodes):
			from graph import HyperGraph
			hg = HyperGraph.from_edges(edges)
			return hg.checkIsolateCycle_byEdgesAnodes(edges, anodes)
	class mat: ##
		"""
			ralbel: None | ( [label ..], ) | [label, ..]
			根据最外围类型判定
			"""
		#lib ##
		def norm_index(index):
			if isinstance(index, int):
				return list(range(index))
			else: return list(index)
		def norm_label(label):
			# -> [ [label] ]
			# label str | list<list> | list<label> | None
			if label == None: ls = []
			elif isinstance(label, str): ls = [ label.split() ]
			elif isinstance(label, list):
				ls = (label,)
			elif isinstance(label[0], tuple): 
				ls = label
			else: raise Exception(f'{label}')
			return ls
		def get_mat_with_label(mat, *, rlabel=None, clabel=None, filler=''):
			rls = Mat.norm_label(rlabel)
			cls = Mat.norm_label(clabel)
			rn, cn = Mat.get_size(mat, check=True)
			cbias, rbias = len(rls), len(cls)
			mat_ = []
			for r in range(rbias):
				row = [filler] * cbias + cls[r]
				mat_.append(row)
			for r in range(rn):
				row = [ rl[r] for rl in rls] + mat[r]
				mat_.append(row)
			return mat_
		#interface ##
		def from_str(s):
			lines = s.strip().split('\n')
			r = [ [ int(e) for e in line.split() ] for line in lines ]
			return r
		def str(mat, *, rlabel=None, clabel=None):
			mat_ = Mat.get_mat_with_label(mat, rlabel=rlabel, clabel=clabel, filler='')
			return Mat.str_raw(mat_)
		def from_func(func, rindex, cindex=None):
			"""
				index: int | list
				"""
			rindex = Mat.norm_index(rindex)
			if cindex == None: cindex = rindex
			mat = [ [func(r,c) for c in cindex] for r in rindex]
			return mat
		# 
		def str_raw(mat, *, style=None, check=True):
			"""
				前后额外加了'\n'
				"""
			rn, cn = my.mat.size(mat, check=check)
			pt = prettytable.PrettyTable(chr(i) for i in range(cn))
			for r in mat:
				pt.add_row(r, divider=True)
			lines = str(pt).strip().split('\n')
			string = '\n' + '\n'.join(lines[2:]) + '\n'
			return string
		def copy(mat):
			return [ row.copy() for row in mat ]
		def size(mat, check=False):
			if check:
				if empty(mat): return 0, 0
				rn = len(mat)
				cn = len(mat[0])
				assert cn >= 1, f'{mat}'
				for r in mat:
					assert len(r) == cn, f'{mat}'
				return rn, cn
			else:
				if empty(mat): return 0, 0
				rn = len(mat)
				cn = len(mat[0])
				return rn, cn
	class squmat:
		def size(mat, check=False):
			if check: 
				rn, cn = my.mat.size(mat, check=check)
				assert rn == cn, f'{mat}'
				return rn
			else: 
				return len(mat)
		def is_symmetry(mat, *, check=True):
			size = my.squmat.get_size(mat, check=check)
			for i in range(1, size):
				for j in range(i):
					if mat[i][j] != mat[j][i]: return False
			return True
		# build
		def build_fill(n, filler):
			return [ [ filler ] * n for i in range(n) ]
		# show
		def tostr(mat):
			r = my.mat.str_raw(mat)
			return r
		str = tostr
	#Structure
	SortedDict = SortedDict
	class GroupMap():
		"""
			不相交的集合组，可以快速通过元素查找所在集合
			没有空集（自动删除）
			attr
				map
				_sets: SetHash(hash=id)
			usage
				self[e] = {} <=> self.add(e)
			"""
		def __init__(self, sets=None):
			self.map = {}
			self._sets = SetHash(hash=id)
			if sets != None: 
				self.add_sets(sets)
			if 0: self.map = my.Inspector(self.map, 'map', print_self=1, before=1, after=1, breakhere=1, inspect=None, inspect_index=2)
		# info
		def __len__(self):
			return len(self._sets)
		def __contains__(self, e):
			return e in self.map
		def __iter__(self):
			return iter(self.sets())
		def __str__(self):
			return mystr(self.sets())
		def __hash__(self):
			return my.set_of_set.hash(self._sets) #不能直接用hash（_sets）,因为是id判断的
		hash = __hash__
		__repr__ = __str__
		def sets(self):
			return self._sets
		def elements(self):
			return my.set.unionm(self._sets)
		# oper
		def __getitem__(self, e):
			return self.map[e]
		def __delitem__(self, e):
			s = self.map.pop(e)
			s.remove(e)
			if len(s) == 0:
				self._sets.remove(s)
		def __setitem__(self, e, s):
			# s原生 / empty
			if len(s) == 0:
				self._sets.add(s)
			else:
				s in self._sets
			if e in self.map:
				s0 = self.map[e]
				s0.remove(e)
				if len(s0) == 0: self._sets.remove(s0)

				self.map[e] = s
			else:
				self.map[e] = s
			s.add(e)
		def add(self, e, s=None):
			"""
				要求s是原生group中的
				"""
			if s == None:
				self.map[e] = {e}
			else:
				self.map[e] = s
				s.add(e)
		def add_set(self, s):
			"""
				默认s是有主的
				"""
			s = set(s)
			for n in s:
				assert n not in self.map
				self.map[n] = s
			self._sets.add(s)
			return self
		def add_sets(self, sets):
			for s in sets:
				assert len(s) != 0
				self.add_set(s)
			return self
		# oper-complex
		def connectm(self, es):
			s0 = set()
			ids_eaten = set()
			for e in es:
				s1 = self.map[e]
				id_ = id(s1)
				if id_ in ids_eaten: continue
				ids_eaten.add(id_)
				self._sets.remove(s1)
				s0 |= s1
			for n in s0:
				self.map[n] = s0
			self._sets.add(s0)
			return self
		def connectm_allownew(self, s):
			"""
				s是外来集合，可能有新元素
				将s所有元素所在集合合并
				"""

			s0 = set()
			s = set(s)
			ids_eaten = set()
			for n in s:
				if n not in self.map: 
					s0.add(n)
				else:
					s1 = self.map[n]
					id_ = id(s1)
					if id_ in ids_eaten: continue
					ids_eaten.add(id_)
					self._sets.remove(s1)
					s0 |= s1
			for n in s0:
				self.map[n] = s0
			self._sets.add(s0)
			return self
		# build
		def copy(self):
			return my.Group.from_sets(self.sets())
		def from_sets(sets):
			self = my.Group()
			self.add_sets(sets)
			return self
		# judge
		def check(self):
			if not de.Group.check: return
			for n, s in self.map.items():
				assert n in s
			for s in self.sets():
				assert len(s) != 0
				assert all(self.map[n] is s for n in s)
		def __eq__(g1, g2):
			if not isinstance(g2, my.GroupMap): return False
			if len(g1) != len(g2): return False
			for s1 in g1.sets():
				e1 = my.set.pick(s1)
				s2 = g2[e1]
				if s1 != s2: return False
			return True
		def covering(self, g2):
			"""
				任意g2中的集合是g1中某个集合的子集
				要求元素相同
				"""
			for s2 in g2:
				n2 = my.set.pick(s2)
				s1 = self.map[n2]
				if s2.issubset(s1): continue
				else: return False
			return True
		# mist
		def connect_count(self):
			"""
				视作图, 图中生成森林的边数
				"""
			return sum( len(s) - 1 for s in self )
	Group = GroupMap
	# debug
	class d:
		def differ_set(s1, s2, **ks):
			diff1 = s1.difference(s2)
			diff2 = s2.difference(s1)
			print(f'>> my.d.differ_set')
			print(f's1: {my.str(s1, **ks)}')
			print(f's2: {my.str(s2, **ks)}')
			print(f's1 - s2: {my.str(diff1, **ks)}')
			print(f's2 - s1: {my.str(diff2, **ks)}')
	class DebugSetting:
		"""
			attr
				_mask:
					None: 无
					bool:
			use
				_print = my.DebugSetting( print, **default ).base(debug)()
				_print().mask(0)
				_print().unmask()
			"""
		def __init__(self, di , **ks):
			assert set(di).issubset( set(ks))
			self.setting = ks | di
			self._mask = None
			self.skin = my.DebugSettingSkin(self)
		
		def getattr(self, name):
			if self._mask is None:
				return self.setting[name]
			else:
				return self._mask
		def __bool__(self):
			raise
		# public
		def __call__(self):
			return self.skin
		def base(self, flag):
			if not flag:
				for n, v in self.setting.items():
					self.setting[n] = 0
			# elif flag == True: pass
			# else: raise Exception(f'{flag}')
			return self
			
		def mask(self, flag):
			assert self._mask is None
			self._mask = flag
			return self
		def unmask(self):
			assert self._mask in {0, 1}
			self._mask = None
			return self
	class DebugSettingSkin:
		"""
			"""
		def __init__(self, proxy):
			self._proxy_ = proxy
		def __call__(self):
			return self._proxy_
		def __getattr__(self, name):
			return self._proxy_.getattr(name)
		def __bool__(self):
			raise
	class Exception(Exception):
		pass			
	#
	class random:
		"""
			choice: 重复
			sample：不重复
			seed和hash有关
			"""
		_seed = None
		def get_seed():
			return my.random._seed
		def seed(seed=Pass):
			if seed is Pass: return my.random._seed
			else:
				my.random._seed = seed
				random.seed(seed)
		# list
		"""
			choice|pick: 选择一个
			sample: 无重复元素
			"""
		def pick_range(*gs, k):
			r = random.choice(range(*gs), k=k)
			return r
		def sample_range(*ran, k):
			"""
				seed: ( len(ran), k, seed )
				"""
			seed = my.random.seed()
			le = my.slice.len(ran)
			seed_ = hash( (le, k, seed) ) ###
			my.random.seed(seed_)
			# my.random.seed_tuple(
			r = random.sample(range(*ran), k=k)
			my.random.seed(seed)
			return r
		def sample_tuple2(range1, range2, *, k):
			"""
				std1, std2: 0 - len-1
				int = std1 * len2 + std2
				range: int/tuple : slice
				"""
			
			len1 = len_range(range1)
			len2 = len_range(range2)
			count = len1 * len2 # 0 - (count-1)
			ints = my.random.sample_range(count, k=k)
			# a_std * b_std
			tuples_std = [ ( i % len2, i // len2 ) for i in ints ]
			map1 = map_range_to_nature(range1)
			map2 = map_range_to_nature(range2)
			tuples = [ (map1(i1), map2(i2)) for i1,i2 in tuples_std ]
			return tuples
		def sample_subset(s, *, size, k):
			li = list(s)
			indexs = my.random.sample_subsets_range(5, size=size, k=k)
			return [ { li[i] for i in index } for index in indexs ]
			# subsets = my.math.subsets(range(len(s)))
		# unit
		def pick(li):
			if not isinstance(li, list): li = list(li)
			return random.choice(li)
		choice = pick
		# float
		def float(a, b):
			assert b >= a
			r = random.uniform(a, b)
			return r
		rand_float = float
		# dist
		def dist_heap(*, k, var):
			"""
				var: 取值数
				k：总数
				return [ .. ] len=var sum=k
				"""
			s = my.random.choice_range(var, k=k)
			r = [ s.count(i) for i in range(var) ]
			return r
	class file:
		# judge
		def exists(path):
			return os.path.exists(path)
		# oper
		def write(path, string, *, file=False):
			with ExitBlock():
				if file == False: file_ = open(path, 'w')
				else: file_ = path
				file_.write(string)	
		def writelines(path, lines, *, file=False):
			string = '\n'.join(lines) + '\n'
			return my.file.write(path, string, file=file)
		def readlines(path, *, file=False):
			if file == False: file_ = open(path, 'r')
			else: file_ = path
			return file_.read().split('\n')
	class data:
		note_data_path = 'data\\_note'
		note_path = '_note.txt'
		note_dict = None #str:str
		datas = {}
		#judge
		def exists(name):
			path = f'data\\{name}'
			return os.path.exists(path)
		#note
		def clear_note():
			with open(note_data_path, 'wb') as data_file:
				pickle.dump({}, data_file)
		def read_note():
			if my.data.note_dict == None:
				my.data.note_dict = {}
				with open(my.data.note_path, 'r') as file:
					lines = file_readlines(file)
					for line in lines:
						if isblank_str(line): continue
						name, note = line.split(' ', maxsplit=1)
						my.data.note_dict[name] = note
			return my.data.note_dict
		def write_note():
			txt = ''
			for name, note in sorted(my.data.note_dict.items()):
				txt += f'{name} {note}\n'
			with ExitBlock():
				with open(my.data.note_path, 'w') as file:
					file.write(txt)
		def set_note(name, note):
			assert isinstance(name, str), f'{name}'
			my.data.read_note()
			note_str = str(note)
			assert all(blk not in note_str for blk in '\n\t'), f'{note}'
			my.data.note_dict[name] = note_str
			my.data.write_note()
		def del_note(name):
			read_note()
			del note_dict[name]
			write_note()
		#oper
		def dump(name, obj, *, note=None):
			path = os.path.join('data', name)
			with ExitBlock():
				with open(path, 'wb') as file:
					pickle.dump(obj, file)
			my.data.datas[name] = obj
			if note != None:
				my.data.set_note(name, note)
		def load(name, default=None):
			path = f'data\\{name}'
			if name in my.data.datas:
				return my.data.datas[name]
			if not my.data.exists(name):
				if default != None: return default
				else: raise Exception(f'{name} dont exist')
				
			with open(path, 'rb') as file:
				return pickle.load(file)			
	class Data:
		def __init__(self, name, default):
			self.name = name
			match _env_.os:
				case 'Linux': self.path = f'../data{os.sep}{self.name}'
				case 'Windows': self.path = f'data\\{self.name}'
				case _: raise Exception(f"not match {_env_.os}")
			self.default = default
			#my.data.datas[self.name] = default
			#self.loaded = False
			self.data = None
		#note
		def set_note(self, *gs, **ks):  return my.data.set_note(self.name, *gs, **ks)
		def del_note(self, *gs, **ks):  return my.data.del_note(self.name, *gs, **ks)
		#judge
		def exists(self): # file exists
			return os.path.exists(self.path)
		#oper
		def load(self):
			self.signal_begin_load()
			path = f'data\\{self.name}'
			if self.data is not None:
				r = self.data
			elif self.exists():
				with open(path, 'rb') as file:
					r = pickle.load(file)
				self.data = r
			else:
				r = self.default
				self.data = r
			return r
		__call__ = load	
		def dump(self, obj, *, note=None):
			with ExitBlock():
				with open(self.path, 'wb') as file:
					pickle.dump(obj, file)
			self.data = obj
			if note != None:
				self.set_note(note)
		def clear(self):
			self.dump(self.default)
		def save(self):
			self.dump(self.data)
		#signal
		def signal_begin_load(self):
			...
	class format(metaclass=callable_class):
		def science_move(value, format, move):
			"""
				science_move(9, '.1', -1) -> 9.0e-1
				"""
			assert isinstance(move, int), f'{move}'
			assert isinstance(format, str), f'{format}'
			assert isnumber(value), f'{type(value)} {value}'
			raw = f'{{:{format}e}}'.format(value)
			base_, power1_ = raw.split('e')
			power2 = int(power1_) + move
			return f'{base_}e{power2:+}'
		def fill(value, length, *, align, fill=' ', expr=None):
			string = str(value)
			count = length - len(string)
			assert isinstance(fill, str) and len(fill) == 1, f'{fill}'
			
			if count < 0:
				if expr == None: return string
				else: return expr
			else:
				if align == enum.left:
					r = string + fill * count
				elif align == enum.right:
					r = fill * count + string
				elif align == enum.center:
					a = count // 2
					b = count - a
					r = fill * a + string + fill * b
				else: raise Exception(f'unexpected [{align}], expecting[{enum.left} {enum.right} {enum.center}')
				return r
		def __call__(value, format, **ks):
			"""
				< ^ >: fill
				^: 偏左
				"""
			subs = my.str.group(format, [my.str.number])
			groups = my.list.group(subs, 2)
			assert len(groups) == 1, f'{groups}'
			for inst, operand in groups:
				if inst == '<':
					operand = int(operand)
					r = my.format.fill(value, operand, align=enum.left, **ks)
				elif inst == '>':
					operand = int(operand)
					r = my.format.fill(value, operand, align=enum.right, **ks)
				elif inst == '^':
					operand = int(operand)
					r = my.format.fill(value, operand, align=enum.center)
				else: raise
			return r
		align = fill
		def div_allow0(a, b, *, inf='oo', NaN='NaN', format=None):
			"""
				format: 给数字用的
				"""
			if b == 0:
				if a == 0:
					return NaN
				else:
					return inf
			else: 
				val = a / b
				if format == None: return str(val)
				else: return f'{{:{format}}}'.format(val)
	class groups:
		#private
		def find_priority(groups, a, *, priority=Pass):
			# priority: index | Pass
			if priority in (Pass, None):
				for i in range(len(groups)):
					if a in groups[i]: return i
				return None
				
			else:
				if a in groups[priority]: return priority
				for i in range(len(groups)):
					if i == priority: continue
					if a in groups[i]: return i
				return None
			# raise Exception(f'{a, groups}')
	class Table(builtins.list):
		"""
			说明：
				list<list>
				自动检查数量对齐
			attr
				split: 横向分割符
				clabels
				row_size
				align
			"""
		def __init__(self, *, clabels=None, split='  ', align=enum.right):
			super().__init__()
			self.split = split
			if clabels != None: 
				if isinstance(clabels, str):
					self.clabels = clabels.split()
				else:
					self.clabels = list(map(str, clabels))
				self.row_size = len(self.clabels)
			else: 
				self.row_size = None
				self.clabels = clabels
			self.align = enum.right
		def __str__(self):
			lines = self.lines()
			string = my.str.from_lines(lines)
			return string
		def tostr_item(self, ri, ci, val):
			r = str(val)
			return r
		def lines(self):
			has_header = self.clabels != None
			rcount = len(self)
			ccount = self.row_size
			str_matrix1 = [ [ self.tostr_item( ri, ci, self[ri][ci] ) for ci in range(ccount) ] for ri in range(rcount) ]
			if has_header: header_matrix1 = [ label for label in self.clabels ]
			# caps
			caps = []
			for ci in range(ccount):
				cap = max( len(row[ci]) for row in str_matrix1 )
				if has_header: cap = max( cap, len(header_matrix1[ci]) )
				caps.append(cap)
			# str_matrix2: align
			str_matrix2 = []
			for ri in range(rcount):
				str_row2 = []
				for ci in range(ccount):
					str1 = str_matrix1[ri][ci]
					str2 = my.format.align(str1, length=caps[ci], align=self.align)
					str_row2.append(str2)
				str_matrix2.append(str_row2)
			if has_header: 
				header_matrix2 = [ my.format.align(label, length=caps[ci], align=self.align) for ci, label in enumerate(header_matrix1) ]
			# lines
			lines = []
			if has_header:
				line = self.split.join( header_matrix2 )
				lines.append(line)
			for ri in range(rcount):
				line = self.split.join( str_matrix2[ri] )
				lines.append(line)
			#
			return lines
		#public
		def append(self, row_):
			row = list(row_)
			if self.row_size == None:
				le = len(row)
				assert le > 0
				self.row_size = le
			else: assert len(row) == self.row_size
			list.append(self, row)
			return self
		def print(self):
			print(self)
	class numeric:
		def in_range(n, n1, n2, *, inclusive=True):
			if inclusive == True:
				return my.math.in_range_inclusive11(n, n1, n2)
			elif inclusive == False:
				return my.math.in_range_inclusive00(n, n1, n2)
			else: raise Exception(f'{inclusive}')
		def in_range_inclusive11(n, n1, n2):
			return n1 <= n <= n2 or n2 <= n <= n1
		def in_range_inclusive00(n, n1, n2):
			return n1 < n < n2 or n2 < n < n1
	class math:
		def multiply(li):
			r = 1
			for i in li:
				r *= i
			return r
		mulm = multiply
		def comb(n, k):
			mul = my.math.multiply
			if isinstance(k, int):
				assert n >= k
				m = min(k, n-k)
				r = mul(range(n-m+1, n+1)) // mul(range(1, m+1))
			else: raise Exception(f'{k}')
			return r
		def ln(a):
			assert a > 0
			return math.log(a)
		class const:
			Euler = euler = 0.57721566490153286060651209
	if "structure":
		def SetOfSet(*gs, **ks):
			return SetHash(*gs, hash=my.set.hash, **ks)
		def DictOfSet(*gs, **ks):
			return DictHash(*gs, hash=my.set.hash, **ks)
	if "dummy":
		class Dummy:
			def __init__(self, *gs, **ks):
				pass
			def __getattr__(self, name):
				return self
			def __call__(self, *gs, **ks):
				pass
		dummy = Dummy()
if "inspector":
	class InsName(Name):
		"""
			owner
			"""
			
		def before_call(self, name_, text='', *, name=None):
			if not self.before: return
			if not self.should_inspect(name_): return
			self.print('%<', name_, text, name=None)
		def after_call(self, name_, text='', *, name=None):
			if not self.after: return
			if not self.should_inspect(name_): return
			self.print('%>', name_, text, name=None)
		def print(self, header, name_, text, *, name=None):
			# id
			id_ = Inspector.id_counter
			Inspector.id_counter += 1
			if id_ not in Inspector.idSet: return
			#
			if name == None: name = name_
			print(f'{header}{id_}  {self.name}.{name}  {text}')
			if self.print_self:
				print(f'   {self.tostr(self.obj)}')
			if self.breakhere:
				breakhere()
			if self.pause:
				pause()		
		def should_inspect(self, name):
			return name in self.inspectList
		def tostr(self, obj):
			return f'{obj}'
	class Inspector:
		"""
			用法
				Inspector(inspected) -> self
				__init__( inspect:callList )
				.set_tostr(lambda obj: ...) # print_self
			arg
				inspect list:callable / str[.split] / None 
					Any默认为可能的修改操作
					其他默认为空
				breakhere:
				conditional:
					None: 若有inspect为真
					True | False
				print_self:
				inspect_index:
				inspect_id: <list|int>
				tostr: print-self
			attr:
				inspectList
				_ins_
			info
				name_index_map <dict>
				inspect_id <set|completeSet>
			"""
		name_index_map = defaultdict(lambda:0)
		id_counter = 0
		idSet = my.completeSet
		nameMap = {}
		def __new__(cls, obj, name, *gs, inspect_index=None, inspect_id=None, **ks):
			# Inspector
			if isinstance(obj, my.Inspector): return obj
			# index
			if inspect_index != None:
				if isinstance(inspect_index, int):
					indexSet = {inspect_index}
				elif isiterable(inspect_index):
					indexSet = set(inspect_index)
				else: raise Exception(f'{0}')
				
				index = Inspector.name_index_map[name]
				if index not in indexSet:
					Inspector.name_index_map[name] += 1
					return obj
			# id
			if inspect_id != None and Inspector.inspect_id is not my.completeSet:
				if isinstance(inspect_id, int):
					idSet = {inspect_id}
				elif isiterable(inspect_id):
					idSet = set(inspect_id)
				else: raise Exception(f'{0}')
				print(f'Inspector: set idSet {idSet}')
				Inspector.idSet = idSet
			#
			otype = type(obj)
			if otype in my.Inspector.oitype_map:
				itype = my.Inspector.oitype_map[otype]
			else:
				itype = AnyInspector
			self = object.__new__(itype)
			self.init(obj, name, *gs, **ks) # 防止自动__init__
			return self
		def init(self, obj, name, *, after=True, before=True, breakhere=False, pause=False, new=True, print_self=False, conditional=None, inspect=None, tostr=lambda obj:str(obj)):
			self._ins_ = InsName()
			self._ins_.obj = obj
			self._ins_.owner = self
			self._ins_.pause = pause
			self._ins_.print_self = print_self
			self._ins_.after = after
			self._ins_.before = before
			self._ins_.conditional = conditional
			self._ins_.breakhere = breakhere
			self._ins_.new = new
			self._ins_.tostr=tostr
			# index name
			self._ins_.index = index = Inspector.name_index_map[name]
			Inspector.name_index_map[name] += 1
			if index == 0: name = name
			else: name = f'{name}{index}'
			self._ins_.name = name
			Inspector.nameMap[name] = self
			#
			otype = type(obj)
			# inspect
			if inspect == None:
				assert type(self) is not AnyInspector
			
				inspectList = set(my.object.get_attrs_method(obj))
				for name in list(inspectList):
					if name in my.collect.type[otype].readonly_method_names: inspectList.remove(name)
			elif isinstance(inspect, str):
				inspectList = set(inspect.split())
			elif is_iterable(inspect):
				inspectList = set(inspect)
			else: raise Exception(f'{0}')
			self._ins_.inspectList = inspectList
			if new:
				self._ins_.print('%>', 'init', f'{type(self._ins_.obj)} - {type(self)}')
		def __str__(self):
			return str(self._ins_.obj)
		def __repr__(self):
			return repr(self._ins_.obj)
		def __getattr__(self, name):
			r = getattr(self._ins_.obj, name)
			# self.print(f'{self._ins_.name}.{name} undefined')
			return r
		# simulate
		def __iter__(self):
			return iter(self._ins_.obj)
		def __len__(self):
			return len(self._ins_.obj)
		def __contains__(self, v):
			return v in self._ins_.obj
		#
		def copy(self, *gs, **ks):
			self._ins_.before_call('copy')
			obj = self._ins_.obj.copy(*gs, **ks)
			r = Inspector(obj, self._ins_.name, 
				print_self=self._ins_.print_self)
			for attr in self._ins_.__dict__:
				if attr in 'obj'.split(): continue
				r._ins_.__dict__[attr] = self._ins_.__dict__[attr]
			self._ins_.after_call('copy')
			return r
		def print(self, text):
			if not self._ins_.after: return
			print('%> ' + text)
			if self._ins_.print_self:
				print(f'{self._ins_.tostr()}')
			if self._ins_.breakhere:
				breakhere()
			if self._ins_.pause:
				pause()
	class DictInspector(Inspector): # 为了in的速度继承dict
		"""
			结构：
			insks insvs flag_ins_list
			"""
		def init(self, *gs, **ks):
			super().init(*gs, **ks)
			# inspect
			self.insList = []
		# overload
		def __getitem__(self, key):
			#print(f'{self._ins_.name}.getitem [')
			r = self._ins_.obj[key]
			return r
		def __setitem__(self, k, v):
			
			if k in self._ins_.obj:
				v_ = self._ins_.obj[k]
				is_inspect = self.is_inspect(k, v) or self.is_inspect(k, v_)
			else:
				is_inspect = self.is_inspect(k, v)
			#
			if is_inspect:
				if k in self._ins_.obj:
					if v_ == v: # repeat
						text = f'{k} : {v}'
						name='repeatitem'
					else: # change
						text = f'{k} : {v_} -> {v}'
						name='changeitem'
				else: # add
					text = f'{k} : {v}'
					name='additem'
			#
			if is_inspect:
				self._ins_.before_call('__setitem__', text, name=name)
				self._ins_.obj[k] = v
				self._ins_.after_call('__setitem__', text, name=name)
			else:
				self._ins_.obj[k] = v
		def __delitem__(self, k):
			v = self._ins_.obj[k]
			if self.is_inspect(k, v):
				self.print(f'{self._ins_.name}.delitem {k} : {v}')
			del self._ins_.obj[k]
		# def __iter__(self, k):
		# 	return iter(self._ins_.obj)
		# misc
		def inspect(self, k=Pass, v=Pass, exprk=Pass, exprv=Pass, breakhere=False):
			"""
				"""
			if breakhere: self._ins_.breakhere = True
			if self._ins_.conditional == None: 
				self._ins_.conditional = True
			#
			if k != Pass and exprk == Pass:
				assert not callable(k)
				insk = lambda key: key == k
			elif k == Pass and exprk != Pass:
				insk = exprk
			else:
				insk = lambda key: True
			#
			if v != Pass and exprv == Pass:
				assert not callable(v)
				insv = lambda val: val == v
			elif v == Pass and exprv != Pass:
				insv = exprv
			else:
				insv = lambda val: True
			#
			ins = lambda k, v: insk(k) and insv(v)
			self.insList.append(ins)
			return self
		def is_inspect(self, key, val):
			if self._ins_.conditional:
				return any( ins(key, val) for ins in self.insList)
			else:
				return True
	class ListInspector(Inspector):
		def __setitem__(self, i, v):
			self._ins_.obj[i] = v
			self.print(f'{self._ins_.name}.setitem {i} = {v}')
		def __getitem__(self, i):
			r = self._ins_.obj[i]
			# self.print(f'{self._ins_.name}.getitem {i} = {v}')
			return r
		def clear(self):
			r = self._ins_.obj.clear()
			self.print(f'{self._ins_.name}.clear')
		def pop(self, *gs):
			r = self._ins_.obj.pop(*gs)
			self.print(f'{self._ins_.name}.pop {gs} = {r}')
			return r
		def append(self, e):
			r = self._ins_.obj.append(e)
			self.print(f'{self._ins_.name}.append {e}')
	class SetInspector(Inspector):
		def init(self, *gs, **ks):
			super().init(*gs, **ks)
			# inspect
			self.insList = []
		def pop(self, *gs):
			r = self._ins_.obj.pop(*gs)
			if self.is_inspect(r):
				self.print(f'{self._ins_.name}.pop {gs} = {r}')
			return r
		def clear(self):
			r = self._ins_.obj.clear(*gs)
			if any( self.is_inspect(e) for e in self._ins_.obj ):
				self.print(f'{self._ins_.name}.clear')
			return r
		def add(self, e):
			r = self._ins_.obj.add(e)
			if self.is_inspect(e):
				self.print(f'{self._ins_.name}.add {e}')
			return r
		def remove(self, e):
			if self.is_inspect(e):
				self.print(f'{self._ins_.name}.remove {e}')
			r = self._ins_.obj.remove(e)
			return r
		# inspect
		def inspect(self, e=Pass, expre=Pass, breakhere=False):
			if breakhere: self._ins_.breakhere = True
			if self._ins_.conditional == None: 
				self._ins_.conditional = True
			if e != Pass:
				assert not callable(e)
				self.insList.append( lambda ele: ele == e)
			if expre != Pass:
				self.insList.append( expre)
			return self
			
		def is_inspect(self, e):
			if self._ins_.conditional:
				return any( inse(e) for inse in self.insList )
			else: return True
	class AnyInspector(Inspector):
		def init(self, obj, *gs, inspect=None, **ks):
			if inspect == None: 
				inspect = set(my.object.get_attrs_method(obj))
				for name in list(inspect):
					if name in my.collect.python.readonly_operation_names: inspect.remove(name)
			super().init(obj, *gs, inspect=inspect, **ks)
			for name in self._ins_.inspectList:
				if name in 'copy'.split(): 
					continue
				assert (my.attr.is_internal(name) or not my.object.hasattr(self, name)), name
				set_inspect_object(self, name)
	Inspector.oitype_map = {
		list: ListInspector,
		dict: DictInspector,
		set: SetInspector,
	}
	# set overload
	inspect_map = {
		set: 'add remove __iand__ __ior__ __and__ __or__'.split(),
		list: ''.split(),
		dict: ''.split(),
	}
	def set_inspect(cls, name):
		def callback(self, *gs, **ks):
			text = f"{my.str(gs, split=' ', brace=None)}  {my.str(ks, split=' ', mapper='=', brace=None)}"
			self._ins_.before_call(name, text)
			r = getattr(self._ins_.obj, name)(*gs, **ks)
			self._ins_.after_call(name, text)
			return r
		setattr(cls, name, callback)
	def set_inspect_object(self, name, *, call=None): # any
		if call == None: call = getattr(self._ins_.obj, name)
		def callback(*gs, **ks):
			text = f"{my.str(gs, split=' ', brace=None)}  {my.str(ks, split=' ', mapper='=', brace=None)}"
			self._ins_.before_call(name, text)
			r = call(*gs, **ks)
			self._ins_.after_call(name, text)
			return r
		setattr(self, name, callback)
	for otype, names in inspect_map.items():
		itype = Inspector.oitype_map[otype]
		for name in set(names) | my.collect.python.operation_names:
			if not my.object.hasattr(itype, name):
				set_inspect(itype, name)
	# AnyInspector
	for name in my.collect.python.operation_names:
		if my.object.hasattr(AnyInspector, name) and getattr(AnyInspector, name) is not getattr(object, name): continue
		set_inspect(AnyInspector, name)
	#
	def set_simualte(cls, name):
		def callback(self, *gs, **ks):
			r = getattr(self._ins_.obj, name)(*gs, **ks)
			# self.print(f'{self._ins_.name}.{name} {my.str(gs, split=' ', brace=None)} {my.str(ks, split=' ', mapper='=')}')
			return r
		setattr(cls, name, callback)
	#
	if 'Inspector_idSet' in globals():
		Inspector.idSet = Inspector_idSet
	my.Inspector = Inspector
class Performance(cProfile.Profile):
	"""
		doc-Profile
			code		  code object
			callcount	 how many times this was called
			reccallcount  how many times called recursively
			totaltime     total time in this entry
			inlinetime    inline time in this entry (not in subcalls)
			calls		 details of the calls

			The calls attribute is either None or a list of
			profiler_subentry objects:

			code		  called code object
			callcount     how many times this is called
			reccallcount  how many times this is called recursively
			totaltime     total time spent in this call
			inlinetime    inline time (not in further subcalls)
		说明
		使用
			1.
				@performance
				def method
			perf.run()
		"""
	tmp_path = 'ground\\tmp\\Performance_55.txt' # 临时数据
	default_path = 'ground\\tmp\\perf.txt'
	def __init__(self, path=None):
		super().__init__()
		if path != None: self.path = path
		else: self.path = Performance.default_path
	def print_entry(self, entry):
		code, callcount, reccallcount, totaltime, inlinetime, calls
	#public
	def __call__(self, method): # descriptor
		def met(*gs, **ks):
			return self.run(lambda: method(*gs, **ks))
		return met
	def set_path(self, path):
		self.path = path
	def run(self, arg):
		if callable(arg):
			return super().runcall(arg)
		elif isinstance(arg, str):
			return super().run(arg)
		else: raise Exception(f'{arg}')
	def print(self, sort='ncalls', **ks):
		"""
			sort:
			"""
		return self.print_stats(sort=sort, **ks)
	def print(self, sort='ncalls', filter=lambda line:True, **ks):
		file = sys.stdout = open(self.tmp_path, 'w+')
		super().print_stats(sort=sort, **ks)
		sys.stdout.close()
		sys.stdout = sys.__stdout__
		#
		lines = my.file.readlines(self.tmp_path)
		lines = lines[:5] + [ line for line in lines[5:] if filter(line) ]
		my.file.writelines(self.path, lines) 
		#
		print(f'Performance.print {self.path}')
my.Performance = Performance
sorted_by_len = my.list2.sorted_by_len
if "desciptor":
	def get_property(func):
		name = func.__name__
		def method(self):
			# if not hasattr(self, '__property_dict'): self.__property_dict = {}
			dic = self._Property__property_dict
			if name in dic: return dic[name]
			r = func(self)
			dic[name] = r
			#d(func.__name__) 
			return r
		return method
	class Property:
		def __init__(self):
			self.__property_dict = {}
		def set_property(obj, name, value):
			obj.__property_dict[name] = value
		def has_property(self, name):
			return name in self.__property_dict
if "basic math operation":
	def moddiv__(a, b, mod):
		assert a >= 0 and b > 0 and mod > 0, f'{a} {b} {mod}'
		a = a % mod
		for i in range(mod):
			if b * i % mod == a: return i
		return None
	def is_even(a):
		return a % 2 == 0
	def is_odd(a):
		return a % 2 == 1
	#div
	def ceildiv(a, b): #int float
		if a % b > 0: return a // b + 1
		else: return a // b
	def ceil_complete(n, unit):
		return ceildiv(n, unit) * unit
	def exactdiv(a, b):
		assert isinstance(a, int), f'{a}'
		assert isinstance(b, int), f'{b}'
		assert a % b == 0
		return a // b
	def ceildiv_int(a, b):
		return (a - 1) // b + 1
if "complicate operation":
	def reduce_p(p1, p2):
		c = math.lcm(p1, p2)
		q1 = c // p1
		q2 = c // p2
		return (c, q1, q2)
	def reduce_rns(r1, r2):
		c, g1, g2 = reduce_p(r1.p, r2.p)
		return (c, r1.q * g1, r2.q * g2)
	def reduce_frac(q, p):
		gcd = math.gcd(q, p)
		return (q // gcd, p // gcd)
	def tryFindPeriod(li):
		#从头开始 重复两次
		for le in range(1, len(li)//2 + 1):
			sub = li[0:le]
			i = 0
			j = le
			while 1:
				if j == len(li): return sub
				if sub[i] != li[j]: break
				i = (i+1) % le
				j += 1
		return False
if "ntheory":
	def is_prime(n):
		return ntheory.isprime(n)
	def coprime(a, b):
		return math.gcd(a, b) == 1
	def factors(n):
		fdic = ntheory.factorint(n)
		r = []
		for factor, count in fdic.items():
			r += [factor] * count
		return r
	def factor_count(n):
		fdic = ntheory.factorint(n)
		return sum(fdic.values())
import plot
if "setup keyboard":
	"""
		按下F9后 ExitBlock中的代码执行完
		flag_block: exitblock中
		flag_exit:
			在中间按下过F9
		"""
	class ExitBlock:
		def __init__(self):
			...
		def __enter__(self):
			global flag_block
			#进入执行, 返回值赋给as后的名称
			assert not flag_block
			flag_block = True
			return self
		def __exit__(self, excType, exc, tb):
			global flag_block, flag_exit
			#返回True则无视异常, 无异常则excType为None
			assert flag_block
			flag_block = False
			if flag_exit: os._exit(0)
			if excType == None: return False # 无异常，不处理
			else: return False
			...
	flag_block = False
	flag_exit = False
	def exit_program():
		global flag_exit
		if not flag_block:
			os._exit(0)
		else:
			print()
			print(f'>>> exit blockd')
			print()
			flag_exit = True
	keyboard.add_hotkey('F9', exit_program)
if de.fix_random:
	def _pick(s):
		r = list(s)[0]
		return r
	my.pick = _pick
		
#
def test():
	print(moddiv(1, 3, 11))
def test():
	li = [1, 1, 2, 1, 1, 2, 1, 0]
	per = tryFindPeriod(li)
	myprint(per)
def test():
	myplt = plot.myplt
	c1 = Color.lightblue
	c2 = Color.pink
	m1 = Color.mix(c1, c2)
	m2 = Color.mix_cut(c1, c2)
	myplt.set_cap(4)
	myplt.color(c1, title=c1.rgb)
	myplt.color(c2, title=c2.rgb)
	myplt.color(m1, title=m1.rgb)
	myplt.color(m2, title=m2.rgb)
	plt.show()
def test():
	seq = list(range(4, 10))
	print(ranged_index(seq, 2, 5))
def test():
	mat = Mat.from_str(f'''
		1 2 7
		2 1 4
		3 4 0
		''')
	print(SquareMat.is_symmetry(mat))
def test():
	d(my.format(6, '^8'))

def test():
	table = my.Table(clabels = 'name string multi')
	for i in range(10):
		table.append((1, 2, 3))
	table.print()
def test(): #SetHash
	s = SetHash(hash=my.set.hash)
	s.add( {1} )
	d(repr(s))
def test():
	s1 = [ {1, 2}, {2} ]
	s2 = [ {2}, {1, 2} ]
	d(my.set_set.hash(s1) == my.set_set.hash(s2))
def test():
	d(my.type.defined_attributes( my.Group ))
def test():
	r = my.comb.comb_range(range(5), (2,None))
	d(r, len(r))
	a = my.math.comb(5,2)
	d(a)
def test():
	s1 = [ {16, 42, 44, 37}]
	s2 = [{40, 48, 42, 43}, {40, 36, 30}, {34, 35, 29, 38}, {32, 35, 36, 23, 41}, {45, 38}]
	s1 = [{40, 48, 42, 43}, {16, 42, 44, 37}, {40, 36, 30}, {34, 35, 29, 38}, {32, 35, 36, 23, 41}]
	s2 = [{40, 48, 42, 43}, {40, 36, 30}, {34, 35, 29, 38}, {32, 35, 36, 23, 41}, {45, 38}]
	d(my.hypergraph.try_nodeSubs_by_edges_no_cycle( my.to_unique(s1 + s2) ))
	d.expand(8,8)

def test():
	
	def f2():
		for i in range(math.floor(1000000000 * 0.2)):
			... 
		# sleep(0)
		...
	t = my.time.time(f2, time_floor=0.5, timeout=1)
	d(t)
if __name__ == '__main__':
	test()