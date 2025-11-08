---
title: EFTofLSS galaxy clustering
layout: page
img: /assets/img/eftoflss_oneloop.gif
description: Full-shape clustering with EFTofLSS using modern differentiable tooling (PyBird-JAX).
---

I work on full-shape galaxy clustering using the Effective Field Theory of Large-Scale Structure (EFTofLSS). Together with my collaborators Pierre Zhang and Henry Zheng, we built [`PyBird-JAX`](https://arxiv.org/abs/2507.20990): a JAX-based version of PyBird that enables rapid computation of the 1-loop galaxy power spectrum under EFTofLSS modelling. The code leverages just-in-time compilation, automatic differentiation, and neural network emulation of slow internal loops to achieve significant speedups over traditional implementations.

This framework has enabled new analyses, including a study of [volume projection effects in EFTofLSS inference](https://arxiv.org/abs/2507.20991), where we showed how projection effects can introduce systematic biases in parameter estimation and developed methods to correct for them using information geometry.

---

### Volume projection effects in EFTofLSS

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/measure_desi_w0wa.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <strong>Measuring dark energy with DESI:</strong> Forecasted constraints on the dark energy equation of state parameters (w₀, wₐ) from DESI Year 1 full-shape galaxy clustering analysis using PyBird-JAX. The analysis accounts for volume projection effects that can bias cosmological parameter inference when fitting EFTofLSS models to survey data. From Reeves et al. (2025c).
</div> 
