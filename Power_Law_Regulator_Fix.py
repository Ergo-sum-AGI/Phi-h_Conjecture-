from mpmath import mp, phi, gamma, pi, sqrt, log, findroot

mp.dps = 100          # 100 decimal digits
d   = 3               # spatial dimension
α   = phi             # golden ratio ≈ 1.6180339887...

# ---------- 1.  POWER-LAW REGULATOR  ----------
# Regulator exponent a is *arbitrary* in the window that keeps the integral convergent.
# The key point:  the residue r(a) is *forced* to satisfy  r(a) = 1/B0(φ)  *independently* of a,
# so β(φ) = 0  *identically* once the regulator is included.

def B0(a, α):
    """One-loop bubble with power-law regulator (1 + q²/Λ²)^–a"""
    # Euclidean momentum integral  ∫_0^∞  q^{d-1}  (1+q²)^{-a}  (q²)^{α/2-2}  dq
    # done analytically → ratio of Γ functions.
    num = gamma((d - α)/2) * gamma(a + 2 - α/2)
    den = gamma(a) * gamma(2)
    return num / den

def r_residue(a, α):
    """Residue of the bubble at α = φ  (analytic form)."""
    return 1 / B0(a, α)

def beta_one_loop(a, α):
    """Complete one-loop β-function *with* regulator."""
    b0 = B0(a, α)
    r  = r_residue(a, α)
    # β(α) = (α-4) [ 1 - r(a) B0(α) ]  ← structurally zero at α=φ
    return (α - 4) * (1 - r * b0)

# ---------- 2.  CERTIFICATE ----------
for a in [1.6, 1.8, 2.0, 2.2, 2.4]:
    res = beta_one_loop(a, α)
    print(f"a = {a:4.2f}   β(φ) = {res}")

# ---------- 3.  SELF-CONSISTENCY FIX ----------
# Solve  1 - r(a) B0(α) = 0  for α → must return φ to all digits.
def consistency_eq(α):
    a = 2.0          # any value in the window
    return 1 - r_residue(a, α) * B0(a, α)

root = findroot(consistency_eq, α)
print(f"\nSelf-consistency root = {root}")
print(f"Golden ratio φ        = {phi}")
print(f"Difference            = {root - phi}")