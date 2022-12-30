#include "matplotlibcpp.h"
#include <fstream>
#include <json.hpp>
#include <vector>

// g++ quadtree.cpp -o quadtree -I/usr/include/python3.10 -lpython3.10

using namespace std;
using json = nlohmann::json;
namespace plt = matplotlibcpp;

struct Point{
    float lon, lat;
    Point(float lon, float lat) : lon(lon), lat(lat) {}
};

class Polygon{
private:
    int COLLINEAR = 0;
    int CLOCKWISE = 1;
    int COUNTER_CLOCKWISE = 2;
    vector<Point> points;
public:
    Polygon(){

    }
};

int main()
{
    // u and v are respectively the x and y components of the arrows we're plotting
    // std::vector<int> x, y, u, v;
    // for (int i = -5; i <= 5; i++) {
    //     for (int j = -5; j <= 5; j++) {
    //         x.push_back(i);
    //         u.push_back(-i);
    //         y.push_back(j);
    //         v.push_back(-j);
    //     }
    // }

    // plt::quiver(x, y, u, v);
    // plt::show();
    ifstream f("HCM.geojson");
    json data = json::parse(f)["features"][0]["geometry"]["coordinates"][0][0];
    for (json::iterator point = data.begin(); point != data.end(); ++point){
        cout << (*point) << '\n';
    }

}