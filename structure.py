from base import *
import math
import sympy
import time as _time
from sympy import ntheory


import matplotlib.pyplot as plt
import numpy as np
import excel
#import nty
import plot
from plot import *
"""
	(0, 2) : 0 1 2
	2 : 0 1 2
	[0 2] : 0 2
	"""
class prompt:
	"""
		"""
	extend = False
def norm_range_single(rg):
	# 8 -> 8
	if isinstance(rg, int): rg = (rg, rg)
	a, b = rg
	assert b >= a
	return a, b
def norm_range_None(rg, index=0):
	# 8 -> (None, 8)
	if isinstance(rg, (np.int32, int)): rg = (None, rg)
	#a, b = rg
	#assert b >= a
	return rg
def norm_range(rg, index=0):
	# 8 -> (0, 8)
	if isinstance(rg, int): rg = (index, rg)
	return rg
def norm_range_real(rg, index=0):
	# 5 -> (0, 1, 2, 3, 4, 5)
	if isinstance(rg, int): r = list(range(index, rg+1))
	elif isinstance(rg, tuple):
		a, b = rg
		r = list(range(a, b+1))
	elif isinstance(rg, list):
		r = rg
	else: raise Exception(f'{rg}')
	return r
def min_None(ite):
	r = None
	for e in ite:
		if r == None or e < r: r = e
	return r
def max_None(ite):
	r = None
	for e in ite:
		if r == None or e > r: r = e
	return r
def is_simple_type(typ):
	return typ in [int, float]

structs = {}
class setting:
	complicate_limit = 1e5
	save_interval = 5000
	refresh_note = True
	dump_prompt = True
	class repr:
		report_get = True
class Structure:
	"""
 		overload decide(r, n)
		cover: 不会覆盖本次运行中产生的同名
		保存：(保证同步，只有前两个都没有时(name==None)mem才会被使用，否则不存在）
			save: my.data
			name: structs
			: self.mem
		"""
	def __init__(self, *, save=False, name=None, dir=None, element_type_=None, cover=False, decide=None):
		if save: assert isinstance(name, str), f'{name}'
		self.element_type_ = element_type_
		self.cover = cover
		self.save = save
		self.name = name
		if dir == None: self.path = self.name
		else: 
			assert name != None, f'no name {path}'
			self.path = os.path.join(dir, name)
		if cover:
			assert save
			assert isinstance(name, str), f'{name}'
			r = self.default()
			structs[self.name] = r
			self.dump(r)
		if name == None: self.mem = None
		if decide == None: pass
		elif isinstance(decide, str):
			self.decide = lambda *gs: decide
		else: raise
	def element_type(self):
		if self.element_type_ == None:
			self.element_type_ = type(self.get_sample_element())
		return self.element_type_
	def set_note(self, mem):
		assert self.save, f'{0}'
		my.data.set_note(self.name, self.note(mem))
	def dump(self, mem):
		assert self.save, f'{0}'
		note = self.note(mem)
		if setting.dump_prompt: print(f'<dump> {self.path} {note}')
		my.data.dump(self.path, mem, note=note)
	def memorize(self, mem):
		if self.save:
			self.dump(mem)
		if self.name != None:
			structs[self.name] = mem
		if self.name == None:
			self.mem = mem
	def decide_ind(self, *gs): 
		if hasattr(self, 'grow'): return 'grow'
		elif hasattr(self, 'single'): return 'single'
		elif hasattr(self, 'recreate'): return 'recreate'
		else: raise Exception(f'{self, dir(self)}')
	def decide_val(self, *gs): 
		if hasattr(self, 'grow'): return 'grow'
		elif hasattr(self, 'single'): return 'single'
		elif hasattr(self, 'recreate'): return 'recreate'
		else: raise Exception(f'{self}')
	# def prepare_extend(self, mem, n): pass
	# def prepare_extend_recreate(self, mem, n): pass
	def load(self):
		if self.name == None:
			if self.mem == None:
				mem = self.default()
				self.mem = mem
			else:
				mem = self.mem
		else:
			if self.name in structs: 
				mem = structs[self.name]
			else:
				if self.save:
					if my.data.exists(self.path):
						mem = my.data.load(self.path)
						structs[self.name] = mem
					else:
						mem = self.default()
						self.memorize(mem)
				else:
					mem = self.default()
					self.memorize(mem)
		if self.save and setting.refresh_note == True:
			self.set_note(mem)
		return mem
	def __call__(self, *gs, **ks):
		if empty(gs): return self.extract_main(self.load())
		return self.get(*gs, **ks)
class SL(Structure):
	"""
		extend 返回least mem
		load -> mem
		"""
	def __init__(self, **ks):
		Structure.__init__(self, **ks)	
	def range_ind(self, li, rg): # -> li
		a, b = rg
		if a == None: a = 0
		return sliced_list(li, a, b+1)
	#extend
	#extend
	def get_len(self, le, *, least=False, raw=False):
		return self.get_ind(self, le-1, least=least, raw=raw)
	#
	def ind(self, i):
		li = self.load()
		if i < len(li): return li[i]
		else:
			li = self.get_ind(i+100, least=True)
		return li[i]
