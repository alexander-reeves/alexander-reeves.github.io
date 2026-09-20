---
layout: post
title: The Catenary - The Mathematics of a Hanging Chain
date: 2026-01-03 10:00:00
description: Two derivations of the shape of a hanging chain, why it is not a parabola, and what the parameter a is actually telling you
tags: [math, physics, calculus, variational-principles]
---

## Introduction

The catenary is one of the most elegant curves in mathematics and physics. It describes the shape that a uniform chain or cable naturally assumes when suspended between two points under the influence of gravity. While it might seem like a simple problem, the catenary connects deep mathematical concepts and provides a nice example of using physics intuition to solve problems.

It also has a good history. Galileo thought the curve was a parabola, and said so in print in 1638. He was close but wrong, and it took until 1691 — after Jakob Bernoulli posed it as a public challenge — for Huygens, Leibniz and Johann Bernoulli to independently get the right answer. Huygens gave it the name _catenaria_, from the Latin for chain.

## The Physical Problem

The set-up of this problem is very simple: simply take a chain of length $L$ with some uniform mass density $\rho$ and suspend this between two points that are (at least for now) at an equal height. See the diagram drawn below:

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/catenary_diagram.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Setup of the catenary problem: a uniform chain of length $L$ suspended between two fixed points at equal height." %}
    </div>
</div>

The one assumption doing all the work here is that the chain is **perfectly flexible and inextensible**: it has no bending stiffness, so it can only pull along its own tangent, and its length is fixed. Everything below follows from that.

## Two routes to the same curve

There are two natural ways to attack this. The first is a balance of forces, which is a classic high school physics problem. The second is a variational argument — the chain settles into whatever shape minimises its potential energy. They are worth doing both, because they arrive at the same differential equation from completely different directions.

### Route 1: balancing forces

Consider the segment of chain running from the lowest point of the curve to some arbitrary point further along. The unknown quantities are:

- **$T_0$**: the horizontal tension at the bottom of the chain
- **$T_1$**: the tension at the upper end of the segment, acting along the tangent to the chain
- **$W$**: the weight of the segment, acting downward
- **$\theta$**: the angle that $T_1$ makes with the horizontal

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/catenary_force_diagram.png" class="img-fluid rounded z-depth-1" zoomable=true caption="Force diagram showing the forces acting on a segment of the chain. The highlighted segment (in red) has length $s$ and experiences tensions $T_0$ and $T_1$, along with its weight $W$." %}
    </div>
</div>

At the lowest point the tangent is horizontal, so the tension there is purely horizontal — that is $T_0$. The segment is in equilibrium, so the horizontal and vertical forces balance separately:

$$
T_1 \cos\theta = T_0, \qquad T_1 \sin\theta = W = \rho g s ,
$$

where $s$ is the arc length of the segment. Dividing one by the other kills $T_1$, which we never cared about:

$$
\tan\theta = \frac{\rho g\, s}{T_0} .
$$

Now, $\tan\theta$ is just the slope of the curve, $y' = \mathrm{d}y/\mathrm{d}x$. So

$$
y' = \frac{\rho g}{T_0}\, s \;\equiv\; \frac{s}{a}, \qquad a \equiv \frac{T_0}{\rho g} .
$$

That single combination $a$ — horizontal tension divided by weight per unit length — is the only parameter in the problem. It has units of length, and we will see shortly what length it is.

