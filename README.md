# Sample ETL Data Job

This is a study project to build a ETL job AWS Lambda.

## Pre-requisites

Setting up AWS RDS/or database is out of scope of this sample, but we need one set up to dump data into it from our ETL job. Once you have it set up and configured, you will need to add a enviroment variable, DB_CONN with a swlalchemy like url with all credential, cryptographed.

### Redshift cluster endpoint

`<cluster_name>.xxxxxxxxxxxx.<region>.redshift.amazonaws.com:<port>`

### DB Connection String

`postgres://<username>:<password>@<hostname>:<port>/<db_name>`
where `<hostname>:<port>` is the cluster endpoint

## Install dependencies

`$ pip install -r requirements.txt`

## Run locally

`sls invoke local -f etlSample`

## Run

`sls invoke -f etlSample`
