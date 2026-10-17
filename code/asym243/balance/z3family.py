import numpy as np
# explicit Z3-symmetric family for q=3, d=1: a=(x,0,z), b=(u,v,w) rotated by 120 deg about e_z
for z in [0.0, 0.1, 0.3, 0.5, 0.7]:
    w = np.sqrt(1 - 2*z*z); x = np.sqrt(1 - z*z); u = -z*w/x; v = np.sqrt(max(0, 1 - w*w - u*u))
    Rz = lambda t: np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    a = [Rz(2*np.pi*k/3) @ np.array([x, 0, z]) for k in range(3)]
    b = [Rz(2*np.pi*k/3) @ np.array([u, v, w]) for k in range(3)]
    V = np.column_stack([np.sqrt(2/3)*a[0], np.sqrt(1/3)*b[0], np.sqrt(2/3)*a[1], np.sqrt(1/3)*b[1], np.sqrt(2/3)*a[2], np.sqrt(1/3)*b[2]])
    P = V.T @ V; U = 2*P - np.eye(6)          # basis r1 s1 r2 s2 r3 s3
    ok = np.allclose(P @ P, P) and all(np.allclose(P[2*i:2*i+2, 2*i:2*i+2], np.diag([2/3, 1/3])) for i in range(3))
    C = U[np.ix_([0, 2, 4], [0, 2, 4])]; ev = np.linalg.eigvalsh(C)
    print(f"z={z}: valid={ok}  eig(Pi_R U Pi_R)={np.round(ev,4)}  trace={ev.sum():.4f}")
