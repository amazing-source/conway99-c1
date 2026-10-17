"""Exact supplementary checks of the switching difference and supported eigenspaces.
Standard library only. Not needed for the two elementary asymmetry proofs.
"""
from fractions import Fraction
from pathlib import Path
from verify_witness import read_adj, require

ROOT=Path(__file__).resolve().parents[1]
def matmul(A,B):
    BT=list(zip(*B))
    return [[sum(x*y for x,y in zip(r,c))for c in BT]for r in A]
def rank(A):
    M=[list(map(Fraction,row))for row in A]
    if not M:return 0
    r=0
    for c in range(len(M[0])):
        pivot=next((i for i in range(r,len(M))if M[i][c]),None)
        if pivot is None:continue
        M[r],M[pivot]=M[pivot],M[r]
        p=M[r][c];M[r]=[x/p for x in M[r]]
        for i in range(r+1,len(M)):
            p=M[i][c]
            if p:M[i]=[x-p*y for x,y in zip(M[i],M[r])]
        r+=1
        if r==len(M):break
    return r
def main():
    ar=read_adj(ROOT/"data/paley25.adj");br=read_adj(ROOT/"data/paley25_to_asymmetric.adj")
    A=[[ar[i]>>j&1 for j in range(25)]for i in range(25)]
    B=[[br[i]>>j&1 for j in range(25)]for i in range(25)]
    E=[[B[i][j]-A[i][j]for j in range(25)]for i in range(25)]
    S=[4,8,12,16,20];F=sorted(set(range(25))-set(S))
    Y=[[A[i][j]for j in F]for i in S]
    D=[[A[i][j]for j in F]for i in F]
    e=[[E[i][j]for j in F]for i in F]
    require(all(x==0 for row in matmul(Y,e)for x in row),"Y E != 0")
    de=matmul(D,e);ed=matmul(e,D);ee=matmul(e,e)
    require(all(de[i][j]+ed[i][j]+ee[i][j]+e[i][j]==0
                for i in range(20)for j in range(20)),"Difference identity fails")
    require(rank(E)==10,"Difference rank not ten")
    projector2=[[5*A[i][j]+15*(i==j)-3 for j in range(25)]for i in range(25)]
    projectorm3=[[-5*A[i][j]+10*(i==j)+2 for j in range(25)]for i in range(25)]
    dims=[]
    for U in [S,sorted(S+[3,7,11,15,24])]:
        dims.append([12-rank([[P[i][j]for j in U]for i in U])for P in [projector2,projectorm3]])
    require(dims==[[7,8],[2,4]],"Supported eigenspace dimension mismatch")
    # Newton identities for the ten nonzero eigenvalues. Rank(E)=10 and symmetry
    # account for the other fifteen zero eigenvalues.
    power=[[int(i==j)for j in range(25)]for i in range(25)]
    traces=[0]
    coefficients=[1]
    for k in range(1,11):
        power=matmul(power,E)
        traces.append(sum(power[i][i]for i in range(25)))
        numerator=-sum(coefficients[k-j]*traces[j]for j in range(1,k+1))
        require(numerator%k==0,"Nonintegral characteristic coefficient")
        coefficients.append(numerator//k)
    require(coefficients==[1,0,-74,0,2041,0,-25636,0,141060,0,-252000],
            "Characteristic polynomial mismatch")
    print("Y E = 0; D E + E D + E^2 + E = 0: exact.")
    print("Difference rank: 10; characteristic polynomial coefficients: checked.")
    print("Supported eigenspace dimensions: (7,8) with one K5; (2,4) with the two specified K5s.")
if __name__=="__main__":
    main()
