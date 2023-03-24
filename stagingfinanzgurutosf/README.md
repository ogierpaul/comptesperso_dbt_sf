# Staging module
* Find the latest excel export from the app on the local desktop
* Transform the excel export to a pandas dataframe
* Upload the dataframe to Snowflake in the staging schema

## Pre-requisites
* Python packages in `requirements.txt`
    * Uses the `upload2sf` package (documentation [here](https://github.com/ogierpaul/upload2sf) )
* Snowflake credentials in `~/.dbt/profiles.yml` or as environment variable (see the upload2sf documentation for more info)
* The excel export from the app on the local desktop

## How to run the script
* Create and activate a virtual environment (For example with `pyenv` or `virtualenv`)
* Install the `requirements.txt` file with `pip install -r requirements.txt`
* Run the script `upload_latest_excel_to_sf_main.sh` in your terminal

## How to run the tests
* Create and activate a virtual environment (For example with `pyenv` or `virtualenv`)
* Install the `requirements.txt` file with `pip install -r requirements.txt`
* Run the tests with `pytest`