The awkwardness is that $s$ is itself an integral of the unknown curve, $s = \int_0^x \sqrt{1 + y'^2}\,\mathrm{d}x'$. The fix is to differentiate the whole equation with respect to $x$, which turns the integral back into an integrand:

$$
\boxed{\; y'' = \frac{1}{a}\sqrt{1 + y'^2} \;}
$$

### Route 2: minimising the energy

The chain hangs in whatever configuration minimises its gravitational potential energy, subject to having a fixed length. The energy is

$$
U = \int \rho g\, y \,\mathrm{d}s = \rho g \int y \sqrt{1 + y'^2}\, \mathrm{d}x ,
$$

and the constraint is

$$
L = \int \sqrt{1 + y'^2}\, \mathrm{d}x = \text{const} .
$$

Introduce a Lagrange multiplier $\lambda$ for the constraint and minimise the combination. Dropping the overall $\rho g$, the functional to extremise has integrand

$$
F(y, y') = (y + \lambda)\sqrt{1 + y'^2} .
$$

Here is the nice part: $F$ has no _explicit_ dependence on $x$. Whenever that happens, the Euler–Lagrange equation has a first integral — the Beltrami identity —

$$
F - y' \frac{\partial F}{\partial y'} = \text{const} .
$$

Computing $\partial F/\partial y' = (y+\lambda)\, y' / \sqrt{1+y'^2}$ and substituting:

$$
(y + \lambda)\sqrt{1 + y'^2} - \frac{(y+\lambda)\, y'^2}{\sqrt{1 + y'^2}}
= \frac{y + \lambda}{\sqrt{1 + y'^2}} = \text{const} \equiv a .
$$

Write $Y = y + \lambda$, which just shifts where we measure height from. Then $Y = a\sqrt{1 + Y'^2}$, and differentiating once recovers

$$
Y'' = \frac{1}{a}\sqrt{1 + Y'^2} ,
$$

which is exactly the equation from the force balance. The two routes agree, and comparing them tells you something the variational calculation alone does not: the Lagrange multiplier enforcing the length constraint is, physically, fixing the horizontal tension in the chain.

### Solving the equation

Set $p = y'$ and the second-order equation becomes first-order and separable:

$$
\frac{\mathrm{d}p}{\sqrt{1 + p^2}} = \frac{\mathrm{d}x}{a}
\quad\Longrightarrow\quad
\sinh^{-1} p = \frac{x}{a} + C .
$$

Put the lowest point of the chain at $x = 0$, where the curve is flat, so $p(0) = 0$ and $C = 0$. Then $y' = \sinh(x/a)$, and integrating once more gives the catenary:

$$
\boxed{\; y(x) = a \cosh\!\left(\frac{x}{a}\right) \;}
$$

where the constant of integration has been used to measure $y$ from a horizontal line one distance $a$ below the lowest point of the chain. That line is called the **directrix**, and choosing it as the origin is what makes every formula below come out clean.

## What the parameter $a$ means

Everything about a catenary is controlled by $a = T_0/\rho g$. Three ways to read it:

- **As a tension.** A tighter chain (large $T_0$) or a lighter one (small $\rho$) gives large $a$ and a flatter curve. Pull a chain infinitely hard and it becomes a straight line.
- **As a height.** The lowest point of the chain sits at exactly $y = a$ above the directrix.
- **As a curvature.** Differentiating twice, the radius of curvature at the vertex is precisely $a$.

Note that there is really only _one_ catenary. Since $y/a = \cosh(x/a)$, changing $a$ just rescales both axes by the same factor — every catenary is a scaled copy of every other. This is a genuine self-similarity, and it is why the curve looks so much like a parabola over a limited range.

{% include figure_themed.liquid
   base="assets/img/catenary_family" ext="png" zoomable=true
   alt="A family of catenary curves y = a cosh(x/a) for a between 0.4 and 4.0, coloured by a, with the directrix marked"
   caption="The one-parameter family $y = a\cosh(x/a)$. Larger $a$ means more horizontal tension and a flatter chain; the vertex of each curve sits at height $y = a$ above the directrix. Because the parameter rescales both axes together, these are all the same curve seen at different magnifications." %}

## Fixing $a$ from the boundary conditions

In a real problem you do not know $a$ — you know the span and how much chain you have. Suspend the chain between $x = -b$ and $x = +b$, so the span is $2b$, and let the total length be $L$. The arc length integral is unusually pleasant here, because $\sqrt{1 + \sinh^2 u} = \cosh u$:

$$
L = \int_{-b}^{b} \sqrt{1 + \sinh^2\!\left(\frac{x}{a}\right)}\, \mathrm{d}x
  = \int_{-b}^{b} \cosh\!\left(\frac{x}{a}\right) \mathrm{d}x
  = 2a \sinh\!\left(\frac{b}{a}\right) .
$$

Writing $u = b/a$, this rearranges to

$$
\frac{\sinh u}{u} = \frac{L}{2b} .
$$

The left-hand side increases monotonically from $1$ (as $u \to 0$) to infinity, so there is exactly one solution whenever $L > 2b$ — that is, whenever the chain is longer than the gap, which it must be. But there is **no closed form** for $u$. This is the one place the problem refuses to be elegant, and you simply solve it numerically. Once you have $a$, the sag follows immediately:

$$
\text{sag} = y(b) - y(0) = a\left[\cosh\!\left(\frac{b}{a}\right) - 1\right] .
$$

{% include figure_themed.liquid
   base="assets/img/catenary_sag" ext="gif" zoomable=true
   alt="Animation of a chain sagging further as more chain is paid out over a fixed span, alongside a plot of sag over span against length over span"
   caption="Paying out more chain over a fixed span. Each frame solves $\sinh(u)/u = L/2b$ numerically for $a$. Note how sharply the sag responds at first — a chain only 2% longer than its span already dips noticeably — and how it then settles into a near-linear crawl." %}

That initial steepness is worth dwelling on. Near $u = 0$, expanding $\sinh u / u \approx 1 + u^2/6$ gives $u \approx \sqrt{6(L - 2b)/2b}$, so the sag grows like the **square root** of the excess length. A cable strung 1% long sags about 6% of its span. This is why overhead power lines have to be tensioned so carefully, and why they visibly droop more on hot days when the metal has expanded by a fraction of a percent.

## The catenary is not a parabola (except when it is)

Galileo's guess was not stupid. Expanding the hyperbolic cosine,

$$
y = a\cosh\!\left(\frac{x}{a}\right) = a + \frac{x^2}{2a} + \frac{x^4}{24 a^3} + \cdots
$$

so for $\lvert x\rvert \ll a$ — a shallow chain, tightly strung — the leading behaviour is exactly a parabola, with the first correction suppressed by $x^2/12a^2$.

{% include figure_themed.liquid
   base="assets/img/catenary_vs_parabola" ext="png" zoomable=true
   alt="Three panels comparing a catenary with a parabola of the same span and sag at length-to-span ratios of 1.02, 1.30 and 2.20, with residual panels below"
   caption="Catenary against the parabola with the same span and the same sag. At $L/\mathrm{span} = 1.02$ the two curves differ by 0.2% of the sag — no measurement Galileo could have made would have separated them. By $L/\mathrm{span} = 2.20$ the gap is roughly 10%, and the catenary is visibly the fuller curve." %}

But there is a sharper point here than "the parabola is an approximation", and it is the bit I find genuinely satisfying. **The parabola is not merely an approximation to the catenary — it is the exact answer to a different problem.**

Go back to the force balance and ask what happens if the load is uniform per unit **horizontal distance** rather than per unit **arc length**. That is the case for a suspension bridge, where the roadway deck is far heavier than the cable holding it. Then the weight of the segment is $w x$, not $\rho g s$, and the equation becomes

$$
y' = \frac{w\, x}{T_0} \quad\Longrightarrow\quad y = \frac{w\, x^2}{2 T_0} ,
$$

a parabola, exactly. So the main cables of the Golden Gate Bridge really are parabolas (to the extent the deck dominates), while a chain hanging under its own weight is a catenary. Which curve you get is decided by what the weight is distributed along.

## Tension along the chain

One more result falls out almost for free. From the horizontal balance $T = T_0 / \cos\theta$, and $\cos\theta = 1/\sqrt{1 + y'^2} = 1/\cosh(x/a)$, so

$$
T(x) = T_0 \cosh\!\left(\frac{x}{a}\right) = T_0\, \frac{y}{a} = \rho g\, y .
$$

The tension at any point on the chain is $\rho g$ times its **height above the directrix** — nothing else. Two points at the same height carry the same tension, regardless of how much chain lies between them or what the span is. Measuring the height of a hanging cable above the right reference line is the same as measuring its tension.

{% include figure_themed.liquid
   base="assets/img/catenary_tension" ext="png" zoomable=true
   alt="A chain coloured by its tension, next to a plot showing tension is exactly linear in height above the directrix"
   caption="Left: the chain coloured by $T/T_0$, minimum at the vertex and maximum at the supports. The vertical bar marks the distance $a$ from the directrix up to the vertex. Right: the relation $T = \rho g y$ is exactly linear — the apparent triviality of the right-hand panel is the whole content of the result." %}

It also explains why chains break at the top. The supports are the highest points, so they carry the greatest tension, by a factor $\cosh(b/a)$ compared to the middle.

## Where this shows up

- **Power lines and overhead cables.** Real catenaries, and the sag calculation above is genuinely how transmission line clearances are set.
- **Suspension bridges.** Parabolas, for the reason given above — though the cables are catenaries before the deck is hung.
- **Arches.** Invert a catenary and every force in it turns from tension into compression, which is exactly what masonry is good at. Hooke stated this in 1675 as an anagram, decoded as _"as hangs the flexible line, so but inverted will stand the rigid arch"_. The Gateway Arch in St. Louis is a weighted catenary, thickened toward the base.
- **Gaudí's hanging models.** For the Colònia Güell chapel, Gaudí built the structure upside down out of strings weighted with birdshot, let gravity find the funicular shape, and photographed it inverted. The building is a catenary surface solved by analogue computer.
- **Soap films.** Rotate a catenary about the directrix and you get the _catenoid_, the minimal surface spanning two coaxial rings — the same variational structure appearing in a different guise.

## Beyond the simple case

The version above is the cleanest one. Some directions it generalises:

- **Unequal support heights.** The curve is still $y = a\cosh((x - x_0)/a)$; you have simply lost the symmetry that put the vertex at $x = 0$. Now two unknowns, $a$ and $x_0$, are fixed by two endpoint conditions plus the length constraint — and the vertex may fall outside the span entirely, in which case the chain never becomes horizontal.
- **Non-uniform density.** With $\rho$ a function of position, the equation becomes $y'' = \rho(s) g \sqrt{1+y'^2}/T_0$ and the hyperbolic cosine is gone. The _catenary of equal strength_ is the special case where the cross-section is tapered so stress is constant throughout, giving $y = -a\ln\cos(x/a)$ instead.
- **Elastic chains.** Let the chain stretch under tension and the arc length itself becomes an unknown function of the load — the elastic catenary, which matters for real steel cables.

## Further reading

- E. H. Lockwood, _A Book of Curves_ (Cambridge, 1961) — a short, readable chapter on the catenary and its relatives.
- E. W. Weisstein, ["Catenary"](https://mathworld.wolfram.com/Catenary.html) on MathWorld — compact reference for the standard results, including the catenoid and the equal-strength case.
- V. I. Arnold, _Mathematical Methods of Classical Mechanics_ — for the Beltrami identity in its proper setting, as conservation of the Hamiltonian for an $x$-independent Lagrangian.

The two diagrams at the top come from [`assets/jupyter/catenary_diagram.ipynb`](https://github.com/alexander-reeves/alexander-reeves.github.io/blob/master/assets/jupyter/catenary_diagram.ipynb), and every plot below them from [`assets/img/generate_catenary_figures.py`](https://github.com/alexander-reeves/alexander-reeves.github.io/blob/master/assets/img/generate_catenary_figures.py) — both in this site's repository, if you want to change the numbers and see what happens.
