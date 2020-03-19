# COVID-19 To Text Corpus

[Kaggle](https://www.kaggle.com/) has provided an excelent [data source](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) for the COVID-19 courtesy of [AI2](https://allenai.org/)
The purpose of this repo is to convert it from the given format into the normal text corpus format.
I.E. one document per file, one sentence per line, pargraphs have a blank line between them.

# Prerequisites

The following packages need to be installed.
I recommend using [Chocolatey](https://chocolatey.org/install).

* [7-zip](https://www.7-zip.org/)
* [Python](https://www.python.org/downloads/)

  
```{ps1}
if('Unrestricted' -ne (Get-ExecutionPolicy)) { Set-ExecutionPolicy Bypass -Scope Process -Force }
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
refreshenv

choco install 7zip.install -y
choco install python3 -y
```

# Modules

All scripts have been tested on Python 3.8.2.
The below modules are need to run the scripts.
The scripts were tested on the noted versions, so YMMV.
**Note**: not all modules are required for all scripts.
If this it the first time running the scripts, the modules will need to be installed.
They can be installed by navigating to the `~/code` folder, then using the below code.

* nltk 3.4.5
* progressbar2 3.47.0

```{shell}
pip install -r requirments.txt
python -c "import nltk;nltk.download('punkt')"
```

# Steps

The below document describes how to recreate the text corpus.
It assumes that a particular path structure will be used, but the commands can be modified to target a different directory structure without changing the code.
I am choosing the `d:/covid19` directory because my d drive is big enough to hold everything.

1. Clone this repo then open a shell to the `~/code` directory.
2. Retrieve the dataset _by hand_.
   Click on the [download](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download) link, saving the file to a know location.   
3. Extract the data in-place with no folder structure.
   The `e` switch flattens the extract so the custom code does not need to recursivaly search the folder structure.
```{shell}
"C:/Program Files/7-Zip/7z.exe" e -od:/covid19/raw "d:/covid19/*.zip"
```
4. [Extract](./code/extract_metadata.py) the meta-data.
   This will create a single `metadata.csv` containing some useful information.
   In general this would be used as part of segementation or as part of a MANOVA.
```{shell}
python extract_metadata.py -in d:/covid19/raw -out d:/covid19/metadata.csv
```
5. [Convert](./code/convert_to_corpus.py) the raw JSON files into the nomal folder corpus format.
   This will create a text corpus folder at the location I.E. `./corpus` containing 2 sub folders, one for the abstract and one for the body.
   Some of the files provide by Kaggle are not full text articles I.E. empty abstract or body.
   These _incomplete_ files are filtered out of the final folders and noted in `error.csv`
```{shell}
python convert_to_corpus.py -in d:/covid19/raw -out d:/covid19/corpus
```