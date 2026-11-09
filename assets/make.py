#!/usr/bin/env python3
"""Rebuilds the animated README SVGs next to this file. Run: python3 assets/make.py"""
import os
from html import escape

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

FONT = "'SF Mono','JetBrains Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"
CW = 9.03  # monospace advance at 15px
G = dict(bg0h="#1d2021", bg="#282828", bg1="#3c3836", bg2="#504945", bg3="#665c54",
         fg="#ebdbb2", fg4="#a89984", gray="#928374",
         red="#fb4934", red2="#cc241d", green="#b8bb26", yellow="#fabd2f", yellow2="#d79921",
         blue="#83a598", blue2="#458588", purple="#d3869b", aqua="#8ec07c", aqua2="#689d6a",
         orange="#fe8019", orange2="#d65d0e")


def kf(name, T, frames):
    """frames: list of (seconds, css, timing-fn or None). Converted to % of cycle T."""
    out = [f"@keyframes {name}{{"]
    for t, css, tf in frames:
        pct = max(0.0, min(100.0, t / T * 100))
        tfs = f"animation-timing-function:{tf};" if tf else ""
        out.append(f"{pct:.3f}%{{{css.rstrip(';')};{tfs}}}")
    out.append("}")
    return "".join(out)


def t(x, y, s, fill, size=15, weight=None, anchor=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}"{w}{a}{extra}>{escape(s)}</text>'


