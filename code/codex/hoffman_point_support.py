"""Necessary common missing-point incidences for a collection of covers.

Every erased point must meet every realised closed outside neighbourhood in
exactly two blocks. These two blocks cannot already share a retained point,
because the closed neighbourhood is a linear double cover of the coclique.
The SAME erased-point rows must work for all selected neighbourhoods.
"""
from itertools import combinations


class PointSupport:
    def __init__(self, point_rows, covers, known_overlap, missing_quotas, count):
        self.point_rows=point_rows
        self.count=count
        self.quota=missing_quotas
        self.by_col=[]
        for j in range(len(missing_quotas)):
            packed=bytearray((len(point_rows)+7)//8)
            for a,row in enumerate(point_rows):
                if j in row:packed[a//8] |= 1<<(a%8)
            self.by_col.append(int.from_bytes(packed,'little'))
        self.universe=(1<<len(point_rows))-1
        self.masks={}
        for cover in covers:
            cols=[j for j in range(len(missing_quotas)) if cover>>j&1]
            b0=b1=b2=b3=0
            for j in cols:
                carry=self.by_col[j]
                b0,carry=b0^carry,b0&carry
                b1,carry=b1^carry,b1&carry
                b2,carry=b2^carry,b2&carry
                b3 ^= carry
            live=self.universe & ~b0 & b1 & ~b2 & ~b3
            for j,k in combinations(cols,2):
                if known_overlap[j][k]:live &= ~(self.by_col[j]&self.by_col[k])
            self.masks[cover]=live

    def possible(self,live):
        if live.bit_count()<self.count:return False
        return all((live&col).bit_count()>=q for col,q in zip(self.by_col,self.quota) if q)

    def describe(self,live):
        return dict(point_rows=live.bit_count(),required_distinct_rows=self.count,
                    deficits=[dict(column=j,available=(live&col).bit_count(),required=q)
                              for j,(col,q) in enumerate(zip(self.by_col,self.quota))
                              if (live&col).bit_count()<q])
