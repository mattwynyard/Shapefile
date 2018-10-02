import shapefile

path = "C:\Onsite\Python\polish.mp"

def main():
    '''Main program start'''

    #w = shapefile.Writer(shapefile.POLYLINE)
    #w.autoBalance = 1

    data = readPolish(path)
    #print data
    createShapeFile(data)

def createShapeFile(data):
    w = shapefile.Writer(shapefile.POLYLINE)
    w.autoBalance = 1

    w.field("roadID",'C')
    w.field("fathID", 'N')
    w.field("start", 'N')
    w.field("end", 'N')
    w.field("side", 'C')
    w.field("type", 'C')
    w.field("label", 'C')
    w.field("lineID", 'N')
    w.field("routeParam", 'C')

    for obj in data:
        roadID = obj["RoadID"]
        fpathID = obj["FPathNo"]
        start = int(obj["Start"])
        end = int(obj["End"])
        side = obj["Side"]
        _type = obj["Type"]
        label = obj["Label"]
        lineID = obj["LineID"]
        route = obj["RouteParam"]
        coords = obj["Data"]
        coords = coords[1:-1].split('),(')
        l = map(lambda x: x.split(','), coords)
        l = map(swap, l)
        
        coords = map(floatList, l)
        #print [coords]

        w.record(roadID, fpathID, start, end, side, _type, label, lineID, route)
        w.line(parts=[coords])
        #w.multipoint(coords)
        
    w.save("C:\\Onsite\\Python\\shape")
    #w.close


def readPolish(path):
    count = -1
    data = []
    dataDict = {"RoadID": "", "FPathNo": "", "Start": "", "End": "", "Side": "", "Type": "", "Label": "", "LineID": "", "RouteParam": "", "Data": []}
    flag = False
    with open(path, 'r') as f:
        for line in f:
            if line.strip('\n') == "[END-IMG ID]":
                flag = True
                count = -1
            if flag == True:
                if line[:7].strip('\n') == ";RoadID":
                    dataDict["RoadID"] = line[8:].strip('\n')
                elif line[:8].strip('\n') == ";FpathNo":
                    dataDict["FPathNo"] = line[9:].strip('\n')
                elif line[:7].strip('\n') == ";StartM":
                    dataDict["Start"] = line[8:].strip('\n')
                elif line[:5].strip('\n') == ";EndM":
                    dataDict["End"] = line[6:].strip('\n')
                elif line[:5].strip('\n') == ";Side":
                    dataDict["Side"] = line[6:].strip('\n')
                elif line[:4].strip('\n') == "Type":
                    dataDict["Type"] = line[5:].strip('\n')
                elif line[:6].strip('\n') == "Label=":
                    dataDict["Label"] = line[6:].strip('\n')
                elif line[:6].strip('\n') == "RoadID":
                    dataDict["LineID"] = line[7:].strip('\n')
                elif line[:10].strip('\n') == "RouteParam":
                    dataDict["RouteParam"] = line[11:].strip('\n')
                elif line[:4].strip('\n') == "Data":
                    dataDict["Data"] = line[6:].strip('\n')
        
            if line.strip('\n') == "[END]":
                data.append(dataDict)
                dataDict = {"RoadID": "", "FPathNo": "", "Start": "", "End": "", "Side": "", "Type": "", "Label": "", "LineID": "", "RouteParam": "", "Data": []}      
                count = -1

            count += 1          
    return data

def floatList(myList):
    return map(float, myList)

def swap(myList):
    #print myList
    zero = myList[1]
    one = myList[0]
    return [zero, one]

if __name__ == '__main__':
    main()

