// Search for an exact three-per-line selection, retaining three per vertical.
// A zero residual is only a 3-ovoid candidate, not yet a verified SRG.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>
using namespace std;

int main(int argc,char**argv){
    if(argc!=5){cerr<<"geometry.txt output.json seconds seed\n";return 2;}
    ifstream in(argv[1]); int nl,np; in>>nl>>np;
    if(nl!=891||np!=729)return 2;
    vector<array<int,9>> lines(nl); vector<vector<int>> on(np);
    for(int i=0;i<nl;i++){
        for(int&v:lines[i])in>>v;
        bool vertical=true;
        for(int v:lines[i])vertical&=(v%81==lines[i][0]%81);
        if(!vertical)for(int v:lines[i])on[v].push_back(i);
    }
    for(auto& ls:on)if(ls.size()!=10)return 3;
    mt19937 rng(stoul(argv[4])); uniform_real_distribution<double> unif(0,1);
    vector<int>x(np),bestx(np),count(nl); int best=1000000,energy=0;
    long long steps=0; int restarts=0;
    auto start=chrono::steady_clock::now(); double seconds=stod(argv[3]);
    auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};
    auto save=[&](){
        ofstream out(argv[2]);out<<"{\"status\":\""<<(best==0?"exact_3_ovoid_candidate":"incomplete_selection")
        <<"\",\"line_squared_residual\":"<<best<<",\"steps\":"<<steps<<",\"seconds\":"<<elapsed()
        <<",\"seed\":"<<argv[4]<<",\"selection\":[";
        bool first=true;for(int i=0;i<np;i++)if(bestx[i]){if(!first)out<<",";first=false;out<<i;}out<<"]}\n";
    };
    while(elapsed()<seconds && best!=0){
        if(restarts%4==0){
            fill(x.begin(),x.end(),0);
            for(int b=0;b<81;b++){
                array<int,9> a{0,1,2,3,4,5,6,7,8};shuffle(a.begin(),a.end(),rng);
                for(int j=0;j<3;j++)x[a[j]*81+b]=1;
            }
        }else x=bestx;
        fill(count.begin(),count.end(),0);
        for(int v=0;v<np;v++)if(x[v])for(int l:on[v])count[l]++;
        energy=0;for(int l=0;l<nl;l++){
            bool vertical=lines[l][0]%81==lines[l][1]%81;
            if(!vertical)energy+=(count[l]-3)*(count[l]-3);
        }
        const int cycle=500000;
        for(int step=0;step<cycle;step++){
            if(step%8192==0 && elapsed()>=seconds)break;
            int b=rng()%81,u,v;
            do{u=(rng()%9)*81+b;}while(!x[u]);
            do{v=(rng()%9)*81+b;}while(x[v]);
            int delta=0;for(int l:on[u])delta+=-2*(count[l]-3)+1;
            for(int l:on[v])delta+=2*(count[l]-3)+1;
            double temp=2.5*pow(0.04,double(step)/cycle);
            if(delta<=0||unif(rng)<exp(-delta/temp)){
                x[u]=0;x[v]=1;for(int l:on[u])count[l]--;for(int l:on[v])count[l]++;energy+=delta;
                if(energy<best){
                    best=energy;bestx=x;save();
                    if(best<120||best%50==0)cout<<"BEST "<<best<<" seconds "<<elapsed()<<endl;
                    if(best==0)break;
                }
            }
            steps++;
        }
        restarts++;
    }
    save();cout<<"FINAL residual "<<best<<" steps "<<steps<<" seconds "<<elapsed()<<endl;
}
