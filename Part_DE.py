#Author: W.M.O.V.J. Bandara
#Date: 12/18/2024
#Student ID: w2120216

# Import modules
import tkinter as tk
import csv
from datetime import datetime
from Part_ABC import validate_date_input, process_csv_data, display_outcomes, save_results_to_file

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, trafficData, date):
        # Initialize histogram properties
        self.trafficData = trafficData
        self.date = date
        self.root = tk.Tk()
        self.root.title("Histogram")
        self.canvas = None
        self.width = 1000
        self.height = 500
        self.marginTop = 80
        self.marginBottom = 50
        self.marginLeft = 50
        self.marginRight = 50
        self.barWidth = 15
        self.groupSpacing = 10
        self.root.configure(bg='white')

        # Add a reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_canvas)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

    def setup_window(self):
        # Create canvas for histogram
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white', highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

    def process_data(self):
        # Initialize count arrays
        elmAvenueCounts = [0] * 24
        hanleyHighwayCounts = [0] * 24

        # Process traffic data by hour
        for record in self.trafficData:
            timeHour = datetime.strptime(record[2], '%H:%M:%S').hour
            if record[0] == "Elm Avenue/Rabbit Road":
                elmAvenueCounts[timeHour] += 1
            else:
                hanleyHighwayCounts[timeHour] += 1

        return elmAvenueCounts, hanleyHighwayCounts

    def draw_histogram(self):
        # Get data and calculate dimensions
        elmCounts, hanleyCounts = self.process_data()
        maxCount = max(max(elmCounts), max(hanleyCounts))
        plotHeight = self.height - self.marginTop - self.marginBottom
        plotWidth = self.width - self.marginLeft - self.marginRight
        scaleFactor = plotHeight / (maxCount + 5)

        # Draw x-axis
        xStart = self.marginLeft
        xEnd = self.width - self.marginRight
        yAxis = self.height - self.marginBottom
        self.canvas.create_line(xStart, yAxis, xEnd, yAxis, width=1)

        # Calculate hour width
        hourWidth = plotWidth / 24

        # Draw bars for each hour
        for hour in range(24):
            groupX = self.marginLeft + hour * hourWidth
            xCenter = groupX + (hourWidth - 2 * self.barWidth - self.groupSpacing) / 2

            # Draw Elm Avenue bar
            heightElm = elmCounts[hour] * scaleFactor
            elmBar = self.canvas.create_rectangle(xCenter, yAxis - heightElm, xCenter + self.barWidth, yAxis, fill='#90EE90', outline='#90EE90')

            # Add Elm Avenue count
            if elmCounts[hour] > 0:
                self.canvas.create_text(xCenter + self.barWidth / 2, yAxis - heightElm - 10, text=str(elmCounts[hour]), fill='#2E8B57', font=('Arial', 8))

            # Draw Hanley Highway bar
            heightHanley = hanleyCounts[hour] * scaleFactor
            hanleyBar = self.canvas.create_rectangle(xCenter + self.barWidth, yAxis - heightHanley, xCenter + 2 * self.barWidth, yAxis, fill='#FFB6C1', outline='#FFB6C1')

            # Add Hanley Highway count
            if hanleyCounts[hour] > 0:
                self.canvas.create_text(xCenter + 1.5 * self.barWidth, yAxis - heightHanley - 10, text=str(hanleyCounts[hour]), fill='#CD5C5C', font=('Arial', 8))

            # Add hour label
            self.canvas.create_text(groupX + hourWidth / 2, yAxis + 15, text=f"{hour:02d}", font=('Arial', 8))

    def add_legend(self):
        # Format date and add title
        formattedDate = datetime.strptime(self.date, '%d/%m/%Y').strftime('%d/%m/%Y')
        self.canvas.create_text(self.width / 2, 30, text=f"Histogram of Vehicle Frequency per Hour ({formattedDate})", font=('Arial', 12, 'bold'))

        # Add legend elements
        legendY = 50
        self.canvas.create_rectangle(self.marginLeft, legendY, self.marginLeft + 15, legendY + 10, fill='#90EE90', outline='#90EE90')
        self.canvas.create_text(self.marginLeft + 25, legendY + 5, text="Elm Avenue/Rabbit Road", anchor='w', font=('Arial', 10))
        self.canvas.create_rectangle(self.marginLeft + 200, legendY, self.marginLeft + 215, legendY + 10, fill='#FFB6C1', outline='#FFB6C1')
        self.canvas.create_text(self.marginLeft + 225, legendY + 5, text="Hanley Highway/Westway", anchor='w', font=('Arial', 10))
        self.canvas.create_text(self.width / 2, self.height - 15, text="Hours 00:00 to 24:00", font=('Arial', 10))

    def reset_canvas(self):
        # Clear the canvas
        self.canvas.delete("all")

    def run(self):
        # Run the histogram application
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        # Initialize processor
        self.currentData = None
        self.date = None

    def clear_previous_data(self):
        # Reset data
        self.currentData = None
        self.date = None

    def handle_user_interaction(self):
        # Get user input for date
        year = validate_date_input("Please enter the year of the survey in the format YYYY: ", 2000, 2024)
        month = validate_date_input("Please enter the month of the survey in the format MM: ", 1, 12, year)
        day = validate_date_input("Please enter the day of the survey in the format DD: ", 1, 31, year, month)
        
        # Format month and day
        if len(str(month)) == 1: 
            month = f"0{month}"
        if len(str(day)) == 1: 
            day = f"0{day}"
        
        # Create file path and date
        filePath = f"traffic_data{day}{month}{year}.csv"
        dateStr = f"{day}/{month}/{year}"
        
        return filePath, dateStr
    
    def validate_continue_input(self):
        # Handle continue/exit choice
        while True:
            try:
                userChoice = input("Do you want to load another dataset? (Y/N): ").upper()
                if userChoice == "Y":
                    main()
                elif userChoice == "N":
                    print("Exit!")
                    exit()
                else:
                    print("Please enter 'Y' or 'N'.")
            except ValueError:
                print("Please enter 'Y' or 'N'.")

    def process_files(self):
        while True:
            self.clear_previous_data()
            filePath, dateStr = self.handle_user_interaction()
            outcomes = process_csv_data(filePath)
            if outcomes:
                self.date = dateStr
                display_outcomes(outcomes, filePath)
                save_results_to_file(outcomes, "results.txt", filePath)      
                try:
                    with open(filePath, mode='r') as file:
                        csvReader = csv.reader(file)
                        next(csvReader)  # Skip header
                        self.currentData = list(csvReader)
                except FileNotFoundError as e:
                    print(f"Error: {e}")
                histogram = HistogramApp(self.currentData, self.date)
                histogram.run()
            self.validate_continue_input()
                             
def main():
    processor = MultiCSVProcessor()
    processor.process_files()

if __name__ == "__main__":
    main()

# References:

# 1. Tkinter documentation. Available at: https://docs.python.org/3/library/tkinter.html
# 2. Claude AI.  Available at: https://claude.ai/
# 3. Stone, B. (2018). Python GUI Development with Tkinter. [online] LinkedIn. Available at: https://www.linkedin.com/learning/python-gui-development-with-tkinter-2.
# 4. Marini, J. (2023). Python Object-Oriented Programming. [online] LinkedIn. Available at: https://www.linkedin.com/learning/python-object-oriented-programming.