class ByInd(SL):
	"""
		li
		"""
	def __init__(self, *, index=0, single=None, recreate=None, grow=None, **ks):
		self.index = index
		if single != None: self.single = single 
		if recreate != None: self.recreate = recreate 
		if grow != None: self.grow = grow
		return ks
	def single_ind(self, *gs, **ks): return self.single(*gs, **ks)
	def recreate_ind(self, *gs, **ks): return self.recreate(*gs, **ks)
	def grow_ind(self, *gs, **ks): return self.grow(*gs, **ks)
	#misc
	def ceil(self):
		return len(self.load()) - 1
	def extract_main(self, mem):
		return mem
	def range_val_enum(self, li, val_rg): # -> ind_rg, li
		#val_rg: None
		if len(li) == 0: return (0, -1), li
		if val_rg == None: return (0, len(li)-1), li
		a, b = val_rg
		if a == self.floor: a = None
		if b >= li[-1]: b = None
		ind_rg, li_ = ranged_seq_index(li, a, b)
		return ind_rg, li_
	def default(self): return [None] * self.index
	def try_load_ind_least(self, ind): # -> li
		assert isinstance(ind, int) and ind >= 0
		mem = self.load()
		li = mem
		ind_ = len(li) - 1
		if ind_ >= ind: return mem, True
		else: return mem, False
	def norm_ind(self, li, ind_rg, *, raw):
		# ind_rg: None
		if ind_rg != None:
			mem_ = self.range_ind(li, ind_rg)
		else: mem_ = li
		return mem_
	def norm_val(self, li, val_rg, *, raw, enum): #-> [ind_rg], li
		# val_rg: None
		assert isinstance(li, list)
		ind_rg, li_ = self.range_val_enum(li, val_rg)
		if enum: return ind_rg, li_
		else: return li_
	def prepare_extend_single_ind(self, mem, n): pass
	#get
	def get_ind_least_raw(self, ind, *, decide=None):
		mem, flag = self.try_load_ind_least(ind)
		li = mem
		if flag == False:
			li = self.extend_ind(li, ind, decide=decide)
			# mem = self.box_ind(li)
			self.memorize(li)
		return li
	def get_ind(self, ind_rg_, *, least=False, raw=False):
		if ind_rg_ == None: least = True
		if ind_rg_ == None: 
			mem = self.load()
		else:
			a, b = ind_rg = norm_range_None(ind_rg_, self.index)
			mem = self.get_ind_least_raw(b)
		if least:
			assert a == None
			return self.norm_ind(mem, None, raw=raw)
		else:
			return list(self.norm_ind(mem, ind_rg, raw=raw))

	def get_val_least_raw(self, val): # -> li
		li = self.load()
		while 1:
			if len(li) == self.index:
				expect_ind = 100
			else:
				val_ = li[-1]
				if val_ >= val: break
				expect_ind = math.ceil( val / val_ * len(li) ) + 100
			li = self.get_ind_least_raw(expect_ind)
		return li
	def get_val(self, val_rg_, *, least=False, raw=False, enum=False):
		if val_rg_ == None: least = True
		if val_rg_ == None:
			mem = self.load()
		else:
			a, b = val_rg = norm_range_None(val_rg_, self.floor)
			mem = self.get_val_least_raw(b)
		if least:
			assert a == None
			return self.norm_val(mem, None, raw=raw, enum=False)
		else:
			return list(self.norm_val(mem, val_rg, raw=raw, enum=False))
	#extend
	def extend_ind_grow(self, li, ind):
		li = self.grow_ind(li, ind)
		return li
	def extend_ind_recreate(self, li, ind):
		li = self.recreate_ind(ind)
		return li
	def extend_ind_single(self, li, ind):
		self.prepare_extend_single_ind(li, ind)
		floor = len(li)
		for i in range(floor, ind+1):
			li.append(self.single_ind(i))
			if self.save and i % setting.save_interval == 0:
				self.dump(li)
		return li
	def extend_ind(self, lis, ind, *, decide=None): # -> li
		assert isinstance(lis,list), f'{lis}'
		if decide == None: decide = self.decide_ind(lis, ind)
		if decide == 'recreate':
			return self.extend_ind_recreate(lis, ind)
		elif decide == 'single':
 			return self.extend_ind_single(lis, ind)
		elif decide == 'grow':
			return self.extend_ind_grow(lis, ind)
		else: raise Exception(f'unexpected [{decide}], expecting[recreate single grow]')
	def extend_ind_step(self, *, step=1000, cycle=None, ceil=None, decide=None, time=True):
		if cycle == None and ceil == None: pass
		elif cycle == None and ceil != None:
			cycle = ceildiv((ceil - self.ceil()), step)
		if decide == None: decide = self.decide_ind(self.load(), ceil)
		return self.extend_ind_step_(step=step, cycle=cycle, time=time, decide=decide)
	def extend_ind_step_(self, *, step, cycle, time, decide):
		assert decide != 'recreate'
		mem = self.load()
		start = ceil_ = len(mem)
		if cycle == None: 
			ceil = cycle = math.inf
		else:
			ceil = ceil_ + cycle * step
		prompt.extend, saved = Flag.mask(prompt.extend, False)
		#print
		cycle_str = cycle if cycle != math.inf else 'oo'
		print()
		print(f'=== extend_step[{decide}] start ===')
		print(f'    step[{step}]    cycle[{cycle_str}]')
		print()
		#
		if time:
			t1_ = _time.time()
		c = 1
		while c <= cycle:
			if time:
				t1 = _time.time()
			ceil_ += step
			mem = self.get_ind_least_raw(ceil_, decide=decide)
			#print
			if time:
				interval = _time.time() - t1
			ceil_str = str(ceil) if ceil != math.inf else 'oo'
			perc_str = f'    {(ceil_ - start) / (ceil-start) * 100:.1f}%' if ceil != math.inf else ''
			time_str = f'    {interval:.1f} s' if time else ''
			print(f'extend_step[{decide}][{c}]    {ceil_} / {ceil_str}{perc_str}{time_str}')
			c += 1
		prompt.extend = saved
		#print
		if time:
			inter_ = _time.time() - t1_
		time_str = f'    {inter_} s' if time else ''
		print()
		print(f'=== extend_step[{decide}] finish ===')
		print()
		print(f'{start} -> {ceil}{time_str}')
		#
