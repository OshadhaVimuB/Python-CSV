#Author: W.M.O.V.J. Bandara
#Date: 11/24/2024
#Student ID: w2120216

# Import modules
import csv

# Task A: Input Validation
def isLeapYear(year):
    isLeap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return isLeap

def validate_date_input(output, minimumValue, maximumValue, year=None, month=None):
    while True:
        try:
            value = int(input(output))
            # If year is leap year fix the maximum days for February
            if month == 2:
                if year != None:
                    if isLeapYear(year) == True:
                        maximumValue = 29
                    else:
                        maximumValue = 28         
            # Fix the maximum days for months
            if month in [1, 3, 5, 7, 8, 10, 12]:
                maximumValue = 31
            elif month in [4, 6, 9, 11]:
                maximumValue = 30
            if minimumValue <= value <= maximumValue:
                return value
            else:
                print(f"Out of range - value must be in the range {minimumValue} and {maximumValue}.")
        except ValueError:
            print("Integer required")

def validate_continue_input():
    while True:
        try:
            value = input("Do you want to load another dataset? (Y/N): ").upper()
            if value == "Y":
                main()
            elif value == "N":
                print("Exit!")
                exit()
            else:
                print("Invalid input - please enter 'Y' or 'N'.")
        except ValueError:
            print("Invalid input - please enter 'Y' or 'N'.")

# Task B: Processed Outcomes
def process_csv_data(file_path):
    totalVehicles = 0
    totalTrucks = 0
    totalElectric = 0
    totalTwoWheeled = 0
    totalBussesNorth = 0
    totalNoTurning = 0
    totalBicycles = 0
    totalOverSpeedLimit = 0
    totalElmAvenue = 0
    totalHanley = 0
    totalElmAvenueScooters = 0
    hours = []
    countHanleyPeak = {}
    timesOfPeak = []
    outputFormatPeakTimeRange = []
    rainHours = []
    countRainHours = {}
    allOutputData = {}
    try:
        with open(file_path, mode='r') as file: # Read csv file (Schafer, 2017)
            vehicles = csv.reader(file)
            next(vehicles) # Skip the header row
            for data in vehicles:
                totalVehicles += 1  # Count total vehicles
                if data[8] == "Truck":
                    totalTrucks += 1
                if data[9] == "True": # Count total electric vehicles
                    totalElectric += 1
                if data[8] in ["Bicycle", "Motorcycle", "Scooter"]:   # Count total two-wheeled vehicles
                    totalTwoWheeled += 1
                if data[0] == "Elm Avenue/Rabbit Road" and data[4] == "N" and data[8] == "Buss":   # Count total busses heading North
                    totalBussesNorth += 1
                if data[3] == data[4]:   # Count total vehicles not turning left or right
                    totalNoTurning += 1
                if data[8] == "Bicycle":  # Count total bicycles
                    totalBicycles += 1
                if int(data[6]) < int(data[7]):  # Count total vehicles over the speed limit
                    totalOverSpeedLimit += 1
                if data[0] == "Elm Avenue/Rabbit Road": # Count total vehicles through Elm Avenue/Rabbit Road junction
                    totalElmAvenue += 1
                if data[0] == "Hanley Highway/Westway": # Count total vehicles through Hanley Highway/Westway junction
                    totalHanley += 1
                if data[0] == "Elm Avenue/Rabbit Road" and data[8] == "Scooter": # Count total scooters through Elm Avenue/Rabbit Road junction
                    totalElmAvenueScooters += 1
                if data[0] == "Hanley Highway/Westway": # Get the peak hour
                    time = data[2]
                    time = time.split(":")
                    hour = int(time[0])
                    hours.append(hour)
                if data[5] in ["Heavy Rain", "Light Rain"]: # Get the hour of rain
                    rainTime = data[2]
                    time = rainTime.split(":")
                    rainHour = int(time[0])
                    rainHours.append(rainHour)
        percentageTrucks = str(round((totalTrucks/totalVehicles) * 100)) + "%" # Count the percentage of trucks
        avgBicycles = round(totalBicycles/24) # Calculate the average number of bicycles per hour
        percentageScooters = str(round((totalElmAvenueScooters/totalElmAvenue) * 100)) + "%" # Calculate the percentage of scooters
        for i in hours: # Get the peak hour (Stack Overflow, 2008)
            if i in countHanleyPeak:
                countHanleyPeak[i] += 1
            else:
                countHanleyPeak[i] = 1
        peakHourHanley = max(countHanleyPeak.values()) 
        for key,value in countHanleyPeak.items():
            if value == peakHourHanley:
                timesOfPeak.append(key)
        for i in timesOfPeak:
            formatPeakTimeRange = (f"between {i:02d}:00 and {i + 1:02d}:00") # for 2 digit format
            outputFormatPeakTimeRange.append(formatPeakTimeRange)
        for i in rainHours: # Get the total hour for rain
            if i in countRainHours:
                countRainHours[i] += 1
            else:
                countRainHours[i] = 1
        totalRainHours = len(countRainHours)

        allOutputData = {
            "The total number of vehicles recorded for this date is": totalVehicles,
            "The total number of trucks recorded for this date is": totalTrucks,
            "The total number of electric vehicles for this date is": totalElectric,
            "The total number of two-wheeled vehicles for this date is": totalTwoWheeled,
            "The total number of Busses leaving Elm Avenue/Rabbit Road heading North is": totalBussesNorth,
            "The total number of Vehicles through both junctions not turning left or right is": totalNoTurning,
            "The percentage of total vehicles recorded that are trucks for this date is": percentageTrucks,
            "the average number of Bikes per hour for this date is": avgBicycles,
            "The total number of Vehicles recorded as over the speed limit for this date is": totalOverSpeedLimit,
            "The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is": totalElmAvenue,
            "The total number of vehicles recorded through Hanley Highway/Westway junction is": totalHanley,
            percentageScooters :"of vehicles recorded through Elm Avenue/Rabbit Road are scooters.",
            "The highest number of vehicles in an hour on Hanley Highway/Westway is": peakHourHanley,
            "The most vehicles through Hanley Highway/Westway were recorded": outputFormatPeakTimeRange[0],
            "The number of hours of rain for this date is": totalRainHours
        }
        return allOutputData
    
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

