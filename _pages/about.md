---
layout: about
title: about
permalink: /
subtitle: Cosmologist · University of Oxford

hero:
  image: hero_mayall.jpg
  alt: The Nicholas U. Mayall 4-metre Telescope at Kitt Peak beneath the Milky Way
  tagline: Combining galaxy surveys and the CMB to work out what the Universe is made of.
  credit: DESI Collaboration/DOE/KPNO/NOIRLab/NSF/AURA/P. Horálek (Institute of Physics in Opava)

profile:
  align: right
  image: profile_pic.jpg
  image_circular: false
  caption: Kitt Peak, during a DESI support observer shift — February 2025.
  more_info: >
    <p>Denys Wilkinson Building</p>
    <p>Keble Road, Oxford OX1 3RH</p>
    <p>alexcharlesreeves@gmail.com</p>

selected_papers: true
social: true
---

I'm a cosmologist at Oxford, here on an SNSF Postdoc.Mobility fellowship.

Most of what I do comes down to squeezing more out of data we already have. Galaxy surveys and the cosmic microwave background measure overlapping things, and analysing them together breaks degeneracies that neither can break on its own. The catch is that you have to model both consistently, all the way through, and that turns out to be most of the work. I spent my PhD building a [pipeline that does it end to end]({{ '/projects/multiprobe-frameworks/' | relative_url }}) — weak lensing, galaxy clustering, BAO, the ISW effect, CMB lensing — and a good deal of time since worrying about the places it could quietly go wrong.

Those places are usually not where you expect. Covariance matrices estimated from too few simulations. Emulators that are accurate on average and badly wrong in the corner of parameter space you care about. [Volume projection effects](https://arxiv.org/abs/2507.20991) that shift a posterior by a fraction of a sigma, which is small until it isn't. A result can move as much from any of these as from the data themselves, which I find both annoying and genuinely interesting.

More recently I've been working on the theory side, on [`PyBird-JAX`](https://arxiv.org/abs/2507.20990) — an EFTofLSS code fast and differentiable enough that you can explore the model space properly instead of one cosmology at a time. Written with Pierre Zhang and Henry Zheng.

I'm a member of [DESI](https://www.desi.lbl.gov/) and [LSST-DESC](https://lsstdesc.org/). Before Oxford I did my PhD with [Alexandre Refregier](https://cosmology.ethz.ch/) at ETH Zürich, and Part III before that at Downing College, Cambridge.

If you're at school and thinking about physics at university, I keep a page of [books and things worth reading]({{ '/advice/' | relative_url }}). Happy to talk about Oxbridge interviews too — just email.
