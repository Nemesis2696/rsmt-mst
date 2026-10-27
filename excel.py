from base import *
import math
import xlwt
import xlrd
from collections import defaultdict
"""
	xwlt.add_palette_colour(name, index) 8 <= index <= 63
	easyxf: 小写
	"""
xf_lib = {}
class default:
	row_height = 300
	col_width = 10
class Dict2(defaultdict):
	"""
		"""
	def __init__(self):
		defaultdict.__init__(self, dict)
	def update(self, dic2):
		for name1, dic_ in dic2.items():
			self[name1].update(dic_)
	def updated(self, dic2):
		r = self.copy()
		r.update(dic2)
		return r
	def copy(self):
		r = Dict2()
		for name, dic in self.items():
			r[name] = dic.copy()
		return r
class Ctable(dict):
	"""
		"""
	def __init__(self):
		...
class Stable:
	"""
		cell[1, 2][name][name]
		row[0][name][name]
		sheet[name][name]
		会叠加
		cell > col > row > sheet
		"""
	def __init__(self):
		self.cell = defaultdict(Dict2)
		self.row = defaultdict(Dict2)
		self.col = defaultdict(Dict2)
		self.sheet = Dict2()
		self.sheet['align']['horizontal'] = 'centre'
class Ztable:
	"""
		row_height[1]
		default_row_height
		"""
	def __init__(self):
		self.default_row_height = default.row_height
		self.default_col_width = default.col_width
		self.row_height = {}
		self.col_width = {}
		self.autofit = True
class Workbook():
	"""
		"""
	def __init__(self):
		self.sheets = []
	def add_sheet_(self, *gs, **ks): ###
		sheet = Sheet(self.workbook.add_sheet(*gs, **ks) )
		sheet.set_col_default_width(30)
		sheet.set_row_default_height(400)
		self.sheets.append(sheet)
		return sheet
	def add_sheet(self):
		sheet = Sheet()
		self.sheets.append(sheet)
		return sheet
	def save(self, fname):
		wb_ = xlwt.Workbook()
		#
		for i, sheet in enumerate(self.sheets):
			#color
			color_index_map = {}
			assert len(sheet.colors) <= 56, f'{sheet.colors}'
			for j, color in enumerate(list(sheet.colors)):
				name = f'C{color.rgb_string}'
				index = j + 8
				color_index_map[color] = index
				xlwt.add_palette_colour(name, index)
				wb_.set_colour_RGB(index, *color.rgb)
			#
			sheet_ = wb_.add_sheet(str(i))
			sheet.save(sheet_, wb_, color_index_map=color_index_map)
		wb_.save(f'{fname}.xls')
		return wb_
	def from_table(table, *gs, **ks):
		wb = Workbook()
		sheet = Sheet.from_table(table, *gs, **ks)
		wb.sheets.append(sheet)
		return wb
	@property
	def sheet(self):
		assert len(self.sheets) == 1
		return self.sheets[0]