# Display the outcomes
def display_outcomes(outcomes, fileName):
    if outcomes is None:
        return  # Exit if file not found
    try:
        print(f"data file selected is: {fileName}")
        for key, value in outcomes.items():
            print(f"{key} {value}")
    except:
        print("An error occurred while displaying the outcomes.")
            
# Task C: Save Results to Text File
def save_results_to_file(outcomes, resultsFile, fileName):
    if outcomes is None:
        return  # Exit if file not found
    try:
        with open(resultsFile, 'a') as file:
            file.write("********************************************\n")
            file.write(f"data file selected is: {fileName}\n")
            file.write("********************************************\n")
            for key, value in outcomes.items():
                file.write(f"{key} {value}\n")
            file.write("\n")
            file.write("\n")
    except (FileNotFoundError, Exception) as e:
        print(f"Error: {e}")
        return None

def main():
    year = validate_date_input("Please enter the year of the survey in the format YYYY: ", 2000, 2024)
    month = validate_date_input("Please enter the month of the survey in the format MM: ", 1, 12, year)
    day = validate_date_input("Please enter the day of the survey in the format DD: ", 1, 31, year, month)
    
    # fix the month and day to have 2 digits
    fixMonth = len(str(month)) 
    if fixMonth == 1:
        month = "0" + str(month)
    fixDay = len(str(day)) 
    if fixDay == 1:
        day = "0" + str(day)
    # Create the file name
    fileName = str("traffic_data"+ str(day) + str(month) + str(year)+".csv")
    # Process the data
    display_outcomes(process_csv_data(fileName), fileName)
    save_results_to_file(process_csv_data(fileName), "results.txt", fileName)
    validate_continue_input()

if __name__ == "__main__":
    main()

# References:
"""
Stack Overflow. (n.d.). Getting key with maximum value in dictionary? [online] Available at: https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary [Accessed 28 Nov. 2024].

Schafer, C. (2017). Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files. [online] YouTube. Available at: https://youtu.be/q5uM4VKywbA [Accessed 28 Nov. 2024].
"""