class ByVal(SL):
	"""
		li, val
		"""
	def __init__(self,*,single=None, recreate=None, grow=None, **ks):
		if single != None: self.single = single 
		if recreate != None: self.recreate = recreate 
		if grow != None: self.grow = grow
		return ks
	
	#grow
	def single_val(self, *gs, **ks): return self.single(*gs, **ks)
	def recreate_val(self, *gs, **ks): return self.recreate(*gs, **ks)
	def grow_val(self, *gs, **ks): return self.grow(*gs, **ks)
	def single_ind(self, *gs, **ks): raise
	def recreate_ind(self, *gs, **ks): raise
	def grow_ind(self, *gs, **ks): raise
	#misc
	def ceil(self):
		return self.load()[1]
	def extract_main(self, mem):
		return mem[0]
	def range_val_enum(self, li, val, val_rg): # -> ind_rg, li, val
		#val_rg: None
		if val_rg == None: return (0, len(li)-1), li, val
		a, b = val_rg
		if a == self.floor: a = None
		if b >= val: 
			b = None
			val_ = val
		else: val_ = b
		ind_rg, li_ = ranged_seq_index(li, a, b)
		return ind_rg, li_, val_
	def default(self): return ([], -1)
	def norm_ind(self, mem, rg, *, raw):
		# rg: None
		li, val = mem
		if rg != None:
			li_ = self.range_ind(li, rg)
			val_ = li[-1]
		else: 
			li_ = li
			val_ = val
		if raw: return li_, val_
		else: return li_
	def norm_val(self, mem, val_rg, *, raw, enum=False): # -> [ind_rg], li, [val]
		# val_rg: None
		assert isinstance(mem, tuple)
		li, val = mem
		ind_rg, li_, val = self.range_val_enum(li, val, val_rg)
		if enum:
			if raw: return ind_rg, li_, val
			else: return ind_rg, li_
		else:
			if raw: return li_, val
			else: return li_
	def try_load_val_least(self, val): # -> mem
		assert isinstance(val, int)
		mem = self.load()
		li, val_ = mem
		if val_ >= val or val == None: return mem, True
		else: return mem, False
	def prepare_extend_single_val(self, mem, n): pass
	#get
	def get_val_least_raw(self, val, *, decide=None):
		mem, flag = self.try_load_val_least(val)
		li, val_ = mem
		if flag == False:
			mem = li, val = self.extend_val(li, val_, val, decide=decide)
			self.memorize(mem)
		return mem
	def get_val(self, val_rg_, *, least=False, raw=False, enum=False):
		if val_rg_ == None: least = True
		if val_rg_ == None: 
			mem = self.load()
		else:
			a, b = val_rg = norm_range_None(val_rg_, self.floor)
			mem = self.get_val_least_raw(b)
		if least:
			assert a == None
			return self.norm_val(mem, None, raw=raw)
		else:
			return list(self.norm_val(mem, val_rg, raw=raw))
	def get_val_gt(self, val, *, least=True, raw=False):
		assert least == True
		li, val_ = mem = self.load()
		if len(li) != 0 and li[-1] >= val: return self.norm_val(mem, None, raw=raw)
		while True:
			if len(li) == 0: expexct_ceil = 100
			else: expect_ceil = math.ceil( val_ / li[-1] * val) + 100
			mem = li, val_ = self.get(expect_ceil, least=True, raw=True)
			if li[-1] >= val: return self.norm_val(mem, None, raw=raw)

	def get_ind_least_raw(self, ind): # -> li, val
		li, val = mem = self.load()
		while True:
			ind_ = len(li) - 1
			if ind_ >= ind: return (li, val)
			expect_val = math.ceil( (val + 10) / (len(li) + 1) * ind) + 100
			assert expect_val > val
			li, val = self.get_val(expect_val, least=True, raw=True)
			assert val / (len(li)+1) < 1000, f'{li}'
		raise
	def get_ind(self, ind_rg_, *, least=False, raw=False):
		if ind_rg_ == None: least = True
		if ind_rg_ == None:
			mem = self.load()
		else:
			a, b = ind_rg = norm_range_None(ind_rg_, self.floor)
			mem = self.get_ind_least_raw(b)
		if least:
			assert a == None
			return self.norm_ind(mem, None, raw=raw)
		else:
			return list(self.norm_ind(mem, ind_rg, raw=raw))
	#extend
	def extend_val_grow(self, li, val_, val):
		li = self.grow_val(li, val_, val)
		return li, val
	def extend_val_recreate(self, li, val_, val):
		li = self.recreate_val(val)
		return li, val
	def extend_val_single(self, li, val_, val):
		for i in range(val_+1, val+1):
			if self.single(i): li.append(i)
			if self.save and i != 0 and i % setting.save_interval == 0:
				self.memorize((li, i))
		self.memorize((li, val))
		return (li, val)
	def extend_val(self, lis, val_, val, *, decide=None): # -> li, val
		assert isinstance(lis, list), f'{lis}'
		if decide == None: decide = self.decide_val(lis, val_, val)
		if decide == 'recreate':
			return self.extend_val_recreate(lis, val_, val)
		elif decide == 'single':
 			return self.extend_val_single(lis, val_, val)
		elif decide == 'grow':
			return self.extend_val_grow(lis, val_, val)
		else: raise Exception(f'unexpected [{decide}], expecting[recreate single grow]')
	def extend_val_step(self, *, step=1000, cycle=None, ceil=None, decide=None, time=True):
		if cycle == None and ceil == None: pass
		elif cycle == None and ceil != None:
			cycle = ceildiv((ceil - self.ceil()), step)
		if decide == None: decide = self.decide_val(self.load(), ceil)
		return self.extend_val_step_(step=step, cycle=cycle, time=time, decide=decide)
	def extend_val_step_(self, *, step, cycle, time, decide):
		assert decide != 'recreate'
		mem = self.load()
		li, ceil_ = mem
		start = ceil_ 
		if cycle == None: 
			ceil = cycle = math.inf
		else:
			ceil = ceil_ + cycle * step
		prompt.extend, saved = Flag.mask(prompt.extend, False)
		#print
		cycle_str = cycle if cycle != math.inf else 'oo'
		print()
		print(f'=== extend_step[{decide}] start ===')
		print(f'    step[{step}]    cycle[{cycle_str}]')
		print()
		#
		if time:
			t1_ = _time.time()
		c = 1
		while c <= cycle:
			if time:
				t1 = _time.time()
			ceil_ += step
			mem = self.get_val_least_raw(ceil_, decide=decide)
			#print
			if time:
				interval = _time.time() - t1
			ceil_str = str(ceil) if ceil != math.inf else 'oo'
			perc_str = f'    {(ceil_ - start) / (ceil-start) * 100:.1f}%' if ceil != math.inf else ''
			time_str = f'    {interval:.1f} s' if time else ''
			print(f'extend_step[{decide}][{c}]    {ceil_} / {ceil_str}{perc_str}{time_str}')
			c += 1
		prompt.extend = saved
		#print
		if time:
			inter_ = _time.time() - t1_
		time_str = f'    {inter_} s' if time else ''
		print()
		print(f'=== extend_step[{decide}] finish ===')
		print()
		print(f'{start} -> {ceil}{time_str}')
		#
