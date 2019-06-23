# Product Clustering


## Run on remote machine

I'm assuming at this point you have access to remote machine. Let's say it has an alias `foo`

Copy the input file containing your product info into the remote machine
```
scp your-local-path/input.csv foo:/home/ubuntu/product-clustering/build/
```

ssh into the machine.
```
ssh foo
```

Run clustering
```
docker run -v ~/product-clustering/build:/build -it product_clustering python run.py --input-filepath=/build/input.csv --output-filepath=/build/output.csv  --importer-colname=INDIAN_IMPORTER_NAME  --product-description-colname=PRODUCT_DESCRIPTION
```

Copy the output to your local machine.
Run this command on your local machine

```
scp foo:/home/ubuntu/product-clustering/build/output.csv your-local-path/
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


