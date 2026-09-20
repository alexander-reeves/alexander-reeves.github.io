"""Figures for the catenary blog post.

Everything here follows from y = a cosh(x/a) with a = T0 / (rho g); the only
numerics are the root solve for `a` given a span and a chain length.

Each figure is rendered twice, once per site theme, and the post picks between
them with the .repo-img-light / .repo-img-dark classes.

Usage:
    python3 assets/img/generate_catenary_figures.py
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.optimize import brentq

THEMES = {
    "light": dict(
        bg="#faf9f6", ink="#131822", soft="#5c6577",
        accent="#2647b8", warm="#d98c2b", ghost="#b9bdc7",
    ),
    "dark": dict(
        bg="#0b0e14", ink="#c9d1e0", soft="#7e8899",
        accent="#8fb4ff", warm="#e8a33d", ghost="#3a4356",
    ),
}

MONO = ["IBM Plex Mono", "DejaVu Sans Mono", "monospace"]
DPI = 170


# ---------------------------------------------------------------------------
# Core catenary relations
# ---------------------------------------------------------------------------

def solve_a(half_span, length):
    """Solve L = 2a sinh(b/a) for a, given half-span b and total length L.

    Substituting u = b/a turns this into sinh(u)/u = L/(2b), which is monotonic
    in u > 0 and so has a unique root whenever L > 2b.
    """
    b, target = half_span, length / (2.0 * half_span)
    if target <= 1.0:
        raise ValueError("chain must be longer than the span")
    f = lambda u: np.sinh(u) / u - target
    u = brentq(f, 1e-9, 500.0)
    return b / u


def catenary(x, a):
    """Height above the vertex."""
    return a * (np.cosh(x / a) - 1.0)


def sag_of(half_span, a):
    return a * (np.cosh(half_span / a) - 1.0)


def style(ax, th, grid=True):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(th["soft"])
        ax.spines[side].set_linewidth(0.7)
    ax.tick_params(colors=th["soft"], labelsize=8, width=0.7, length=3)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(MONO)
    if grid:
        ax.grid(alpha=0.18, color=th["soft"], linewidth=0.5)
    ax.set_axisbelow(True)


def label(ax, text, th, size=9):
    ax.set_title(text, fontsize=size, color=th["soft"], fontfamily=MONO, loc="left", pad=8)


def finish(fig, th, path):
    fig.savefig(path, facecolor=th["bg"], dpi=DPI)
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------------------
# 1. Catenary vs parabola
# ---------------------------------------------------------------------------

def fig_vs_parabola(theme):
    th = THEMES[theme]
    b = 1.0
    ratios = [1.02, 1.30, 2.20]  # L / span

    fig, axes = plt.subplots(
        2, 3, figsize=(11.0, 5.4), dpi=DPI,
        gridspec_kw=dict(height_ratios=[2.4, 1.0], hspace=0.38, wspace=0.26),
    )
    fig.patch.set_facecolor(th["bg"])

    x = np.linspace(-b, b, 800)
    for col, r in enumerate(ratios):
        a = solve_a(b, r * 2 * b)
        s = sag_of(b, a)
        y_cat = catenary(x, a)
        y_par = s * (x / b) ** 2  # same span, same sag

        ax = axes[0, col]
        ax.plot(x, y_cat, color=th["accent"], lw=2.0, label="catenary", zorder=3)
        ax.plot(x, y_par, color=th["warm"], lw=1.6, ls=(0, (4, 2.5)), label="parabola", zorder=2)
        ax.fill_between(x, y_cat, y_par, color=th["warm"], alpha=0.16, lw=0, zorder=1)
        ax.plot([-b, b], [s, s], "o", color=th["ink"], ms=4.5, zorder=4)
        ax.invert_yaxis()
        ax.set_xlim(-b * 1.08, b * 1.08)
        label(ax, r"$L/\mathrm{span} = %.2f$   $a = %.3f$" % (r, a), th)
        style(ax, th)
        if col == 0:
            leg = ax.legend(frameon=False, fontsize=8.5, loc="lower center")
            for t in leg.get_texts():
                t.set_color(th["ink"])
                t.set_fontfamily(MONO)

        ax = axes[1, col]
        resid = 100.0 * (y_cat - y_par) / s
        ax.axhline(0, color=th["soft"], lw=0.7, alpha=0.6)
        ax.plot(x, resid, color=th["ink"], lw=1.4)
        ax.fill_between(x, 0, resid, color=th["ink"], alpha=0.10, lw=0)
        ax.set_xlim(-b * 1.08, b * 1.08)
        ax.set_xlabel(r"$x$ / half-span", fontsize=8.5, color=th["soft"], fontfamily=MONO)
        peak = np.abs(resid).max()
        label(ax, r"difference, %% of sag   (max %.1f%%)" % peak, th, size=8.5)
        style(ax, th)

    finish(fig, th, "assets/img/catenary_vs_parabola_%s.png" % theme)


# ---------------------------------------------------------------------------
# 2. The family y = a cosh(x/a)
# ---------------------------------------------------------------------------

def fig_family(theme):
    th = THEMES[theme]
    b = 1.0
    fig, ax = plt.subplots(figsize=(8.4, 5.0), dpi=DPI)
    fig.patch.set_facecolor(th["bg"])

    cmap = LinearSegmentedColormap.from_list("plate", [th["accent"], th["warm"]])
    a_values = np.geomspace(0.40, 4.0, 8)
    x = np.linspace(-b, b, 700)

    for i, a in enumerate(a_values):
        c = cmap(i / (len(a_values) - 1))
        y = a * np.cosh(x / a)
        ax.plot(x, y, color=c, lw=1.9, solid_capstyle="round")
        ax.plot([0], [a], "o", color=c, ms=4)

    ax.axhline(0, color=th["soft"], lw=0.9, ls=(0, (5, 3)), alpha=0.8)
    ax.text(
        -b * 0.98, -0.26, "directrix   y = 0",
        color=th["soft"], fontsize=8.5, fontfamily=MONO, va="bottom",
    )
    ax.annotate(
        "vertex sits at  y = a",
        xy=(0, a_values[-1]), xytext=(-0.93, 4.62),
        color=th["ink"], fontsize=9, fontfamily=MONO, va="center",
        arrowprops=dict(arrowstyle="-", color=th["soft"], lw=0.8, shrinkA=6, shrinkB=4),
    )

    ax.set_xlim(-b, b)
    ax.set_ylim(-0.3, 5.0)
    ax.set_xlabel(r"$x$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    ax.set_ylabel(r"$y$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    label(ax, r"$y = a\,\cosh(x/a)$   for   $a = 0.40 \ldots 4.0$", th, size=10)
    style(ax, th)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=a_values[0], vmax=a_values[-1]))
    cb = fig.colorbar(sm, ax=ax, pad=0.02, fraction=0.04)
    cb.set_label(r"$a = T_0 / \rho g$", fontsize=9, color=th["soft"], fontfamily=MONO)
    cb.ax.tick_params(colors=th["soft"], labelsize=8, width=0.7, length=3)
    cb.outline.set_edgecolor(th["soft"])
    cb.outline.set_linewidth(0.6)
    for lbl in cb.ax.get_yticklabels():
        lbl.set_fontfamily(MONO)

    fig.tight_layout()
    finish(fig, th, "assets/img/catenary_family_%s.png" % theme)


# ---------------------------------------------------------------------------
# 3. Tension along the chain
# ---------------------------------------------------------------------------

def fig_tension(theme):
    th = THEMES[theme]
    b, L = 1.0, 2.8
    a = solve_a(b, L)
    x = np.linspace(-b, b, 600)
    y = a * np.cosh(x / a)  # height above the directrix
    T = y / a  # T / T0, since T = rho g y and T0 = rho g a

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(11.6, 4.4), dpi=DPI, gridspec_kw=dict(width_ratios=[1.45, 1.0], wspace=0.46)
    )
    fig.patch.set_facecolor(th["bg"])

    cmap = LinearSegmentedColormap.from_list("plate", [th["accent"], th["warm"]])
    pts = np.array([x, y]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, cmap=cmap, norm=Normalize(T.min(), T.max()), lw=4.0, capstyle="round")
    lc.set_array(T[:-1])
    ax.add_collection(lc)

    ax.axhline(0, color=th["soft"], lw=0.9, ls=(0, (5, 3)), alpha=0.8)
    ax.text(-b * 0.98, -0.13, "directrix   y = 0", color=th["soft"], fontsize=8.5, fontfamily=MONO)
    ax.plot([0, 0], [0, a], color=th["soft"], lw=0.8)
    ax.text(0.03, a / 2, r"$a$", color=th["ink"], fontsize=10, fontfamily=MONO, va="center")

    ax.set_xlim(-b * 1.05, b * 1.05)
    ax.set_ylim(-0.16, y.max() * 1.12)
    ax.set_xlabel(r"$x$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    ax.set_ylabel(r"$y$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    label(ax, r"chain coloured by tension $T/T_0$", th, size=10)
    style(ax, th)

    cb = fig.colorbar(lc, ax=ax, pad=0.02, fraction=0.045)
    cb.set_label(r"$T / T_0$", fontsize=9, color=th["soft"], fontfamily=MONO)
    cb.ax.tick_params(colors=th["soft"], labelsize=8, width=0.7, length=3)
    cb.outline.set_edgecolor(th["soft"])
    cb.outline.set_linewidth(0.6)
    for lbl in cb.ax.get_yticklabels():
        lbl.set_fontfamily(MONO)

    ax2.plot(y / a, T, color=th["accent"], lw=2.2)
    ax2.set_xlabel(r"$y / a$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    ax2.set_ylabel(r"$T / T_0$", fontsize=9.5, color=th["soft"], fontfamily=MONO)
    label(ax2, r"$T = \rho g\, y$  — tension is set by height alone", th, size=9.5)
    style(ax2, th)

    fig.tight_layout()
    finish(fig, th, "assets/img/catenary_tension_%s.png" % theme)


# ---------------------------------------------------------------------------
# 4. Animation: paying out more chain
# ---------------------------------------------------------------------------

def gif_sag(theme):
    th = THEMES[theme]
    b = 1.0
    # ping-pong so the loop reads smoothly; kept short to keep the GIF small
    ratios = np.concatenate([
        np.linspace(1.02, 2.6, 44),
        np.linspace(2.6, 1.02, 44),
    ])

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(9.6, 4.3), dpi=82, gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.3)
    )
    fig.patch.set_facecolor(th["bg"])

    x = np.linspace(-b, b, 500)
    (curve,) = ax.plot([], [], color=th["accent"], lw=2.6, solid_capstyle="round")
    (anchors,) = ax.plot([-b, b], [0, 0], "o", color=th["ink"], ms=6)
    txt = ax.text(
        0.02, 0.03, "", transform=ax.transAxes,
        color=th["ink"], fontsize=9.5, fontfamily=MONO, va="bottom",
    )
    # frame the deepest chain in the sweep, with room below it for the readout
    deepest = sag_of(b, solve_a(b, ratios.max() * 2 * b))
    ax.set_xlim(-b * 1.12, b * 1.12)
    ax.set_ylim(-deepest * 1.32, 0.20)
    ax.set_xlabel(r"$x$ / half-span", fontsize=9, color=th["soft"], fontfamily=MONO)
    label(ax, "paying out more chain over a fixed span", th, size=9.5)
    style(ax, th)

    all_r = np.linspace(1.001, 2.6, 300)
    all_sag = np.array([sag_of(b, solve_a(b, r * 2 * b)) / (2 * b) for r in all_r])
    ax2.plot(all_r, all_sag, color=th["ghost"], lw=1.6)
    (dot,) = ax2.plot([], [], "o", color=th["warm"], ms=7)
    ax2.set_xlabel(r"$L\,/\,$span", fontsize=9, color=th["soft"], fontfamily=MONO)
    ax2.set_ylabel(r"sag$\,/\,$span", fontsize=9, color=th["soft"], fontfamily=MONO)
    label(ax2, "sag grows fast, then slowly", th, size=9.5)
    style(ax2, th)

    def update(i):
        r = ratios[i]
        a = solve_a(b, r * 2 * b)
        s = sag_of(b, a)
        curve.set_data(x, catenary(x, a) - s)  # hang from the anchors
        txt.set_text("L/span = %.2f\na      = %.3f\nsag    = %.3f" % (r, a, s))
        dot.set_data([r], [s / (2 * b)])
        return curve, txt, dot

    fig.tight_layout()
    anim = FuncAnimation(fig, update, frames=len(ratios), interval=55, blit=False)
    out = "assets/img/catenary_sag_%s.gif" % theme
    anim.save(out, writer=PillowWriter(fps=16), savefig_kwargs=dict(facecolor=th["bg"]))
    plt.close(fig)
    optimise_gif(out)
    print("wrote", out)


def optimise_gif(path):
    """Shrink a GIF with ImageMagick, if it is installed.

    Pillow writes a full-colour frame per step, which runs to several MB. A
    palette pass cuts that by ~85% with no visible loss. Skipped silently when
    ImageMagick is unavailable, so the script still works without it.
    """
    import shutil
    import subprocess

    binary = shutil.which("magick") or shutil.which("convert")
    if binary is None:
        print("  (ImageMagick not found — leaving %s unoptimised)" % path)
        return
    subprocess.run(
        [binary, path, "-layers", "optimize", "-colors", "128", path], check=True
    )


if __name__ == "__main__":
    for theme in ("light", "dark"):
        fig_vs_parabola(theme)
        fig_family(theme)
        fig_tension(theme)
        gif_sag(theme)