class SeqBase(SL):
	"""
		$$: 递增 全数字
 		(seq, ceil)
		int
		floor
		get = get_val
		"""
	def __init__(self, *, floor=0, min_element=None, **ks):
		self.floor = floor
		self.min_element_ = min_element
		SL.__init__(self, element_type_=int, **ks)
	def get_enum_____(self, rg): ##
		a, b = rg = norm_range_list(rg)
		i = self.index
		index = []
		mem = []
		while 1:
			x = self.single(i)
			if a <= x <= b: 
				index.append(i)
				r.append(x)
			elif x > b: break
			i += 1
		return index, r
	#extend
	#private
	#mem
	#
	def ind(self, i):
		s = self.get_ind(i+100, least=True)
		return s[i]
	def min_element(self):
		if self.min_element_ == None: self.min_element_ = self.ind(0)
		return self.min_element_
	def element_type(self):
		return int
	def report_common(self, seq, val_rg):
		a, b = val_rg = norm_range(val_rg)
		index1, s1 = self.get_enum(val_rg)
		index2, s2 = seq.get_enum(val_rg)
		i = 0
		j = 0
		res = []
		while 1:
			if not (empty(s1) or empty(s2)):
				a1 = s1[i]
				a2 = s2[j]
				if a1 > a2:
					j += 1
					if j == len(s2): break
				elif a1 < a2:
					i += 1
					if i == len(s1): break
				else:
					res.append((i, j, s1[i]))
					i += 1
					if i == len(s1): break
					j += 1
					if j == len(s2): break
		print(f'=== report ===')
		print(f'range {a} - {b}')
		print(f'seq1[{len(s1)}] seq2[{len(s2)}] common[{len(res)}]')
		print(f'index1 index2 value')
		for i1, i2, v in res:
			print(f'{v} {i1} {i2}')
	def format(self, val_rg_, **ks):
		val_rg = norm_range(val_rg_, self.index)
		ind_rg, li = self.get_val(val_rg, enum=True)
		return SeqBaseFormat(self, li, ind_rg=ind_rg, name=self.name, **ks)
	#list
	def test():
		return Seq(single=lambda n: n%3 == 2, floor=0, name='test')
	def count(self, **ks):
		return SeqCount(self, **ks)
	def cap(self, save=False, **ks):
		assert save == False, f'{0}'
		return SeqCap(self, save=False, **ks)
	#index_seq / list
	def wrap(self, wrap, *, seq=True, **ks):
		if seq: return SeqWrap_Seq(self, wrap=wrap, **ks)
		else: return SeqWrap_Seq(self, wrap=wrap, **ks)
	def float(self, seed=0, **ks):
		# swing=10 -> [0,10]
		return SeqFloat(self, seed=seed, **ks)
