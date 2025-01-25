Database Population Guide


---Important: Every time you run the app, the database will be populated with data from the CSV files. This means that if you run the app multiple times, the database will be populated multiple times, which could lead to duplicates or unintended data changes.

Production Consideration:

In a production environment, it is recommended not to include the population logic in the main app.
Instead, you should populate the database on demand by running a local script that populates the database only once or when necessary.
After the initial population setup, remove the population part from the app to prevent accidental re-population.
Steps to Handle Database Population in Production:
Initial Setup:
When setting up the application for the first time, you can let the app populate the database using the built-in population logic.
Post-Setup:
After the initial database setup, remove the population code from the app.
On-Demand Population:
If you ever need to populate the database with data (after a reset or to add new data), run a separate local script to do this in the production database.
This ensures that your app's main logic does not accidentally overwrite or duplicate data.