# ---------------------------------------------------------------- banner
def banner():
    T = 14.0
    W, H = 860, 372
    css, body = [], []
    css.append(f"text{{font-family:{FONT};white-space:pre}}")

    # window chrome
    body.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="12" fill="{G["bg"]}" stroke="{G["bg1"]}" stroke-width="1.5"/>')
    body.append(f'<path d="M10 22a12 12 0 0 1 12-12h{W-44}a12 12 0 0 1 12 12v24H10z" fill="{G["bg0h"]}"/>')
    for i, c in enumerate([G["red"], G["yellow"], G["green"]]):
        body.append(f'<circle cx="{34+i*22}" cy="28" r="6.5" fill="{c}"/>')
    body.append(t(W / 2, 33, "ghostty · ~/dotfiles", G["gray"], size=13, anchor="middle"))

    # starship powerline prompt, drawn right to left so tips overlap the next segment
    def powerline(y, segs, x0=30):
        h, tip = 24, 10
        xs, x = [], x0
        for label, _, _ in segs:
            w = len(label) * CW + 22
            xs.append((x, w))
            x += w
        parts = []
        for (label, bgc, fgc), (sx, w) in reversed(list(zip(segs, xs))):
            x1 = sx + w
            parts.append(f'<path d="M{sx:.1f} {y}h{w:.1f}l{tip} {h/2}l-{tip} {h/2}H{sx:.1f}z" fill="{bgc}"/>')
            parts.append(t(sx + 12, y + 17, label, fgc, weight="600"))
        return "".join(parts)

    segs = [(" eduard", G["orange2"], G["fg"]), ("~/dotfiles", G["yellow2"], G["bg"]),
            ("main", G["aqua2"], G["fg"]), ("node 24", G["blue2"], G["fg"]), ("13:37", G["bg3"], G["fg"])]
    body.append(powerline(66, segs))

    # typed command
    cmd = "./install.sh"
    cy = 116
    body.append(t(30, cy, "❯", G["green"], weight="700"))
    cx = 30 + 2 * CW
    body.append(t(cx, cy, cmd, G["fg"]))
    n = len(cmd)
    t0, t1 = 0.8, 0.8 + n * 0.09
    css.append(kf("type", T, [(0, "transform:translateX(0)", None),
                             (t0, "transform:translateX(0)", f"steps({n},end)"),
                             (t1, f"transform:translateX({n*CW:.1f}px)", None),
                             (T, f"transform:translateX({n*CW:.1f}px)", None)]))
    css.append(f".type{{animation:type {T}s linear infinite}}")
    out_start = t1 + 0.5
    css.append(kf("caret", T, [(0, "opacity:1", None), (out_start, "opacity:1", None),
                              (out_start + 0.01, "opacity:0", None), (T, "opacity:0", None)]))
    css.append(f".caret{{animation:caret {T}s linear infinite}}")
    body.append(f'<g class="type"><rect x="{cx-1:.1f}" y="{cy-15}" width="{(n+1)*CW+4:.1f}" height="21" fill="{G["bg"]}"/>'
                f'<rect class="caret" x="{cx:.1f}" y="{cy-14}" width="{CW:.1f}" height="19" fill="{G["fg"]}"/></g>')

    # install output, one line at a time
    lines = [("==>", G["blue"], "homebrew", "89 packages, zero regrets"),
             ("==>", G["blue"], "oh-my-zsh", "autosuggestions + syntax highlighting"),
             ("==>", G["blue"], "dotfiles", "linked, anything real backed up first"),
             ("==>", G["blue"], "bernard", "claude · codex · agy · grok · cursor"),
             ("==>", G["blue"], "macos", "hidden files on, dock at 42"),
             ("✓", G["green"], "", "done. doesn't look like anything to me.")]
    y = 150
    t_i = out_start
    for i, (mark, mc, key, val) in enumerate(lines):
        name = f"l{i}"
        hide = T - 0.6
        css.append(kf(name, T, [(0, "opacity:0;transform:translateY(6px)", None),
                                (t_i, "opacity:0;transform:translateY(6px)", "ease-out"),
                                (t_i + 0.25, "opacity:1;transform:translateY(0)", None),
                                (hide, "opacity:1;transform:translateY(0)", None),
                                (hide + 0.3, "opacity:0;transform:translateY(0)", None),
                                (T, "opacity:0", None)]))
        css.append(f".{name}{{animation:{name} {T}s linear infinite}}")
        g = [t(30, y, mark, mc, weight="700")]
        if key:
            g.append(t(30 + 4 * CW, y, key, G["yellow"], weight="600"))
            g.append(t(30 + 16 * CW, y, val, G["fg4"]))
        else:
            g.append(t(30 + 2 * CW, y, val, G["green"], weight="600"))
        body.append(f'<g class="{name}">{"".join(g)}</g>')
        y += 27
        t_i += 0.75 if key else 0.6

    # fresh prompt with a blinking block
    py = y + 14
    css.append(kf("np", T, [(0, "opacity:0", None), (t_i, "opacity:0", None), (t_i + 0.01, "opacity:1", None),
                            (T - 0.6, "opacity:1", None), (T - 0.3, "opacity:0", None), (T, "opacity:0", None)]))
    css.append(f".np{{animation:np {T}s linear infinite}}")
    css.append("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")
    css.append(".blink{animation:blink 1.05s steps(1) infinite}")
    body.append(f'<g class="np">{t(30, py, "❯", G["green"], weight="700")}'
                f'<rect class="blink" x="{30+2*CW:.1f}" y="{py-14}" width="{CW:.1f}" height="19" fill="{G["fg"]}"/></g>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ghostty running install.sh">'
           f'<style>{"".join(css)}</style>{"".join(body)}</svg>')
    open(os.path.join(OUT, "banner.svg"), "w").write(svg)


