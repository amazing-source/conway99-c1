// Local norm16 D--Z catalogue. Optional fixed endpoints for one D edge.
// Input made by
// norm16_dz_catalogue.py --write-instance. Quotient by Aut(Z) only.
#include <algorithm>
#include <array>
#include <bit>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
using Domain = bitset<512>;

struct Search {
    array<unsigned,11> zr{};
    array<unsigned,8> core{};
    array<array<int,8>,8> dc{};
    array<int,11> initial_columns{};
    array<int,55> initial_pairs{};
    vector<unsigned> masks;
    vector<vector<int>> rowpairs;
    vector<vector<int>> rowvertices;
    int edge_d=-1,edge_e=-1;
    unsigned endpoint_r=0,endpoint_t=0;
    array<Domain,11> containing_col{};
    array<Domain,55> containing_pair{};
    array<vector<Domain>,3> compatible;
    vector<vector<int>> images;
    Domain all;
    uint64_t nodes=0, count=0;
    bool stopped=false;
    double seconds=30;
    ofstream solutions;
    array<unsigned,8> chosen{};
    array<int,8> chosen_index{};
    bool spectral=false;
    array<array<long long,8>,8> sh{};
    array<array<long long,11>,11> sw{};
    vector<vector<long long>> cost;
    array<array<vector<Domain>,8>,8> spectral_pair;
    array<Domain,8> spectral_domain;
    uint64_t killed3=0,killed4=0;
    chrono::steady_clock::time_point started;

    void read(const string& path) {
        ifstream in(path);
        for(auto &r:zr) in>>r;
        for(auto &r:core) in>>r;
        int nauto; in>>nauto;
        vector<array<int,11>> autos(nauto);
        for(auto &p:autos) for(auto &z:p) in>>z;
        if(!in) throw runtime_error("Bad input");
        if(in>>edge_d) {
            if(!(in>>edge_e>>endpoint_r>>endpoint_t)) throw runtime_error("Bad endpoint input");
            if(edge_d<0||edge_d>7||edge_e<0||edge_e>7||edge_d==edge_e
               ||popcount(endpoint_r)!=5||popcount(endpoint_t)!=5)
                throw runtime_error("Invalid fixed endpoints");
        }
        array<pair<int,int>,55> pairs;
        int k=0;
        for(int i=0;i<11;++i) for(int j=i+1;j<11;++j) {
            pairs[k]={i,j};
            initial_pairs[k++]=2-int((zr[i]>>j)&1)-popcount(zr[i]&zr[j]);
        }
        for(int i=0;i<11;++i) initial_columns[i]=2+popcount(zr[i]);
        for(int i=0;i<8;++i) for(int j=0;j<8;++j) dc[i][j]=2-popcount(core[i]&core[j]);
        array<int,2048> maskindex; maskindex.fill(-1);
        for(unsigned m=0;m<2048;++m) if(popcount(m)==4||(edge_d>=0&&(m==endpoint_r||m==endpoint_t))) {
            bool fixed=(edge_d>=0&&(m==endpoint_r||m==endpoint_t));
            bool ok=true;
            int degree_sum=0;
            for(int z=0;z<11;++z) if((m>>z)&1) degree_sum+=popcount(zr[z]);
            if(degree_sum>6&&!fixed) continue; // Note253, local common-neighbour budget.
            for(int z=0;z<11;++z) if(popcount(m&zr[z])>2-int((m>>z)&1)) ok=false;
            if(!ok&&!fixed) continue;
            int id=masks.size(); masks.push_back(m); maskindex[m]=id;
            if(!fixed) all.set(id);
            vector<int> vs;
            for(int z=0;z<11;++z) if((m>>z)&1) {vs.push_back(z); containing_col[z].set(id);}
            rowvertices.push_back(vs);
            vector<int> ps;
            for(int p=0;p<55;++p) {
                auto [i,j]=pairs[p];
                if(((m>>i)&1)&&((m>>j)&1)) {ps.push_back(p); containing_pair[p].set(id);}
            }
            rowpairs.push_back(ps);
        }
        if(masks.size()>512) throw runtime_error("Row domain exceeds bitset capacity");
        for(int c=0;c<3;++c) {
            compatible[c].resize(masks.size());
            for(size_t i=0;i<masks.size();++i) for(size_t j=0;j<masks.size();++j)
                if(popcount(masks[i]&masks[j])<=c) compatible[c][i].set(j);
        }
        images.resize(nauto,vector<int>(masks.size()));
        for(int t=0;t<nauto;++t) for(size_t i=0;i<masks.size();++i) {
            unsigned m=0;
            for(int z:rowvertices[i]) m|=1u<<autos[t][z];
            images[t][i]=maskindex[m];
            if(images[t][i]<0) throw runtime_error("Symmetry does not preserve row set");
        }
        if(edge_d>=0) {
            chosen_index[edge_d]=maskindex[endpoint_r]; chosen[edge_d]=endpoint_r;
            chosen_index[edge_e]=maskindex[endpoint_t]; chosen[edge_e]=endpoint_t;
        }
    }

