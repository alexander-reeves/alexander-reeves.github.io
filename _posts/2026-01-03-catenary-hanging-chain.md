---
layout: post
title: The shape of a hanging chain
date: 2026-01-03 10:00:00
description: Deriving the catenary from a force balance and from energy minimisation, and comparing it with the parabola
tags: [math, physics, calculus, variational-principles]
---

A chain hanging between two points looks a lot like a parabola, but the curve is actually a hyperbolic cosine, called the catenary. In this post I derive it in two ways, first from a force balance and then by minimising the potential energy, and then compare it with the parabola.

The comparison is the part I find most interesting. A cable carrying a load spread evenly along the horizontal, like the main cable of a suspension bridge, hangs in an exact parabola. The two curves come from the same equation with different load distributions.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/catenary_diagram.png" class="img-fluid rounded z-depth-1" zoomable=true caption="A uniform chain of length $L$ hanging between two points at the same height." %}
    </div>
</div>

Take a chain of length $L$ with uniform mass per unit length $\rho$ and hang it from two points at the same height. I will assume the chain is perfectly flexible, so it has no bending stiffness and can only pull along its own tangent, and that it does not stretch.

## Force balance

Consider the segment of chain between the lowest point and some point further along the curve. Three forces act on it. At the bottom there is a tension $T_0$, which is horizontal because the chain is flat there. At the other end there is a tension $T_1$ along the tangent, at an angle $\theta$ to the horizontal. The weight of the segment, $\rho g s$, acts downwards, where $s$ is its arc length.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/catenary_force_diagram.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Forces on the highlighted segment: the tension $T_0$ at the bottom, the tension $T_1$ along the tangent, and the weight $W$." %}
    </div>
</div>

Balancing the horizontal and vertical components gives

$$
T_1 \cos\theta = T_0, \qquad T_1 \sin\theta = \rho g s .
$$

The horizontal component of the tension is therefore $T_0$ at every point of the chain. Dividing the two equations removes $T_1$,

$$
\tan\theta = \frac{\rho g\, s}{T_0} .
$$

The slope of the curve is $y' = \tan\theta$, so

$$
y' = \frac{s}{a}, \qquad a \equiv \frac{T_0}{\rho g} .
$$

The length $a$, the horizontal tension divided by the weight per unit length, is the only parameter in the problem.

