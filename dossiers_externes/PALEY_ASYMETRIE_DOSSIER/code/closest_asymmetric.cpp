#include <iostream>
#include <vector>
#include <cstdint>
#include <climits>
int main(){int n,nt,ns;std::cin>>n>>nt;std::vector<std::pair<int,int>> tw(nt);for(auto&[a,b]:tw)std::cin>>a>>b;
std::vector<uint32_t>A(n);for(auto&x:A)std::cin>>x;std::cin>>ns;int global=INT_MAX,bestsi=-1,bestg=-1,bestid=-1;
std::vector<uint32_t>best;
for(int s=0;s<ns;s++){int id;std::cin>>id;std::vector<uint32_t>D(n);for(auto&x:D)std::cin>>x;
for(int g=0;g<(1<<nt);g++){int p[25];for(int i=0;i<n;i++)p[i]=i;for(int z=0;z<nt;z++)if(g>>z&1)std::swap(p[tw[z].first],p[tw[z].second]);
int dif=0;for(int i=0;i<n&&dif<global;i++)for(int j=i+1;j<n;j++){dif+=int((A[i]>>j&1u)!=(D[p[i]]>>p[j]&1u));if(dif>=global)break;}
if(dif<global){global=dif;bestsi=s;bestg=g;bestid=id;best.assign(n,0);for(int i=0;i<n;i++)for(int j=0;j<n;j++)best[i]|=(D[p[i]]>>p[j]&1u)<<j;std::cerr<<"BEST "<<global<<" id "<<id<<" sample "<<s<<" relabel "<<g<<"\n";}
}}
std::cout<<"RESULT "<<global<<" "<<bestsi<<" "<<bestg<<" "<<bestid<<"\nROWS";for(auto x:best)std::cout<<" "<<x;std::cout<<"\n";
}