class Seq(ByVal, SeqBase, ):
	"""
		"""
	...	
	def __init__(self, **ks):
		ks = ByVal.__init__(self, **ks)
		SeqBase.__init__(self, **ks)
	def note(self, mem):
		li, val = mem
		return val
	get = ByVal.get_val
	extend_step = ByVal.extend_val_step
	# def get_index(self):
class IndexSeq(ByInd, SeqBase, ):
	"""
		li
		get = get_value
		"""
	def __init__(self, *, least=False, raw=False, **ks):
		ks = ByInd.__init__(self, **ks)
		SeqBase.__init__(self, **ks)
		#return self.get_ind(le-1, least=least, raw=raw)
	def note(self, mem):
		li = mem
		value_str = 'None' if len(li) == 0 else li[-1]
		return f'index[{len(li)-1}] value[{value_str}]'
	get = ByInd.get_val
class List(ByInd ):
	"""
		a == None 时 返回从0开始的序列
		format, enum除外
		"""
	def __init__(self, *, element_type=None, **ks):
		ks = ByInd.__init__(self, **ks)
		SL.__init__(self, **ks)
	#extend
	def note(self, r):
		return len(r) - 1
	get = ByInd.get_ind
	def extend_ind(self, mem, ind, **ks):
		assert ind <= setting.complicate_limit or is_simple_type(self.element_type()), f'{0}'
		return ByInd.extend_ind(self, mem, ind, **ks)
	def grow_ind(self, *gs, **ks):
		return self.grow(*gs, **ks)
	#
	def get_sample_element(self):
		return self.get_first()
	def format(self, ind_rg_, **ks):
		ind_rg = norm_range(ind_rg_, self.index)
		li = self.get_ind(ind_rg)
		return ListFormat(self, li, ind_rg=ind_rg, **ks)
	def enum(self, rg_):
		a, b = rg = norm_range_list(rg_)
		li = self.get(b, least=True)
		r = [ (i, li[i]) for i in range(a, b+1) ]
		return r
	def upline(self, rg_):
		# 无视None
		a, b = rg = norm_range_list(rg_)
		x = []
		y = []
		li = self.get(b, least=True)
		max_ = -math.inf
		for i in range(self.index, b+1):
			e = li[i]
			if e == None: continue
			if e > max_:
				if a <= i:
					x.append(i)
					y.append(e)
				max_ = e
		return x, y
	def get_first(self):
		return self.ind(self.index)
	#list
	def random(n):
		li = np.random.randint(n+1, size=n+1)
		return List_fix(li)
	def test():
		li = List(single=lambda i: i % 3, index=2, save=False)
		return li
	def len(self, *, save=False, **ks):
		return self.wrap(wrap=len, save=save, **ks)
	def min(self, **ks):
		return self.wrap(wrap=min_None, name=f'min({self.name})', **ks)
	def wrap(self, wrap, **ks):
		return ListWrap(self, wrap=wrap, **ks)
	def count(self, element, *, ratio=False, filter=None, save=False, name=None, **ks):
		if ratio:
			c = ListCount(self, element, save=save, filter=filter)
			if name == None:
				name = f'ratioCount({self.name},{element})'
			return c.ratio(name=name, save=save, **ks)
		else: 
			return ListCount(self, element, save=save, filter=filter, **ks)
	def ratio(self, **ks):
		def ratio(i, e):
			return e / i
		return ListWrap(self, wrap=ratio, **ks)
	def density(self, element, filter=None, length=1000, name=None, save=False, **ks):
		if name == None: name = f'density({self.name},{element})[{length}]'
		c = self.count(element, filter=filter, save=save)
		den = Density(c, name=name, save=save, length=length, **ks)
		return den
class SLFormat:
	"""
		"""
	def __init__(self, owner, li, *, ind_rg, name=None, filter=lambda i,e: e != None, wrap=None, name_wrap=None):
		a, b = self.ind_rg = ind_rg
		self.plot_exist = False
		self.owner = owner
		self.li = li
		self.element_type = self.owner.element_type()
		#
		if name == None: name = self.owner.name
		else: name = name
		if name_wrap != None and name != None: name = name_wrap(name)
		self.name = name
		#
		x = []
		y = []
		if self.element_type in (int, float):
			for i, e in zip(list(range(a, b+1)), self.li):
				if filter(i, e):
					x.append(i)
					if wrap == None: y.append(e)
					else: y.append(wrap(i, e))
		elif self.element_type == list:
			assert len(li) == 0 or len(li[0]) == 0 or type(li[0][0]) == int, f'{li[0]}'
			
			for i, li in zip(list(range(a, b+1)), self.li):
				for e in li:
					if filter(i, e):
						x.append(i)
						if wrap == None: y.append(e)
						else: y.append(wrap(i, e))
		else: raise Exception(f'{self.element_type}')
		self.x = x
		self.y = y
		...
	def draw_base(self, newplot=None, **ks):
		if newplot == None:
			if self.plot_exist:
				newplot = False
			else: 
				newplot = True
				self.plot_exist = True
		ks['newplot'] = newplot
		if 'title' not in ks: ks['title'] = self.name
		return ks
	def show(self):
		myplt.show()
	def print(self, *, enum=False, wrap=lambda i:i):
		a, b = self.ind_rg
		real_rg = list(range(a, b+1))
		if a > b:
			print('empty')
			return
		sample = self.li[0]
		if self.element_type() != int: newline = True
		elif enum: newline = True
		else: newline = False
		if newline: end = '\n'
		else: end = ' '
		if enum:
			for i, e in zip(real_rg, self.li):
				myprint(f'{i}: {wrap(e)}', end=end)
		else:
			for e in self.li:
				myprint(f'{wrap(e)}', end=end)
