import numpy as np
import csv
import json
import matplotlib.pyplot as plt
from scraper import scrape_marks  

url = "https://rawmarks.info/hsie/economics/"
course_name = "Economics"
csv_file, title = scrape_marks(url)

raw_marks = []
hsc_marks = []

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        raw_marks.append(float(row[1]))      # raw mark
        hsc_marks.append(float(row[2]))      # HSC mark

raw_marks = np.array(raw_marks)
hsc_marks = np.array(hsc_marks)

x_shift = raw_marks - 100
y_shift = hsc_marks - 100

A = np.vstack([x_shift**3, x_shift**2, x_shift]).T
coeffs, *_ = np.linalg.lstsq(A, y_shift, rcond=None)
a, b, c = coeffs

def anchored_poly(x):
    xs = x - 100
    return a*xs**3 + b*xs**2 + c*xs + 100

f_raw_to_hsc = np.poly1d([
    a, 
    -300*a + b, 
    30000*a - 200*b + c, 
    -1_000_000*a + 10_000*b - 100*c + 100
])
print([
    a, 
    -300*a + b, 
    30000*a - 200*b + c, 
    -1_000_000*a + 10_000*b - 100*c + 100
])
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
f_agg_to_atar = np.poly1d([1.66950188e-22, -5.48669938e-19,  8.02957890e-16, -6.88690028e-13,
  3.83199429e-10, -1.44494178e-07,  3.73867545e-05, -6.55359401e-03,
  7.44697672e-01, -4.93033035e+01,  1.47653860e+03])

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
plt.xlim(50, 100)
plt.ylim(70, 100)
plt.show()
