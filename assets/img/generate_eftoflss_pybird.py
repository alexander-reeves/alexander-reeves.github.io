#!/usr/bin/env python3
"""
Generate animation showing 1-loop EFTofLSS power spectrum build-up.
Shows the different contributions to the dark matter power spectrum at 1-loop order.
Uses PyBird to accurately compute 1-loop SPT corrections.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.interpolate import interp1d

# Set style
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['axes.grid'] = False
plt.rcParams['figure.facecolor'] = 'white'

print("Initializing PyBird...")

# Import PyBird
from pybird.correlator import Correlator  
from pybird.symbolic import Symbolic

# Cosmological parameters (Planck 2018)
z = 0.0  # Redshift
cosmo_params = {
    'omega_b': 0.02237,
    'omega_cdm': 0.12,
    'h': 0.6736,
    'ln10^{10}A_s': 3.044,
    'n_s': 0.9649
}

# k array for linear P(k) - need dense sampling
kk = np.logspace(-5, 0, 500)  

print("Computing linear power spectrum with PyBird...")
# Initialize Symbolic cosmology class for linear P(k)
M = Symbolic()
M.set(cosmo_params)
M.compute(kk, z)
pk_lin_interp = M.pk_lin
f = M.f  # Growth rate


# k array for final output
k = np.logspace(-2, 0, 200)  # k from 0.01 to 1 h/Mpc

print("Computing 1-loop corrections with PyBird...")
# Initialize PyBird Correlator
N = Correlator()

# Configure for real space, dark matter only, power spectrum
config = {
    'output': 'mPk',        # matter power spectrum
    'multipole': 0,         # monopole (real space)
    'z': z,
    'optiresum': False,     # No IR resummation for clarity
    'with_stoch': False,    # No stochastic terms (pure DM)
    'with_nnlo_counterterm': False,  # No NNLO counterterms
    'with_bias': True,      # Enable bias terms so we can access b22, b13
    'kmax': 0.4,            # Maximum k for computation
    'km': 1.0,
    'kr': 1.0,
    'nd': 3e-4,
    'eft_basis': 'westcoast'
}

N.set(config)

# Dark matter biases for real space (no redshift distortions, f=0)
bs_dm = {
    'b1': 1.0,
    'b2': 0.0,
    'b3': 0.0,
    'b4': 0.0,
    'cct': 0.0,
    'cr1': 0.0,
    'cr2': 0.0
}

# Compute the power spectrum components
# PyBird needs kk and pk_lin for cosmology, and bias when with_bias=True
N.compute({'kk': kk, 'pk_lin': pk_lin_interp, 'bias': bs_dm})

# PyBird computes on its own internal k-grid
# Get the internal k-grid from PyBird
k_bird = N.co.k  # PyBird's internal k-grid

# The biases were already set in the compute() call above
# PyBird internally called setBias(), so b22 and b13 are now available

# For monopole (l=0) in real space
l_monopole = 0

# Get P11, P22, P13 arrays
# When with_bias=True, P22 and P13 are shape (N22, Nk) and (N13, Nk)
P11 = N.bird.P11  # Shape: (Nk,)
P22 = N.bird.P22  # Shape: (36 bias terms, k)
P13 = N.bird.P13  # Shape: (15 bias terms, k)

# Get the bias coefficient arrays for dark matter at monopole
# b22 and b13 have shape (Nl, Nbias) where Nl is number of multipoles
b11_coeffs = N.bird.b11[l_monopole]  # Scalar for monopole
b22_coeffs = N.bird.b22[l_monopole]  # Shape: (36,)
b13_coeffs = N.bird.b13[l_monopole]  # Shape: (15,)

print(f"PyBird k-grid shape: {k_bird.shape}")
print(f"P11 shape: {P11.shape}, P22 shape: {P22.shape}, P13 shape: {P13.shape}")
print(f"b11 coeff: {b11_coeffs}")
print(f"b22 coeffs shape: {b22_coeffs.shape}, b13 coeffs shape: {b13_coeffs.shape}")
print(f"b22 non-zero terms: {np.sum(np.abs(b22_coeffs) > 1e-10)}")
print(f"b13 non-zero terms: {np.sum(np.abs(b13_coeffs) > 1e-10)}")

# Apply proper bias weighting using einsum (like PyBird does internally)
# For dark matter at monopole: einsum('b,bx->x', b_coeffs, P_component)
P11_bird = b11_coeffs * P11  # Simple scalar multiplication for P11
P_22_bird = np.einsum('b,bx->x', b22_coeffs, P22)
P_13_bird = np.einsum('b,bx->x', b13_coeffs, P13)

# Total loop correction
Ploop_bird = P_22_bird + P_13_bird

# Total 1-loop
P_1loop_bird = P11_bird + Ploop_bird

print(f"Dark matter components (properly bias-weighted):")
print(f"P11 shape: {P11_bird.shape}, P22 shape: {P_22_bird.shape}, P13 shape: {P_13_bird.shape}")
print(f"Ploop shape: {Ploop_bird.shape}")
print(f"Max P22/P11: {(P_22_bird/P11_bird).max()*100:.1f}%")
print(f"Max P13/P11: {(P_13_bird/P11_bird).max()*100:.1f}%")
print(f"Max Ploop/P11: {(Ploop_bird/P11_bird).max()*100:.1f}%")
k_015_idx = np.argmin(np.abs(k_bird-0.15))
print(f"Ploop/P11 at k=0.15 h/Mpc: {(Ploop_bird/P11_bird)[k_015_idx]*100:.1f}%")

# Now interpolate all components to a consistent output k-grid
k_output = np.logspace(-2, np.log10(0.35), 150)  # k from 0.01 to 0.35 h/Mpc

# Interpolate to output grid
interp_P11 = interp1d(k_bird, P11_bird, kind='cubic', bounds_error=False, fill_value='extrapolate')
interp_P22 = interp1d(k_bird, P_22_bird, kind='cubic', bounds_error=False, fill_value='extrapolate')
interp_P13 = interp1d(k_bird, P_13_bird, kind='cubic', bounds_error=False, fill_value='extrapolate')
interp_Ploop = interp1d(k_bird, Ploop_bird, kind='cubic', bounds_error=False, fill_value='extrapolate')
interp_P1loop = interp1d(k_bird, P_1loop_bird, kind='cubic', bounds_error=False, fill_value='extrapolate')

# Apply interpolation
k = k_output
P11 = interp_P11(k)
P_22 = interp_P22(k)
P_13 = interp_P13(k)
Ploop = interp_Ploop(k)
P_1loop = interp_P1loop(k)
P_lin = P11

print(f"\nOutput k range: {k[0]:.3f} to {k[-1]:.3f} h/Mpc (shape: {k.shape})")
print(f"P_lin range: {P_lin.min():.1f} to {P_lin.max():.1f} (Mpc/h)^3")
print(f"Max 1-loop correction: {((Ploop/P_lin).max())*100:.1f}% at k={k[np.argmax(Ploop/P_lin)]:.3f} h/Mpc")
k_015_idx = np.argmin(np.abs(k-0.15))
print(f"Ploop/P_lin at k=0.15 h/Mpc: {(Ploop/P_lin)[k_015_idx]*100:.1f}%")

# Create figure with two subplots - square layout to match multiprobe animation
fig = plt.figure(figsize=(8, 8))
gs = fig.add_gridspec(2, 1, height_ratios=[2.2, 1.2], hspace=0.25)
ax_main = fig.add_subplot(gs[0])
ax_ratio = fig.add_subplot(gs[1])

# Set up main plot - adjust limits based on actual P(k)
P_min = min(P_lin.min(), P_1loop.min()) * 0.5
P_max = max(P_lin.max(), P_1loop.max()) * 2.0
k_min, k_max = k.min(), k.max()
ax_main.set_xlim(k_min, k_max)
ax_main.set_ylim(P_min, P_max)
ax_main.set_xscale('log')
ax_main.set_yscale('log')
ax_main.set_ylabel(r'$P(k)$ $[h^{-3}\,\mathrm{Mpc}^3]$', fontsize=14)
ax_main.set_xlabel(r'$k$ $[h\,\mathrm{Mpc}^{-1}]$', fontsize=14)
ax_main.grid(True, alpha=0.2, which='both')
ax_main.set_title('1-Loop SPT Power Spectrum (Dark Matter, Real Space)', 
                  fontsize=15, weight='bold', pad=15)

# Set up ratio plot
ax_ratio.set_xlim(k_min, k_max)
ax_ratio.set_ylim(-0.05, 0.50)
ax_ratio.set_xscale('log')
ax_ratio.set_xlabel(r'$k$ $[h\,\mathrm{Mpc}^{-1}]$', fontsize=14)
ax_ratio.set_ylabel(r'$\Delta P / P_{\mathrm{lin}}$', fontsize=13)
ax_ratio.grid(True, alpha=0.2, which='both')
ax_ratio.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Store line objects
lines = {}
text_objects = []
ratio_lines = {}

def animate(frame):
    """Animation function."""
    # Clear previous lines
    for line in lines.values():
        if line:
            line.remove()
    lines.clear()
    
    for line in ratio_lines.values():
        if line:
            line.remove()
    ratio_lines.clear()
    
    for text in text_objects:
        text.remove()
    text_objects.clear()
    
    if frame < 50:
        # Phase 1: Show linear power spectrum (P_11) - SLOWER
        alpha = min(frame / 30, 1.0)
        line, = ax_main.plot(k, P_lin, color='#2C3E50', linewidth=4, 
                            label=r'$P_{11}(k)$ [linear]', alpha=alpha)
        lines['linear'] = line
        
        # Add label with larger font
        text = ax_main.text(0.05, 0.95, r'Tree-level: $P_{11}(k)$ (linear matter power)',
                          transform=ax_main.transAxes, fontsize=14,
                          verticalalignment='top',
                          bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.85),
                          color='#2C3E50', weight='bold', alpha=alpha)
        text_objects.append(text)
        
        # Ratio plot
        ax_ratio.axhline(y=0, color='#2C3E50', linestyle='--', linewidth=2, alpha=alpha)
        
    elif frame < 110:
        # Phase 2: Add P_22 (bubble/box diagrams) - SLOWER
        line_lin, = ax_main.plot(k, P_lin, color='#2C3E50', linewidth=3.5, 
                                label=r'$P_{11}$', alpha=0.6)
        lines['linear'] = line_lin
        
        alpha = min((frame - 50) / 35, 1.0)
        line_22, = ax_main.plot(k, P_22, color='#E74C3C', linewidth=4, 
                               linestyle='--', label=r'$P_{22}(k)$', alpha=alpha)
        lines['p22'] = line_22
        
        # Combined so far
        P_so_far = P_lin + P_22
        line_combined, = ax_main.plot(k, P_so_far, color='#9B59B6', linewidth=4.5,
                                      label=r'$P_{11} + P_{22}$', alpha=alpha*0.8)
        lines['combined_22'] = line_combined
        
        # Labels - larger and clearer
        text1 = ax_main.text(0.05, 0.95, r'Adding $P_{22}(k)$ corrections',
                           transform=ax_main.transAxes, fontsize=14,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.85),
                           color='#E74C3C', weight='bold', alpha=alpha)
        text_objects.append(text1)
        
        text2 = ax_main.text(0.05, 0.87, r'(bubble & box diagrams)',
                           transform=ax_main.transAxes, fontsize=12,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.75),
                           alpha=alpha*0.9)
        text_objects.append(text2)
        
        # Ratio plot
        ratio_22 = P_22 / P_lin
        line_r22, = ax_ratio.plot(k, ratio_22, color='#E74C3C', linewidth=3,
                                 linestyle='--', label=r'$P_{22}/P_{11}$', alpha=alpha)
        ratio_lines['p22'] = line_r22
        
    elif frame < 150:
        # Phase 3: Add P_13 (triangle diagrams)
        line_lin, = ax_main.plot(k, P_lin, color='#2C3E50', linewidth=3, 
                                alpha=0.4)
        lines['linear'] = line_lin
        
        line_22, = ax_main.plot(k, P_22, color='#E74C3C', linewidth=3, 
                               linestyle='--', alpha=0.4)
        lines['p22'] = line_22
        
        alpha = min((frame - 110) / 25, 1.0)
        line_13, = ax_main.plot(k, P_13, color='#3498DB', linewidth=4,
                               linestyle='--', label=r'$P_{13}(k)$', alpha=alpha)
        lines['p13'] = line_13
        
        # Combined 1-loop (from PyBird)
        line_1loop, = ax_main.plot(k, P_1loop, color='#27AE60', linewidth=5,
                                  label=r'$P_{\mathrm{1-loop}}$', alpha=alpha*0.9)
        lines['1loop'] = line_1loop
        
        # Labels - larger and clearer
        text1 = ax_main.text(0.05, 0.95, r'Adding $P_{13}(k)$ corrections',
                           transform=ax_main.transAxes, fontsize=14,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.85),
                           color='#3498DB', weight='bold', alpha=alpha)
        text_objects.append(text1)
        
        text2 = ax_main.text(0.05, 0.87, r'(triangle diagrams)',
                           transform=ax_main.transAxes, fontsize=12,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan', alpha=0.75),
                           alpha=alpha*0.9)
        text_objects.append(text2)
        
        text3 = ax_main.text(0.05, 0.79, r'$P_{\mathrm{1-loop}} = P_{11} + P_{22} + 2P_{13}$',
                           transform=ax_main.transAxes, fontsize=12,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.75),
                           color='#27AE60', weight='bold', alpha=alpha*0.8)
        text_objects.append(text3)
        
        # Ratio plot
        ratio_22 = P_22 / P_lin
        ratio_13 = P_13 / P_lin
        ratio_total = Ploop / P_lin
        
        line_r22, = ax_ratio.plot(k, ratio_22, color='#E74C3C', linewidth=2,
                                 linestyle='--', alpha=0.4)
        ratio_lines['p22'] = line_r22
        
        line_r13, = ax_ratio.plot(k, ratio_13, color='#3498DB', linewidth=2.5,
                                 linestyle='--', alpha=alpha)
        ratio_lines['p13'] = line_r13
        
        line_rtotal, = ax_ratio.plot(k, ratio_total, color='#27AE60', linewidth=3.5,
                                    label=r'$P_{\mathrm{loop}}/P_{11}$', alpha=alpha*0.8)
        ratio_lines['total'] = line_rtotal
        
    else:
        # Phase 4: Show validity range
        line_lin, = ax_main.plot(k, P_lin, color='#2C3E50', linewidth=3, 
                                alpha=0.3, label=r'$P_{11}$')
        lines['linear'] = line_lin
        
        line_1loop, = ax_main.plot(k, P_1loop, color='#27AE60', linewidth=5,
                                  label=r'$P_{\mathrm{1-loop}}$ (PyBird)')
        lines['1loop'] = line_1loop
        
        
        # Show validity range (reduced opacity)
        alpha_shade = 0.01
        alpha_shade = min((frame - 105) / 20, 0.06)
        k_validity = min(0.25, k_max)
        ax_main.axvspan(k_min, k_validity, alpha=alpha_shade, color='green', zorder=1)
        ax_ratio.axvspan(k_min, k_validity, alpha=alpha_shade, color='green', zorder=1)
        
        alpha_text = min((frame - 105) / 20, 1.0)
        text1 = ax_main.text(0.05, 0.95, r'Valid range: $k \lesssim 0.25\,h\,\mathrm{Mpc}^{-1}$',
                           transform=ax_main.transAxes, fontsize=13,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                           color='#27AE60', weight='bold', alpha=alpha_text)
        text_objects.append(text1)
        
        text2 = ax_main.text(0.05, 0.87, r'Beyond: need higher loops, EFT counterterms and IR-resummation to fit to BAO',
                           transform=ax_main.transAxes, fontsize=11,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
                           alpha=alpha_text*0.8)
        text_objects.append(text2)
        
        # Ratio plot
        ratio_total = Ploop / P_lin
        line_rtotal, = ax_ratio.plot(k, ratio_total, color='#27AE60', linewidth=3,
                                     label=r'PyBird')
        ratio_lines['total'] = line_rtotal

        
        # Mark levels
        for level, label in [(0.1, '10%'), (0.2, '20%'), (0.3, '30%')]:
            ax_ratio.axhline(y=level, color='gray', linestyle=':', linewidth=1.5, 
                           alpha=alpha_text*0.5)
            if level == 0.2:
                text3 = ax_ratio.text(0.35, level+0.02, label,
                                    fontsize=10, color='gray', alpha=alpha_text*0.7)
                text_objects.append(text3)
    
    # Legend
    if frame > 35:
        ax_main.legend(loc='lower left', fontsize=10, framealpha=0.9)
    
    return list(lines.values()) + list(ratio_lines.values()) + text_objects

# Create animation - SLOWER with more frames and hold final frame
print("Generating animation...")
anim = FuncAnimation(fig, animate, frames=240, interval=70, blit=True)

# Save animation - hold final frames longer
writer = PillowWriter(fps=16)  # Slower frame rate for better readability
anim.save('eftoflss_oneloop.gif', writer=writer, dpi=100)
print("Animation saved as eftoflss_oneloop.gif")

plt.close()
print("Done!")

