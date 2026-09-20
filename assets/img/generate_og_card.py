"""Generate the about-page hero band (light + dark) and the Open Graph card.

Spectra are computed with CAMB so the figure is physically honest rather than
decorative. Styling matches the site theme defined in _sass/_custom.scss.

Usage:
    python3 assets/img/generate_hero_band.py
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import camb

# --- site palette (mirrors _sass/_custom.scss) -----------------------------
THEMES = {
    "light": dict(
        bg="#faf9f6",
        ink="#131822",
        soft="#5c6577",
        accent="#2647b8",
        warm="#d98c2b",
        rule="#131822",
        rule_alpha=0.16,
    ),
    "dark": dict(
        bg="#0b0e14",
        ink="#c9d1e0",
        soft="#7e8899",
        accent="#8fb4ff",
        warm="#e8a33d",
        rule="#c9d1e0",
        rule_alpha=0.20,
    ),
}

MONO = ["IBM Plex Mono", "DejaVu Sans Mono", "monospace"]


def compute_spectra():
    """CMB TT spectrum, linear matter power spectrum, and the BAO wiggle ratio."""
    pars = camb.set_params(
        H0=67.36,
        ombh2=0.02237,
        omch2=0.1200,
        mnu=0.06,
        tau=0.0544,
        As=2.1e-9,
        ns=0.9649,
        lmax=2500,
        WantTransfer=True,
        redshifts=[0.0],
        kmax=2.0,
    )
    results = camb.get_results(pars)

    powers = results.get_cmb_power_spectra(pars, CMB_unit="muK", raw_cl=False)
    tt = powers["total"][:, 0]
    ell = np.arange(tt.size)
    sel = (ell >= 2) & (ell <= 2500)

    kh, _, pk = results.get_matter_power_spectrum(minkh=1e-3, maxkh=1.0, npoints=600)
    pk = pk[0]

    ratio = bao_wiggle_ratio(kh, pk, h=0.6736, ombh2=0.02237, omch2=0.1200)

    return ell[sel], tt[sel], kh, pk, ratio


def eh98_nowiggle(k_hmpc, h, ombh2, omch2, ns=0.9649, tcmb=2.7255):
    """Eisenstein & Hu (1998) zero-baryon ("no-wiggle") power spectrum shape.

    Reference: ApJ 496, 605, eqs. (26)-(31). Returns P_nw(k) up to a constant.
    """
    om0h2 = ombh2 + omch2
    fb = ombh2 / om0h2
    theta = tcmb / 2.7

    # sound horizon, eq. (26)
    s = 44.5 * np.log(9.83 / om0h2) / np.sqrt(1.0 + 10.0 * ombh2 ** 0.75)

    # shape suppression, eq. (31)
    alpha_gamma = (
        1.0
        - 0.328 * np.log(431.0 * om0h2) * fb
        + 0.38 * np.log(22.3 * om0h2) * fb ** 2
    )

    k = k_hmpc * h  # Mpc^-1
    gamma_eff = om0h2 / h * (
        alpha_gamma + (1.0 - alpha_gamma) / (1.0 + (0.43 * k * s) ** 4)
    )

    q = k * theta ** 2 / (gamma_eff * h)
    l0 = np.log(2.0 * np.e + 1.8 * q)
    c0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    t0 = l0 / (l0 + c0 * q ** 2)

    return k_hmpc ** ns * t0 ** 2


def bao_wiggle_ratio(kh, pk, h, ombh2, omch2, poly_deg=6):
    """Isolate the acoustic oscillations in P(k).

    Divide by the EH98 no-wiggle shape, then divide out a smooth polynomial in
    log k to absorb the few-percent broadband mismatch between the fitting
    formula and CAMB, leaving the oscillations centred on unity.
    """
    pnw = eh98_nowiggle(kh, h, ombh2, omch2)
    raw = pk / pnw
    logk = np.log(kh)
    coeffs = np.polyfit(logk, np.log(raw), poly_deg)
    return raw / np.exp(np.polyval(coeffs, logk))


def style_axes(ax, th):
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(th["rule"])
        ax.spines[side].set_alpha(th["rule_alpha"] * 3)
        ax.spines[side].set_linewidth(0.7)
    ax.tick_params(
        colors=th["soft"], labelsize=10.5, width=0.8, length=3.5, pad=3
    )
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(MONO)
    ax.grid(alpha=th["rule_alpha"] * 0.55, color=th["rule"], linewidth=0.5)
    ax.set_axisbelow(True)


def panel_label(ax, text, th):
    ax.set_title(
        text,
        fontsize=10.5,
        color=th["soft"],
        fontfamily=MONO,
        loc="left",
        pad=7,
    )


def render(theme_name, data, outfile, figsize=(11.0, 2.9), dpi=200, og=False):
    th = THEMES[theme_name]
    ell, tt, kh, pk, ratio = data

    fig, axes = plt.subplots(1, 3, figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(th["bg"])

    # --- CMB TT -------------------------------------------------------------
    ax = axes[0]
    ax.plot(ell, tt, color=th["accent"], lw=1.9, solid_joinstyle="round")
    ax.fill_between(ell, 0, tt, color=th["accent"], alpha=0.07)
    ax.set_xscale("log")
    ax.set_xlim(2, 2500)
    ax.set_ylim(0, tt.max() * 1.12)
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.tick_params(axis="y", length=0)
    panel_label(ax, r"CMB  $\mathcal{D}_\ell^{TT}$  [$\mu$K$^2$]", th)
    ax.set_xlabel(r"multipole  $\ell$", fontsize=10.5, color=th["soft"], fontfamily=MONO)
    style_axes(ax, th)

    # --- matter power spectrum ---------------------------------------------
    ax = axes[1]
    ax.plot(kh, pk, color=th["accent"], lw=1.9)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(kh.min(), kh.max())
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.tick_params(axis="y", which="both", length=0)
    panel_label(ax, r"matter  $P(k)$  $z=0$", th)
    ax.set_xlabel(
        r"$k$  [$h\,$Mpc$^{-1}$]", fontsize=10.5, color=th["soft"], fontfamily=MONO
    )
    style_axes(ax, th)

    # --- BAO wiggles --------------------------------------------------------
    ax = axes[2]
    ax.axhline(1.0, color=th["rule"], alpha=th["rule_alpha"] * 2.5, lw=0.7)
    ax.plot(kh, ratio, color=th["warm"], lw=1.9)
    ax.set_xscale("log")
    # below k ~ 0.03 h/Mpc there is no genuine acoustic signal left to show
    ax.set_xlim(3.2e-2, kh.max())
    ax.set_ylim(0.93, 1.08)
    panel_label(ax, r"BAO  $P(k)\,/\,P_{\rm smooth}(k)$", th)
    ax.set_xlabel(
        r"$k$  [$h\,$Mpc$^{-1}$]", fontsize=10.5, color=th["soft"], fontfamily=MONO
    )
    style_axes(ax, th)

    fig.subplots_adjust(left=0.035, right=0.985, top=0.83, bottom=0.235, wspace=0.17)
    fig.savefig(outfile, facecolor=th["bg"], dpi=dpi)
    plt.close(fig)
    print("wrote", outfile)


def render_og(data, outfile):
    """1200x630 Open Graph card: the CMB spectrum with the name over it."""
    th = THEMES["dark"]
    ell, tt, kh, pk, ratio = data

    fig = plt.figure(figsize=(12.0, 6.3), dpi=100)
    fig.patch.set_facecolor(th["bg"])
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_facecolor(th["bg"])
    ax.plot(ell, tt, color=th["accent"], lw=2.4, alpha=0.95)
    ax.fill_between(ell, 0, tt, color=th["accent"], alpha=0.12)
    ax.set_xscale("log")
    ax.set_xlim(2, 2500)
    ax.set_ylim(0, tt.max() * 2.6)  # push the curve into the lower third
    ax.axis("off")

    ax.text(
        0.055,
        0.70,
        "Alexander C. T. Reeves",
        transform=ax.transAxes,
        fontsize=44,
        color=th["ink"],
        fontfamily=["Instrument Serif", "Iowan Old Style", "Georgia", "serif"],
    )
    ax.text(
        0.055,
        0.60,
        "SNSF POSTDOC.MOBILITY FELLOW  ·  ASTROPHYSICS, UNIVERSITY OF OXFORD",
        transform=ax.transAxes,
        fontsize=12.5,
        color=th["soft"],
        fontfamily=MONO,
    )
    ax.text(
        0.055,
        0.52,
        "combined probes  ·  EFTofLSS  ·  differentiable inference",
        transform=ax.transAxes,
        fontsize=13,
        color=th["warm"],
        fontfamily=MONO,
    )

    fig.savefig(outfile, facecolor=th["bg"], dpi=100)
    plt.close(fig)
    print("wrote", outfile)


if __name__ == "__main__":
    # The three-panel band this script used to draw was dropped when the about
    # page moved to a photographic hero; only the Open Graph card is still used.
    print("running CAMB ...")
    data = compute_spectra()
    render_og(data, "assets/img/og_card.png")
