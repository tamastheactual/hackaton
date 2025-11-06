#include <ranges>
#include <print>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <map>
#include <string>
#include <tuple>

struct Passenger
{
    std::string name;
    std::string mother_name;
    struct
    {
        int year;
        int month;
        int day;
    } birth_date;
    std::vector<int> children;  // 3. feladathoz
};

std::vector<Passenger> passengers;

int main()
{
    std::ifstream in("utaslista.txt");
    if (!in)
        return 1;
    std::string line;
    while (std::getline(in, line)) 
    {
        auto& passenger = passengers.emplace_back();
        std::istringstream iss(line);
        std::getline(iss, passenger.name, ',');
        std::string birth_date;
        std::getline(iss, birth_date, ',');
        passenger.birth_date = 
        {
            std::stoi(birth_date.substr(0, 4)),
            std::stoi(birth_date.substr(5, 2)),
            std::stoi(birth_date.substr(8, 2)) 
        };
        std::getline(iss, passenger.mother_name);
    }