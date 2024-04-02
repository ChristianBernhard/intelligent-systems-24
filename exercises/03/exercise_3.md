# Exercise Sheet 3

## Exercise 1: Fuzzy Clustering
a)
i = number of cluster centers
n = # data points
betai = cluster prototype?
d = distance function

u is the value we are trying to optimize

instead of binary clustering (traditionally, THIS or THIS class), we do fuzzy clustering:
degree to 

i)
ii)
iii)

b) U3 because it had the lowest cost

c)

## Exercise 2: Finetuning of Foundation Models
How these 2 train:
Autoregressive: predict next token on previous token sequence
Masked Transformers: mask out random words and try to predict that masked out token.


finetuning:
convetional: update all params
parameter-efficient: add and fine tune additional smaller params (freeze original weights)

methods for finetuning: supervised vs. unsupervised