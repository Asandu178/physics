import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

h = 6.625e-34       # J·s (const lui Plank)
e = 1.602e-19       # C sarcina (electronului)
m = 9.109e-31       # kg (masa electronului)
L = 0.135           # m (distanta dintre stratul de grafit si ecran)
d1 = 2.13e-10       # m
d2 = 1.23e-10       # m

print(matplotlib.get_backend())


df = pd.read_excel("data.xlsx")

df["1/sqrt(U)(V^-1)"] = 1/np.sqrt(df["U(kV)"] * 1000)
# inmultim cu 1e12 pt a face transformarea m -> pm
df["lambda1(pm)"] = d1 * (df["D1(cm)"] * 1e-2) / (2*L) * 1e12 # pt a ajunge in picometri din metri
df["lambda2(pm)"] = d2 * (df["D2(cm)"] *1e-2) / (2*L) * 1e12 # analog
df["lambda_t(pm)"] = h / (np.sqrt(2 * m * e)) * df["1/sqrt(U)(V^-1)"] * 1e12 # lungimea de unda teoretica

print(df.head())

df.to_excel("data.xlsx", index=False)

plt.plot(df["U(kV)"], df["lambda1(pm)"], 'o-', label="λ1 experimental")
plt.plot(df["U(kV)"], df["lambda2(pm)"], 's-', label="λ2 experimental")
plt.plot(df["U(kV)"], df["lambda_t(pm)"], '^-', label="λ teoretic")
plt.xlabel("Tensiune de accelerare U (kV)")
plt.ylabel("Lungime de undă (pm)")
plt.title("Compararea lungimilor de undă ale electronilor")
plt.legend()
plt.grid(True)

# Salvare în fișier imagine
plt.savefig("grafic_lab3.png", dpi=300)
print("✅ Grafic salvat ca 'grafic_lab3.png'")
