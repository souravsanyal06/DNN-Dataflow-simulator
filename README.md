# DNN-Dataflow-simulator
 Implementation of Input Stationary, Weight Stationary and Output Stationary dataflow for given neural network on a tiled architecture.

Two variants are modelled.

## 1) Dense dataflow - 
data structures are fetched from DRAM independent of their values
## 2) Sparse dataflow -
Two types -
a) Input Dependent Weight Zero - Inputs are fetched and if they are zero, respective weights are not fetched
b) Weight Dependent Input Zero - Weights are fetched and if they are zero, respective inputs are not fetched

Calculates reduction in total DRAM transfers for sparse dataflow w.r.t dense dataflow


In root directory, create an empty directory called results:
mkdir results

To run:
Go to src/ directory

python main.py -d cifar10 -m resnet18 -o t.txt





 
