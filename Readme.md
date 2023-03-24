# Comptesperso with dbt and snowflake
* Create my personal expenses reports with the help of python, DBT and Snowflake
* Input data is one excel export from the app FinanzGuru
* Output is a set of tables in Snowflake showing my expenses by category

## How to use it
### Pre-requisites
* Having a FinanzGuru plus account
* Having a Snowflake account
* DBT
* Python: see the `requirements.txt` file

### Snowflake configuration
* The snowflake configuration can be stored in the `dbt_project.yml` file
* For more details see the [upload2sf](https://github.com/ogierpaul/upload2sf) tutorial

### Steps
* Export your data from FinanzGuru
* Follow the steps in `stagingfinanzgurutosf/README.md`
* Run dbt with `dbt build` or `dbt run`

### Disclaimer
* This is a personal project