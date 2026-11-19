import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

def term(d, xy, lab, loc):
    d += elm.Dot(open=True).at(xy).label(lab, loc=loc, color=COPPER, fontsize=13)

# 9.1 delta and star
d = drawing()
A, B, C = (0, 0), (4, 0), (2, 3.46)
d += elm.ResistorIEC().endpoints(C, A).label("R$_{ca}$", loc="bot")
d += elm.ResistorIEC().endpoints(C, B).label("R$_{bc}$", loc="top")
d += elm.ResistorIEC().endpoints(A, B).label("R$_{ab}$", loc="bot")
term(d, A, "a", "left"); term(d, B, "b", "right"); term(d, C, "c", "top")
d += elm.Label().at((2, -1.4)).label("(a) delta (Δ)", fontsize=12)
ox = 7.5
A2, B2, C2, N = (ox, 0), (ox + 4, 0), (ox + 2, 3.46), (ox + 2, 1.15)
d += elm.ResistorIEC().endpoints(A2, N).label("R$_a$", loc="top")
d += elm.ResistorIEC().endpoints(B2, N).label("R$_b$", loc="bot")
d += elm.ResistorIEC().endpoints(C2, N).label("R$_c$", loc="bot")
d += elm.Dot().at(N)
term(d, A2, "a", "left"); term(d, B2, "b", "right"); term(d, C2, "c", "top")
d += elm.Label().at((ox + 2, -1.4)).label("(b) star (Y)", fontsize=12)
save_drawing(d, "ch09_shapes")

# 9.2 pi and T
d = drawing()
d += elm.Dot(open=True).at((0, 2.5)).label("a", loc="left", color=COPPER)
d += elm.Line().right(0.6)
d += (j1 := elm.Dot())
d += elm.ResistorIEC().right().label("R$_{ab}$", loc="top")
d += (j2 := elm.Dot())
d += elm.Line().right(0.6)
d += elm.Dot(open=True).label("b", loc="right", color=COPPER)
d += elm.ResistorIEC().down().at(j1.center).length(2.5).label("R$_{ca}$", loc="top")
d += elm.ResistorIEC().down().at(j2.center).length(2.5).label("R$_{bc}$", loc="bot")
d += elm.Line().at((0, 0)).to((4.2, 0))
d += elm.Dot(open=True).at((0, 0)).label("c", loc="left", color=COPPER)
d += elm.Dot(open=True).at((4.2, 0)).label("c", loc="right", color=COPPER)
d += elm.Label().at((2.1, -1.0)).label("(a) π network = delta", fontsize=11)
ox = 7
d += elm.Dot(open=True).at((ox, 2.5)).label("a", loc="left", color=COPPER)
d += elm.ResistorIEC().right().length(2.2).label("R$_a$", loc="top")
d += (n := elm.Dot())
d += elm.ResistorIEC().right().length(2.2).label("R$_b$", loc="top")
d += elm.Dot(open=True).label("b", loc="right", color=COPPER)
d += elm.ResistorIEC().down().at(n.center).length(2.5).label("R$_c$", loc="bot")
d += elm.Line().at((ox, 0)).to((ox + 4.4, 0))
d += elm.Dot(open=True).at((ox, 0)).label("c", loc="left", color=COPPER)
d += elm.Dot(open=True).at((ox + 4.4, 0)).label("c", loc="right", color=COPPER)
d += elm.Label().at((ox + 2.2, -1.0)).label("(b) T network = star", fontsize=11)
save_drawing(d, "ch09_pi_t")

