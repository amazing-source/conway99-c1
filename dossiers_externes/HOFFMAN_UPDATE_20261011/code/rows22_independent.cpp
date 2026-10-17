// Independent row enumeration: binary include/exclude branching and saturation.
// This does not call rows22.cpp and does not use its multi-candidate branching.
#include <bitset>
#include <vector>
#include <fstream>
#include <iostream>
#include <array>
#include <chrono>
#include <string>
using Bits=std::bitset<128>;
int b=0,c=0;std::vector<std::vector<int>> points;std::vector<Bits> at,ban;
std::ofstream output;long long nodes=0,leaves=0;bool stopped=false;double limit;
std::chrono::steady_clock::time_point began;
void visit(Bits avail,Bits sel,std::vector<int> quota,int need){
 if(stopped)return;++nodes;
 if((nodes&65535)==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()>limit){stopped=true;return;}
 bool again=true;
 while(again){
  again=false;
  if(need<0||int(avail.count())<need)return;
  for(int p=0;p<c;p++){
   if(quota[p]<0)return;
   if(quota[p]==0){auto old=avail;avail&=~at[p];if(avail!=old)again=true;}
  }
  for(int p=0;p<c;p++)if(quota[p]>0){
   Bits candidates=avail&at[p];int n=candidates.count();
   if(n<quota[p])return;
   if(n==quota[p]){
    // Every candidate at this point must be included.
    for(int a=0;a<b;a++)if(candidates[a]){
     if(!avail[a])return; // incompatibility with a forced predecessor
     sel.set(a);avail&=~ban[a];--need;
     for(int q:points[a])--quota[q];
    }
    again=true;break;
   }
  }
 }
 if(need==0){for(int q:quota)if(q)return;++leaves;
  for(int a=0;a<b;a++)if(sel[a])output<<a<<' ';output<<'\n';return;}
 int pickp=-1,small=100000;
 for(int p=0;p<c;p++)if(quota[p]>0){int size=(avail&at[p]).count();if(size<small){pickp=p;small=size;}}
 if(pickp<0)return;
 int pick=-1,best=-1;
 for(int a=0;a<b;a++)if(avail[a]&&at[pickp][a]){int score=(avail&ban[a]).count();if(score>best){best=score;pick=a;}}
 if(pick<0)return;
 // Complementary disjoint binary branches, no symmetry assumption.
 Bits left=avail;left.reset(pick);
 visit(left,sel,quota,need);
 sel.set(pick);for(int p:points[pick])--quota[p];
 visit(left&~ban[pick],sel,quota,need-1);
}
int main(int argc,char**argv){
 if(argc!=5){std::cerr<<"rows22_independent INSTANCE OUTPUT row seconds\n";return 2;}
 std::ifstream in(argv[1]);in>>c>>b;if(!in||c>128||b>128)return 3;
 points.resize(b);at.resize(c);ban.resize(b);
 for(int p=0;p<c;p++)for(int a=0;a<b;a++){int x;in>>x;if(x){points[a].push_back(p);at[p].set(a);}}
 std::vector<int>need(b);std::vector<std::vector<int>>qs(b,std::vector<int>(c));
 for(int a=0;a<b;a++){in>>need[a];for(int p=0;p<c;p++)in>>qs[a][p];}
 if(!in)return 3;
 for(int a=0;a<b;a++)for(int d=0;d<b;d++){
  int intersection=0;for(int p:points[a])if(at[p][d])intersection++;
  if(a==d||intersection>=2)ban[a].set(d);
 }
 int target=std::stoi(argv[3]);limit=std::stod(argv[4]);
 output.open(argv[2]);if(!output)return 3;
 Bits av;for(int a=0;a<b;a++)if(!ban[target][a])av.set(a);
 began=std::chrono::steady_clock::now();visit(av,Bits{},qs[target],need[target]);output.close();
 std::cout<<target<<' '<<leaves<<' '<<nodes<<' '<<(stopped?"STOPPED":"EXHAUSTED")<<' '<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<'\n';
 return stopped?4:0;
}
