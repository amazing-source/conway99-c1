// Exhaust all linear maps preserving the 22 BvLS connection vectors in F_3^5.
#include <array>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>
using V=std::array<int,5>;
int code(V v){int s=0;for(int x:v)s=3*s+x;return s;}
int main(int argc,char**argv){
 std::ifstream in(argv[1]);std::vector<V> hs(11);for(auto&v:hs)for(auto&x:v)in>>x;
 std::vector<V> s;bool allowed[243]={};for(auto v:hs)for(int a:{1,2}){for(auto&x:v)x=x*a%3;s.push_back(v);allowed[code(v)]=true;}
 // Source basis: h0..h4 are the reversed standard basis in this dataset.
 for(int j=0;j<5;j++)for(int r=0;r<5;r++)if(hs[j][r]!=(r==4-j))return 3;
 std::ofstream out(argv[2]);int count=0;std::array<int,5> ii;
 for(int a=0;a<22;a++)for(int b=0;b<22;b++)if(a/2!=b/2)
 for(int c=0;c<22;c++)if(c/2!=a/2&&c/2!=b/2)
 for(int d=0;d<22;d++)if(d/2!=a/2&&d/2!=b/2&&d/2!=c/2)
 for(int e=0;e<22;e++)if(e/2!=a/2&&e/2!=b/2&&e/2!=c/2&&e/2!=d/2){
  ii={a,b,c,d,e};bool ok=true;
  for(int j=5;j<11;j++){V v{};for(int r=0;r<5;r++)for(int t=0;t<5;t++)v[r]=(v[r]+hs[j][4-t]*s[ii[t]][r])%3;if(!allowed[code(v)]){ok=false;break;}}
  if(!ok)continue;
  // Check invertibility directly (safety; images of cap could otherwise collapse).
  int m[5][5];for(int r=0;r<5;r++)for(int t=0;t<5;t++)m[r][t]=s[ii[t]][r];int rank=0;
  for(int j=0;j<5;j++){int k=rank;while(k<5&&!m[k][j])k++;if(k==5)continue;for(int t=0;t<5;t++)std::swap(m[k][t],m[rank][t]);int inv=m[rank][j];for(int t=j;t<5;t++)m[rank][t]=m[rank][t]*inv%3;for(int r=rank+1;r<5;r++){int z=m[r][j];for(int t=j;t<5;t++)m[r][t]=(m[r][t]-z*m[rank][t]+6)%3;}rank++;}
  if(rank!=5)continue;
  count++;for(int r=0;r<5;r++)for(int t=4;t>=0;t--)out<<s[ii[t]][r]<<' ';out<<'\n';
 }
 std::cout<<count<<'\n';
}
