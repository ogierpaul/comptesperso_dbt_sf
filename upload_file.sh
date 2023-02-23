source ~/.virtualenvs/cicd/bin/activate
python -m pip install --upgrade -r ./stagingfinanzgurutosf/requirements.txt
python -m pip install --upgrade -e ./stagingfinanzgurutosf
python -m upload_file