Since $s = \int_0^x\sqrt{1+y'^2}\,\mathrm{d}x'$, differentiating with respect to $x$ gives an equation for $y$ alone,

$$
y'' = \frac{1}{a}\sqrt{1 + y'^2} .
$$

## Energy minimisation

The same equation follows from minimising the gravitational potential energy of the chain at fixed length,

$$
U = \rho g \int y \sqrt{1 + y'^2}\, \mathrm{d}x
\quad\text{subject to}\quad
\int \sqrt{1 + y'^2}\, \mathrm{d}x = L .
$$

Adding a Lagrange multiplier $\lambda$ for the length constraint and dropping the overall factor of $\rho g$, the integrand to extremise is

$$
F(y, y') = (y + \lambda)\sqrt{1 + y'^2} .
$$

$F$ has no explicit dependence on $x$, so the Euler-Lagrange equation has the first integral $F - y'\,\partial F/\partial y' = \text{const}$, known as the Beltrami identity. It is the same statement as energy conservation for a Lagrangian with no explicit time dependence, with $x$ in place of time. Substituting $F$,

$$
(y + \lambda)\sqrt{1 + y'^2} - \frac{(y+\lambda)\,y'^2}{\sqrt{1 + y'^2}}
= \frac{y + \lambda}{\sqrt{1 + y'^2}} = \text{const} .
$$

Calling the constant $a$ and differentiating once more gives the force-balance equation again, with $y$ shifted by $\lambda$. The multiplier has a physical meaning as well. As shown in the section on tension below, $\rho g (y + \lambda)$ is the tension at each point of the chain.

## Solving the equation

Writing $p = y'$, the equation separates,

$$
\frac{\mathrm{d}p}{\sqrt{1+p^2}} = \frac{\mathrm{d}x}{a}
\quad\Longrightarrow\quad
\sinh^{-1}p = \frac{x}{a} ,
$$

where I have put the lowest point at $x = 0$, where $p = 0$. Then $y' = \sinh(x/a)$ and

$$
y = a \cosh\!\left(\frac{x}{a}\right) .
$$

I have used the constant of integration to put the origin a distance $a$ below the lowest point of the chain. This horizontal line is called the **directrix**, and measuring heights from it keeps the later formulae simple. With this choice, $a$ is also the height of the lowest point above the directrix, and the radius of curvature there. Increasing the tension increases $a$ and makes the chain flatter.

All catenaries have the same shape up to a change of scale, because $y/a = \cosh(x/a)$ and changing $a$ stretches both axes by the same factor.

{% include figure_themed.liquid
   base="assets/img/catenary_family" ext="png" zoomable=true
   alt="A family of catenary curves y = a cosh(x/a) for a between 0.4 and 4.0, coloured by a, with the directrix marked"
   caption="The family $y = a\cosh(x/a)$. The lowest point of each curve is at height $a$ above the directrix." %}

## Fixing $a$ from the span and the length

In practice we know the span and the length of the chain rather than $a$. For supports at $x = \pm b$, the length is

$$
L = \int_{-b}^{b}\cosh\!\left(\frac{x}{a}\right)\mathrm{d}x = 2a\sinh\!\left(\frac{b}{a}\right) ,
$$

using $\sqrt{1+\sinh^2 u} = \cosh u$. With $u = b/a$ this becomes

$$
\frac{\sinh u}{u} = \frac{L}{2b} .
$$

The left-hand side increases monotonically from 1, so there is a single solution whenever $L > 2b$. It has no closed form and has to be found numerically. Once $a$ is known, the sag is $a[\cosh(b/a) - 1]$.

{% include figure_themed.liquid
   base="assets/img/catenary_sag" ext="gif" zoomable=true
   alt="Animation of a chain sagging further as more chain is let out over a fixed span, next to a plot of sag over span against length over span"
   caption="More chain is let out over a fixed span, with $a$ found numerically for each frame." %}

For a chain only slightly longer than the span, $\sinh u / u \approx 1 + u^2/6$, so $u \approx \sqrt{6\epsilon}$, where $\epsilon = L/2b - 1$ is the fractional excess length. The sag therefore grows like $\sqrt{\epsilon}$, which is why it rises so quickly at the start of the animation. A cable 1% longer than its span sags by about 6% of the span. This is why the tension in overhead power lines has to be set carefully, and why they sag more on hot days. A temperature rise of 30 K lengthens a steel cable by a few hundredths of a percent, and the square root turns that into a visible extra sag.

## Comparison with the parabola

Expanding the hyperbolic cosine,

$$
y = a + \frac{x^2}{2a} + \frac{x^4}{24a^3} + \cdots
$$

For $\lvert x \rvert \ll a$ the leading term after the constant is a parabola, and the next correction is smaller by a factor $x^2/12a^2$. A shallow chain is therefore very close to a parabola, and the difference grows as the chain sags more.

{% include figure_themed.liquid
   base="assets/img/catenary_vs_parabola" ext="png" zoomable=true
   alt="Three panels comparing a catenary with a parabola of the same span and sag, at length-to-span ratios of 1.02, 1.30 and 2.20, with residual panels"
   caption="Catenary and parabola with the same span and sag. The largest difference is 0.2% of the sag for $L/\mathrm{span} = 1.02$ and about 10% for $L/\mathrm{span} = 2.2$." %}

Galileo described this approximation in _Two New Sciences_ (1638). In the Fourth Day he writes:

> Besides I must tell you something which will both surprise and please you, namely, that a cord stretched more or less tightly assumes a curve which closely approximates the parabola. [...] the coincidence is more exact in proportion as the parabola is drawn with less curvature or, so to speak, more stretched; so that using parabolas described with elevations less than 45° the chain fits its parabola almost perfectly.

(Galileo, _Two New Sciences_, Fourth Day, translated by H. Crew and A. de Salvio, [p. 310](https://galileoandeinstein.phys.virginia.edu/tns_draft/tns_280to295.html).) He is often described as having claimed that the chain is exactly a parabola. In this passage he calls it an approximation that improves as the curve gets flatter, which agrees with the $x^2/12a^2$ correction above. The exact curve was found in 1691 by Huygens, Leibniz and Johann Bernoulli, in response to a challenge set by Jakob Bernoulli.

Now change the load. Suppose the weight is spread uniformly along the horizontal, $w$ per unit length in $x$, instead of uniformly along the chain. The weight of the segment is then $wx$ rather than $\rho g s$, and the force balance gives

$$
y' = \frac{w\,x}{T_0} \quad\Longrightarrow\quad y = \frac{w\,x^2}{2T_0} ,
$$

which is an exact parabola. This is a good model for a suspension bridge, where the deck hangs from the main cable and is much heavier than the cable itself. The main cables of a suspension bridge are therefore close to parabolic, while a chain hanging under its own weight is a catenary.

## Tension along the chain

Since $T = T_0/\cos\theta$ and $\cos\theta = 1/\cosh(x/a)$,

$$
T(x) = T_0\cosh\!\left(\frac{x}{a}\right) = \rho g\, y .
$$

The tension at any point equals $\rho g$ times the height of that point above the directrix. This is the combination $\rho g(y + \lambda)$ from the energy calculation, with heights now measured from the directrix. Two points at the same height carry the same tension. The tension is largest at the supports, where it is larger than at the bottom by a factor $\cosh(b/a)$.

{% include figure_themed.liquid
   base="assets/img/catenary_tension" ext="png" zoomable=true
   alt="A chain coloured by its tension, next to a plot showing tension is exactly linear in height above the directrix"
   caption="Tension along the chain, and the linear relation $T = \rho g y$." %}

## Arches

Turning a catenary upside down changes every tension into a compression of the same size. Masonry is strong in compression and weak in tension, so an inverted catenary is a natural shape for an arch that carries its own weight. Robert Hooke stated this in 1675 as a Latin anagram, which decodes to _"as hangs the flexible line, so but inverted will stand the rigid arch"_. Antoni Gaudí used the same idea for the Colònia Güell chapel, which he designed with an upside-down model made of strings loaded with small weights.

## Extensions

- **Unequal support heights.** The solution is still $y = a\cosh((x - x_0)/a)$, with $x_0$ as an extra unknown. If the difference in height is large enough, the lowest point lies outside the span and the chain is never horizontal.
- **Non-uniform density.** The equation changes and the solution is no longer a hyperbolic cosine. A well-known case is the catenary of equal strength, where the cross-section is tapered so that the stress is the same everywhere. Its shape is $y = -a\ln\cos(x/a)$, which has vertical asymptotes at $x = \pm\pi a/2$, so there is a maximum possible span.
- **Elastic chains.** If the chain stretches under tension, the arc length depends on the tension. This is the elastic catenary, which is the relevant case for real steel cables.

## References

- E. H. Lockwood, _A Book of Curves_ (Cambridge University Press, 1961).
- E. W. Weisstein, [Catenary](https://mathworld.wolfram.com/Catenary.html), MathWorld.
- V. I. Arnold, _Mathematical Methods of Classical Mechanics_, for the Beltrami identity.
- Galileo Galilei, _Dialogues Concerning Two New Sciences_ (1638), translated by H. Crew and A. de Salvio.

The two diagrams at the top were made in [this notebook](https://github.com/alexander-reeves/alexander-reeves.github.io/blob/master/assets/jupyter/catenary_diagram.ipynb), and the other figures with [this script](https://github.com/alexander-reeves/alexander-reeves.github.io/blob/master/assets/img/generate_catenary_figures.py).
