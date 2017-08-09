import os
import json
import subprocess
import sys

python_path = sys.executable

def dependencies():
    subprocess.call('pip install -U requests', shell=True)
    subprocess.call('{} margin.py'.format(python_path, shell=True))
    quit()

if (subprocess.call('pip install requests', shell=True)):
    subprocess.call('{} margin.py'.format(python_path, shell=True))
    quit()

import requests

os.system('cls')

########################################################################################################
#   SUMMARY CLASS
########################################################################################################

class Summary(object) :
    """ Summary object used to fetch data with the RuneScape API. Contains the following attributes.

    Attrributes:
        summaryDict: Dictionary pulled directly from the API
        idDict: Dictionary containing the id list pulled from the summaryDict attribute. """

    def __init__(self, masterList) :
        """ Return a Summary Object with the attributes as defined above. """
        r = requests.get(masterList)
        self.summaryDict = r.json()
        self.idDict = {}
        for key in self.summaryDict:
            self.idDict[self.summaryDict[key]["name"].lower()] = self.summaryDict[key]["id"]
    
    def queryName(self, itemName) :
        """ Queries the Summary object for the given item name. Returns the a string containing the 
        item ID if the item is found, and returns a 'None' if it is not. """
        if itemName in self.idDict :
            itemID = self.idDict['{}'.lower().format(itemName)]
            return itemID
        else :
            return None


########################################################################################################
#   TRANSACTION DATA CLASS
########################################################################################################

class TransactionData(object) :
    """ Returns a TransactionData Object which can be used to fetech data with the API and process the
    result. It contains the following attributes. 

    Attributes:
        transactionHistory: A Dict object containing all the transaction history for the last hour as
            recieved by the API.
        activeHistory: A Dict object containing the 100 most recent transactions.   ! 
        buyingHistory: A List object containing the active buying history.          !
        sellingHistory: A List object containing the active selling history.        !
        averageBuying: An Int containing the average buying price.                  !
        averageSelling: An Int containing the average selling price."""             

    def __init__(self, baseURL, itemID) :
        """ Returns a TransactionData object with the above attributes. """
        transactionURL = baseURL.format(itemID)
        r = requests.get(transactionURL)
        self.transactionHistory = r.json()

    def getActiveHistory(self) :
        """ Returns a Dict object containing the 100 most recent transactions. """
        activeHistory = list(self.transactionHistory[-101:-1])
        return activeHistory

    def getBuyingHistory(self, activeHistory) :
        """ Returns a integer List object containing the most recent buying history. """
        buyingHistoryStr = []
        # Get strings
        for i in range(len(activeHistory)) :
            if 'buyingPrice' in activeHistory[i] :
                buyingHistoryStr.append(activeHistory[i]['buyingPrice'])
        # Convert to ints
        buyingHistoryInt = []
        buyingHistoryInt = [int(numeric_string) for numeric_string in buyingHistoryStr]

        return buyingHistoryInt

    def getSellingHistory(self, activeHistory) :
        """ Returns a integer List object containing the most recent selling history. """
        sellingHistoryStr = []
        # Get strings
        for i in range(len(activeHistory)) :
            if 'sellingPrice' in activeHistory[i] :
                sellingHistoryStr.append(activeHistory[i]['sellingPrice'])
        # Convert to ints
        sellingHistoryInt = []
        sellingHistoryInt = [int(numeric_string) for numeric_string in sellingHistoryStr]

        return sellingHistoryInt

    def getAvgBuying(self, buyingHistoryInt) :
        """ Returns the average buying price. """
        avgBuy = sum(buyingHistoryInt) / len(buyingHistoryInt)
        return avgBuy

    def getAvgSelling(self, sellingHistoryInt) :
        """ Returns the average selling price. """
        avgSell = sum(sellingHistoryInt) / len(sellingHistoryInt)
        return avgSell

    def getResult(self, avgBuy, avgSell) :
        """ Returns a float containing the margin. """
        margin = avgBuy - avgSell
        return margin


########################################################################################################
#   MAIN
########################################################################################################

masterListURL = 'https://rsbuddy.com/exchange/summary.json'
transactionListURL = 'https://api.rsbuddy.com/grandExchange?i={}&a=graph&g=1'

summary = Summary(masterListURL)

os.system('cls')

print(' --------------------------------------')
print('|Old School Runescape Margin Calculator|')
print(' --------------------------------------\n')

while(True) :

    itemName = input('Item name: ')
    itemID = summary.queryName(itemName)

    if itemID == None :
        print('Not a valid item, try again boss\n\n')
        continue
    
    transactionData = TransactionData(transactionListURL, itemID)
    activeHistory = transactionData.getActiveHistory()
    buyingHistory = transactionData.getBuyingHistory(activeHistory)
    sellingHistory = transactionData.getSellingHistory(activeHistory)
    avgBuy = transactionData.getAvgBuying(buyingHistory)
    avgSell = transactionData.getAvgSelling(sellingHistory)
    margin = transactionData.getResult(avgBuy, avgSell)


    print('\nItem ID: {}'.format(itemID))
    print('Your buying price is: {:,.2f} gp'.format(avgSell))
    print('Your selling price is: {:,.2f} gp'.format(avgBuy))
    print('Profit margin is: {:,.2f} gp'.format(margin))

    print('\n')
    
