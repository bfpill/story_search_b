Whenever we want to deploy to heroku we can sync the pyproject / requirements with this: 

poetry export -f requirements.txt --dev --output requirements.txt

run that

