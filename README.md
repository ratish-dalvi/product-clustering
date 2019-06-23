# Product Clustering


## Run using Docker 

## Install docker

``` 
https://docs.docker.com/docker-for-windows/install/
```

## Download docker container

``` 
https://docs.docker.com/docker-for-windows/install/
```


## Development Mode

To make changes to the program and run it locally without docker

###  Cloning the repo

``` python
git clone https://github.com/ratish-dalvi/product-clustering.git

```

###  Installation

Install anaconda, Python 3.7 version from `https://www.anaconda.com/distribution/`


### Running the program

```
python run.py --input-filepath=/Users/rdalvi/Downloads/2018Finaltry.csv --output-filepath=/Users/rdalvi/Downloads/2018Finaltry_output.csv  --importer-colname=INDIAN_IMPORTER_NAME  --product-description-colname=PRODUCT_DESCRIPTION
```

To get a description of the arguments:

```
python run.py --help
```