class SeqBaseFormat(SLFormat):
	"""
		"""
	def __init__(self, owner, li, **ks):
		SLFormat.__init__(self, owner, li, **ks)
	def draw(self, type='vline', dire='h', **ks):
		ks = self.draw_base(**ks)
		a, b = self.val_rg
		y = self.y
		if type == 'line': plot.myplt.seq_line(y, dire=dire, **ks)
		elif type == 'dot': plot.myplt.seq_dot(y, dire=dire, **ks)
		else: raise Exception(f'{0}')
		if self.name != None: plt.title(self.name)
		return self
class ListFormat(SLFormat):
	"""
		不接受None-range
		自动清除None
		"""
	def __init__(self, owner, li, **ks):
		SLFormat.__init__(self, owner, li, **ks)
	#draw
	def draw(self, **ks):
		ks = self.draw_base(**ks)
		a, b = self.ind_rg
		x = self.x
		y = self.y
		plot.myplt.scatter(x, y, **ks)
		if self.name != None: plt.title(self.name)
		return self
	def draw_upline(self, color='red', marker='p', markersize=None, **ks):
		ks = self.draw_base(**ks)
		x, y = self.owner.upline(self.ind_rg)
		if markersize == None: markersize = myplt.fit_marker_size(len(x), di=1)
		plot.myplt.plot(x, y, color=color, marker=marker, markersize=markersize, **ks)
		return self
	def draw_fit(self, fit):
		x = self.x
		y = self.y
		if fit == 1:
			args = np.polyfit(x, y, 1)
			myplt.plot_poly(args, rank=1, fmt='k-')
		else: raise Exception(f'{fit}')
	#
class SeqCount(List):
	"""
		"""
	def __init__(self, seq, *, save=False, name=None):
		if name == None: 
			if seq.name != None: name = f'count({seq.name})'
		self.seq = seq
		List.__init__(self, save=save, index=seq.floor, name=name)
	def grow(self, mem, ceil):
		li = mem
		s = self.seq.get(ceil+1, least=True)
		ceil_ = len(mem) - 1
		floor = ceil_ + 1
		i = 0
		while s[i] <= ceil_: i += 1
		count = li[-1] if not len(li) != 0 else 0
		last_e = ceil_ + 1
		for j in range(i, len(s)):
			li += [j] * (s[j] - last_e)
			last_e = s[j]
		li += [len(s)] * (ceil-last_e)
		return li
class SeqCap(List):
	"""
		"""
	def __init__(self, seq, *, save=False, name=None):
		if name == None: 
			if seq.name != None: name = f'cap({seq.name})'
		self.seq = seq
		List.__init__(self, save=save, index=seq.floor, name=name)
	def grow(self, li, ceil):
		li = li
		s = self.seq.get_val_gt(ceil, least=True)
		ceil_ = len(li) - 1
		floor = ceil_ + 1
		i = 0
		for j in range(floor, ceil+1):
			while s[i] <= j: i += 1
			li.append(s[:i])
		return li
class SeqWrap_Seq(IndexSeq):
	"""
		要求递增 无限
		"""
	def __init__(self, seq_, *, name=None, wrap, **ks):
		if name == None: 
			if seq_.name != None: name = f'{wrap.__name__}({seq_.name})'
		self.seq_ = seq_
		self.wrap = wrap
		IndexSeq.__init__(self, name=name, **ks)
	def recreate(self, ceil):
		lis = self.li(ceil, least=True)
		return [None] * self.index + [self.wrap(e) for e in lis]
	def grow(self, li, ind):
		ind_ = len(li) - 1
		oseq = self.seq_.get_ind(ind, least=True)
		for i in range(ind_+1, ind+1):
			li.append(self.wrap(oseq[i]))
		return li
class SeqWrap_List(List):
	"""
		"""
	def __init__(self, seq_, *, wrap, save=False, name=None, **ks):
		if name == None: 
			if seq_.name != None: name = f'{wrap.__name__}({seq_.name})'
		self.seq_ = seq_
		self.wrap = wrap
		List.__init__(self, name=name, **ks)
	def recreate(self, ceil):
		lis = self.li(ceil, least=True)
		return [None] * self.index + [self.wrap(e) for e in lis]
	def grow(self, li, ind):
		ind_ = len(li) - 1
		oseq = self.seq_.get_ind(ind, least=True)
		for i in range(ind_+1, ind+1):
			li.append(self.wrap(oseq[i]))
		return li
