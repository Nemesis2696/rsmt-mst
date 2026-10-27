from base import *
import math

def sorted2(li) -> tuple:
	a, b = li
	if a > b: return b, a
	else: return a, b


def is_std( e): # None | sorted
	if e == None: return True
	else:
		n1, n2 = e
		return n1 < n2
def sorted_nn(n1, n2):
	if n1 < n2: return n1, n2
	else: return n2, n1
def edges_to_std(edges) -> set:
	return { sorted2(e) for e in edges }
def test():
	...

if __name__ == '__main__':
	test()