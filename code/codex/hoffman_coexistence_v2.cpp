// Exact search for a central outside neighbourhood and its ten labelled
// transported rows, coupled to a common pool of erased-point incidences.
// An exhausted negative result excludes a retained Hoffman incidence template.
// A positive result is ONLY a necessary star relaxation, never an SRG.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <deque>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using U=uint64_t;
using Mask=unsigned __int128;
using Bits=std::vector<U>;
using Domains=std::array<Bits,10>;
constexpr int V=77;
int pop(Mask x){return std::popcount(U(x))+std::popcount(U(x>>64));}
int first(Mask x){return U(x)?std::countr_zero(U(x)):64+std::countr_zero(U(x>>64));}
std::vector<int> elements(Mask m){std::vector<int> r;while(m){int j=first(m);r.push_back(j);m&=m-1;}return r;}
bool any(const Bits& a){for(U w:a)if(w)return true;return false;}
int count(const Bits& a){int n=0;for(U w:a)n+=std::popcount(w);return n;}
Bits full(int n){Bits a((n+63)/64,~U(0));if(n%64)a.back()=(U(1)<<(n%64))-1;return a;}
bool intersects(const Bits&a,const Bits&b){for(size_t w=0;w<a.size();++w)if(a[w]&b[w])return true;return false;}
bool subset(const Bits&a,const Bits&b){for(size_t w=0;w<a.size();++w)if(a[w]&~b[w])return false;return true;}
bool at_least(const Bits&a,const Bits&b,int needed){for(size_t w=0;w<a.size();++w){needed-=std::popcount(a[w]&b[w]);if(needed<=0)return true;}return false;}
void intersect(Bits&a,const Bits&b){for(size_t w=0;w<a.size();++w)a[w]&=b[w];}
std::vector<int> indices(const Bits&a){std::vector<int> out;for(size_t w=0;w<a.size();++w){U m=a[w];while(m){int b=std::countr_zero(m);out.push_back(64*w+b);m&=m-1;}}return out;}