class Sheet:
	"""
		"""
	def __init__(self):
		self.ctable = Ctable()
		self.stable = Stable()
		self.ztable = Ztable()
		self.colors = set()
	def row(self, r):
		return Row(self, r)
	def col(self, i):
		return Col(self, i)
	def row_height(self, r):
		rt = self.ztable.row_height.get(r, self.ztable.default_row_height)
		return rt
	def col_width(self, c):
		return self.ztable.col_cidth.get(c, self.ztable.default_col_width)
	def set_row_height(self, r, height):
		self.ztable.row_height[r] = height
	def set_col_width(self, c, width):
		self.ztable.col_width[c] = width
	def used_rows(self):
		rows = set()
		for r in self.stable.row: rows.add(r)
		for r, c in self.stable.cell: rows.add(r)
		for r, c in self.ctable: rows.add(r)
		return rows
	def used_cols(self):
		cols = set()
		for c in self.stable.col: cols.add(c)
		for r, c in self.stable.cell: cols.add(c)
		for r, c in self.ctable: cols.add(c)
		return cols
	def autofit_col_width(self, c):
		lens = [ len(txt) for txt in self.col(c).texts() ]
		maxlen = max(lens)
		self.col(c).width = maxlen + 1
	def cell(self, r, c):
		return Cell(self, r, c)
	def save(self, sheet_, wb_, *, color_index_map=None): #改变 stable.cell
		#row col
		stable = self.stable
		ctable = self.ctable
		ztable = self.ztable
		used_rows = self.used_rows()
		used_cols = self.used_cols()
		row_max = max(used_rows)
		col_max = max(used_cols)
		for r, style in stable.row.items():
			sheet_.row(r).set_style(get_xf(style, color_index_map))
		for c, style in stable.col.items():
			sheet_.col(c).set_style(get_xf(style, color_index_map))
		# for r, rstyle in stable.row.items():
		# 	for c, cstyle in stable.col.items():
		# 		style = rstyle.updated(cstyle)
		# 		stable.cell[r, c] = style.updated(stable.cell[r, c])
		#cell value&style
		cells = set()
		cells |= ctable.keys()
		cells |= stable.cell.keys()
		for r in stable.row:
			for c in stable.col:
				cells.add((r,c))
		#blank_cell_styles = set(stable.cell.keys())
		for x in cells:
			r, c = x
			text = ctable.get(x, None)
			style = stable.sheet.copy()
			rstyle = stable.row.get(r, False)
			if rstyle != False: style.update(rstyle)
			cstyle = stable.col.get(c, False)
			if cstyle != False: style.update(cstyle)
			cell_style = stable.cell.get( x, False)
			if cell_style != False: 
				style.update(cell_style)
			xf = get_xf(style, color_index_map )
			sheet_.write(r, c, text, style=xf)
		#size
		if ztable.autofit:
			for c in used_cols:
				if c not in ztable.col_width:
					self.autofit_col_width(c)
		sheet_.set_row_default_height(ztable.default_row_height)
		#sheet_.set_col_default_width(ztable.default_col_width)
		for r in used_rows:
			if r not in ztable.row_height:
				sheet_.row(r).height = ztable.default_row_height
		for c in range(col_max+51):
			if c not in ztable.col_width:
				sheet_.col(c).width = ztable.default_col_width * 256
		for r, height in ztable.row_height.items():
			sheet_.row(r).height = height
		for c, width in ztable.col_width.items():
			#d(ztable.col_width)
			sheet_.col(c).width = width * 256
	def from_table(table, *, rlabel=[], clabel=[], note=None, color={}):
		self = Sheet()
		rn = len(table)
		cn = len(table[0])
		rbias = len(clabel) + 1
		cbias = len(rlabel) + 1
		rtotal = rn + rbias
		ctotal = cn + cbias
		ctable = self.ctable
		stable = self.stable
		ztable = self.ztable
		#ctable
		#note
		if note != None: ctable[0, 0] = note
		#label
		for i, (name, labels) in enumerate(clabel):
			ctable[i, cbias-1] = name
			for c, label in enumerate(labels):
				ctable[i, c+cbias] = label
		for i, (name, labels) in enumerate(rlabel):
			ctable[rbias-1, i] = name
			for r, label in enumerate(labels):
				ctable[r+rbias, i] = label
		#array
		for r in range(rn):
			for c in range(cn):
				ctable[r+rbias, c+cbias] = table[r][c]
		#stable
		stable.row[rbias-1]['border']['bottom'] = 'medium'
		stable.col[cbias-1]['border']['right'] = 'medium'
		for (r, c), clr in color.items():
			x = (r+rbias, c+cbias)
			self.colors.add(clr)
			stable.cell[x]['pattern']['pattern_fore_colour'] = clr
			stable.cell[x]['pattern']['pattern'] = 'solid'
		return self
class Cell:
	"""
		"""
	def __init__(self, sheet, r, c):
		self.sheet = sheet
		self.r = r
		self.c = c
	def write(self, value):
		self.sheet.ctable[self.r, self.c] = value
	def set_style(self, style):
		self.sheet.stable.cell[self.r, self.c] = style
