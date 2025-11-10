# Fetch data from The COVID Tracking Project API
# Save JSON and CSV versions into data/raw/

mkdir -p data/raw

curl -L -o data/raw/us_daily.json       https://api.covidtracking.com/v1/us/daily.json
curl -L -o data/raw/us_daily.csv        https://api.covidtracking.com/v1/us/daily.csv
curl -L -o data/raw/us_current.json     https://api.covidtracking.com/v1/us/current.json
curl -L -o data/raw/us_current.csv      https://api.covidtracking.com/v1/us/current.csv

curl -L -o data/raw/states_daily.json   https://api.covidtracking.com/v1/states/daily.json
curl -L -o data/raw/states_daily.csv    https://api.covidtracking.com/v1/states/daily.csv
curl -L -o data/raw/states_current.json https://api.covidtracking.com/v1/states/current.json
curl -L -o data/raw/states_current.csv  https://api.covidtracking.com/v1/states/current.csv

curl -L -o data/raw/states_info.json    https://api.covidtracking.com/v1/states/info.json
curl -L -o data/raw/states_info.csv     https://api.covidtracking.com/v1/states/info.csv

echo "Files saved in data/raw/"
