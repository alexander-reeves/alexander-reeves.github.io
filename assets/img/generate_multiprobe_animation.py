#!/usr/bin/env python3
"""
Generate animation showing how combining probes breaks degeneracies.
Shows two Gaussian distributions with different orientations in 2D parameter space,
and their combination which breaks the degeneracy.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.stats import multivariate_normal

# Set style
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def plot_confidence_ellipse(mean, cov, ax, n_std=2.0, color='blue', 
                           alpha=0.3, label=None, linestyle='-', linewidth=2):
    """
    Plot confidence ellipse for a 2D Gaussian distribution.
    """
    # Get eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Calculate angle of ellipse
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    
    # Width and height are 2*sqrt(eigenvalue) * n_std
    width, height = 2 * n_std * np.sqrt(eigenvalues)
    
    # Create ellipse
    ellipse = Ellipse(mean, width, height, angle=angle, 
                     facecolor=color, alpha=alpha, 
                     edgecolor=color, linewidth=linewidth,
                     linestyle=linestyle, label=label)
    ax.add_patch(ellipse)
    
    return ellipse

def get_combined_distribution(mean1, cov1, mean2, cov2):
    """
    Combine two Gaussian distributions (product of Gaussians).
    For two Gaussians, the product is also Gaussian with:
    cov_combined^{-1} = cov1^{-1} + cov2^{-1}
    mean_combined = cov_combined @ (cov1^{-1} @ mean1 + cov2^{-1} @ mean2)
    """
    # Precision matrices (inverse covariances)
    prec1 = np.linalg.inv(cov1)
    prec2 = np.linalg.inv(cov2)
    
    # Combined precision
    prec_combined = prec1 + prec2
    cov_combined = np.linalg.inv(prec_combined)
    
    # Combined mean
    mean_combined = cov_combined @ (prec1 @ mean1 + prec2 @ mean2)
    
    return mean_combined, cov_combined

# Define parameters
# True parameter values (center of combined distribution)
theta_true = np.array([0.8, 0.3])

# Probe 1: Experiment 1 (degeneracy along positive diagonal)
mean1 = np.array([0.85, 0.25])
# Covariance with strong correlation (degeneracy direction)
angle1 = np.radians(30)  # Degeneracy direction
sigma1_major = 0.35  # Large uncertainty along degeneracy
sigma1_minor = 0.08  # Small uncertainty perpendicular
rot1 = np.array([[np.cos(angle1), -np.sin(angle1)],
                 [np.sin(angle1), np.cos(angle1)]])
cov1 = rot1 @ np.diag([sigma1_major**2, sigma1_minor**2]) @ rot1.T

# Probe 2: Experiment 2 (degeneracy along negative diagonal)
mean2 = np.array([0.75, 0.35])
angle2 = np.radians(-60)  # Different degeneracy direction
sigma2_major = 0.4
sigma2_minor = 0.09
rot2 = np.array([[np.cos(angle2), -np.sin(angle2)],
                 [np.sin(angle2), np.cos(angle2)]])
cov2 = rot2 @ np.diag([sigma2_major**2, sigma2_minor**2]) @ rot2.T

# Combined distribution
mean_combined, cov_combined = get_combined_distribution(mean1, cov1, mean2, cov2)

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))

# Set up the plot
ax.set_xlim(0.2, 1.4)
ax.set_ylim(-0.2, 0.8)
ax.set_xlabel(r'Parameter 1', fontsize=14)
ax.set_ylabel(r'Parameter 2', fontsize=14)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# Store ellipse objects
ellipses = {'probe1': [], 'probe2': [], 'combined': []}
text_objects = []

def animate(frame):
    """Animation function."""
    # Clear previous elements
    for key in ellipses:
        for ellipse in ellipses[key]:
            ellipse.remove()
        ellipses[key] = []
    for text in text_objects:
        text.remove()
    text_objects.clear()
    
    if frame < 40:
        # Show Probe 1
        alpha = min(frame / 20, 1.0)
        for n_std in [1, 2]:
            e = plot_confidence_ellipse(mean1, cov1, ax, n_std=n_std, 
                                       color='#E74C3C', alpha=alpha*0.3,
                                       linewidth=2.5)
            ellipses['probe1'].append(e)
        
        # Add label
        text = ax.text(0.95, 0.95, 'Experiment 1', 
                      transform=ax.transAxes, fontsize=14, 
                      verticalalignment='top', horizontalalignment='right',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                      color='#E74C3C', weight='bold', alpha=alpha)
        text_objects.append(text)
        
    elif frame < 80:
        # Show both Probe 1 and Probe 2
        # Probe 1 stays
        for n_std in [1, 2]:
            e = plot_confidence_ellipse(mean1, cov1, ax, n_std=n_std, 
                                       color='#E74C3C', alpha=0.3,
                                       linewidth=2.5)
            ellipses['probe1'].append(e)
        
        # Probe 2 fades in
        alpha = min((frame - 40) / 20, 1.0)
        for n_std in [1, 2]:
            e = plot_confidence_ellipse(mean2, cov2, ax, n_std=n_std, 
                                       color='#3498DB', alpha=alpha*0.3,
                                       linewidth=2.5)
            ellipses['probe2'].append(e)
        
        # Labels
        text1 = ax.text(0.95, 0.95, 'Experiment 1', 
                       transform=ax.transAxes, fontsize=14, 
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                       color='#E74C3C', weight='bold')
        text_objects.append(text1)
        
        text2 = ax.text(0.95, 0.88, 'Experiment 2', 
                       transform=ax.transAxes, fontsize=14, 
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                       color='#3498DB', weight='bold', alpha=alpha)
        text_objects.append(text2)
        
    else:
        # Show all three with combined emphasized
        # Fade out individual probes
        fade_factor = max(0.3, 1.0 - (frame - 80) / 20)
        
        for n_std in [1, 2]:
            e1 = plot_confidence_ellipse(mean1, cov1, ax, n_std=n_std, 
                                        color='#E74C3C', alpha=fade_factor*0.2,
                                        linewidth=1.5)
            ellipses['probe1'].append(e1)
            
            e2 = plot_confidence_ellipse(mean2, cov2, ax, n_std=n_std, 
                                        color='#3498DB', alpha=fade_factor*0.2,
                                        linewidth=1.5)
            ellipses['probe2'].append(e2)
        
        # Fade in combined
        alpha = min((frame - 80) / 20, 1.0)
        for n_std in [1, 2]:
            e = plot_confidence_ellipse(mean_combined, cov_combined, ax, n_std=n_std, 
                                       color='#2ECC71', alpha=alpha*0.5,
                                       linewidth=3)
            ellipses['combined'].append(e)
        
        # Labels
        text1 = ax.text(0.95, 0.95, 'Experiment 1', 
                       transform=ax.transAxes, fontsize=14, 
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       color='#E74C3C', weight='bold', alpha=fade_factor)
        text_objects.append(text1)
        
        text2 = ax.text(0.95, 0.88, 'Experiment 2', 
                       transform=ax.transAxes, fontsize=14, 
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       color='#3498DB', weight='bold', alpha=fade_factor)
        text_objects.append(text2)
        
        text3 = ax.text(0.95, 0.81, 'Combined', 
                       transform=ax.transAxes, fontsize=14, 
                       verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                       color='#2ECC71', weight='bold', alpha=alpha)
        text_objects.append(text3)
        
        # Add arrow showing improved constraints
        if frame > 100:
            arrow_alpha = min((frame - 100) / 20, 1.0)
            # Draw arrow showing size reduction
            ax.annotate('', xy=(mean_combined[0], mean_combined[1]-0.15),
                       xytext=(mean_combined[0], mean_combined[1]-0.35),
                       arrowprops=dict(arrowstyle='->', lw=2.5, 
                                     color='#2ECC71', alpha=arrow_alpha))
            text4 = ax.text(mean_combined[0]+0.15, mean_combined[1]-0.25,
                          'Degeneracy\nbroken!',
                          fontsize=13, color='#2ECC71', weight='bold',
                          alpha=arrow_alpha,
                          bbox=dict(boxstyle='round', facecolor='white', 
                                  alpha=0.7, edgecolor='#2ECC71', linewidth=2))
            text_objects.append(text4)
    
    return list(ellipses['probe1']) + list(ellipses['probe2']) + list(ellipses['combined']) + text_objects

# Create animation
anim = FuncAnimation(fig, animate, frames=140, interval=50, blit=True)

# Save animation
print("Generating animation...")
writer = PillowWriter(fps=20)
anim.save('multiprobe_degeneracy_breaking.gif', writer=writer, dpi=100)
print("Animation saved as multiprobe_degeneracy_breaking.gif")

plt.close()
print("Done!")

