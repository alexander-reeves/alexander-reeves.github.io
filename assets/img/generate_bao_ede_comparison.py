#!/usr/bin/env python3
"""
Generate a BAO animation comparing wave propagation with and without Early Dark Energy.
Shows side-by-side how EDE reduces the sound horizon at recombination.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import patches

# Create figure with two subplots (side by side)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='white')
for ax in [ax1, ax2]:
    ax.set_facecolor('white')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_aspect('equal')
    ax.axis('off')


# Subplot titles
title1 = ax1.text(0.5, 0.95, 'Standard ΛCDM',
                  transform=ax1.transAxes, ha='center', va='top',
                  fontsize=13, weight='bold', color='#2C7BB6')
title2 = ax2.text(0.5, 0.95, 'With Early Dark Energy',
                  transform=ax2.transAxes, ha='center', va='top',
                  fontsize=13, weight='bold', color='#E74C3C')

# Subtitles
subtitle1 = ax1.text(0.5, -0.05, '',
                     transform=ax1.transAxes, ha='center', va='bottom',
                     fontsize=9, color='#34495E')
subtitle2 = ax2.text(0.5, -0.05, '',
                     transform=ax2.transAxes, ha='center', va='bottom',
                     fontsize=9, color='#34495E')

# Speed of sound in baryon-photon plasma (in units of c)
c_s = 1.0 / np.sqrt(3.0)

# Sound horizon sizes
r_LCDM = 150.0      # Standard ΛCDM (Planck measurement)
r_EDE = 135.0       # With early dark energy (10 Mpc smaller)
reduction_pct = (1 - r_EDE/r_LCDM) * 100

# Visual scaling factor (makes circles smaller on screen without changing physics values)
visual_scale = 0.9

# Store objects to remove
objects_left = []
objects_right = []

def init():
    """Initialize animation"""
    return []

def draw_wave_pulse(ax, objects_list, r_pulse, pulse_width, t, color_map='Blues', edge_color='#2C7BB6'):
    """Draw a wave pulse with gradient effect"""
    n_rings = 5
    cmap = plt.colormaps[color_map]
    for i in range(n_rings):
        r_inner = r_pulse - pulse_width * (i / n_rings)
        r_outer = r_pulse - pulse_width * ((i + 1) / n_rings)
        
        if r_outer > 0:
            alpha = 0.5 * (1 - i / n_rings) * (1 - t * 0.3)
            color_val = 0.3 + 0.6 * (i / n_rings)
            
            ring = patches.Wedge((0, 0), r_outer, 0, 360, 
                                width=r_outer-max(0, r_inner),
                                facecolor=cmap(color_val),
                                edgecolor='none', alpha=alpha)
            ax.add_patch(ring)
            objects_list.append(ring)
    
    # Draw outer edge of pulse
    if r_pulse > 0:
        pulse_edge = patches.Circle((0, 0), r_pulse, fill=False,
                                   edgecolor=edge_color, linewidth=3,
                                   alpha=0.8)
        ax.add_patch(pulse_edge)
        objects_list.append(pulse_edge)

def draw_central_source(ax, objects_list, frame, phase):
    """Draw the central overdensity (source of perturbation)"""
    if phase == 'propagate':
        size = 40 * (1.0 + 0.15 * np.sin(2 * np.pi * frame / 15))
    else:
        size = 40
    
    central = patches.Circle((0, 0), 5, fill=True, facecolor='#F39C12',
                           edgecolor='#E67E22', linewidth=2, zorder=10)
    ax.add_patch(central)
    objects_list.append(central)

def animate(frame):
    """Animation function"""
    # Clear previous objects
    for obj in objects_left:
        obj.remove()
    for obj in objects_right:
        obj.remove()
    objects_left.clear()
    objects_right.clear()
    
    if frame < 100:
        # Phase 1: Both waves propagating outward
        t = frame / 100.0  # Normalized time 0 to 1
        
        # ΛCDM pulse (left)
        r_pulse_lcdm = t * r_LCDM
        pulse_width = 15.0
        draw_wave_pulse(ax1, objects_left, r_pulse_lcdm * visual_scale, pulse_width, t, 
                       'Blues', '#2C7BB6')
        draw_central_source(ax1, objects_left, frame, 'propagate')
        
        # EDE pulse (right) - propagates to smaller radius
        r_pulse_ede = t * r_EDE
        draw_wave_pulse(ax2, objects_right, r_pulse_ede * visual_scale, pulse_width, t,
                       'Reds', '#E74C3C')
        draw_central_source(ax2, objects_right, frame, 'propagate')
        
        # Update subtitles
        subtitle1.set_text(f'Acoustic wave propagating\n$r_s$ = {r_pulse_lcdm:.1f} Mpc')
        subtitle2.set_text(f'Faster expansion → smaller $r_s$\n$r_s$ = {r_pulse_ede:.1f} Mpc')
        
    elif frame < 120:
        # Phase 2: Freeze-out (recombination)
        fade_in = (frame - 100) / 20.0
        
        # ΛCDM frozen pulse (left)
        frozen_lcdm = patches.Circle((0, 0), r_LCDM * visual_scale, fill=False,
                                    edgecolor='#2C7BB6', linewidth=4,
                                    alpha=fade_in * 0.9)
        ax1.add_patch(frozen_lcdm)
        objects_left.append(frozen_lcdm)
        
        # Subtle interior rings for ΛCDM
        for i in range(4):
            r_shade = r_LCDM * visual_scale * (1 - 0.2 * i)
            shade = patches.Circle((0, 0), r_shade, fill=False,
                                  edgecolor='#2C7BB6', linewidth=1.5,
                                  alpha=fade_in * 0.2 * (1 - 0.2 * i))
            ax1.add_patch(shade)
            objects_left.append(shade)
        
        draw_central_source(ax1, objects_left, frame, 'frozen')
        
        # EDE frozen pulse (right)
        frozen_ede = patches.Circle((0, 0), r_EDE * visual_scale, fill=False,
                                   edgecolor='#E74C3C', linewidth=4,
                                   alpha=fade_in * 0.9)
        ax2.add_patch(frozen_ede)
        objects_right.append(frozen_ede)
        
        # Subtle interior rings for EDE
        for i in range(4):
            r_shade = r_EDE * visual_scale * (1 - 0.2 * i)
            shade = patches.Circle((0, 0), r_shade, fill=False,
                                  edgecolor='#E74C3C', linewidth=1.5,
                                  alpha=fade_in * 0.2 * (1 - 0.2 * i))
            ax2.add_patch(shade)
            objects_right.append(shade)
        
        draw_central_source(ax2, objects_right, frame, 'frozen')
        
        # Update subtitles
        subtitle1.set_text('Recombination: oscillations freeze\nSound horizon $r_s$ ≈ 150 Mpc')
        subtitle2.set_text('Same recombination redshift\nBut sound horizon $r_s$ ≈ 135 Mpc')
        
    else:
        # Phase 3: Show side-by-side comparison with overlay
        progress = min(1.0, (frame - 120) / 30.0)
        
        # === LEFT PANEL: Show both horizons overlaid ===
        # ΛCDM (solid blue)
        lcdm_circle = patches.Circle((0, 0), r_LCDM * visual_scale, fill=False,
                                    edgecolor='#2C7BB6', linewidth=4,
                                    alpha=0.9)
        ax1.add_patch(lcdm_circle)
        objects_left.append(lcdm_circle)
        
        # Add EDE circle to left panel for comparison
        if progress > 0.3:
            ede_alpha = min(1.0, (progress - 0.3) / 0.3)
            ede_circle_left = patches.Circle((0, 0), r_EDE * visual_scale, fill=False,
                                            edgecolor='#E74C3C', linewidth=3,
                                            alpha=ede_alpha * 0.7, linestyle='--')
            ax1.add_patch(ede_circle_left)
            objects_left.append(ede_circle_left)
            
            # Shaded region showing reduction
            reduction_wedge = patches.Wedge((0, 0), r_LCDM * visual_scale, -30, 60,
                                          width=(r_LCDM - r_EDE) * visual_scale,
                                          facecolor='#E74C3C',
                                          alpha=ede_alpha * 0.15,
                                          edgecolor='none')
            ax1.add_patch(reduction_wedge)
            objects_left.append(reduction_wedge)
        
        # Add dimension lines showing the difference - placed at bottom for clarity
        if progress > 0.6:
            arrow_alpha = min(1.0, (progress - 0.6) / 0.3)
            
            # Vertical position at bottom (scaled)
            y_pos = -r_LCDM * visual_scale - 20
            
            # Draw dimension lines (architectural style)
            # Line extending from LCDM circle
            line1 = plt.Line2D([r_LCDM * visual_scale, r_LCDM * visual_scale], 
                              [-r_LCDM * visual_scale - 5, y_pos], 
                              color='#2C7BB6', linewidth=1.5, alpha=arrow_alpha)
            ax1.add_line(line1)
            objects_left.append(line1)
            
            # Line extending from EDE circle  
            line2 = plt.Line2D([r_EDE * visual_scale, r_EDE * visual_scale], 
                              [-r_EDE * visual_scale - 5, y_pos],
                              color='#E74C3C', linewidth=1.5, alpha=arrow_alpha, linestyle='--')
            ax1.add_line(line2)
            objects_left.append(line2)
            
            # Horizontal dimension arrow between them
            arrow = patches.FancyArrowPatch((r_EDE * visual_scale, y_pos), 
                                           (r_LCDM * visual_scale, y_pos),
                                           arrowstyle='<->', mutation_scale=15,
                                           color='#E74C3C', linewidth=2,
                                           alpha=arrow_alpha)
            ax1.add_patch(arrow)
            objects_left.append(arrow)
            
            # Clean label showing the difference
            arrow_label = ax1.text((r_LCDM + r_EDE) / 2 * visual_scale, y_pos - 10, 
                                  f'{int(r_LCDM - r_EDE)} Mpc',
                                  ha='center', va='top', fontsize=11,
                                  color='#E74C3C', weight='bold',
                                  alpha=arrow_alpha)
            objects_left.append(arrow_label)
            
        
        draw_central_source(ax1, objects_left, frame, 'frozen')
        
        # === RIGHT PANEL: Show EDE only ===
        ede_circle = patches.Circle((0, 0), r_EDE * visual_scale, fill=False,
                                   edgecolor='#E74C3C', linewidth=4,
                                   alpha=0.9)
        ax2.add_patch(ede_circle)
        objects_right.append(ede_circle)
        
        # Add ΛCDM ghost for reference
        if progress > 0.3:
            ghost_alpha = min(1.0, (progress - 0.3) / 0.3) * 0.3
            lcdm_ghost = patches.Circle((0, 0), r_LCDM * visual_scale, fill=False,
                                       edgecolor='#2C7BB6', linewidth=2,
                                       alpha=ghost_alpha, linestyle=':')
            ax2.add_patch(lcdm_ghost)
            objects_right.append(lcdm_ghost)
        
        draw_central_source(ax2, objects_right, frame, 'frozen')
        
        # Update subtitles
        if progress < 0.5:
            subtitle1.set_text('Standard cosmology (Planck)\n$r_s$ ≈ 150 Mpc (solid)')
            subtitle2.set_text('With early dark energy\n$r_s$ ≈ 135 Mpc')
        else:
            subtitle1.set_text('EDE increases expansion rate\n→ less time for sound to travel')
            subtitle2.set_text('~15 Mpc reduction\nobservable in BAO measurements')
    
    return objects_left + objects_right + [subtitle1, subtitle2]

# Create animation
print("Generating BAO EDE comparison animation...")
anim = FuncAnimation(fig, animate, init_func=init, frames=200,
                    interval=60, blit=True)

# Save animation
writer = PillowWriter(fps=18)
anim.save('bao_ede_comparison.gif', writer=writer, dpi=100)
print("Animation saved as bao_ede_comparison.gif")

plt.close()
print("Done!")
print(f"\nThis animation shows:")
print(f"  • Sound horizon in ΛCDM: {r_LCDM:.0f} Mpc")
print(f"  • Sound horizon with EDE: {r_EDE:.0f} Mpc")
print(f"  • Reduction: {reduction_pct:.1f}%")

