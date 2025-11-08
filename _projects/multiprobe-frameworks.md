---
title: Multiprobe frameworks
layout: page
img: /assets/img/multiprobe_degeneracy_breaking.gif
description: End-to-end, differentiable pipelines combining CMB and LSS probes for robust cosmology.
importance: 1
---

During my PhD, I built an end-to-end, differentiable pipeline that combines multiple cosmological probes—weak lensing, galaxy clustering, BAO, CMB primary anisotropies, integrated Sachs-Wolfe effect, and CMB lensing—in a single, self-consistent inference framework. This includes simulation-based covariances, fast emulators, and cross-correlation measurements to maximise information while controlling systematics across datasets.

The pipeline was first developed and validated on mock data in [Reeves et al. (2024)](https://arxiv.org/abs/2309.03258), then applied to real data in [Reeves et al. (2025a)](https://arxiv.org/abs/2502.01722), where we explored neutrino mass constraints and dynamical dark energy. Most recently, the framework has been extended to DESI Legacy Imaging Survey data in [Reeves et al. (2025b)](https://arxiv.org/abs/2510.06114), where we compared early and late-time dark energy models. 

---

### Pipeline overview

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/pipeline_diagram.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <strong>Multiprobe pipeline architecture:</strong> Schematic showing the end-to-end framework combining simulations, theory predictions, and observational data across multiple cosmological probes. The pipeline uses simulation-based covariances and fast emulators to enable joint inference across CMB and LSS datasets.
</div>

### Subset of pipeline spectra

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/data_vs_theory.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <strong>Measured data vector:</strong> Cross-correlations between DESI Legacy Imaging Survey (galaxy positions and shapes) with CMB lensing and the integrated Sachs-Wolfe (ISW) effect. The theory prediction (red) shows excellent agreement with the measured data (black points). From Reeves et al. (2025b).
</div>

