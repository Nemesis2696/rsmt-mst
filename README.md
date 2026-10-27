# rsmt-mst

中国科学技术大学本科毕业论文程序，二〇二四年六月。

题目：超图最小生成树算法——平推算法和在 RSMT 问题上的应用。终稿是 `超图最小生成树算法-平推算法和在RSMT问题上的应用.pdf`。

GeoSteiner 求直角斯坦纳最小树时，后一步是在一批局部连线（FST）里选出总长最短、又能连通全部端点的一组。这些 FST 看成超边，问题就是超图最小生成树。本仓库实现的是这一步，有三种做法：简单平推、过滤、匹配。对照过 GeoSteiner。规模大约到一百多个点，比 GeoSteiner 慢。

## 文件

`rsmt2.py` 是论文程序，自身几乎纯手写。默认入口 `test()` 走简单平推，调用 `graph.py` 里的 `cacu_mst2`。过滤和匹配在同一函数后面的 `mst_test`。

`graph.py` 是超图和最小生成树。`base.py`、`plot.py`、`perf.py`、`structure.py`、`excel.py` 是当时的个人库，`rsmt2.py` 会直接或间接 import，所以按原文件放进来。

这些 `.py` 从毕业论文归档复制。算法保持原样，只把简单平推里每一步都画图改成了 `verbose_pic` 非 0 时才画。

## AI 参与

`rsmt2.py` 自身几乎纯手写。

本次做了文件挑选、复制，以及把三份小超图抄成 `examples/` 里的文本。`run_example.py` 由 AI 编写，用来读这些文本并调用原来的简单平推。`graph.py` 里简单平推每一步原来都会画图；现在只有 `verbose_pic` 非 0 时才画，计算本身没有改。本 README 由 AI 生成。

## 运行

```text
pip install -r requirements.txt
python run_example.py
```

默认跑 `examples/10-0.txt` 和 `examples/10-1.txt`。简单平推的总长应分别是 23 和 25。

`examples/50-0.txt` 是 `rsmt2.py` 里 `test()` 原来读的那一份，点更多：

```text
python run_example.py examples/50-0.txt
```

`rsmt2.py` 底部的 `test()` 仍会读取本机的 `data/rsmt`，那份数据没有放进仓库。

## 样例

`examples/` 里有三份论文实验用过的小超图，从原来的数据里抄成文本：`10-0.txt`、`10-1.txt`、`50-0.txt`。编号是 `(端点数, 种子)`。文件里的数字是原数据，文本排版是这次整理时写的。竖线前是端点编号，竖线后是这条超边的权重。