    void read_spectral(const string& path) {
        ifstream in(path);
        long long scale; in>>scale;
        for(auto &r:sh) for(auto &x:r) in>>x;
        for(auto &r:sw) for(auto &x:r) in>>x;
        if(!in) throw runtime_error("Bad spectral input");
        // K has entries3 or-4. Each cost has121 products, so this
        // bound keeps all preprocessing sums safely inside signed64.
        for(auto &r:sh) for(auto x:r)
            if(x < -1000000000000LL || x > 1000000000000LL)
                throw runtime_error("H input exceeds exact64 preprocessing bound");
        for(auto &r:sw) for(auto x:r)
            if(x < -1000000000000LL || x > 1000000000000LL)
                throw runtime_error("Q inverse input exceeds exact64 preprocessing bound");
        spectral=true;
        vector<array<long long,11>> kw(masks.size()), k(masks.size());
        for(size_t i=0;i<masks.size();++i) {
            for(int z=0;z<11;++z) k[i][z]=3-7*int((masks[i]>>z)&1);
            for(int z=0;z<11;++z) for(int w=0;w<11;++w) kw[i][z]+=k[i][w]*sw[w][z];
        }
        cost.assign(masks.size(),vector<long long>(masks.size()));
        for(size_t i=0;i<masks.size();++i) for(size_t j=0;j<masks.size();++j)
            for(int z=0;z<11;++z) cost[i][j]+=kw[i][z]*k[j][z];
        for(int d=0;d<8;++d) for(size_t i=0;i<masks.size();++i)
            if(sh[d][d]-cost[i][i]>=0) spectral_domain[d].set(i);
        for(int d=0;d<8;++d) for(int e=0;e<8;++e) {
            spectral_pair[d][e].resize(masks.size());
            for(size_t i=0;i<masks.size();++i) for(size_t j=0;j<masks.size();++j) {
                long long x=sh[d][d]-cost[i][i],y=sh[e][e]-cost[j][j],z=sh[d][e]-cost[i][j];
                // Four-by-four determinant expansion uses at most24 products
                // of four entries, each <1e9: it fits signed128 exactly.
                if(abs(x)>=1000000000LL||abs(y)>=1000000000LL||abs(z)>=1000000000LL)
                    throw runtime_error("Spectral scale exceeds exact128 bound");
                if(x>=0&&y>=0&&(__int128)x*y-(__int128)z*z>=0)
                    spectral_pair[d][e][i].set(j);
            }
        }
    }

    static __int128 det3(const array<array<long long,3>,3>& a) {
        return (__int128)a[0][0]*( (__int128)a[1][1]*a[2][2]-(__int128)a[1][2]*a[2][1])
              -(__int128)a[0][1]*( (__int128)a[1][0]*a[2][2]-(__int128)a[1][2]*a[2][0])
              +(__int128)a[0][2]*( (__int128)a[1][0]*a[2][1]-(__int128)a[1][1]*a[2][0]);
    }
    long long entry(int d,int e) {return sh[d][e]-cost[chosen_index[d]][chosen_index[e]];}
    bool partial_spectral(int d,unsigned placed) {
        for(int i=0;i<8;++i) if((placed>>i)&1)
            for(int j=i+1;j<8;++j) if((placed>>j)&1) {
                array<int,3> labels{d,i,j}; array<array<long long,3>,3> m;
                for(int u=0;u<3;++u) for(int v=0;v<3;++v) m[u][v]=entry(labels[u],labels[v]);
                if(det3(m)<0) {++killed3;return false;}
            }
        for(int i=0;i<8;++i) if((placed>>i)&1)
            for(int j=i+1;j<8;++j) if((placed>>j)&1)
                for(int k=j+1;k<8;++k) if((placed>>k)&1) {
                    array<int,4> labels{d,i,j,k}; __int128 det=0;
                    for(int omit=0;omit<4;++omit) {
                        array<array<long long,3>,3> m;
                        for(int u=0;u<3;++u) {
                            int col=0;
                            for(int v=0;v<4;++v) if(v!=omit) m[u][col++]=entry(labels[u+1],labels[v]);
                        }
                        det+=(omit%2?-1:1)*(__int128)entry(d,labels[omit])*det3(m);
                    }
                    if(det<0) {++killed4;return false;}
                }
        return true;
    }

