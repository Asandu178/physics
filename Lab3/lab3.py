import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import linregress

h = 6.625e-34       # J·s (const lui Plank)
e = 1.602e-19       # C sarcina (electronului)
m = 9.109e-31       # kg (masa electronului)
L = 0.135           # m (distanta dintre stratul de grafit si ecran)
d1 = 2.13e-10       # m
d2 = 1.23e-10       # m

print(matplotlib.get_backend())


df = pd.read_excel("data.xlsx")

df["1/sqrt(U)(V^-1/2)"] = 1/np.sqrt(df["U(kV)"] * 1000)
# inmultim cu 1e12 pt a face transformarea m -> pm
df["lambda1(pm)"] = d1 * (df["D1(cm)"] * 1e-2) / (2*L) * 1e12 # pt a ajunge in picometri din metri
df["lambda2(pm)"] = d2 * (df["D2(cm)"] *1e-2) / (2*L) * 1e12 # analog
df["lambda_t(pm)"] = h / (np.sqrt(2 * m * e)) * df["1/sqrt(U)(V^-1/2)"] * 1e12 # lungimea de unda teoretica

print(df.head())

df.to_excel("data.xlsx", index=False)

x = df["1/sqrt(U)(V^-1/2)"]
D1 = df["D1(cm)"]
D2 = df["D2(cm)"]

# Regressii liniare
slope1, intercept1, r1, _, _ = linregress(x, D1)
slope2, intercept2, r2, _, _ = linregress(x, D2)

# Convertim k din cm în metri
k1 = slope1 * 1e-2  # m·V^1/2
k2 = slope2 * 1e-2  # m·V^1/2

# Calculăm constantele de rețea folosind formula:
# d = (2 * L * h) / (k * sqrt(2 * m * e))
def calc_d(k):
    return (2 * L * h) / (k * np.sqrt(2 * m * e))

d1_calc = calc_d(k1) * 1e12  # pm
d2_calc = calc_d(k2) * 1e12  # pm

# Afișare
print(f" Panta k1 = {slope1:.4f} cm·V^1/2 => d1 = {d1_calc:.2f} pm (teoretic: 213 pm)")
print(f" Panta k2 = {slope2:.4f} cm·V^1/2 => d2 = {d2_calc:.2f} pm (teoretic: 123 pm)")
# R^2 coef de determinare ce masoara acuratetea aproximarii
# coef de corelatie
print(f" R^2 regresie D1: {r1**2:.4f}")
print(f" R^2 regresie D2: {r2**2:.4f}")

# Plot
plt.figure(figsize=(8, 6))
plt.plot(x, D1, 'o', label='D1 experimental')
plt.plot(x, slope1 * x + intercept1, '-', label='Regresie D1')

plt.plot(x, D2, 's', label='D2 experimental')
plt.plot(x, slope2 * x + intercept2, '--', label='Regresie D2')

plt.xlabel("1/√U (V⁻¹ᐟ²)")
plt.ylabel("Diametru inel (cm)")
plt.title("Determinarea constantelor de rețea ale grafitului")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("constante_retea_d1_d2.png", dpi=300)
plt.show()

print("📈 Grafic salvat ca 'constante_retea_d1_d2.png'")
