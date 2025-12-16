#https://github.com/Majdawad88/dht_plotting.git

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import sys

# The logfile will be passed into this script as a runtime argument.
# Example: python3 graph_dht.py my_logfile.txt
logFile = sys.argv[1]

# Create an empty figure for the subplots. There will be two in this case.
fig = plt.figure()

# Create the first subplot, and label it as temperature (celcius).
# First number is the total number of plots, next the column, last the row.
ax1 = fig.add_subplot(2,1,1)
ax1.set_ylabel('Temp')

# Create the second subplot, and label it as humidity.
ax2 = fig.add_subplot(2,1,2)
ax2.set_ylabel('Humid')

# The following lists will hold all the data we will be working with.
times = []
temps = []
humids = []

def readLog(filename, times, temps, humids):

   # Open the log file and extract the raw contents:
   with open(filename, 'r') as f:
       content = f.read()

   # Split the contents on new line characters. After, each reading is a cell.
   content = content.split('\n')

   # Iterate over readings in log file. Skip the first line, because it's a header.
   for line in content[1:]:

       # Split the line on each comma into an array.
       split = line.split(',')

       # The timestamp for this reading.
       time = split[0]

       # The temperature value for this reading.
       temp = split[1]

       # The humidity value for this reading.
       humid = split[2]
      
       # Compare timestamp to past timestamps. Only store this data if it is new.
       if time not in times:

           # Add the readings to their respective arrays.
           times.append(time)
           temps.append(temp)
           humids.append(humid)

def animate(i, times, temps, humids):
   # Readlog() function is called every animate of the graph (checking new info). 
   readLog(logFile, times, temps, humids)
  
   # Only consider the last 20 lines of each data array. 
   # This causes a 'scrolling effect' on the graph.
   times = times[-20:]
   temps = temps[-20:]
   humids = humids[-20:]

   # Wipe clean all subplots.
   ax1.clear()
   ax2.clear()

   # The last number of the timestamp, which is the seconds value.
   seconds = [time.split('-')[-1] for time in times]

   # Plot all temperature data on the y-axis against seconds data on the x-axis.
   ax1.plot(seconds, temps)
   ax1.set_ylabel('Temp')

   # Plot all humidity data on the y-axis against seconds data on the x-axis.
   ax2.plot(seconds, humids)
   ax2.set_ylabel('Humid')

# Call the animate function every 5 seconds, with data arrays as parameters.
ani = animation.FuncAnimation(fig, animate, fargs=(times, temps, humids), interval=5000)

# Finally, show the graph.
plt.show()

