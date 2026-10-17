#include <cstdint>
#include <vector>
#include <iostream>
int main(){int n,p,k,lam,mu;if(!(std::cin>>n>>k>>lam>>mu>>p)||n>25||n<1||p<1||p>=n)return 2;std::vector<uint32_t>A(n);for(auto&x:A)std::cin>>x;std::vector<int>S(p),F;uint32_t sm=0;for(auto&x:S){std::cin>>x;sm|=1u<<x;}for(int i=0;i<n;i++)if(!(sm>>i&1))F.push_back(i);int f=F.size();std::vector<uint32_t>B(p);std::vector<std::vector<int>>rhs(p,std::vector<int>(f));for(int a=0;a<p;a++)for(int i=0;i<f;i++){B[a]|=((A[S[a]]>>F[i])&1u)<<i;rhs[a][i]=mu+(lam-mu)*int((A[S[a]]>>F[i])&1u)-__builtin_popcount(A[S[a]]&A[F[i]]&sm);}std::cout<<f<<" "<<lam<<" "<<mu<<"\n";for(int i=0;i<f;i++){int need=k-__builtin_popcount(A[F[i]]&sm);std::vector<uint32_t>dom;for(uint32_t m=0;m<(1u<<f);m++){if((m>>i&1)||__builtin_popcount(m)!=need)continue;bool ok=true;for(int a=0;a<p;a++)if(__builtin_popcount(m&B[a])!=rhs[a][i]){ok=false;break;}if(ok)dom.push_back(m);}std::cout<<dom.size();for(auto m:dom)std::cout<<" "<<m;std::cout<<"\n";}for(int i=0;i<f;i++){for(int j=0;j<f;j++)std::cout<<__builtin_popcount(A[F[i]]&A[F[j]]&sm)<<" ";std::cout<<"\n";}
std::vector<std::pair<int,int>>twins;
for(int i=0;i<f;i++){std::vector<int>cl;for(int j=0;j<f;j++)if((A[F[i]]&sm)==(A[F[j]]&sm))cl.push_back(j);if(cl.size()==2&&cl[0]==i)twins.push_back({cl[0],cl[1]});}
std::cout<<twins.size()<<"\n";for(auto[u,v]:twins)std::cout<<u<<" "<<v<<"\n";
}