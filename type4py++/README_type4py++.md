# Type4py++ : train our model

## Description

Our tool type4py++ is a learning based developed based on type4py. 

## Dataset

For Type4Py, we use the **ManyTypes4Py** dataset. You can download the latest version of the dataset [here](https://doi.org/10.5281/zenodo.4044635).
You should download the dataset and unzip it. 

the file tree:

├── CHANGELOG.md
├── MT4Py_VTHs.csv
├── ManyTypes4PyDataset.spec
├── README.md
├── dataset_split.csv
├── duplicate_files.txt
├── mypy-dependents-by-stars.json
**├── processed_projects_clean**
**├── processed_projects_complete**
└── type_checked_files.txt

You can select one dataset (processed_projects_clean or processed_projects_complete) to train and test.

## Installation Guide

### Requirements

Here are the recommended system requirements for training Type4Py on the MT4Py dataset:
- Linux-based OS (Ubuntu 18.04 or newer)
- Python 3.6 or newer
- A high-end NVIDIA GPU (w/ at least 8GB of VRAM)
- A CPU with 16 threads or higher (w/ at least 64GB of RAM)

### Quick Install

The conda environment we used are stored in `type4py++.yaml`

```
cd type4py 
pip install .
```

## Usage Guide

Follow the below steps to train and evaluate the learning-based model.

We **highly recommend** you to use ManyTypes4Py dataset, as our experiments are conducted on it.

### 1. Extraction

If you download dataset from [dataset](# Dataset), you don't need this step. 

```
$ type4py extract --c $DATA_PATH --o $OUTPUT_DIR --d $DUP_FILES --w $CORES
```
Description:
- `$DATA_PATH`: The path to the Python corpus or dataset.
- `$OUTPUT_DIR`: The path to store processed projects.
- `$DUP_FILES`: The path to the duplicate files, i.e., the `*.jsonl.gz` file produced by CD4Py. [Optional]
- `$CORES`: Number of CPU cores to use for processing projects.

### 2. Preprocessing

You should copy the `data dir`(either processed_projects_clean or processed_projects_complete)(selected in [dataset](# Dataset)) and other files in download files to `type4py/data`, then rename it as `processed_projects` 

The directory should look like this: 

```
$ type4py preprocess --o $OUTPUT_DIR
```
Description:
- `$OUTPUT_DIR`: The path that was used in the first step to store processed projects. For the MT4Py dataset, use the directory in which the dataset is extracted.

it will produce file like `_ml_param_test.csv` in `./data`, data structure is :

```csv
file,func_name,func_descr,arg_name,arg_type,arg_comment,other_args,arg_occur,aval_types,arg_type_enc_all,param_aval_enc
```

### 3. Vectorizing

```
$ type4py vectorize --o $OUTPUT_DIR
```
Description:
- `$OUTPUT_DIR`: The path that was used in the previous step to store processed projects.

it will produce `vectors` file dir in `./data`

### 4. Learning

```
$ type4py learn --o $OUTPUT_DIR --c --p $PARAM_FILE --m $MODEL_TYPE
```
Description:
- `$OUTPUT_DIR`: The path that was used in the previous step to store processed projects.
- `--c`: Trains the complete model. Use `type4py learn -h` to see other configurations.
- `--p $PARAM_FILE`: The path to user-provided hyper-parameters for the model. See [this](https://github.com/saltudelft/type4py/blob/main/type4py/model_params.json) file as an example. [Optional]
- `--m $MODEL_TYPE: `select encoder model : (LSTM,transformer,GRU,transformer_attentionFusion,LSTM_max_pooling,GRU_max_pooling) [Optional]
- `--r_c`: it will load checkpoint and restart training. [Optional]

it will produce file like `type4py_complete_LSTM_model.py` in `./data`

### 5. Testing

```
$ type4py predict --o $OUTPUT_DIR --c
```

Description:
- `$OUTPUT_DIR`: The path that was used in the first step to store processed projects.
- `--c`: Predicts using the complete model. Use `type4py predict -h` to see other configurations.
- `--r_c`: it will read cluster result and restart predict. [Optional]
- `--m $MODEL_TYPE: `select encoder model : (LSTM,transformer,GRU,transformer_attentionFusion,LSTM_max_pooling,GRU_max_pooling) [Optional]

it will produce cluster result and prediction result in `./data`

the data structure in `prediction.json` like :

```python
{
        "original_type": "logging.Logger", # label
        "predictions": [
            [
                "logging.Logger",
                0.9999999999999998
            ] # prediction label and logit
        ],
        "task": "Parameter",
        "is_parametric": false
    }
```

 The predictions are in the same order as in [.csv](# Preprocessing), so you can index the file and variable names for this prediction

### 6. Evaluating

```
$ type4py eval --o $OUTPUT_DIR --t c --tp 1
```

Description:
- `$OUTPUT_DIR`: The path that was used in the first step to store processed projects.
- `--t`: Evaluates the model considering different prediction tasks. E.g., `--t c` considers all predictions tasks,
  i.e., parameters, return, and variables. [Default: c]
- `--tp 1`: Considers Top-10 predictions for evaluation. For this argument, You can choose a positive integer between 1 and 10. [Default: 10]

Use `type4py eval -h` to see other options.
