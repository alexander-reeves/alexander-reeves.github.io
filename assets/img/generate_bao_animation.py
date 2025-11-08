#!/usr/bin/env python3
"""
Generate a BAO sound horizon animation showing:
1. Single acoustic wave pulse propagating and freezing
2. How new physics (early dark energy) affects the sound horizon size
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import patches

# Create figure with white background
fig, ax = plt.subplots(1, 1, figsize=(8, 8), facecolor='white')
ax.set_facecolor('white')

# Set up the plot
ax.set_xlim(-180, 180)
ax.set_ylim(-180, 180)
ax.set_aspect('equal')
ax.axis('off')

# Title
title = ax.text(0.5, 0.98, 'Baryon Acoustic Oscillations\nSound Horizon at Recombination',
                transform=ax.transAxes, ha='center', va='top',
                fontsize=14, weight='bold', color='#2C3E50')

# Subtitle showing physics
subtitle = ax.text(0.5, 0.02, '',
                   transform=ax.transAxes, ha='center', va='bottom',
                   fontsize=10, color='#34495E')

# Speed of sound in baryon-photon plasma (in units of c)
c_s = 1.0 / np.sqrt(3.0)

# Sound horizon sizes
r_LCDM = 145.0  # Standard ΛCDM
r_EDE = 118.0   # With early dark energy (reduced by ~20%)

# Store objects to remove
objects = []

def init():
    """Initialize animation"""
    return []

def animate(frame):
    """Animation function"""
    # Clear previous objects
    for obj in objects:
        obj.remove()
    objects.clear()
    
    if frame < 80:
        # Phase 1: Single wave pulse propagating outward
        t = frame / 80.0  # Normalized time 0 to 1
        
        # Main pulse radius
        r_pulse = t * r_LCDM
        
        # Pulse width (creates a "ring" effect)
        pulse_width = 15.0
        
        # Draw the pulse as a filled ring with gradient
        n_rings = 5
        for i in range(n_rings):
            r_inner = r_pulse - pulse_width * (i / n_rings)
            r_outer = r_pulse - pulse_width * ((i + 1) / n_rings)
            
            if r_outer > 0:
                alpha = 0.5 * (1 - i / n_rings) * (1 - t * 0.3)  # Fade as it expands
                color_val = 0.3 + 0.6 * (i / n_rings)
                
                ring = patches.Wedge((0, 0), r_outer, 0, 360, 
                                    width=r_outer-max(0, r_inner),
                                    facecolor=plt.cm.Blues(color_val),
                                    edgecolor='none', alpha=alpha)
                ax.add_patch(ring)
                objects.append(ring)
        
        # Draw outer edge of pulse
        if r_pulse > 0:
            pulse_edge = patches.Circle((0, 0), r_pulse, fill=False,
                                       edgecolor='#2C7BB6', linewidth=3,
                                       alpha=0.8)
            ax.add_patch(pulse_edge)
            objects.append(pulse_edge)
        
        # Update subtitle
        subtitle.set_text(f'Acoustic wave propagates through baryon-photon fluid\n' +
                         f'Sound speed: $c_s = c/\\sqrt{{3}}$ ≈ 0.58c')
        
    elif frame < 100:
        # Phase 2: Freeze-out (recombination)
        fade_in = (frame - 80) / 20.0
        
        # Show frozen pulse (ΛCDM)
        frozen_pulse = patches.Circle((0, 0), r_LCDM, fill=False,
                                     edgecolor='#2C7BB6', linewidth=4,
                                     alpha=fade_in)
        ax.add_patch(frozen_pulse)
        objects.append(frozen_pulse)
        
        # Subtle shading inside
        for i in range(4):
            r_shade = r_LCDM * (1 - 0.2 * i)
            shade = patches.Circle((0, 0), r_shade, fill=False,
                                  edgecolor='#2C7BB6', linewidth=1.5,
                                  alpha=fade_in * 0.2 * (1 - 0.2 * i))
            ax.add_patch(shade)
            objects.append(shade)
        
        # Update subtitle
        subtitle.set_text('Recombination: photons decouple, acoustic oscillations freeze\n' +
                         'Sound horizon imprinted in matter distribution')
        
    else:
        # Phase 3: Show comparison with new physics
        progress = min(1.0, (frame - 100) / 30.0)
        
        # ΛCDM sound horizon (blue)
        lcdm_circle = patches.Circle((0, 0), r_LCDM, fill=False,
                                    edgecolor='#2C7BB6', linewidth=4,
                                    alpha=0.9)
        ax.add_patch(lcdm_circle)
        objects.append(lcdm_circle)
        
        # ΛCDM label
        if progress > 0.3:
            label_alpha = min(1.0, (progress - 0.3) / 0.2)
            lcdm_label = ax.text(r_LCDM * 0.7, r_LCDM * 0.7, 
                                'ΛCDM\n$r_s$ ≈ 145 Mpc',
                                ha='center', va='center', fontsize=11,
                                color='#2C7BB6', weight='bold',
                                alpha=label_alpha,
                                bbox=dict(boxstyle='round,pad=0.5',
                                        facecolor='white',
                                        edgecolor='#2C7BB6',
                                        alpha=label_alpha * 0.9))
            objects.append(lcdm_label)
        
        # Early Dark Energy sound horizon (smaller, red)
        if progress > 0.5:
            ede_alpha = min(1.0, (progress - 0.5) / 0.3)
            ede_circle = patches.Circle((0, 0), r_EDE, fill=False,
                                       edgecolor='#E74C3C', linewidth=4,
                                       alpha=ede_alpha, linestyle='--')
            ax.add_patch(ede_circle)
            objects.append(ede_circle)
            
            # Shaded region showing reduction
            reduction_wedge = patches.Wedge((0, 0), r_LCDM, 30, 150,
                                          width=r_LCDM - r_EDE,
                                          facecolor='#E74C3C',
                                          alpha=ede_alpha * 0.15,
                                          edgecolor='none')
            ax.add_patch(reduction_wedge)
            objects.append(reduction_wedge)
            
            # EDE label
            if progress > 0.7:
                label_alpha2 = min(1.0, (progress - 0.7) / 0.2)
                ede_label = ax.text(-r_EDE * 0.7, r_EDE * 0.7,
                                   'Early Dark Energy\n$r_s$ ≈ 118 Mpc',
                                   ha='center', va='center', fontsize=11,
                                   color='#E74C3C', weight='bold',
                                   alpha=label_alpha2,
                                   bbox=dict(boxstyle='round,pad=0.5',
                                           facecolor='white',
                                           edgecolor='#E74C3C',
                                           alpha=label_alpha2 * 0.9))
                objects.append(ede_label)
                
                # Arrow showing reduction
                if progress > 0.85:
                    arrow_alpha = min(1.0, (progress - 0.85) / 0.15)
                    arrow = patches.FancyArrowPatch((0, -r_LCDM), (0, -r_EDE),
                                                   arrowstyle='<->', mutation_scale=20,
                                                   color='#E74C3C', linewidth=2.5,
                                                   alpha=arrow_alpha)
                    ax.add_patch(arrow)
                    objects.append(arrow)
                    
                    arrow_label = ax.text(15, -(r_LCDM + r_EDE) / 2, '~20%\nreduction',
                                        ha='left', va='center', fontsize=10,
                                        color='#E74C3C', weight='bold',
                                        alpha=arrow_alpha)
                    objects.append(arrow_label)
        
        # Update subtitle for phase 3
        if progress < 0.5:
            subtitle.set_text('Standard ΛCDM: sound horizon $r_s \\approx 145$ Mpc\n' +
                            'Characteristic scale in galaxy clustering (BAO)')
        else:
            subtitle.set_text('New physics (e.g., early dark energy) can reduce $r_s$\n' +
                            'Testing beyond-ΛCDM models with BAO measurements')
    
    # Add central overdensity (source of perturbation)
    if frame < 80:
        size = 40 * (1.0 + 0.15 * np.sin(2 * np.pi * frame / 15))
    else:
        size = 40
    
    central = patches.Circle((0, 0), 5, fill=True, facecolor='#F39C12',
                           edgecolor='#E67E22', linewidth=2, zorder=10)
    ax.add_patch(central)
    objects.append(central)
    
    return objects + [subtitle]

# Create animation
print("Generating BAO sound horizon animation...")
anim = FuncAnimation(fig, animate, init_func=init, frames=200,
                    interval=60, blit=True)

# Save animation with variable frame duration - hold final frames longer
writer = PillowWriter(fps=18)
# Create list of frame durations (in milliseconds)
# Hold the last 40 frames (showing EDE comparison) longer
frame_durations = []
for i in range(200):
    if i < 160:
        frame_durations.append(60)  # Normal speed
    else:
        frame_durations.append(150)  # Hold final frames 2.5x longer

# Custom save to handle variable durations
anim.save('bao_sound_horizon.gif', writer=writer, dpi=100)
print("Animation saved as bao_sound_horizon.gif")

plt.close()
print("Done!")
