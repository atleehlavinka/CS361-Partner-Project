import json
import os
import shutil
import time
from datetime import datetime

def updateTotals(salesList, transactionTotal):
    with open('totals.json', 'r+') as file:
        file_data = json.load(file)
        i = 0
        for itemI in file_data["totalAmounts"]:
            for itemJ in salesList:
                if itemI["name"] == itemJ:
                    file_data["totalAmounts"][i]["total"] = round(file_data["totalAmounts"][i]["total"] + salesList[itemJ], 2)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
            i += 1
            
    with open('totals.json', 'r+') as file:
        file_data = json.load(file)
        file_data["totalRevenue"] = file_data["totalRevenue"] + transactionTotal
        file.seek(0)
        json.dump(file_data, file, indent=4)

while True:
    processingFolder = os.getcwd() + "/processing"
    archiveFolder = os.getcwd() + "/archive"
    processingDirectory = os.listdir(processingFolder)
    archiveDirectory = os.listdir(archiveFolder)
    salesList = {}
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")

    if len(processingDirectory) == 0:
        print(currentTime, "- No files found")
    else:
        print(currentTime, "- File found. Now processing...")
        for file in processingDirectory:
            total = open('processing/' + file)
            totalData = json.load(total)
            transactionTotal = totalData["transaction_total"]
            for item in totalData["items_sold"]:
                salesList[item["name"]] = item["qty_sold"]
        total.close()
        updateTotals(salesList, transactionTotal)

        for file in processingDirectory:
            sourceFile = os.path.join(processingFolder, file)
            fileDestination = os.path.join(archiveFolder, file)
            shutil.move(sourceFile, fileDestination)

    time.sleep(10)
