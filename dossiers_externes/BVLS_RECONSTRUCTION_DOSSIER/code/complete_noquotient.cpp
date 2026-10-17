// Exact row CSP + partial-state permutation reduction, with labelled completion weights.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <chrono>
#include <string>
#include <map>
#include <boost/multiprecision/cpp_int.hpp>
using Big=boost::multiprecision::cpp_int;
struct Mask{std::array<unsigned long long,4>w;bool bit(int i)const{return (w[i/64]>>(i%64))&1;}};
int n;std::vector<std::vector<Mask>> rows;std::vector<std::vector<int>>Z;
std::vector<int>picked;std::ofstream out;unsigned long long nodes=0,leaves=0,maxleaves;Big total=0;bool stopped=false;double seconds;
std::chrono::steady_clock::time_point t0;
int dot(const Mask&a,const Mask&b){int s=0;for(int k=0;k<4;k++)s+=__builtin_popcountll(a.w[k]&b.w[k]);return s;}
bool compat(int i,int a,int j,int b){const auto&r=rows[i][a];const auto&s=rows[j][b];int e=r.bit(j);return e==s.bit(i) && dot(r,s)+Z[i][j]==2-e;}
Big binom(int m,int k){Big b=1;for(int j=1;j<=k;j++){b*=m-j+1;b/=j;}return b;}
void dfs(std::vector<std::vector<int>>dom,std::vector<int>colors,Big weight,int depth){
 if(stopped)return;nodes++;
 if(nodes%1024==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()>seconds){stopped=true;return;}
 if(depth==n){leaves++;total+=weight;out<<weight<<' ';for(int a:picked)out<<a<<' ';out<<'\n';if(leaves>=maxleaves)stopped=true;return;}
 int i=-1;
 for(int j=0;j<n;j++)if(picked[j]<0&&(i<0||dom[j].size()<dom[i].size()))i=j;
 if(dom[i].empty())return;
 std::map<int,std::vector<int>>groups;for(int j=0;j<n;j++)if(picked[j]<0&&j!=i)groups[colors[j]].push_back(j);
 for(int a:dom[i]){
  const Mask&r=rows[i][a];bool good=true;Big mult=1;
  for(const auto&[c,grp]:groups){if(true)continue;int ones=0;bool zero=false;for(int j:grp){if(r.bit(j)){if(zero){good=false;break;}ones++;}else zero=true;}if(!good)break;mult*=binom(grp.size(),ones);}
  if(!good)continue;
  auto nd=dom;for(int j=0;j<n;j++)if(picked[j]<0&&j!=i){
   nd[j].clear();for(int b:dom[j])if(compat(i,a,j,b))nd[j].push_back(b);
   if(nd[j].empty()){good=false;break;}
  }
  if(!good)continue;
  auto nc=colors;std::map<std::pair<int,bool>,int>cd;
  for(int j=0;j<n;j++)if(picked[j]<0&&j!=i){auto key=std::make_pair(colors[j],r.bit(j));if(!cd.count(key))cd[key]=cd.size();nc[j]=cd[key];}
  picked[i]=a;dfs(std::move(nd),std::move(nc),weight*mult,depth+1);picked[i]=-1;if(stopped)return;
 }
}
int main(int argc,char**argv){if(argc<5)return 2;std::ifstream in(argv[1]);in>>n;if(!in||n>256)return 2;std::vector<int>colors(n);for(int&c:colors)in>>c;Z.assign(n,std::vector<int>(n));for(auto&r:Z)for(int&c:r)in>>c;rows.resize(n);std::vector<std::vector<int>>dom(n);for(int i=0;i<n;i++){int k;in>>k;rows[i].resize(k);for(int a=0;a<k;a++){for(auto&w:rows[i][a].w)in>>w;dom[i].push_back(a);}}if(!in)return 2;out.open(argv[2]);seconds=std::stod(argv[3]);maxleaves=std::stoull(argv[4]);picked.assign(n,-1);t0=std::chrono::steady_clock::now();dfs(dom,colors,Big(1),0);std::cout<<(stopped?"STOPPED":"EXHAUSTED")<<" nodes "<<nodes<<" leaves "<<leaves<<" labelled "<<total<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()<<'\n';}