class Row:
	"""
		"""
	def __init__(self, sheet, row):
		self.sheet = sheet
		self.row = row
	def set_style(self, style):
		self.sheet.stable.row[self.row] = style
	@property
	def height(self):
		return self.sheet.row_height(self.row)
	@height.setter
	def height(self, height):
		self.sheet.set_row_height(self.row, height)
class Col:
	"""
		"""
	def __init__(self, sheet, col):
		self.sheet = sheet
		self.col = col
	def set_style(self, style):
		self.sheet.stable.col[self.col] = style
	@property
	def width(self):
		return self.sheet.col_width(self.col)
	@width.setter
	def width(self, width):
		self.sheet.set_col_width(self.col, width)
	def cells(self):
		rt = []
		for (r, c), text in self.sheet.ctable.items():
			if c == self.col:
				rt.append((r, c))
		return rt
	def texts(self):
		rt = []
		for (r, c), text in self.sheet.ctable.items():
			if c == self.col:
				rt.append(str(text))
		return rt
class Style(defaultdict):
	"""
		"""
	def __init__(self):
		defaultdict.__init__(self, dict)
		self['align']['vertical'] = 'centre'
		self['align']['horizontal'] = 'centre'
def get_xf(dic, color_index_map=None):
	string = ''
	for name1, dic2 in dic.items():
		string += f'{name1}:'
		for name2, value in dic2.items():
			if isinstance(value, Color): value = color_index_map[value]
			string += f'{name2} {value},'
		string += ';'
	return xf_lib.get(string, xlwt.easyxf(string) )
def fulltable(table, *, rlabel=[], clabel=[]): ###
	"""
		label: [ (name, list) .. ]
		"""
	rn = len(table)
	cn = len(table[0])
	rbias = len(clabel) + 1
	cbias = len(rlabel) + 1
	rtotal = rn + rbias
	ctotal = cn + cbias
	ctable = [ [ '' ] * ctotal for r in range(rtotal) ]
	for i, (name, labels) in enumerate(clabel):
		ctable[i][cbias-1] = name
		for c, label in enumerate(labels):
			ctable[i][c+cbias] = label
	for i, (name, labels) in enumerate(rlabel):
		ctable[rbias-1][i] = name
		for r, label in enumerate(labels):
			ctable[r+rbias][i] = label
	for r in range(rn):
		for c in range(cn):
			ctable[r+rbias][c+cbias] = table[r][c]
	return ctable
def save_table( table, name, **ks):
	wb = Workbook.from_table(table, **ks)
	wb.save(name)
	return wb
def test():
	table = [[1, 1], [2, 2]]
	wb = save_table( table, 'a',
		clabel=[('n', [3, 2])],
		color={(0,0):Color.lightBlue}
	)
	s = wb.sheet
	print(s.stable.cell[1, 0])
def test1():
	table = [[1, 1], [2, 2]]
	ft = fulltable(table,
		rlabel=[(1, [0, 0])],
		clabel=[('n', [3, 2]),
			('', [1, 2]),],
		)
	print(ft)
def test1():
	style = Style()
	style['border']['left_color'] = 'red'
	style['border']['left'] = 'thick'
	wb=Workbook()
	sheet = wb.add_sheet()
	sheet.cell(5, 2).write(1)
	sheet.cell(5, 1).set_style(style)
	sheet.row(1).height = 200
	sheet.col(1).width = 1
	#sheet.col(2).width = default.col_width
	wb_ = wb.save('a')
	sheet_ = wb_.get_sheet(0)
def test1():
	wb = xlwt.Workbook()
	sheet = wb.add_sheet('0')
	sheet.set_col_default_width(1000)
	col = sheet.col(0)
	xlwt.add_palette_colour('cblue', 0x8)
	wb.set_colour_RGB(0x8, 251, 228, 228)
	xf = xlwt.easyxf('pattern: pattern solid, fore_color cblue')
	col.set_style(xf)
	sheet.write(5, 5, 4, style=xf)
	#d(sheet.col(0).has_default_width)
	wb.save('a.xls')
	help(xlwt.add_palette_colour)
if __name__ == '__main__':
	test()