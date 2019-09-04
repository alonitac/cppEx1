#include <iostream>
#include "GFNumber.h"

int main() {
    GFNumber n1, n2;
    std::cin >> n1;
    std::cin >> n2;
    if (std::cin.fail()) return 1;
    std::cout << n1 + n2 << std::endl;
    std::cout << n1 - n2 << std::endl;
    std::cout << n2 - n1 << std::endl;
    std::cout << n1 * n2 << std::endl;

    int* len1;
    int* len2;
    GFNumber* factors1 = n1.getPrimeFactors(len1);
    GFNumber* factors2 = n1.getPrimeFactors(len2);

    for (int i=0;i<*len1;i++){
        std::cout << factors1[i] << " ";
    }
    std::cout << std::endl;

    for (int i=0;i<*len2;i++){
        std::cout << factors2[i] << " ";
    }

    delete[] factors1;
    delete[] factors2;
    return 0;
}