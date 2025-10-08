import numpy as np
import matplotlib.pyplot as plt

# Data from annual NESA scaling report
aggregates = np.array([478.1, 458.8, 447.8, 433.8, 404.2, 370.0, 341.8, 315.8, 290.8, 267.2, 244.1, 221.1, 198.3, 175.5])
atar = np.array([102, 100, 99.00, 98.00, 95.00, 90.00, 85.00, 80.00, 75.00, 70.00, 65.00, 60.00, 55.00, 50.00])

yearly_data = np.array([
    [478.1, 478.8, 478.1, 479.8, 477.4],
    [458.8, 458.7, 459.9, 459.3, 455.9],
    [447.8, 448.0, 449.1, 449.5, 445.6],
    [433.8, 433.7, 434.3, 435.0, 431.6],
    [404.2, 404.8, 404.6, 405.5, 403.5],
    [370.1, 369.8, 368.9, 370.0, 369.2],
    [341.8, 340.2, 338.9, 340.2, 340.2],
    [315.8, 313.5, 310.9, 313.0, 312.6],
    [290.8, 288.0, 285.2, 287.4, 286.2],
    [267.2, 263.8, 259.5, 261.8, 260.6],
    [244.1, 239.8, 234.4, 236.8, 235.4],
    [221.1, 217.2, 210.4, 212.5, 210.1],
    [198.3, 195.4, 186.4, 188.2, 185.3],
    [175.5, 172.8, 162.8, 164.3, 160.6]
])

avg_aggregates = yearly_data.mean(axis=1)

avg_aggregates = np.append(avg_aggregates, 500)
avg_aggregates = np.append(avg_aggregates, 490)
atar = np.append(atar, 104)
atar = np.append(atar, 103)

degree = 5
poly = np.poly1d(np.polyfit(avg_aggregates, atar, degree))

print("Polynomial mapping Average Aggregate to ATAR:")
print(poly)
print("Coefficients (highest degree first):")
print(poly.coeffs)

x_line = np.linspace(min(avg_aggregates)-5, max(avg_aggregates)+5, 200)
y_line = poly(x_line)

plt.figure(figsize=(8,6))
plt.scatter(avg_aggregates, atar, color='blue', label='Data points')
plt.plot(x_line, y_line, color='red', linestyle='--', linewidth=2, label=f'Poly deg {degree}')
plt.xlabel("Average Aggregate")
plt.ylabel("ATAR")
plt.title("Average Aggregate → ATAR (with 500 added)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.show()
