#cd /Users/paul_ogier/PycharmProjects/comptesperso_dbt_sf/
#pyenv local comptesperso_dbt_sf
#python -m pip install --upgrade -r ./stagingfinanzgurutosf/requirements.txt
#python -m pip install --upgrade -e /Users/paul_ogier/PycharmProjects/comptesperso_dbt_sf/stagingfinanzgurutosf
#cd /Users/paul_ogier/PycharmProjects/comptesperso_dbt_sf/corrections
#python -m upload_corrections
cd /Users/paul_ogier/PycharmProjects/comptesperso_dbt_sf/comptesperso_dbt_sf
dbt test --select models/sources/corrections
dbt run --select models/warehouse/