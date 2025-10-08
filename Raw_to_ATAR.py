import numpy as np
import csv
import json
import matplotlib.pyplot as plt
from scraper import scrape_marks  

url = "https://rawmarks.info/mathematics/mathematics-extension-2/"
course_name = "Mathematics Extension 2"
csv_file, title = scrape_marks(url)

raw_marks = []
hsc_marks = []

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        raw_marks.append(float(row[1])*2)      # raw mark
        hsc_marks.append(float(row[2])*2)      # HSC mark

raw_marks = np.array(raw_marks)
hsc_marks = np.array(hsc_marks)


f_raw_to_hsc = np.poly1d(np.polyfit(raw_marks, hsc_marks, 3))


# Load HSC to SCA / Aggregate data from JSON

with open('courses.json', 'r') as file:
    data = json.load(file)


course_data = data[course_name]

stats = ["Max Mark", "P99", "P90", "P75", "P50", "P25"]

# Multiply by 2 (as data is for one unit, *2 to get /100)
hsc_points = np.array([course_data['hsc'][s]*2 for s in stats])
sca_points = np.array([course_data['sca'][s]*2 for s in stats])

g_hsc_to_sca = np.poly1d(np.polyfit(hsc_points, sca_points, 3))

# Compose Raw to Aggregate

h_raw_to_agg = g_hsc_to_sca(f_raw_to_hsc)

# Define Aggregate to ATAR polynomial
f_agg_to_atar = np.poly1d([8.826e-12, -1.666e-08, 1.097e-05, -0.003403, 0.7176, -14.3])

final_poly = f_agg_to_atar(h_raw_to_agg)



x_raw = np.linspace(50, 100, 200)

agg_scaled = h_raw_to_agg(x_raw) * 5.0     # *5 as aggregate is /500
y_atar = f_agg_to_atar(agg_scaled)         


# Enforce increasing monotonicity

try:
    from sklearn.isotonic import IsotonicRegression
    ir = IsotonicRegression(increasing=True, out_of_bounds='clip')
    y_atar_monotone = ir.fit_transform(x_raw, y_atar)
    method_used = "IsotonicRegression (sklearn)"
except Exception:
    y_atar_monotone = np.maximum.accumulate(y_atar)
    method_used = "np.maximum.accumulate (fallback)"

y_atar_monotone = np.clip(y_atar_monotone, 0, 99.95)

plt.figure(figsize=(8,6))
plt.plot(x_raw, y_atar_monotone, color='purple', linewidth=2)
plt.xlabel("Raw Mark")
plt.ylabel("ATAR Contribution")
plt.title(f"Raw Mark → ATAR Contribution ({course_name})")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(30, 100)
plt.ylim(60, 100)
plt.show()