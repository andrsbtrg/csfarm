# CSFarm
#### Video Demo: https://youtu.be/lpvZmMoYlJY

#### Description:

This repo contains a web application made to track productivity of dairy farms. It was made as the final project of CS50x. 

The app lets user's register with their Name, register a new Farm in a specific Country and Location, and then register Animals and their productivity on a daily basis. The app has four main pages:

- `/` -> Home: See the current farm name and general statistics.
- `/Animals` -> See the current animals in the farm and add new ones.
- `/Milk` -> Add new milk productivity readings each day.
- `/Analytics` -> See the past days productivity with charts and tables.

For the backend, the app uses [Flask](https://flask.palletsprojects.com/en/3.0.x/) and records the data from the users in a SQL (sqlite) database. For communicating with the database, the repo has some helper methods located in `helpers.py`.

The database was designed to have 4 Tables: `Users`, `Farms`, `Animals` and `Production`. 

`Users` contains the information of all users registered on the web app; `Farms` contains the definition of Farms, and relates each Farm with a User Id. Similarly, `Animals` contains every animal added by the users and each animal is related to a Farm Id and User Id. Lastly, `Production` holds the records of the milk production by each animal on each date, and is related to `Animals` by Animal Id.

For the front end, the app uses pre-rendered (Jinja) HTML templates mostly. To add some interactivity, the app uses [HTMX](https://htmx.org/) attributes; for example to add asynchronous request without re-rendering the whole page when a new Animal is added to the Animals page.
For the charts, the app uses javascript library [D3.js](https://d3js.org/) to help with the visualization of SVG graphics.

How to start:
```sh
python -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
flask run --debug
```

#### Features:

- Tabs: Farm, Animals, Milk, History
- Someone can create a new account and add a new farm with some basic information
- Add a new cow information with her information: Name, age, parents, siblings
- Add daily production of milk for each cow
- Visualize the production with different filters

