// Local norm16 D--Z catalogue, with D independent. Input made by
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
    vector<array<int,6>> rowpairs;
    vector<array<int,4>> rowvertices;
    array<Domain,11> containing_col{};
    array<Domain,55> containing_pair{};
    array<vector<Domain>,3> compatible;
    vector<vector<int>> images;
    Domain all;
    uint64_t nodes=0, count=0;
    bool stopped=false;
    double seconds=30;
    chrono::steady_clock::time_point started;

    void read(const string& path) {
        ifstream in(path);
        for(auto &r:zr) in>>r;
        for(auto &r:core) in>>r;
        int nauto; in>>nauto;
        vector<array<int,11>> autos(nauto);
        for(auto &p:autos) for(auto &z:p) in>>z;
        if(!in) throw runtime_error("Bad input");
        array<pair<int,int>,55> pairs;
        int k=0;
        for(int i=0;i<11;++i) for(int j=i+1;j<11;++j) {
            pairs[k]={i,j};
            initial_pairs[k++]=2-int((zr[i]>>j)&1)-popcount(zr[i]&zr[j]);
        }
        for(int i=0;i<11;++i) initial_columns[i]=2+popcount(zr[i]);
        for(int i=0;i<8;++i) for(int j=0;j<8;++j) dc[i][j]=2-popcount(core[i]&core[j]);
        array<int,2048> maskindex; maskindex.fill(-1);
        for(unsigned m=0;m<2048;++m) if(popcount(m)==4) {
            bool ok=true;
            int degree_sum=0;
            for(int z=0;z<11;++z) if((m>>z)&1) degree_sum+=popcount(zr[z]);
            if(degree_sum>6) continue; // Note253, local common-neighbour budget.
            for(int z=0;z<11;++z) if(popcount(m&zr[z])>2-int((m>>z)&1)) ok=false;
            if(!ok) continue;
            int id=masks.size(); masks.push_back(m); maskindex[m]=id; all.set(id);
            array<int,4> vs; k=0;
            for(int z=0;z<11;++z) if((m>>z)&1) {vs[k++]=z; containing_col[z].set(id);}
            rowvertices.push_back(vs);
            array<int,6> ps; k=0;
            for(int p=0;p<55;++p) {
                auto [i,j]=pairs[p];
                if(((m>>i)&1)&&((m>>j)&1)) {ps[k++]=p; containing_pair[p].set(id);}
            }
            rowpairs.push_back(ps);
        }
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
        }
    }

    void visit(const array<Domain,8>& domains, unsigned remaining,
               const array<int,11>& columns, const array<int,55>& pairs,
               const vector<int>& group) {
        ++nodes;
        if((nodes&8191)==0 && elapsed()>seconds) {stopped=true; return;}
        if(!remaining) {++count; return;}
        int d=-1, best=1000;
        for(int i=0;i<8;++i) if((remaining>>i)&1) {
            int size=domains[i].count();
            if(size<best) {d=i; best=size;}
        }
        if(!best) return;
        unsigned next=remaining&~(1u<<d);
        int nleft=popcount(next);
        for(size_t j=0;j<masks.size()&&!stopped;++j) if(domains[d][j]) {
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
            if(good) visit(nd,next,nc,np,stabilizer);
        }
    }
    double elapsed() {return chrono::duration<double>(chrono::steady_clock::now()-started).count();}
    void run() {
        Domain initial=all;
        for(int p=0;p<55;++p) if(!initial_pairs[p]) initial&=~containing_pair[p];
        array<Domain,8> domains; domains.fill(initial);
        vector<int> group(images.size()); iota(group.begin(),group.end(),0);
        started=chrono::steady_clock::now();
        visit(domains,255,initial_columns,initial_pairs,group);
        cout<<"{\"status\":\""<<(stopped?"STOPPED":"EXHAUSTED")
            <<"\",\"count_mod_Aut_Z\":"<<count<<",\"nodes\":"<<nodes
            <<",\"seconds\":"<<elapsed()<<",\"Aut_Z\":"<<images.size()<<"}\n";
    }
};
int main(int argc,char**argv) {
    if(argc<2) return 2;
    Search search;
    search.read(argv[1]);
    if(argc>2) search.seconds=stod(argv[2]);
    search.run();
}