struct Search {
 int root=0,erased=0,n=0,np=0;
 std::array<int,V> quota{},missing{};
 int known[V][V]{};
 std::vector<Mask> rows,points;
 std::vector<Bits> support;
 std::array<Bits,V> point_columns;
 std::vector<uint8_t> row_intersection;
 long long nodes=0,trials=0,arc_prunes=0,quota_prunes=0,point_prunes=0;
 int tested=0;
 bool limited=false,found=false,use_support=true;
 double seconds=300;
 long long max_nodes=50000000;
 std::chrono::steady_clock::time_point start=std::chrono::steady_clock::now();
 std::array<int,10> centres{},patterns{},words{};
 std::array<std::vector<int>,10> domain;
 std::array<std::array<Bits,10>,10> compatible;
 std::array<std::array<Bits,V>,10> columns;
 int witness_central=-1;
 std::array<int,10> witness_centres{},witness_rows{};
 Bits witness_pool;
 double elapsed()const{return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();}
 void read(const std::string&path){
  std::ifstream in(path);int width;
  in>>width>>root>>erased>>n>>np;
  if(width!=V||!in)throw std::runtime_error("invalid header");
  for(int&x:quota)in>>x;for(int&x:missing)in>>x;
  for(auto&r:known)for(int&x:r)in>>x;
  auto load=[&](int size,int weight,std::vector<Mask>&out){
   for(int a=0;a<size;++a){Mask m=0;for(int t=0;t<weight;++t){int j;in>>j;if(j<0||j>=V)throw std::runtime_error("column");m|=Mask(1)<<j;}
    if(pop(m)!=weight||!in)throw std::runtime_error("row");out.push_back(m);}
  };
  load(n,10,rows);load(np,14,points);
  if(erased&&np==0)throw std::runtime_error("empty point domain must be handled before native search");
 }
 void prepare(){
  row_intersection.resize(size_t(n)*n);
  for(int a=0;a<n;++a)for(int b=0;b<=a;++b)
   row_intersection[size_t(a)*n+b]=row_intersection[size_t(b)*n+a]=pop(rows[a]&rows[b]);
  if(!use_support||!erased)return;
  int wp=(np+63)/64;
  support.assign(n,Bits(wp));
  for(int j=0;j<V;++j){point_columns[j]=Bits(wp);for(int a=0;a<np;++a)if(points[a]>>j&1)point_columns[j][a/64]|=U(1)<<(a%64);}
  for(int r=0;r<n;++r)for(int p=0;p<np;++p){
   Mask m=rows[r]&points[p];if(pop(m)!=2)continue;
   int j=first(m);m&=m-1;int k=first(m);
   if(known[j][k]==0)support[r][p/64]|=U(1)<<(p%64);
  }
 }
 bool point_possible(const Bits&pool){
  if(!use_support||!erased)return true;
  if(count(pool)<erased){++point_prunes;return false;}
  for(int j=0;j<V;++j)if(missing[j]&&!at_least(pool,point_columns[j],missing[j])){++point_prunes;return false;}
  return true;
 }
 void make_constraints(){
  for(int x=0;x<10;++x){
   words[x]=(domain[x].size()+63)/64;
   for(int j=0;j<V;++j){columns[x][j]=Bits(words[x]);for(size_t a=0;a<domain[x].size();++a)
    if(rows[domain[x][a]]>>j&1)columns[x][j][a/64]|=U(1)<<(a%64);}
  }
  for(int x=0;x<10;++x)for(int y=x+1;y<10;++y){
   int j=centres[x],k=centres[y];int hi,lo;
   if(patterns[x]==patterns[y])lo=hi=2;
   else{hi=1-known[j][k];lo=std::max(0,hi-std::min(missing[j],missing[k]));}
   compatible[x][y]=Bits(domain[x].size()*words[y]);
   compatible[y][x]=Bits(domain[y].size()*words[x]);
   for(size_t a=0;a<domain[x].size();++a)for(size_t b=0;b<domain[y].size();++b){
    int r=domain[x][a],s=domain[y][b],v=row_intersection[size_t(r)*n+s];
    if(r!=s&&lo<=v&&v<=hi){compatible[x][y][a*words[y]+b/64]|=U(1)<<(b%64);
     compatible[y][x][b*words[x]+a/64]|=U(1)<<(a%64);}
   }
  }
 }
 bool propagate(Domains&ds,Bits&pool){
  bool again=true;
  while(again){
   Domains before=ds;
   std::deque<std::pair<int,int>> queue;
   for(int x=0;x<10;++x)for(int y=0;y<10;++y)if(x!=y)queue.emplace_back(x,y);
   while(!queue.empty()){
    auto[x,y]=queue.front();queue.pop_front();bool changed=false;
    for(int a:indices(ds[x])){
     bool ok=false;size_t offset=size_t(a)*words[y];
     for(int w=0;w<words[y];++w)if(compatible[x][y][offset+w]&ds[y][w]){ok=true;break;}
     if(!ok){ds[x][a/64]&=~(U(1)<<(a%64));changed=true;}
    }
    if(!any(ds[x])){++arc_prunes;return false;}
    if(changed)for(int z=0;z<10;++z)if(z!=x&&z!=y)queue.emplace_back(z,x);
   }
   for(int j=0;j<V;++j){
    int can=0,must=0;std::array<bool,10>may{},certain{};
    for(int x=0;x<10;++x){may[x]=intersects(ds[x],columns[x][j]);certain[x]=subset(ds[x],columns[x][j]);can+=may[x];must+=certain[x];}
    if(must>quota[j]||can<quota[j]){++quota_prunes;return false;}
    if(must==quota[j]){for(int x=0;x<10;++x)if(may[x]&&!certain[x])for(int w=0;w<words[x];++w)ds[x][w]&=~columns[x][j][w];}
    else if(can==quota[j])for(int x=0;x<10;++x)if(may[x])intersect(ds[x],columns[x][j]);
   }
   if(use_support&&erased){
    // Only forced rows shrink the point pool here. This is weaker than the
    // Python union-of-domain filter and therefore cannot introduce exclusions.
    for(int x=0;x<10;++x)if(count(ds[x])==1)intersect(pool,support[domain[x][indices(ds[x])[0]]]);
    if(!point_possible(pool))return false;
   }
   again=ds!=before;
  }
  return true;
 }
 bool dfs(Domains ds,Bits pool){
  ++nodes;
  if(nodes>max_nodes||(nodes%1024==0&&elapsed()>seconds)){limited=true;return false;}
  if(!propagate(ds,pool))return false;
  int best=-1,small=1000000000;
  for(int x=0;x<10;++x){int s=count(ds[x]);if(s>1&&s<small){best=x;small=s;}}
  if(best<0){
   witness_centres=centres;for(int x=0;x<10;++x)witness_rows[x]=domain[x][indices(ds[x])[0]];
   witness_pool=pool;return true;
  }
  for(int a:indices(ds[best])){
   Domains child=ds;std::fill(child[best].begin(),child[best].end(),0);child[best][a/64]=U(1)<<(a%64);
   if(dfs(std::move(child),pool))return true;
   if(limited)return false;
  }
  return false;
 }
 void solve(){
  Mask one=0;for(int j=0;j<V;++j)if(quota[j]==1)one|=Mask(1)<<j;
  for(int central=0;central<n&&!found&&!limited;++central){
   if(elapsed()>seconds){limited=true;break;}
   ++tested;Mask R=rows[central];auto singles=elements(R&one),zeros=elements(R&~one);
   if(singles.size()!=4||zeros.size()!=6)throw std::runtime_error("central type counts");
   Bits pool=(use_support&&erased)?support[central]:Bits();
   if(!point_possible(pool))continue;
   std::vector<std::vector<int>> bins(V*V);
   for(int a=0;a<n;++a){Mask p=R&rows[a];int sz=pop(p);
    if(sz==1&&(p&one)){int j=first(p);bins[j*V+j].push_back(a);}
    if(sz==2&&!(p&one)){int j=first(p);p&=p-1;int k=first(p);bins[j*V+k].push_back(a);}
   }
   bool viable=true;for(int j:singles)if(bins[j*V+j].empty())viable=false;
   if(!viable)continue;
   bool allowed[V][V]{};
   for(int j:zeros)for(int k:zeros)if(j<k&&!known[j][k]){
    auto&v=bins[j*V+k];for(size_t a=0;a<v.size()&&!allowed[j][k];++a)for(size_t b=0;b<a;++b)
     if(row_intersection[size_t(v[a])*n+v[b]]==2){allowed[j][k]=true;break;}
   }
   std::vector<std::pair<int,int>> matching;
   auto match=[&](auto&&self,std::vector<int>left)->void{
    if(found||limited)return;
    if(left.empty()){
     int x=0;for(int j:singles){centres[x]=j;patterns[x]=j*V+j;domain[x]=bins[patterns[x]];++x;}
     for(auto[j,k]:matching)for(int v:{j,k}){centres[x]=v;patterns[x]=j*V+k;domain[x]=bins[patterns[x]];++x;}
     ++trials;make_constraints();Domains ds;for(int a=0;a<10;++a)ds[a]=full(domain[a].size());
     if(dfs(ds,pool)){found=true;witness_central=central;}return;
    }
    int j=left[0];for(size_t b=1;b<left.size();++b){int k=left[b];if(!allowed[j][k])continue;
     std::vector<int> rest;for(size_t a=1;a<left.size();++a)if(a!=b)rest.push_back(left[a]);
     matching.emplace_back(j,k);self(self,rest);matching.pop_back();if(found||limited)return;
    }
   };
   match(match,zeros);
   if(tested%100==0)std::cout<<"PROGRESS centres "<<tested<<" matchings "<<trials<<" nodes "<<nodes<<" arc_prunes "<<arc_prunes<<" point_prunes "<<point_prunes<<" seconds "<<elapsed()<<std::endl;
  }
 }
 void save(const std::string&path){
  std::ofstream out(path);std::string status=found?"FEASIBLE_LABELLED_STAR_NOT_SRG":limited?"UNKNOWN":"UNSAT_ALL_BOUNDARY_EXTENSIONS";
  out<<"{\n\"status\":\""<<status<<"\",\n\"centres_tested\":"<<tested<<",\n\"matchings_tested\":"<<trials<<",\n\"nodes\":"<<nodes
     <<",\n\"arc_prunes\":"<<arc_prunes<<",\n\"quota_prunes\":"<<quota_prunes<<",\n\"point_prunes\":"<<point_prunes<<",\n\"seconds\":"<<elapsed()
     <<",\n\"point_support_enabled\":"<<(use_support?"true":"false");
  if(found){out<<",\n\"central_index\":"<<witness_central<<",\n\"assigned_centres\":[";for(int x=0;x<10;++x)out<<(x?",":"")<<witness_centres[x];
   out<<"],\n\"transported_indices\":[";for(int x=0;x<10;++x)out<<(x?",":"")<<witness_rows[x];out<<"],\n\"point_pool\":[";
   auto p=indices(witness_pool);for(size_t a=0;a<p.size();++a)out<<(a?",":"")<<p[a];out<<"]";}
  out<<"\n}\n";
  std::cout<<"RESULT "<<status<<" centres "<<tested<<" matchings "<<trials<<" nodes "<<nodes<<" seconds "<<elapsed()<<std::endl;
 }
};
int main(int argc,char**argv){
 try{if(argc<3)throw std::runtime_error("usage: input output [seconds] [nodes] [support:0|1]");
  Search s;if(argc>3)s.seconds=std::stod(argv[3]);if(argc>4)s.max_nodes=std::stoll(argv[4]);if(argc>5)s.use_support=std::stoi(argv[5]);
  s.read(argv[1]);s.prepare();std::cout<<"PREPARED "<<s.n<<" covers "<<s.np<<" point_rows seconds "<<s.elapsed()<<std::endl;s.solve();s.save(argv[2]);
 }catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 1;}
}
