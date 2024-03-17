# CSFarm
#### Video Demo: https://youtu.be/lpvZmMoYlJY

#### Description:

This repo contains a web application designed to streamline the management of dairy farms by providing a comprehensive platform for tracking productivity metrics. This project was developed as the final assignment for [CS50x](https://cs50.harvard.edu/x/2024/), a renowned introductory course to computer science offered by [Harvard University](https://www.harvard.edu/).

The application enables users to register, create and manage farms, record data on animal productivity, and analyze historical trends through intuitive web interfaces.

##### Files and functionality:

1. **app.py:** This file serves as the main entry point for the Flask application. It defines the routes and logic for handling user requests, rendering HTML templates, and interacting with the database. Key functionalities include user authentication, farm creation, animal management, milk productivity recording, and analytics display.

2. **helpers.py:** Within this file reside various helper functions utilized throughout the application to streamline Flask interactions and perform data manipulation tasks. These functions enhance code readability and maintainability. By encapsulating common operations, such as user authentication into reusable functions, the application achieves a higher level of modularity and extensibility.

1. **models.py**: This file contains Class definitions for the Animals, Farm and Production, which encapsulate the logic and methods that can be achieved withon the database. This module's methods can be used to query the database for the current user and return the list of Animals, Farms or Production, with a known data structure.

2. **database.py:** This file contains various helper functions used to get generic interactions with the database.

3. **templates/:** This directory contains HTML templates utilized by Flask to render dynamic web pages. Each template corresponds to a specific page or functionality within the application. For instance, the `index.html` template renders the home page, displaying farm statistics and relevant information. Similarly, templates such as `animals.html`, `milk.html`, and `analytics.html` handle the presentation of animal management, milk productivity recording, and analytics functionalities, respectively.

4. **static/:** Within this directory, static assets such as CSS stylesheets, JavaScript files, and image resources are stored. These assets contribute to the visual and interactive aspects of the web application, enhancing user experience and interface design. By separating static assets from dynamic content, the application maintains a clean and organized directory structure, facilitating ease of maintenance and scalability.

##### Design choices:

1. For the backend, the app uses [Flask](https://flask.palletsprojects.com/en/3.0.x/) and records the data from the users in a SQL (sqlite) database. The decision to use Flask for developing this web application was motivated by its lightweight and modular nature. Flask offers a minimalistic yet powerful toolkit for building web applications, making it well-suited for projects of varying complexity. Additionally, Flask's extensive documentation and vibrant community support provided invaluable resources for overcoming challenges and implementing best practices throughout the development process.


2. For data storage and retrieval, SQLite was chosen as the backend database management system. SQLite's simplicity, efficiency, and seamless integration with Flask made it an ideal choice for this project. Despite its lightweight footprint, SQLite offers robust functionality, supporting the relational database model necessary for managing complex data structures such as farms, animals, and production records. Furthermore, SQLite's file-based architecture simplifies deployment and maintenance, eliminating the need for complex database setup procedures. The database was designed to have 4 Tables: `Users`, `Farms`, `Animals` and `Production`.



3. `Users` contains the information of all users registered on the web app; `Farms` contains the definition of Farms, and relates each Farm with a User Id. Similarly, `Animals` contains every animal added by the users and each animal is related to a Farm Id and User Id. Lastly, `Production` holds the records of the milk production by each animal on each date, and is related to `Animals` by Animal Id.



4. For the front end, the app uses pre-rendered (Jinja) HTML templates mostly. To add some interactivity, the app uses [HTMX](https://htmx.org/) attributes; for example to add asynchronous request without re-rendering the whole page when a new Animal is added to the Animals page.

For the charts, the app uses javascript library [D3.js](https://d3js.org/) to help with the visualization of SVG graphics.

How to start:
```sh
python -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
flask run --debug
```

##### Features:

- Tabs: Farm, Animals, Milk, History
- Someone can create a new account and add a new farm with some basic information
- Add a new cow information with her information: Name, age, parents, siblings
- Add daily production of milk for each cow
- Visualize the production with different filters