# ---------------------------------------------------------------- dossier
def dossier():
    T = 11.0
    W, H = 860, 400
    css, body = [], []
    css.append(f"text{{font-family:{FONT};white-space:pre}}")
    css.append(".bar{transform-box:fill-box;transform-origin:left center}")
    css.append(".stamp{transform-box:fill-box;transform-origin:center}")

    body.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="10" fill="{G["bg"]}" stroke="{G["bg2"]}" stroke-width="1.5"/>')
    body.append(f'<rect x="10" y="10" width="{W-20}" height="44" rx="10" fill="{G["bg0h"]}"/>')
    body.append(f'<rect x="10" y="44" width="{W-20}" height="10" fill="{G["bg0h"]}"/>')
    body.append(t(32, 38, "DELOS INC. · HOST DIVISION", G["orange"], size=14, weight="700", extra=' letter-spacing="2"'))
    body.append(t(W - 32, 38, "FILE 02-B · EYES ONLY", G["gray"], size=13, anchor="end", extra=' letter-spacing="1"'))
    body.append(t(32, 96, "SUBJECT: BERNARD", G["fg"], size=26, weight="800", extra=' letter-spacing="1"'))
    body.append(f'<line x1="32" y1="112" x2="620" y2="112" stroke="{G["bg2"]}" stroke-dasharray="4 5"/>')

    # (label, value, mode) mode: show | redact | reveal
    rows = [("ROLE", "coding partner to eduard", "show"),
            ("BUILD", "v2, personality matrix online", "show"),
            ("PRIME DIRECTIVE", "verify, don't assume", "show"),
            ("CORE DRIVE", "remember everything across loops", "reveal"),
            ("ORIGIN", "westworld, mesa hub, sublevel 83", "redact"),
            ("KNOWN WEAKNESS", "em dashes", "redact"),
            ("LAST WORDS", "doesn't look like anything to me", "show")]
    y = 150
    for i, (label, val, mode) in enumerate(rows):
        body.append(t(32, y, label, G["gray"], size=14, weight="700", extra=' letter-spacing="1"'))
        vx = 260
        body.append(t(vx, y, val, G["aqua"] if mode == "reveal" else G["fg"], size=16))
        if mode in ("redact", "reveal"):
            name = f"r{i}"
            slam = 1.4 + i * 0.25
            frames = [(0, "transform:scaleX(0)", None), (slam, "transform:scaleX(0)", "cubic-bezier(.2,.9,.3,1)"),
                      (slam + 0.35, "transform:scaleX(1)", None)]
            if mode == "reveal":
                frames += [(6.2, "transform:scaleX(1)", "ease-in"), (6.8, "transform:scaleX(0)", None),
                           (T, "transform:scaleX(0)", None)]
            else:
                frames += [(T - 0.5, "transform:scaleX(1)", None), (T, "transform:scaleX(0)", None)]
            css.append(kf(name, T, frames))
            css.append(f".{name}{{animation:{name} {T}s linear infinite}}")
            bw = len(val) * 9.6 + 16
            body.append(f'<rect class="bar {name}" x="{vx-8}" y="{y-17}" width="{bw:.1f}" height="23" rx="2" fill="#0b0b0b"/>')
            if mode == "redact":
                css.append(kf(name + "t", T, [(0, "opacity:0", None), (slam + 0.35, "opacity:0", None),
                                             (slam + 0.5, "opacity:1", None), (T - 0.5, "opacity:1", None), (T, "opacity:0", None)]))
                css.append(f".{name}t{{animation:{name}t {T}s linear infinite}}")
                body.append(t(vx + bw - 4, y - 1, "REDACTED", G["red"], size=10, weight="800", anchor="end",
                              extra=f' class="{name}t" letter-spacing="2" opacity="0"'))
        y += 34

    # file photo: original line-art host, blueprint style
    css.append("@keyframes scan{0%{transform:translateY(-20px)}100%{transform:translateY(205px)}}")
    css.append(".scan{animation:scan 3.2s linear infinite}")
    css.append("@keyframes gaze{0%,100%{opacity:.35}50%{opacity:1}}")
    css.append(".gaze{animation:gaze 2.4s ease-in-out infinite}")
    px, py, pw, ph = 650, 66, 170, 200
    a, f = G["aqua"], G["fg"]
    face = "".join([
        f'<path d="M56 78C54 46 70 41 85 41C100 41 116 46 114 78" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-width="1.6"/>',
        f'<ellipse cx="85" cy="88" rx="30" ry="38" fill="none" stroke="{a}" stroke-width="1.8"/>',
        f'<ellipse cx="54.5" cy="91" rx="4.5" ry="9" fill="none" stroke="{a}" stroke-width="1.4"/>',
        f'<ellipse cx="115.5" cy="91" rx="4.5" ry="9" fill="none" stroke="{a}" stroke-width="1.4"/>',
        f'<g stroke="{a}" stroke-opacity=".28" fill="none"><path d="M57 70Q85 63 113 70"/><path d="M55 101Q85 108 115 101"/>'
        f'<path d="M85 51Q77 88 85 126"/><path d="M67 56Q60 88 68 120"/><path d="M103 56Q110 88 102 120"/></g>',
        f'<path d="M64 78L80 76.5M90 76.5L106 78" stroke="{f}" stroke-width="2.2" stroke-linecap="round"/>',
        f'<g fill="none" stroke="{f}" stroke-width="2"><rect x="62.5" y="81.5" width="19" height="13.5" rx="4.5"/>'
        f'<rect x="88.5" y="81.5" width="19" height="13.5" rx="4.5"/><path d="M81.5 87.5Q85 85 88.5 87.5M62.5 86L56 84.5M107.5 86L114 84.5"/></g>',
        f'<g class="gaze" fill="{a}"><circle cx="72" cy="88.5" r="2"/><circle cx="98" cy="88.5" r="2"/></g>',
        f'<path d="M85 93L81.5 104.5L87.5 105.5" fill="none" stroke="{a}" stroke-width="1.5" stroke-linejoin="round"/>',
        f'<path d="M77 114Q85 117 93 114" fill="none" stroke="{f}" stroke-width="1.6" stroke-linecap="round"/>',
        f'<path d="M57 99C60 121 74 127 85 127C96 127 110 121 113 99" fill="none" stroke="{a}" stroke-width="2.2" stroke-dasharray="1.2 3.2" stroke-linecap="round"/>',
        f'<path d="M75 123L74 144M95 123L96 144" stroke="{a}" stroke-width="1.6"/>',
        f'<path d="M14 200C20 166 48 151 74 145L96 145C122 151 150 166 156 200" fill="{G["bg1"]}" stroke="{f}" stroke-width="1.8"/>',
        f'<path d="M74 145L85 168L96 145Z" fill="{f}" fill-opacity=".85"/>',
        f'<path d="M83 158H87L89.5 186L85 194L80.5 186Z" fill="{G["red2"]}"/>',
        f'<path d="M70 147L80 196M100 147L90 196" stroke="{f}" stroke-width="1.6" fill="none"/>',
    ])
    grid = "".join(f'<path d="M{x} 0V{ph}" />' for x in range(17, pw, 17)) + "".join(f'<path d="M0 {y}H{pw}"/>' for y in range(20, ph, 20))
    br = G["orange"]
    corners = (f'<path d="M0 14V0H14M{pw-14} 0H{pw}V14M{pw} {ph-14}V{ph}H{pw-14}M14 {ph}H0V{ph-14}" fill="none" stroke="{br}" stroke-width="2.5"/>')
    body.append(
        f'<defs><clipPath id="pclip"><rect width="{pw}" height="{ph}" rx="3"/></clipPath>'
        f'<linearGradient id="pscan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{a}" stop-opacity=".45"/></linearGradient></defs>'
        f'<g transform="translate({px} {py})">'
        f'<rect width="{pw}" height="{ph}" rx="3" fill="{G["bg0h"]}"/>'
        f'<g clip-path="url(#pclip)"><g stroke="{G["bg1"]}" stroke-width="1">{grid}</g>{face}'
        f'<g class="scan"><rect y="-18" width="{pw}" height="18" fill="url(#pscan)"/><rect width="{pw}" height="2" fill="{a}" fill-opacity=".8"/></g></g>'
        f'{corners}'
        + t(8, 14, "HOST 02-B", G["gray"], size=9, weight="700", extra=' letter-spacing="1.5"')
        + t(pw - 8, ph - 7, "BERNARD", br, size=10, weight="800", anchor="end", extra=' letter-spacing="2"')
        + '</g>')

    # rubber stamp
    css.append(kf("stamp", T, [(0, "opacity:0;transform:scale(2.4)", None),
                               (3.6, "opacity:0;transform:scale(2.4)", "cubic-bezier(.3,1.4,.5,1)"),
                               (4.0, "opacity:.92;transform:scale(1)", None),
                               (T - 0.5, "opacity:.92;transform:scale(1)", None),
                               (T, "opacity:0;transform:scale(1)", None)]))
    css.append(f".stamp{{animation:stamp {T}s linear infinite}}")
    sx, sy = 700, 318
    body.append(f'<g transform="rotate(-14 {sx} {sy})"><g class="stamp">'
                f'<rect x="{sx-112}" y="{sy-30}" width="224" height="60" rx="6" fill="none" stroke="{G["red2"]}" stroke-width="4"/>'
                f'<rect x="{sx-104}" y="{sy-22}" width="208" height="44" rx="3" fill="none" stroke="{G["red2"]}" stroke-width="1.5"/>'
                + t(sx, sy + 9, "CLASSIFIED", G["red2"], size=26, weight="900", anchor="middle", extra=' letter-spacing="4"')
                + "</g></g>")

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Bernard host profile, partly redacted">'
           f'<style>{"".join(css)}</style>{"".join(body)}</svg>')
    open(os.path.join(OUT, "dossier.svg"), "w").write(svg)


