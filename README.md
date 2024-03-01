Whenever we want to deploy to heroku we can sync the pyproject / requirements with this: 

poetry export -f requirements.txt --dev --output requirements.txt

run that




to run for dev: 

source .venv/bin/activate


uvicorn app.app:app --reload




