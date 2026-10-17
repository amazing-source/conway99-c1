"""Decode a graph6 adjacency, with no graph-library dependency."""
import numpy as np
def read_graph6(path):
 b=path.read_bytes().strip()
 if b.startswith(b'>>graph6<<'):b=b[10:]
 d=[x-63 for x in b];assert all(0<=x<64 for x in d)
 if d[0]<63:n=d[0];off=1
 elif d[1]<63:n=(d[1]<<12)+(d[2]<<6)+d[3];off=4
 else:n=0;off=8
 if off==8:
  for x in d[2:8]:n=(n<<6)+x
 assert n<=10000 and len(d)-off==(n*(n-1)//2+5)//6
 A=np.zeros((n,n),dtype=np.int64);pos=0
 for j in range(1,n):
  for i in range(j):
   bit=(d[off+pos//6]>>(5-pos%6))&1;A[i,j]=A[j,i]=bit;pos+=1
 return A
