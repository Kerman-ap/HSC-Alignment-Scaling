import json
import numpy as np
import matplotlib.pyplot as plt

# Load JSON data
with open('courses.json', 'r') as file:
    data = json.load(file)

course_name = "Mathematics Extension 2"
course_data = data[course_name]

hsc = course_data['hsc']
sca = course_data['sca']


stats = ["Max Mark", "P99", "P90", "P75", "P50", "P25"]


x = np.array([hsc[s]*2 for s in stats])
y = np.array([sca[s]*2 for s in stats])


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
plt.figure(figsize=(8,6))
for i, stat in enumerate(stats):
    plt.scatter(x[i], y[i], color=colors[i], label=stat, s=100)

degree = 3
coeffs = np.polyfit(x, y, degree)  
poly = np.poly1d(coeffs)

x_fit = np.linspace(min(x)-1, max(x)+1, 100)
y_fit = poly(x_fit)

plt.plot(x_fit, y_fit, color='pink', linestyle='--', linewidth=2, label=f'Fit')

plt.xlabel("HSC Score")
plt.ylabel("SCA Score")
plt.title(f"HSC vs SCA with Polynomial Regression - {course_name}")
plt.legend()
plt.grid(True)
plt.show()
