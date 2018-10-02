# -*- coding: utf-8 -*-
"""
GISC405 Assignment 1
Script to traverse file directory and extract latitude longitude coordinates
from .csv and .txt files. Write a .csv file containing all the coordinates and
then builld a shape file for arcGIS
Author: Matt Wynyard March 2018
"""

import os, csv
import Tkinter 
import tkFileDialog 
import shapefile

def main():
    '''Main program start'''
    
    root = Tkinter.Tk()
    root.withdraw() #keep Tkinter root window hidden   
    folderPath = tkFileDialog.askdirectory(parent=root) #browse to toplevel folder   
    os.chdir(folderPath)
    os.chdir("..")
    os.getcwd()
    fileList = getFileList(checkOS(), folderPath) 
    coordinates = readFiles(fileList)   
    data = convertDecimal(coordinates)   
    writeFile(os.getcwd(), data) 
    createShapeFile(os.getcwd())

"""
Writes a shapefile for arcGIS and saves to current working directory
@param - path the file path of the file to read
"""    
def createShapeFile(path):
        
    s = shapefile.Writer(shapefile.POINT)    
    with open(path + '\\coordinates.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')      
        s.autoBalance  = 1        
        s.field("PID",'N')
        s.field("Longtitude",'N', decimal=4)
        s.field("Latitude", 'N',decimal=4)
        
        next(reader, None) #skip header row
        
        for row in reader:
            PID = row[0]
            latitude = float(row[2])
            longitude = float(row[1])               
            s.record(PID,longitude, latitude)
            s.point(longitude, latitude)
            
        s.save(path + '\\coordinates.csv')
        print "Shape files written to: " + path
        
"""
creates an empty list and uses os.walk() to insert all .csv amd .txtfiles in 
the top level folder and its subfolders into the list
@path -- the path of the top level folder containing files
@return -- a list containing all the file paths of the files
"""
def getFileList(seperator, folderPath):    
    fileList = []
    count = 0
    for foldername, subfolders, filenames in os.walk(folderPath):    
        for f in filenames:
            if not f.startswith('.'): #ignore hidden files
                if checkFileExtension(f) == 'csv' or checkFileExtension(f) == 'txt':
                    fileList.append(foldername + seperator + f)
                    count += 1
    return fileList

"""
Opens files from a list of file path and reads data of each file line by line.
Ignores header row in each file. Data is put into a 2D list
@param - fileList the list containing the file paths of each file
@return - list containing coordinate data for each line within a list
"""
def readFiles(fileList):
    rowList = []
    count = 0
    for myFile in fileList:
        if checkFileExtension(myFile) == "txt":
            delimeter = '\t'
        else:
            delimeter = ';'
        with open(myFile, 'r')  as f:
            reader = csv.reader(f)
            for line in reader:
                if count > 0:
                    latLong = getLatLong(line[0], delimeter)
                    rowList.append(latLong[-6:])
                count += 1
        count = 0
    return rowList

"""
creates and writes a csv ffile containing header row and latitude longitude
data - file saved to current working drectory
@param - folderPath the path of where folder saved
@param - data a list containing cooordinates convert to decimal
"""
def writeFile(path, data):
        with open(path + checkOS() + 'coordinates.csv', "wb") as f:
            writer = csv.writer(f, delimiter=',')
            count = 1
            writer.writerow(["PID", "longtitude", "latitude"])
            for line in data:
                line.insert(0, count)
                writer.writerow(line)
                count += 1
        print str(count - 1) + " lat/long coordinates written to: \n" + path + "\coordinates.csv"
"""
Converts each line of data from a string into into a list. Data is split on
delimeter supplied
@param line - the line containing the data
@param delimeter - the deleimeter char ie ; or tab(\t)
@return - lineList the list containing each data from each line
"""         
def getLatLong(line, delimeter):
    lineList = line.split(delimeter)    
    return lineList

"""obtains the file extension of the file
@poaram f the file to check
@return a string containing the file extension
"""
def checkFileExtension(f):
    return f.split('.')[-1]

"""
Converts minutes or seconds to decimal by dividing by 60 or 3600
@param - x minutes or seconds to convert
@param n - conversion faxctor 60 or 3600
@return minutes or seconds converted to decimal
"""
def convert(x, n):
    return float(x) / n

"""
Checks if coordinate negative and adds or subtracts converted minutes or 
seconds to degrees
@param - coordinate to convert
@return - coordinate fully converted to decimal
"""
def buildCoordinate(x):
    if float(x[0]) < 0:
        return float(x[0]) - convert(x[1], 60) - convert(x[2], 3600)
    else:
        return float(x[0]) + convert(x[1], 60) + convert(x[2], 3600)

"""
Extracts coordinates (lat/long) for conversion to deicmal and puts into  a new
list
@param - coordinatesList - list containing unconverted lat/long coordinates
@return - list containing converted coordinates
"""    
def convertDecimal(coordinatesList):
    coordinates = []
    for x in coordinatesList:
        longitude = buildCoordinate(x[:3])
        latitude = buildCoordinate(x[3:])
        coordinates.append([longitude, latitude])
    return coordinates
         
"""
checks if operating system is windows or unix
@return -- char directory seperator of operating system
"""
def checkOS():
    if os.name == 'nt':
        return '\\' #windows
    else:
        return '/' #linux/os

if __name__ == '__main__':
    main()