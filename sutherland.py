import numpy as np
import matplotlib.pyplot as plt

def sutherland_viscosity(T, T_ref=288.15, mu_ref=1.716e-5, S=110.4):
    """Sutherland Law: mu = mu_ref * (T/T_ref)^1.5 * (T_ref + S)/(T + S)"""
    return mu_ref * (T/T_ref)**1.5 * (T_ref + S)/(T + S)

def joukowski(z, R, center):
    return z + 1/z

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Temperature cases: Cold, Standard, Hot
temperatures = [250, 288.15, 350] # Kelvin
labels = ['T = 250K: Cold', 'T = 288K: ISA', 'T = 350K: Hot']
colors = ['blue', 'green', 'red']
linestyles = ['-', '--', '-.']

theta = np.linspace(0, 2*np.pi, 1000)

for i, T in enumerate(temperatures):
    mu = sutherland_viscosity(T)
    # Couple viscosity to mapping parameters: Higher T -> Higher mu -> Thicker boundary layer -> More camber
    camber_factor = 1.0 + 0.2 * (mu - sutherland_viscosity(288.15))/sutherland_viscosity(288.15)
    
    R = 1.05 * camber_factor
    center = -0.05 + 0.1*(camber_factor-1) + 0.03*(camber_factor-1)*1j
    
    z_circle = center + R * np.exp(1j * theta)
    w_airfoil = joukowski(z_circle, R, center)
    
    ax1.plot(np.real(w_airfoil), np.imag(w_airfoil), 
            color=colors[i], linestyle=linestyles[i], linewidth=2.5, label=labels[i])

ax1.axis('equal')
ax1.grid(True, linestyle=':')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('(a) Airfoil Shape vs Temperature')
ax1.legend()

# Plot 2: Sutherland Law Curve
T_range = np.linspace(200, 400, 200)
mu_range = sutherland_viscosity(T_range)
ax2.plot(T_range, mu_range*1e5, 'k-', linewidth=2)
for i, T in enumerate(temperatures):
    ax2.plot(T, sutherland_viscosity(T)*1e5, 'o', color=colors[i], markersize=8)

ax2.grid(True, linestyle=':')
ax2.set_xlabel('Temperature T [K]')
ax2.set_ylabel('Dynamic Viscosity μ [x10^-5 Pa·s]')
ax2.set_title('(b) Sutherland Law: μ(T) Coupling')

plt.suptitle('Non-Isothermal Conformal Mapping: Viscosity-Temperature Coupling', fontsize=14)
plt.tight_layout()
plt.savefig('fig7.5_non_isothermal.png', dpi=300, bbox_inches='tight')
plt.show()