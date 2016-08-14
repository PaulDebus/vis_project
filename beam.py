def run(L, B, H, X, P, E):
    alpha = X/L
    beta = (L-X)/L
    moment_inertia = (B*H**3)/12
    f = min(alpha, beta)
    U = (3-4*f**2)/(48*E*moment_inertia)*f*P*L**3

    Va = beta*P
    Vb = alpha*P

    M = alpha*beta*P*L
    return(L, B, H, X, P, E, Va, Vb, M, U)
