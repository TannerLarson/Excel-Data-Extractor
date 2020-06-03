__author__ = 'Tanner Larson'

import sys
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os.path
from pathlib import Path
import xlsxwriter

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import QApplication, QPushButton, QComboBox, QRadioButton
from PySide2.QtCore import Slot, QUrl, QObject, Signal, Property, QStringListModel


# Model for my output is global so both Bridge and main can print to it
model = QStringListModel()
model.setStringList(["Please enter the details of your search",
"", "Keep in mind:", '',
"Unspecified categories will be treated as if all were selected.",
"More files will proportionally increase the execute time",
"Output may not be recent if excel paths are not in decending order",
"The solution category is far from 100% accurate, don't rely a lot on it"])


def getParentDir():

    if getattr(sys, 'frozen' ,False): # For the executable
        print('frozen')
        parentDir = Path(sys.executable).parent
    else:
        print('Not frozen')
        parentDir =  Path(__file__).parent

    return parentDir



class Bridge(QObject):


    def __init__(self, parent=None):
        super().__init__()
        self.data = {}



    @Slot(str, str, str, str, str, str, int, str, bool, bool, bool, bool,\
            bool, bool, bool, bool, bool, bool)
    def setData(self, region, vertical, vendor, solution, sort, outType, \
            numLines, xlFiles, isOptane, isNand, isClient, isDC, isIoT,  \
            wSubmitted, wApproved, pending, lost, cancelled):
        self.data['region'] = region
        self.data['vertical'] = vertical
        self.data['vendor'] = vendor
        self.data['solution'] = solution
        self.data['sort'] = sort
        self.data['outType'] = outType
        self.data['numLines'] = numLines
        xlFiles = xlFiles.replace('\\', '/').replace('\"', '')
        xlFileList = xlFiles.split('\n')
        self.data['xlFiles'] = xlFileList
        self.data['driveType'] = {}
        self.data['driveType']['optane'] = isOptane
        self.data['driveType']['nand'] = isNand
        self.data['segment'] = {}
        self.data['segment']['client'] = isClient
        self.data['segment']['dc'] = isDC
        self.data['segment']['iot'] = isIoT
        self.data['status'] = {}
        self.data['status']['Win Submitted'] = wSubmitted
        self.data['status']['Win Approved'] = wApproved
        self.data['status']['Pending'] = pending
        self.data['status']['Lost'] = lost
        self.data['status']['Cancelled'] = cancelled



    def getSolution(self, df):
        # TODO: These keywords reflect organization on Nino's excel.  This could use a serious overhaul
        keyWords = {
            'vSAN': ['vsan', 'vmware', 'vxrail'],
            'Ceph': 'ceph',
            'IMDT': 'imdt',
            'Database': ['s2d', 'ms sql', 'spark', 'bigdata', 'a2', 'oracle', 'hana', 'analytics', 'big data'],
            'Hyperflex': ['hyperflex', 'hpx', 'hx'],
            'HPC': 'hpc',
            'EDA': 'eda',
            'Cloud Storage': ['cloud storage', 'custom', 'cdn'],
            'Nutanix': 'nutanix',
            'CAS/Caching': ['caching', 'swap'],
        } # <---- AI not included because the string "ai" is very common and all instances of 'AI' were submitted manually in Nino's sheet

        def calculateSolution(row):
            for key, value in keyWords.items():
                if isinstance(value, list):
                    for definition in value:
                        # Order of if statements matter here
                        if definition in str(row['Solution Detail']).lower():
                            return key
                        if definition in str(row['Opportunity Name']).lower():
                            return key
                        if definition in str(row['Description']).lower():
                            return key
                else:
                    # Order of if statements matter here
                    if definition in str(row['Solution Detail']).lower():
                        return key
                    if definition in str(row['Opportunity Name']).lower():
                        return key
                    if definition in str(row['Description']).lower():
                        return key
            return 'Unknown'

        listSolutions = []
        for index, row in df.iterrows():
            listSolutions.append(calculateSolution(row))
        df['Solution'] = listSolutions
        return df



    # Prints all values selected in output box
    # This is mostly for easier debugging

    @Slot()
    def printValues(self):
        list = []
        for key in self.data:
            list.append(str(key) + " : " + str(self.data[key]))




    # Called when submit button is pressed
    # Filters and sorts data
    @Slot()
    def getData(self):
        # Check if path exists
        for path in reversed(self.data['xlFiles']):
            # Ignore whitespace
            if path == '' or path.isspace():
                self.data['xlFiles'].remove(path)
                continue
            if not os.path.isfile(path):
                model.setStringList(["File doesn't exist"])
                return

        # Read in excel documents and compile into one data frame
        df = pd.read_excel(self.data['xlFiles'][0], 'Raw Data ')
        df['sheet'] = self.data['xlFiles'][0]
        for i in range(0, len(self.data['xlFiles'])):
            if i == 0:
                continue
            dfNew = pd.read_excel(self.data['xlFiles'][i], 'Raw Data ')
            dfNew['sheet'] = self.data['xlFiles'][i] # Add column to keep track of sheet
            df = pd.concat([df, dfNew], join='inner')


        # Clean up duplicates
        df = df.drop_duplicates(subset=['Opportunity Name', 'Opportunity ID', 'Description'])

        # Check if Nino's excel sheet was used
        if not 'Quarter' in df:
            # Add a solution column
            df = self.getSolution(df)


        # Apply relevant filters
        if self.data['region'] != 'Ignore':
            df = df[(df['Opportunity Region'] == self.data['region'])]

        if self.data['vertical'] != 'Ignore':
            df = df[(df['Vertical Market'] == self.data['vertical'])]

        if self.data['vendor'] != 'Ignore':
            if self.data['vendor'] == 'Blank':
                df = df[(pd.isna(df['Vendor Group']))]
            else:
                df = df[(df['Vendor Group'] == self.data['vendor'])]

        if self.data['solution'] != 'Ignore':   # NOTE: This will work only with Nino's taskforce
            if self.data['vendor'] == 'Blank':
                df = df[(pd.isna(df['Solution']))]
            else:
                df = df[(df['Solution'] == self.data['solution'])]

        if self.data['driveType']['optane']:
            optane = ['Optane Client', 'Optane Datacenter']
            df = df[df['KPI Product Group'].isin(optane)]

        if self.data['driveType']['nand']:
            nand = ['NAND', 'NAND Datacenter', 'NAND Ruler']
            df = df[df['KPI Product Group'].isin(nand)]

        segment = []
        filterSegment = False
        if self.data['segment']['client']:
            segment.append('NSG-Client')
            filterSegment = True

        if self.data['segment']['dc']:
            segment.append('NSG-Data Center')
            filterSegment = True

        if self.data['segment']['iot']:
            segment.append('NSG-IoT')
            filterSegment = True

        if filterSegment:
            df = df[df['BU Product Segment'].isin(segment)]

        status = []
        filterStatus = False
        for key in self.data['status']:
            if self.data['status'][key]:
                status.append(key)
                filterStatus = True

        if filterStatus:
            df = df[df['Status'].isin(status)]


        # Sort data by self.data['sort']
        if self.data['sort'] == 'Total Price':
            df = df.sort_values(by=['KPI - Total Price'], ascending=False)

        elif self.data['sort'] == 'Quantity':
            df = df.sort_values(by=['KPI - Quantity'], ascending=False)

        else:
            print("Could not find sort string")


        # Check if df is empty
        if df.empty:
            model.setStringList(['No opportunities found'])
            return


        # Include only the amount of rows specified
        df = df.head(self.data['numLines'])


        # Export depending on selected output type
        if self.data['outType'] == 'Text':
            # Format Data
            out = []
            count = 1
            for i, row in df.iterrows():
                toAdd = [
                '------------{}------------'.format(count), '',
                'Op Name:', row['Opportunity Name'], '',
                'Excel Sheet:', row['sheet'], '',
                'Status:', row['Status'], '',
                'Region:', row['Opportunity Region'], '',
                'ID:', row['Opportunity ID'], '',
                'Stage:', row['Stage'], '',
                'Description:', row['Description'], '',
                'Owner:', row['Opportunity Owner'], '',
                'Account Name:', row['Account Name'], '',
                'Country:', row['Account Country'], '',
                'Solution:', row['Solution'], '',
                'Vertical Market:', row['Vertical Market'], '',
                'Segment:', row['BU Product Segment'], '',
                'Series:', row['Product Series'], '',
                'Product Name:', row['Product Name'], '',
                'Sales Group:', row['Sales Group'], '',
                'Vendor:', row['Vendor Group'], '',
                'Created Date:', row['Created Date'], '',
                'KPI Date:', row['KPI - Date'], '',
                'Decision Date:', row['Decision Date'],
                'Last Activity Date:', row['Last Activity Date'], '',
                'Probability (%):', row['Probability (%)'], '',
                'Quantity:', '{:,}'.format(row['KPI - Quantity']), '',
                'List Price:', '$ {:,}'.format(row['List Price']), '',
                'Total Price:', '$ {:,}'.format(row['KPI - Total Price']), ''
                ]
                out.extend(map(str, toAdd))
                count += 1
            model.setStringList(out)

        elif self.data['outType'] == '.xlsx':
            xlPath = Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) / 'searchResults.xlsx'
            try:
                df.to_excel(xlPath)
            except:
                model.setStringList(['Failed', '', 'Make sure you don\'t have the searchResults file open'])
            model.setStringList(['Success!', '', 'Excel exported to desktop'])

        elif self.data['outType'] == '.csv':
            csvPath = Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) / 'searchResults.csv'
            try:
                df.to_csv(csvPath)
            except:
                model.setStringList(['Failed', '', 'Make sure you don\'t have the searchResults file open'])
            model.setStringList(['Success!', '', 'CSV exported to desktop'])

        else:
            print("Output type string not recognized")




def main():
    app = QGuiApplication(sys.argv)
    bridge = Bridge()

    #Set up engine and connect to qml
    engine = QQmlApplicationEngine(app)
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.rootContext().setContextProperty("myModel", model)
    engine.load(QUrl('view.qml'))
    if not engine.rootObjects():
        print("Root Objects not found")
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
