# Guiding the PLMs with Semantic Anchors as Intermediate Supervision: Towards Interpretable Semantic Parsing
This is the source code repository for the paper. If there is any suggestion or question, feel free to leave it as an issue here.

## Setup Environment

All required packages and versions can be found in the environment configuration file `environment.yml`, or you may simply build an identical conda environment like this:

```bash
conda env create -f environment.yml
conda activate sean
```

## Usage
### 0. Data Preparation

To download the dataset we included in our experiment, please visit their webpages listed below:

KQA Pro:    [here]()
Overnight:  [here]
WikiSQL:    [here]

### 1. Training & Inference
Simply run the script `./run_all.sh` with layer number and head number specified. You may easily adjust other parameters, such as batch size, epoch number and mask rate, by modifying the script file. The results reported in [paper](https://arxiv.org/abs/2007.06934) can be reproduced by setting the layer number to `2` and head number to `6` while keeping other parameter settings in the script unchanged.

```bash
./run_all.sh LAYER_NUM HEAD_NUM
```

### 2. Result Evaluation

Compute the BLUE-4, METEOR and ROUGE score by running the script `./score.sh` with the reference file path and the inference result path specified. 

```bash
./score.sh REFERENCE PREDICTION
```
## Performance
CoreGen significantly outperforms previous state-of-the-art models with at least 28.18% improvement on BLEU-4 score. 

| Model       | BLEU-4    | ROUGE-1   | ROUGE-2   | ROUGE-L   | METEOR    |
| ----------- | --------- | --------- | --------- | --------- | --------- |
| NMT         | 14.17     | 21.29     | 12.19     | 20.85     | 12.99     |
| NNGen       | 16.43     | 25.86     | 15.52     | 24.46     | 14.03     |
| PtrGNCMsg   | 9.78      | 23.66     | 9.61      | 23.67     | 11.41     |
| **CoreGen** | **21.06** | **32.87** | **20.17** | **30.85** | **16.53** |

In our experiment comparing vanilla Transformer and CoreGen on model’s convergence along the fine-tuning procedure, CoreGen also converges faster to achieve equivalent generation quality as the vanilla Transformer model at 25 training epochs ahead. 

More details about the performance of CoreGen are presented and analyzed in the [paper](https://arxiv.org/abs/2007.06934).
