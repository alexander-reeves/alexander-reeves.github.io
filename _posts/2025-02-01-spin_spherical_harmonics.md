---
layout: post
title: Understanding Spin Spherical Harmonics in Cosmology
date: 2025-02-01 09:00:00
description: A deep dive into the mathematics of spin spherical harmonics and their applications in cosmology
tags: [math, cosmology, weak-lensing]
---

When we look at the sky, we see various cosmic fields painted on the celestial sphere. Some of these fields are simpler than others - they're just about measuring how bright or hot something is at each point. But others have a more complex geometric nature, involving orientations and patterns that rotate with our viewing perspective. These are spin fields and can be decomposed into "spin-weighted spherical harmonics" that respect U(1) symmetry. These are concepts that I was introduced to early on in my PhD and I felt as though there was not a clear reference describing their mathemtical properties. Here is my attempt to formalize the maths behind these fields and show that it is really no different to what physicists are used to from quantum mechanics.

## What is a "spin field"?

The "spin" of a field is associted with how the field transforms under a rotation of coordinates. Let's start with some familiar examples:

1. **Spin-0 Fields**: The simplest cosmic fields are scalar fields, which have no preferred direction. The cosmic microwave background (CMB) temperature is an example - at each point on the sky, we just measure a single number representing the temperature. When we rotate our coordinate system, these measurements don't change.

2. **Spin-2 Fields**: Now consider cosmic shear from weak gravitational lensing. When we observe distant galaxies, their shapes are distorted by the gravitational effects of matter along the line of sight. This distortion has both a magnitude (how much the galaxy image is distorted) and a direction (the axis along which the stretching occurs). The crucial part: if we rotate our coordinate system by an angle ψ, the measured shear components transform with a factor of e^{2iψ}. This factor of 2 in the exponential is why we call it a spin-2 field.

## Mathematical Description

To describe these fields mathematically, we need spin spherical harmonics. Regular (spin-0) spherical harmonics $$Y_{lm}(\theta,\phi)$$ are a failar concept, but for spin-s fields, we need their generalization, $$_{s}Y_{lm}(\theta,\phi)$$.

The spin-weighted spherical harmonics satisfy:
$$
\eth \,_{s}Y_{lm} = \sqrt{(l-s)(l+s+1)}\,_{s+1}Y_{lm}
$$
$$
\bar{\eth} \,_{s}Y_{lm} = -\sqrt{(l+s)(l-s+1)}\,_{s-1}Y_{lm}
$$

where $$\eth$$ and $$\bar{\eth}$$ are the spin-raising and spin-lowering operators respectively. These operators are the spherical analogs of quantum mechanical ladder operators, and they help us understand how to move between different spin states.

## The Spin Raising and Lowering Operators

The explicit form of these operators in spherical coordinates is:
$$
\eth = -\sin^s\theta\left(\frac{\partial}{\partial\theta} + \frac{i}{\sin\theta}\frac{\partial}{\partial\phi}\right)\sin^{-s}\theta
$$
$$
\bar{\eth} = -\sin^{-s}\theta\left(\frac{\partial}{\partial\theta} - \frac{i}{\sin\theta}\frac{\partial}{\partial\phi}\right)\sin^{s}\theta
$$

These might look intimidating, but they're deeply connected to something familiar from quantum mechanics: angular momentum operators.

## Connection to Quantum Mechanics

The similarity to quantum mechanics isn't coincidental. Just as the angular momentum raising and lowering operators $$L_±$$ help us navigate between different angular momentum states, $$\eth$$ and $$\bar{\eth}$$ help us move between different spin states. In fact, we can write:

$$
L_± = L_x \pm iL_y
$$

which is analogous to how we construct spin operators from the directional derivatives on the sphere.

## Application to Cosmic Shear

For weak lensing, we typically work with spin-2 fields. The shear field $$\gamma(\theta,\phi)$$ can be decomposed into E-modes and B-modes:

$$
\gamma(\theta,\phi) = \sum_{lm} (E_{lm} + iB_{lm})\, _{2}Y_{lm}(\theta,\phi)
$$

This decomposition is crucial because:
1. E-modes are created by gravitational lensing (to first order)
2. B-modes should be zero in the absence of systematics
3. This provides a powerful way to check for systematic errors in our measurements

## Visualizing Spin Fields

To understand spin fields visually:
- Spin-0: Think of a temperature map, where each point just has a value
- Spin-1: Think of a vector field, like wind directions on a weather map
- Spin-2: Think of headless vectors or ellipses, like the shapes of galaxies in a weak lensing map

<!-- <div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/spin_fields.jpg" class="img-fluid rounded z-depth-1" zoomable=true caption="Visualization of different spin fields on the sphere. Left: Spin-0 (temperature). Center: Spin-1 (vectors). Right: Spin-2 (ellipses)." %}
    </div>
</div> -->

## Practical Implementation

In practice, computing spin spherical harmonics involves:
1. Starting with regular spherical harmonics
2. Applying spin raising/lowering operators numerically
3. Using recursion relations for efficiency

Popular codes like `healpy` implement these calculations efficiently, allowing us to work with full-sky maps of spin-2 fields.

## Conclusion

Spin spherical harmonics provide the mathematical framework needed to properly analyze geometric fields on the sky. While the mathematics can seem daunting, the underlying concepts connect beautifully to quantum mechanics and provide powerful tools for modern cosmological analysis.

In future posts, we'll explore how these concepts apply to specific analyses in weak lensing and what we can learn about the universe from these measurements.
