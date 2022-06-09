# Empathetic Dialogues emotion classificaition

NLP final project.  
## Re-present submission
Follow below steps to re-present submission:  
1. install requirements first!
    ```
    pip install -r requirements.txt
    ```  
2. Download the [trained model](https://drive.google.com/drive/folders/1OrUys926809LzPYX3ulLLAmNj07Dezgr?usp=sharing) !  
3. place config.json and pytorch_model.bin to `best_model` folder.  
(or you can name this folder by yourself, but you need to modify `model_path` in [config.yaml](config.yaml) )
4. place `fixed_train.csv`, `fixed_valid.csv` and `fixed_test.csv` in `data` folder. (Don't change file name!!!)  
5. run [ed_data_extract.py](ed_data_extract.py) to pre-process csv file.  
check bellow parameter in [config.yaml](config.yaml):  
`train_file_path`: set as "`data/empathetic_dialogues/train.csv`"  
`valid_file_path`: set as"`data/empathetic_dialogues/valid.csv`"  
`test_file_path`: set as "`data/empathetic_dialogues/test.csv`"  
 `original_test_file_path`: set as "`data/fixed_test.csv`", where original testing file is.  
6. Open [ed_eval.ipynb](ed_eval.ipynb) and follow the guide to create submission.

## Introduction
### [ed_classification.ipynb](ed_classification.ipynb)
- used to train model, need to set [config.yaml](config.yaml) first.
### [ed_eval.ipynb](ed_eval.ipynb)
- just like `ed_classification.ipynb`, but only for testing
- follow guides to re-present submission 
### [ed_data_extract.py](ed_data_extract.py)
- extract data from original data
### [EDA.ipynb](EDA.ipynb)
- EDA for extracted data, only have random deletion and random swap
### [everythingDataset.py](everythingDataset.py)
- custom dataset
### [everythingDataset2.py](everythingDataset2.py)
- another custom dataset
### [analysis.ipynb](analysis.ipynb)
- analyze data: check distribution of training data