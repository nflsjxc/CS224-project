### Description
This is the static analyze tool for python type inference. 

### Usage
First install the environment based on `requirements.txt` and `conda.yaml`
For type inference, use the instruction:
```
python main.py --repo $REPO_DIR
```
Description:
+ `$REPO_DIR`: directory to the repository to be analyzed

The results will be shown in `fused_types.json`