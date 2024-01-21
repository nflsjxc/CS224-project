## Requirements

Python >= 3.9

Linux

## Install

Run the following command in the root directory:

```sh
pip install -r requirements.txt
```

## Usage

1. Download the dataset from the [release](https://github.com/JohnnyPeng18/TypeGen/releases/tag/data) and unzip it

2. TypeGen relies on the OpenAI services, so fill your OpenAI API keys in `config.py` first.
   
3. Run TypeGen on the dataset

```
python typegen/typegen.py -s data -r predictions.json 
```

## Evaluate

**For generative approaches such as TypeGen:**

```
python typegen/evaluate.py -s predictions.json -t data/testset_transformed.json -m -c
```

Remove the option `-c` if COT prompt is not used.