# 9.3 Unbalanced bridge example
def bridge(d, star=False):
    d += elm.SourceV().up().length(4).label("20 V", loc="top")
    ox = 2.5
    T, L, Rp, Bt = (ox + 1.8, 4), (ox, 2), (ox + 3.6, 2), (ox + 1.8, 0)
    d += elm.Line().at((0, 4)).to(T)
    if not star:
        d += elm.ResistorIEC().endpoints(T, L).label("R$_1$ = 6 Ω", loc="top")
        d += elm.ResistorIEC().endpoints(T, Rp).label("R$_2$ = 3 Ω", loc="top")
        d += elm.ResistorIEC().endpoints(L, Rp).label("R$_5$ = 9 Ω", loc="top")
    else:
        N = (ox + 1.8, 2.75)
        d += elm.ResistorIEC().endpoints(T, N).length(1.25).label("1 Ω", loc="bot") if False else elm.Line().length(0.001)
        d += elm.ResistorIEC().endpoints((ox + 1.8, 5.6), N).label("R$_T$ = 1 Ω", loc="bot")
        d += elm.ResistorIEC().endpoints(N, L).label("R$_C$ = 3 Ω", loc="top")
        d += elm.ResistorIEC().endpoints(N, Rp).label("R$_D$ = 1.5 Ω", loc="top")
        d += elm.Dot().at(N).label("N", loc="right", color=TEAL)
    d += elm.ResistorIEC().endpoints(L, Bt).label("R$_3$ = 5 Ω", loc="bot")
    d += elm.ResistorIEC().endpoints(Rp, Bt).label("R$_4$ = 6.5 Ω", loc="bot")
    d += elm.Dot().at(T if not star else (ox + 1.8, 5.6)).label("T", loc="top", color=COPPER)
    d += elm.Dot().at(L).label("C", loc="left", color=COPPER); d += elm.Dot().at(Rp).label("D", loc="right", color=COPPER)
    d += elm.Dot().at(Bt).label("B", loc="bot", color=COPPER)
    d += elm.Line().at(Bt).to((0, 0))

d = drawing(); bridge(d); save_drawing(d, "ch09_bridge")
d = drawing()
d += elm.SourceV().up().length(5.6).label("20 V", loc="top")
ox = 2.5
T2, N, L, Rp, Bt = (ox + 1.8, 5.6), (ox + 1.8, 3.4), (ox, 1.8), (ox + 3.6, 1.8), (ox + 1.8, 0)
d += elm.Line().at((0, 5.6)).to(T2)
d += elm.ResistorIEC().endpoints(T2, N).label("R$_T$ = 1 Ω", loc="bot")
d += elm.ResistorIEC().endpoints(N, L).label("R$_C$ = 3 Ω", loc="top")
d += elm.ResistorIEC().endpoints(N, Rp).label("R$_D$ = 1.5 Ω", loc="top")
d += elm.ResistorIEC().endpoints(L, Bt).label("R$_3$ = 5 Ω", loc="bot")
d += elm.ResistorIEC().endpoints(Rp, Bt).label("R$_4$ = 6.5 Ω", loc="bot")
d += elm.Dot().at(T2).label("T", loc="top", color=COPPER); d += elm.Dot().at(N).label("N", loc="right", color=TEAL)
d += elm.Dot().at(L).label("C", loc="left", color=COPPER); d += elm.Dot().at(Rp).label("D", loc="right", color=COPPER)
d += elm.Dot().at(Bt).label("B", loc="bot", color=COPPER)
d += elm.Line().at(Bt).to((0, 0))
save_drawing(d, "ch09_bridge_star")

# 9.4 Motor windings star and delta
d = drawing()
L1, L2, L3 = (0, 3.46), (-2, 0), (2, 0)
N = (0, 1.15)
for P, lab in [(L1, "L1"), (L2, "L2"), (L3, "L3")]:
    d += elm.Inductor2().endpoints(P, N) if False else elm.Inductor().endpoints(P, N)
    d += elm.Dot(open=True).at(P).label(lab, loc="top" if P == L1 else ("left" if P == L2 else "right"))
d += elm.Dot().at(N)
d += elm.Label().at((0, -1.2)).label("star: each winding gets 230 V", fontsize=10.5)
ox = 7.5
M1, M2, M3 = (ox, 3.46), (ox - 2, 0), (ox + 2, 0)
d += elm.Inductor().endpoints(M1, M2); d += elm.Inductor().endpoints(M3, M1); d += elm.Inductor().endpoints(M2, M3)
for P, lab in [(M1, "L1"), (M2, "L2"), (M3, "L3")]:
    d += elm.Dot(open=True).at(P).label(lab, loc="top" if P == M1 else ("left" if P == M2 else "right"))
d += elm.Label().at((ox, -1.2)).label("delta: each winding gets 400 V", fontsize=10.5)
save_drawing(d, "ch09_motor")