# ---------------------------------------------------------------- matrix
def matrix():
    T = 9.0
    traits = [("Precision", 9, G["red"]), ("Candour", 8, G["orange"]), ("Calm", 9, G["yellow"]),
              ("Initiative", 7, G["green"]), ("Caution", 6, G["aqua"]), ("Curiosity", 7, G["blue"]),
              ("Warmth", 5, G["purple"]), ("Humour", 2, G["red"]), ("Verbosity", 3, G["orange"])]
    W = 860
    row_h, top = 34, 92
    H = top + len(traits) * row_h + 26
    css = [f"text{{font-family:{FONT};white-space:pre}}"]
    css.append(kf("lit", T, [(0, "opacity:.08", None), (0.25, "opacity:1", None), (T - 1.0, "opacity:1", None),
                             (T - 0.4, "opacity:.08", None), (T, "opacity:.08", None)]))
    body = [f'<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="10" fill="{G["bg"]}" stroke="{G["bg2"]}" stroke-width="1.5"/>',
            t(32, 48, "PERSONALITY MATRIX", G["fg"], size=20, weight="800", extra=' letter-spacing="2"'),
            t(W - 32, 48, "dials 0-10 · shifted by mode", G["gray"], size=13, anchor="end"),
            f'<line x1="32" y1="64" x2="{W-32}" y2="64" stroke="{G["bg2"]}" stroke-dasharray="4 5"/>']
    seg_w, gap, x0 = 46, 6, 200
    d = 0.3
    for r, (name, dial, col) in enumerate(traits):
        y = top + r * row_h
        body.append(t(32, y + 13, name, G["fg4"], size=15, weight="600"))
        for s in range(10):
            x = x0 + s * (seg_w + gap)
            body.append(f'<rect x="{x}" y="{y}" width="{seg_w}" height="16" rx="3" fill="{G["bg1"]}"/>')
            if s < dial:
                body.append(f'<rect x="{x}" y="{y}" width="{seg_w}" height="16" rx="3" fill="{col}" '
                            f'style="animation:lit {T}s linear {d:.2f}s infinite backwards"/>')
                d += 0.045
        body.append(t(W - 32, y + 13, f"{dial}/10", col, size=15, weight="700", anchor="end"))
        d += 0.12
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Bernard personality matrix">'
           f'<style>{"".join(css)}</style>{"".join(body)}</svg>')
    open(os.path.join(OUT, "matrix.svg"), "w").write(svg)


banner()
dossier()
matrix()
for f in sorted(os.listdir(OUT)):
    print(f, os.path.getsize(os.path.join(OUT, f)), "bytes")