class SeqFloat(IndexSeq):
	"""
		要求：seq无重复
		会避免重复, 长度和seq一样
		index 0-99 ... 内元素范围在[ seq[0], seq[100] ) (unit=100)
		长度永远是unit整数倍（除了一开始）
		floor < 100
		index = 0
		整数
		"""
	def __init__(self, seq, *, seed, unit=1000, save=False, name=None, **ks):
		self.unit = unit
		self.seq = seq
		self.seed = seed
		if name == None: 
			if seq.name != None: name = f'float({seq.name},seed={seed},unit={unit})'
		self.seq = seq
		assert seq.floor < unit, f'{0}'
		
		IndexSeq.__init__(self, save=save, index=0, floor=seq.floor, name=name, **ks)
	def grow(self, li, ind):
		unit = self.unit
		ind = ceil_complete(ind+1, self.unit) - 1
		seq = self.seq.get_ind(ind, least=True)
		ind_ = len(li) - 1
		assert (ind_ + 1) % unit == 0, f'{ind_}'
		
		for p in range(ind_+1, ind+1, unit):
			seed = self.seed + p * 13
			sub = sorted(my.random.choice_range(seq[p], seq[p+unit], unit, seed=seed, replace=False))
			li += sub
		return li
class ListWrap(List):
	"""
		"""
	def __init__(self, li, *, wrap, save=False, name=None):
		if name == None: 
			if li.name != None: name = f'{wrap.__name__}({li.name})'
		self.li = li
		self.wrap = wrap
		List.__init__(self, save=save, index=li.index, name=name)
	def grow(self, li, val):
		lis = self.li.get_ind(ind, least=True)
		floor = len(li)
		for i in range(floor,ind+1):
			e = lis[i]
			li.append(self.wrap(i, e))
		return li
class ListCount(List):
	"""
		"""
	def __init__(self, li, element, *, filter=None, save=False, name=None):
		if name == None: 
			if li.name != None: name = f'count({li.name},{element})'
		self.li = li
		self.element = element
		self.filter = filter
		List.__init__(self, save=save, index=li.index, name=name)
	def grow(self, li, ind):
		lis = self.li.get_ind(ind, least=True)
		floor = len(li)
		if len(li) == self.index: count = 0
		else: count = li[-1]
		if self.filter == None:
			for e in lis[floor:ind+1]:
				if e == self.element: count += 1
				li.append(count)
		else:
			for i in range(floor,ind+1):
				e = lis[i]
				if e == self.element and self.filter(i,e) : count += 1
				li.append(count)
		return li
class List_fix(List):
	"""
		"""
	def __init__(self, li, **ks):
		self.li = li
		List.__init__(self, **ks)
	def get_least_raw(self, ceil):
		assert len(self.li) - 1 >= ceil
		return self.li
class Density(List):
	"""
		"""
	def __init__(self, count_li, *, length, save=False, **ks):
		self.count_li = count_li
		self.length = length
		List.__init__(self, save=save, index=count_li.index, **ks)
	def grow(self, li, ind):
		length = self.length
		lis = self.count_li.get(ind+length, least=True)
		floor = len(li)
		for i in range(floor, ind+1):
			count = lis[i+length]-lis[i]
			den = count / length
			li.append(den)
		return li
class Table:
	"""
		"""
	def __init__(self, *, index=(0,0), rlabel=[('', lambda i:i)], clabel=[('', lambda i:i)],
		color=None, note=None, **ks):
		#rlabel: single int->name
		Structure.__init__(self, **ks)
		self.index_r, self.index_c = index
		self.rlabel = self.norm_labels(rlabel)
		self.clabel = self.norm_labels(clabel)
		self.color = color
		self.note=note
	def norm_labels(self, labels):
		labels = norm_list(labels)
		if (not empty(labels)) and isinstance(labels[0], str):
			labels[0] = (labels[0], lambda i:i)
		return labels
	def array(self, range_r = 10, range_c = 10):
		range_r = norm_range_real(range_r, self.index_r)
		range_c = norm_range_real(range_c, self.index_c)
		return [ [ self.single_(r, c) for c in range_c ] for r in range_r ]
	def format(self, range_r, range_c):
		range_r = norm_range_real(range_r, self.index_r)
		range_c = norm_range_real(range_c, self.index_c)
		array = self.array(range_r, range_c)
		rlabel = [ (name, [f'{single(i)}' for i in range_r]) for name, single in self.rlabel ]
		clabel = [ (name, [f'{single(i)}' for i in range_c]) for name, single in self.clabel ]
		if self.color == None: color = {}
		else:
			color = {}
			for r, i in enumerate(range_r):
				for c, j in enumerate(range_c):
					clr = self.color(i, j)
					if clr != None:
						color[r, c] = clr
		return TableFormat(array=array, rlabel=rlabel, clabel=clabel, note=self.note, color=color)