    void visit(const array<Domain,8>& domains, unsigned remaining,
               const array<int,11>& columns, const array<int,55>& pairs,
               const vector<int>& group) {
        ++nodes;
        if((nodes&8191)==0 && elapsed()>seconds) {stopped=true; return;}
        if(!remaining) {
            ++count;
            if(solutions.is_open()) {
                for(int i=0;i<8;++i) solutions<<(i ? " " : "")<<chosen[i];
                solutions<<'\n';
            }
            return;
        }
        int d=-1, best=1000;
        for(int i=0;i<8;++i) if((remaining>>i)&1) {
            int size=domains[i].count();
            if(size<best) {d=i; best=size;}
        }
        if(!best) return;
        unsigned next=remaining&~(1u<<d);
        int nleft=popcount(next);
        for(size_t j=0;j<masks.size()&&!stopped;++j) if(domains[d][j]) {
            chosen_index[d]=j;
            if(spectral&&!partial_spectral(d,255&~remaining)) continue;
            vector<int> stabilizer;
            bool canonical=true;
            for(int g:group) {
                int target=images[g][j];
                if(masks[target]<masks[j]) {canonical=false; break;}
                if(target==int(j)) stabilizer.push_back(g);
            }
            if(!canonical) continue;
            auto nc=columns;
            for(int z:rowvertices[j]) --nc[z];
            bool good=true;
            for(int c:nc) if(c<0||c>nleft) good=false;
            if(!good) continue;
            auto np=pairs;
            Domain forbidden;
            for(int p:rowpairs[j]) {
                if(--np[p]<0) throw runtime_error("Negative pair capacity");
                if(!np[p]) forbidden|=containing_pair[p];
            }
            Domain required=all;
            for(int z=0;z<11;++z) {
                if(nc[z]==0) forbidden|=containing_col[z];
                else if(nc[z]==nleft) required&=containing_col[z];
            }
            auto nd=domains;
            for(int i=0;i<8;++i) if((next>>i)&1) {
                nd[i]&=compatible[dc[d][i]][j]&~forbidden&required;
                if(spectral) nd[i]&=spectral_pair[d][i][j];
                if(nd[i].none()) good=false;
            }
            if(!good) continue;
            for(int z=0;z<11&&good;++z) {
                int lower=0,upper=0;
                for(int i=0;i<8;++i) if((next>>i)&1) {
                    upper+=(nd[i]&containing_col[z]).any();
                    lower+=(nd[i]&~containing_col[z]).none();
                }
                if(nc[z]<lower||nc[z]>upper) good=false;
            }
            if(good) {
                chosen[d]=masks[j];
                visit(nd,next,nc,np,stabilizer);
            }
        }
    }
    double elapsed() {return chrono::duration<double>(chrono::steady_clock::now()-started).count();}
    void run() {
        Domain initial=all;
        for(int p=0;p<55;++p) if(!initial_pairs[p]) initial&=~containing_pair[p];
        array<Domain,8> domains; domains.fill(initial);
        if(spectral) for(int i=0;i<8;++i) domains[i]&=spectral_domain[i];
        vector<int> group(images.size()); iota(group.begin(),group.end(),0);
        unsigned remaining=255;
        bool good=true;
        if(edge_d>=0) {
            remaining&=~((1u<<edge_d)|(1u<<edge_e));
            for(int d:{edge_d,edge_e}) {
                int j=chosen_index[d];
                for(int z:rowvertices[j]) --initial_columns[z];
                for(int p:rowpairs[j]) --initial_pairs[p];
                if(spectral&&!spectral_domain[d][j]) good=false;
                for(int i=0;i<8;++i) if((remaining>>i)&1) {
                    for(size_t m=0;m<masks.size();++m)
                        if(popcount(masks[m]&masks[j])!=dc[d][i]) domains[i].reset(m);
                    if(spectral) domains[i]&=spectral_pair[d][i][j];
                }
            }
            if(spectral&&!spectral_pair[edge_d][edge_e][chosen_index[edge_d]][chosen_index[edge_e]]) good=false;
            Domain forbidden,required=all;
            for(int p=0;p<55;++p) {
                if(initial_pairs[p]<0) good=false;
                if(initial_pairs[p]==0) forbidden|=containing_pair[p];
            }
            for(int z=0;z<11;++z) {
                if(initial_columns[z]<0||initial_columns[z]>6) good=false;
                if(initial_columns[z]==0) forbidden|=containing_col[z];
                if(initial_columns[z]==6) required&=containing_col[z];
            }
            for(int i=0;i<8;++i) if((remaining>>i)&1) domains[i]&=required&~forbidden;
        }
        started=chrono::steady_clock::now();
        if(good) visit(domains,remaining,initial_columns,initial_pairs,group);
        cout<<"{\"status\":\""<<(stopped?"STOPPED":"EXHAUSTED")
            <<"\",\"count_mod_Aut_Z\":"<<count<<",\"nodes\":"<<nodes
            <<",\"seconds\":"<<elapsed()<<",\"Aut_Z\":"<<images.size()
            <<",\"spectral_minors_up_to\":"<<(spectral?4:0)
            <<",\"killed3\":"<<killed3<<",\"killed4\":"<<killed4<<"}\n";
    }
};
int main(int argc,char**argv) {
    try {
    if(argc<2) return 2;
    Search search;
    search.read(argv[1]);
    if(argc>2) search.seconds=stod(argv[2]);
    if(argc>3&&string(argv[3])!="-") search.solutions.open(argv[3]);
    if(argc>4) search.read_spectral(argv[4]);
    search.run();
    } catch(const exception& e) {
        cerr<<e.what()<<'\n';
        return 1;
    }
}
