The micro.py microservice will run consistently in the background looking for new files to drop into the processing folder. The microservice will read through the sales data from a transaction and grab the total cost plus the items and their quantities. These are then passed along to be added to the totals.json file. This file can be used to grab the total sales data.

STEPS:
1. Run micro.py.
2. Route transactions in JSON form from the main.py program to the processing folder.
3. Allow time for the microservice to update the totals.json file.
4. the sales JSON file will be moved to the archive folder.
4. Use the totals.json file to output the total number of items sold, and total revenue.

5. ![image](https://github.com/atleehlavinka/CS361-Partner-Project/assets/81734135/c88d31e9-9f27-4a16-afd6-05427cbdf261)
