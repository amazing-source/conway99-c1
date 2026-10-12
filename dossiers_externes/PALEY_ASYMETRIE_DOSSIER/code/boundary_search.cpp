#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <vector>
#include <random>
#include <string>
using U=uint32_t; using D=std::vector<std::vector<U>>;
int n,lam,mu;int C[25][25];std::vector<std::pair<int,int>> twins;
U chosen[25];uint64_t nodes=0,sols=0,labelled=0,cap=1000,nodecap=1000000;
bool stopped=false;double seconds=20;std::chrono::steady_clock::time_point start;
bool compatible(int i,U x,int j,U y){int a=(x>>j)&1u;return a==int((y>>i)&1u)&&__builtin_popcount(x&y)+C[i][j]==mu+(lam-mu)*a;}
void dfs(const D& dom,U left,uint64_t weight){
 if(stopped)return;nodes++;
 if(nodes>nodecap||(nodes%1024==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>seconds)){stopped=true;return;}
 if(!left){sols++;labelled+=weight;std::cout<<"SOL "<<weight;for(int i=0;i<n;i++)std::cout<<" "<<chosen[i];std::cout<<"\n";if(sols>=cap)stopped=true;return;}
 int i=-1;for(int j=0;j<n;j++)if(left>>j&1u)if(i<0||dom[j].size()<dom[i].size())i=j;
 U rest=left^(1u<<i);std::vector<std::pair<int,int>> equal;
 for(auto [u,v]:twins)if((rest>>u&1u)&&(rest>>v&1u)){
   bool ok=true;for(int a=0;a<n;a++)if(!(left>>a&1u)&&((chosen[a]>>u&1u)!=(chosen[a]>>v&1u))){ok=false;break;}
   if(ok)equal.push_back({u,v});
 }
 for(U x:dom[i]){
   bool canonical=true;for(auto[u,v]:equal)if(!(x>>u&1u)&&(x>>v&1u)){canonical=false;break;}
   if(!canonical)continue;int split=0;for(auto[u,v]:equal)if((x>>u&1u)!=(x>>v&1u))split++;
   D next(n);bool ok=true;
   for(int j=0;j<n;j++)if(rest>>j&1u){
     for(U y:dom[j])if(compatible(i,x,j,y))next[j].push_back(y);
     if(next[j].empty()){ok=false;break;}
   }
   if(!ok)continue;chosen[i]=x;dfs(next,rest,weight*(1ull<<split));if(stopped)return;
 }
}
int main(int argc,char**argv){
 if(!(std::cin>>n>>lam>>mu)||n<1||n>24)return 2;D dom(n);
 for(auto&v:dom){int k;std::cin>>k;v.resize(k);for(auto&x:v)std::cin>>x;}
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)std::cin>>C[i][j];
 int nt=0;if(std::cin>>nt)for(int i=0;i<nt;i++){int u,v;std::cin>>u>>v;twins.push_back({u,v});}
 if(argc>1)cap=std::stoull(argv[1]);if(argc>2)seconds=std::stod(argv[2]);if(argc>3)nodecap=std::stoull(argv[3]);
 if(argc>4){std::mt19937 rng(std::stoi(argv[4]));for(auto&v:dom)std::shuffle(v.begin(),v.end(),rng);}
 start=std::chrono::steady_clock::now();dfs(dom,(1u<<n)-1,1);
 std::cout<<"END "<<(stopped?"STOPPED":"EXHAUSTED")<<" nodes "<<nodes<<" solutions "<<sols<<" labelled "<<labelled<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
}
