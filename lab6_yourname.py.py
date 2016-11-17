#******Set Environment******#
import os
import math


#******Set Classes & Functions******#
class City:
    def __init__(self, CityName = 'none', CityLabel = 'none', Lat = -999, Lon = -999, Pop = {}):
        self.cityName = CityName
        self.label = CityLabel
        self.lat = Lat
        self.lon = Lon
        self.pop = Pop

    #Method to calculate Great Circle Distance between two cities. As it is written, 'self' and 'othercity' must be entered as Cities[i],Cities[j] 
    def printDistance(self,othercity):
        #change coordinates to radians:
        latitude1 = math.radians(self.lat)
        longitude1 = math.radians(self.lon)
        latitude2 = math.radians(othercity.lat)
        longitude2 = math.radians(othercity.lon)

        #create variables for great circle route
        slat1 = math.sin(latitude1)
        slat2 = math.sin(latitude2)
        clat1 = math.cos(latitude1)
        clat2 = math.cos(latitude2)
        londif = longitude1 - longitude2
        clondif = math.cos (londif)

        # here I use the variables defined above to calculate the great circle distance in radians, relying on the order of operations to do things correctly
        d = math.acos (slat1 * slat2 + clat1 * clat2 * clondif)
        #convert raidans to kilometers
        distance = 6300 *d
        
        #return the distance to the user
        print 'The distance between %s and %s is %.2f kilometers.' % (self.label,othercity.label,distance)

    #method to calculate population change in one city over a set amount of time.  . As it is written, 'self' and 'othercity' must be entered as Cities[i],Cities[j]
    #parameters include the city, and the two years to be compared
    def printPopChange(self,year1,year2):
        #population dif calculated
        popDif = self.pop[year1]-self.pop[year2]
        #return population difference
        print 'The population in %s changed by %f million between %d and %d' % (self.label,popDif,year1,year2)
        
        
        


#******Script******#
#protect the script in a try/except function for file formatting issues
try:
    #set the working directory to where I stored the file based on user input (I don't want to hard-code a path in my program)
    directory = raw_input('Enter the path of the directory you want to work in> ')
    os.chdir(directory)

    #identify the file you want to work with.
    setFile = raw_input('Enter the csv file you want to open, including its extension> ')
    #open the file as a read-only.  CSV files are text files.
    cityFile = open(setFile,'rt')
    

    #read the csv file lines.  We're good to check the formatting of the CSV doc
    cityList = cityFile.readlines()
    Cities = []
    cityFile.close()
    print 'Environment set'
    print

    #now that the file is open, check that the formatting is correct
    try:
        #read the first line of the csv, testing that the headers are correct. EXPLAIN
        print 'Testing .csv format...'
        #create a list of the headers, split by commas
        cityFile2 = open(setFile, 'rt')
        line1 = cityFile2.readline()
        line1b = line1.replace(',',' ')
        headings = line1b.split()
        #create a tuple of the required headings for the script to run
        testHeadings = ('id','latitude','longitude','city','label','yr1970','yr1975','yr1980','yr1985','yr1990','yr1995','yr2000','yr2005','yr2010')
        #Go through each list, comparing the required headings to the headings in the CSV file.  Crash the program if they don't match, providing an explanation of what columns are needed.
        #create count variable to use as a requirement to start the next part of the program.
        count=0
        for c in range(len(headings)):
            real = headings [c]
            test = testHeadings [c]
            if real==test:
                count+=1
            else:
                print 'Column', real,'should be',test
                f = 1/0
        print '.csv formatted correctly.'
        print

        cityFile2.close()

        #once you've confirmed the 14 columns, procide (through while loop):
        while count == 14:
            #loop through the csv files, one line at a time
            for city in cityList:
                #split the list of one line (one city) by commas
                cityValues = city.split(',')

                #assign variables for later use.  Nested under if function to eliminate first row of headings (would have 'id' as the first column).  I know there's a csv module that fixes this, but this works with the tools I know for now.
                if cityValues[0] != 'id' :
                    try:
                        #test each lat/lon value for a proper range; crash the program if not, with directions.
                        if -90<=float(cityValues[1])<=90:
                            lat = float(cityValues[1])
                        #crash scenario-- same for lon, but with -180 to 180 range
                        else: f = 1/0
                        if -180<=float(cityValues[2])<=180:
                            lon = float(cityValues[2])
                        else: f = 1/0
                    except:
                        print 'Your latitude and longitude values must be numerical and within a proper range.'
                        print
                    name = cityValues[3]
                    label = cityValues[4]
                    #create a Dictionary of population, to be stored in each city instance
                    #test that data in the CSV format has been entered in proper format by encasing in try/except
                    try:
                        pop = {1970:float(cityValues[5]), 1975:float(cityValues[6]), 1980:float(cityValues[7]), 1985:float(cityValues[8]), 1990:float(cityValues[9]), 1995:float(cityValues[10]), 2000:float(cityValues[11]), 2005:float(cityValues[12]), 2010:float(cityValues[13])}
                    except: print 'Your population values must be numerical.'
                    #create an instance based CityLabel
                    instance = City(CityName = name, CityLabel = label, Lat = lat, Lon = lon, Pop = pop)
                    Cities.append(instance)

            #report each city instance, calling the different class attributes as defined in class City
            for city in Cities:
                #use formating to call each city's name, and the location and population, by year.
                print '%s:' % (city.label, )
                print '%4sLocation: %.2f latitude, %.2f longitude' % ('',city.lat, city.lon)
                print '%4sPopulation in Millions' % ('', )
                for year in range(1970,2015,5):
                    print '%12s: %.2f' % (year, city.pop[year])
                print

            break

    #the file is formatted incorrectly
    except: print 'Your .csv file is not properly formatted.  Check the data, and that it has the following columns:\nid,latitude,longitude,city,label,yr1970,yr1975,yr1980,yr1985,yr1990,yr1995,yr2000,yr2005,yr2010'

#the directory or filename doesn't exist, or is incorrectly entered.
except: print 'You must enter a valid directory and provide an existing file with a .csv extension'