class TableFormat:
	"""
		color: { (0,0) : 'red' }
		"""
	def __init__(self, *, array, rlabel, clabel, note, color):
		self.array = array
		self.rlabel = rlabel
		self.clabel = clabel
		self.note = note
		self.color = color
	def save_excel(self, name):
		return excel.save_table(self.array, name, rlabel=self.rlabel, clabel=self.clabel, note=self.note, color=self.color)
	def show(self):
		range_r = self.index_r
		range_c = self.index_c
		array = self.array(range_r, range_c)
		fig, ax = plt.subplots()
		rlabel = self.rlabel
		clabel = self.clabel
		if self.color == None: color = None
		else:
			color = []
			for i in range_r:
				row = []
				for j in range_c:
					c = self.color(i, j)
					if c == None: c = 'white'
					row.append(c)
				color.append(row)
		tab = plt.table(cellText=array, colLabels=clabel, rowLabels=rlabel, loc='center', cellLoc='center', rowLoc='center',
			cellColours=color)
		plt.axis('off')
		plt.show()

if "Repr":
	class Repr:
		"""
			reprtype: line | ilnes | table
			"""
		def __init__(self, *, datadir=None, reprdir=None, cover=False, reprtype, name):
			if datadir == None: datadir = 'repr'
			else: datadir = os.path.join('repr', datadir)
			self.datapath = os.path.join(datadir, name)
			if reprdir == None: reprdir = 'repr'
			else: reprdir = os.path.join('repr', reprdir)
			self.reprpath = os.path.join('ground', reprdir, name+'.txt')
			# self.cover = cover
			#
			self.name = name
			self.reprtype = reprtype
			if cover: self.mem = self.default()
			else: self.mem = self.read()
		def default(self):
			return {}
		def __str__(self):
			return str(self.mem)
		def read(self):
			return my.data.load(self.datapath, default={})
		def write(self):
			self.write_data()
			self.write_repr()
		def write_repr(self):
			my.file.write(self.reprpath, self.get_text())
		def write_data(self):
			my.data.dump(self.datapath, self.mem)
		def get_text(self):
			txt = ''
			items = [(self.format_i(i), self.format(i, e)) for i, e in sorted_dict(self.mem).items()]
			if self.reprtype == 'line':
				for i, e in items:
					txt += f'{i}: {e}\n'
			elif self.reprtype == 'lines':
				raise
			elif self.reprtype == 'table':
				raise
			elif self.reprtype == 'dict':
				for i, e in items:
					txt += f'{i}\n'
					for name, string in e.items():
						txt += f'\t{name}= {string}\n'
			else: raise Exception(f'unexpected [{self.reprtype}], expecting[{'line'} {'lines'} {'table'} {'dict'}')
			return txt
			
			s = Tab.str(self.dic, rorder='sort', corder='ceil tail ratio'.split())
		#overload
		def format_i(self, i):
			return str(i)
		#interface
		def refresh(self):
			self.write_repr()
		def get(self, i):
			if i in self.mem:
				if setting.repr.report_get: print(f'<{self.name}> pass {i}')
				return self.mem[i]
			else:
				entry = self.get_entry(i)
				self.mem[i] = entry
				self.write()
				if setting.repr.report_get: print(f'<{self.name}> finish {i}')
				return entry
#import
__this__ = __import__(__name__)
plot.structure = __this__
def test():
	s1 = SeqSingle( lambda i: 2 ** i )
	s2 = SeqSingle( lambda i: 3 * i + 1 )
	s1.report_common(s2, 10000)
def test():
	def f(m, n):
		return (n ** 2) % m
	def color(i, j):
		if f(i, j) == 0: 
			if j < i: return Color.pink + Color.lightblue
			else: return Color.pink
		elif j < i: return Color.lightblue
		return None
	table = Table(f, index=(2, 0), color=color, rlabel='m', clabel='n', note='(n ** 2) % m)'
	)
	ind_ = nty.Prime()(50)
	table(rg, 30).save_excel('b')
def test():
	k_index = 1
	n_index = 1
	z_range = 100
	def single(k, z):
		if z % k == 0 and z // k % 3 == 1 and ((z // k - 1) // 3) >= n_index:
			return 1
		return 0
	def total(z):
		r = sum( single(v, z) for v in range(k_index, z+1) )
		return r
	def color(k, z):
		if single(k, z): return Color.lightBlue
	tab = Table(single, index=(k_index, 0), color=color, rlabel=['k'], clabel=['z', ('total', total)], note='')
	tab(z_range // 4 + 1, z_range).save_excel('ground\\sieve_k(3n+1)')
def test():
	def f(i):
		return i % 4 == 0
	s = Seq(single=f, index=1, save=True, name='test', cover=True)
	print(s(100))
def test():
	def f(i):
		return i % 3 == 0
	s = Seq(single=f, index=1, save=False, name='test', cover=False)
	print(s((2, 100)))
	myprint(s.get_len(50) )
	myprint(s.ind(50) )
def test():
	s = Seq.test()
	sc = s.count()
	print(list(s(10)))
	print(sc(10))
def test():
	def single(i):
		return i+1
	s = IndexSeq(single=single)
	def wrap(i):
		return i + 2
	s2 = s.wrap(wrap, seq=True, save=True, name='test', cover=True)
	print(s2(10))
def test(): # test List
	li = List.test()
	c = li.density(0)
	c.format(10).draw().show()
	print(c.name)
def test():
	s = Seq.test()
	f = s.float(seed=0)
	a = s.get_ind(300)
	b = f.get_ind(300)
	print(a, b, len(a), len(b))
if __name__ == '__main__':
	test()