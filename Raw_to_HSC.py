import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.colors import LinearSegmentedColormap
from scraper import scrape_marks

# URL to take data from
url = "https://rawmarks.info/mathematics/mathematics-extension-2/"
csv_file, title = scrape_marks(url)

# Read File
rows = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        rows.append(row)

years = np.array([int(x[0]) for x in rows])
raws = np.array([float(x[1]) for x in rows])
aligned = np.array([float(x[2]) for x in rows])

# Polynomial regression
x_shifted = raws - 100
y_shifted = aligned - 100

#Cubic with no constant term
A = np.vstack([x_shifted**3, x_shifted**2, x_shifted]).T
coeffs, *_ = np.linalg.lstsq(A, y_shifted, rcond=None)
a, b, c = coeffs

def aligned_poly(x):
    x_shift = x - 100
    return a*x_shift**3 + b*x_shift**2 + c*x_shift + 100

x_line = np.linspace(20, 100, 200)
y_line = aligned_poly(x_line)

# Aligned Bands
plt.axhspan(90, 100, facecolor="lightblue", alpha=0.3)  
plt.axhspan(80, 90, facecolor="lightgreen", alpha=0.3)  
plt.axhspan(70, 80, facecolor="yellow", alpha=0.3)      
plt.axhspan(0, 70, facecolor="lightcoral", alpha=0.3)   

plt.plot(x_line, y_line, color="black", linestyle="--", linewidth=2, label="Polynomial Fit")

# Scatter plot
norm = plt.Normalize(years.min(), years.max())
cmap = LinearSegmentedColormap.from_list("red_to_blue", ["blue", "red"])
scatter = plt.scatter(raws, aligned, marker="x", c=years, cmap=cmap, norm=norm, alpha=0.8)

# Sidebar
cbar = plt.colorbar(scatter)
cbar.set_label("Year")
cbar_ticks = np.arange(years.min(), years.max() + 1, 5)
cbar.set_ticks(cbar_ticks)
cbar.set_ticklabels([str(int(t)) for t in cbar_ticks])

plt.xlabel("Raw Mark (/100)")
plt.ylabel("Aligned Mark (/100)")
plt.title(f"Raw vs Aligned Marks ({title})")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(20, 100)
plt.ylim(20, 100)

plt.show()
