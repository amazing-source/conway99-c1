// Exact binary row-domain enumeration for a fixed SRG boundary.
// Integer arithmetic; STOPPED is never a complete domain.
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using Mask=std::bitset<256>;
int nf,ns,target,depth0; std::vector<int> previous; std::vector<Mask> rowmask,conflict;std::vector<std::vector<int>> colrows;
std::uint64_t nodes=0,count=0,limit;double seconds;bool stopped=false;
std::chrono::steady_clock::time_point t0;std::ofstream out;
void dfs(Mask available,Mask chosen,std::vector<int> r,int left){
 if(stopped)return;
 nodes++;
 if((nodes&16383)==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()>seconds){stopped=true;return;}
 if(left<0)return;
 for(int s=0;s<ns;s++){if(r[s]<0)return;if(r[s]==0)available&=~rowmask[s];}
 if((int)available.count()<left)return;
 if(left==0){for(int v:r)if(v)return; ++count;
  if(out.is_open()){for(int a=0;a<nf;a++)if(chosen[a])out<<a<<' ';out<<'\n';}
  if(count>=limit)stopped=true;return;}
 int sr=-1,best=100000000;
 for(int s=0;s<ns;s++)if(r[s]){
  int m=(available&rowmask[s]).count(),w;
  if(m<r[s])return;
  if(r[s]==1)w=m;else if(r[s]==2)w=m*(m-1)/2;else w=10000000+m;
  if(w<best){best=w;sr=s;}
 }
 if(sr==-1){ // Generic fallback for zero columns: canonical subset order.
  int first=-1;for(int a=0;a<nf;a++)if(available[a]){first=a;break;}
  if(first<0)return;
  auto av=available;av.reset(first);dfs(av,chosen,r,left);
  chosen.set(first);av&=~conflict[first];dfs(av,chosen,r,left-1);return;
 }
 auto opts=available&rowmask[sr]; auto next=available&~rowmask[sr];
 std::vector<int> ls;for(int a=0;a<nf;a++)if(opts[a])ls.push_back(a);
 // Counts <=2 for this campaign. Reject unsupported constraints explicitly.
 if(r[sr]>2){std::cerr<<"unsupported quota\n";std::exit(3);}
 if(r[sr]==1){for(int a:ls){if(previous[a]>=0&&!chosen[previous[a]])continue;auto rr=r;for(int s:colrows[a])rr[s]--;auto cc=chosen;cc.set(a);dfs(next&~conflict[a],cc,std::move(rr),left-1);}}
 else for(int i=0;i<(int)ls.size();i++)for(int j=i+1;j<(int)ls.size();j++){
  int a=ls[i],b=ls[j];if(conflict[a][b])continue;if(previous[a]>=0&&!chosen[previous[a]])continue;if(previous[b]>=0&&previous[b]!=a&&!chosen[previous[b]])continue;
  auto rr=r;for(int s:colrows[a])rr[s]--;for(int s:colrows[b])rr[s]--;
  auto cc=chosen;cc.set(a);cc.set(b);dfs(next&~conflict[a]&~conflict[b],cc,std::move(rr),left-2);
 }
}
int main(int argc,char**argv){
 if(argc<5){std::cerr<<"rows INSTANCE PREFIX seconds limit [first last]\n";return 2;}
 std::ifstream in(argv[1]);in>>ns>>nf;if(!in||nf>256||ns>256){std::cerr<<"bad input\n";return 2;}
 rowmask.resize(ns);colrows.resize(nf);conflict.resize(nf);
 for(int s=0;s<ns;s++)for(int a=0;a<nf;a++){int b;in>>b;if(b){rowmask[s].set(a);colrows[a].push_back(s);}}
 std::vector<std::vector<int>>R(nf,std::vector<int>(ns));std::vector<int>d(nf);
 for(int a=0;a<nf;a++){in>>d[a];for(int s=0;s<ns;s++)in>>R[a][s];}
 if(!in){std::cerr<<"short input\n";return 2;}
 for(int a=0;a<nf;a++)for(int b=0;b<nf;b++){
  int c=0;for(int s:colrows[a])if(rowmask[s][b])c++;
  if(a==b||c>=2)conflict[a].set(b);
 }
 seconds=std::stod(argv[3]);limit=std::stoull(argv[4]);
 int first=argc>5?std::stoi(argv[5]):0,last=argc>6?std::stoi(argv[6]):nf;
 for(target=first;target<last;target++){
  previous.assign(nf,-1);for(int a=0;a<nf;a++)if(a!=target)for(int b=0;b<a;b++)if(b!=target && colrows[a]==colrows[b])previous[a]=b;
  nodes=count=0;stopped=false;t0=std::chrono::steady_clock::now();
  if(std::string(argv[2])!="-")out.open(std::string(argv[2])+"_"+std::to_string(target)+".rows");
  Mask av;for(int a=0;a<nf;a++)if(a!=target)av.set(a);
  dfs(av,Mask{},R[target],d[target]);
  if(out.is_open())out.close();
  std::cout<<target<<' '<<count<<' '<<nodes<<' '<<(stopped?"STOPPED":"EXHAUSTED")<<' '<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count()<<std::endl;
 }
}
