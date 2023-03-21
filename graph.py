import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('data.log', delimiter=',', usecols=(0,1), dtype='datetime64[s], f8', names=['datetime', 'temperature'], skip_header=6)

plt.plot(data['datetime'], data['temperature'])
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Data')
plt.show()
