#include <cstdint>
#include <iostream>
#include <vector>
int main(){int n;if(!(std::cin>>n)||n>25||n<1)return 2;std::vector<uint32_t>a(n);for(auto&x:a)std::cin>>x;uint32_t full=(1u<<n)-1;int count[31]={0};
for(uint32_t s=1;s<full;s++){int k=__builtin_popcount(s);if(k<4||(k&1))continue;int d=-1;bool ok=true;for(uint32_t r=s;r;r&=r-1){int u=__builtin_ctz(r),du=__builtin_popcount(a[u]&s);if(d<0)d=du;else if(d!=du){ok=false;break;}}if(!ok)continue;
for(uint32_t r=full^s;r;r&=r-1){int u=__builtin_ctz(r),du=__builtin_popcount(a[u]&s);if(du!=0&&du!=k/2&&du!=k){ok=false;break;}}if(ok){count[k]++;std::cout<<"SET "<<k<<" "<<s<<"\n";}}
for(int k=4;k<=n;k+=2)std::cout<<"COUNT "<<k<<" "<<count[k]<<"\n";}