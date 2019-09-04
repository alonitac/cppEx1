#include <cassert>
#include <iostream>
#include <cmath>
#include "GFNumber.h"
#include "GField.h"

GFNumber::GFNumber(): GFNumber(0, GField(2 ,1)){}

GFNumber::GFNumber(long n): GFNumber(n, GField(2, 1)){}

GFNumber::GFNumber(long n, const GField gf)
{
    assert(n > 1);
    _n = n % gf.gerOrder();
    _gf = gf;
}

GFNumber::GFNumber(const GFNumber& gfn): GFNumber(gfn.getNember(), gfn.getField()){}

GFNumber::~GFNumber(){}

long GFNumber::getNember() const{ return _n;}

GField GFNumber::getField() const{ return _gf;}

bool GFNumber::getIsPrime() const{ return GField::isPrime(_n);}

long rhoPoly(long x){
    return x*x+1;
}

long rho(long n){
    assert(n % 2 != 0);
    // rho
    long x = rand() % n;
    long y = x;
    long p = 1;
    while (p==1)
    {
        x = rhoPoly(x);
        y = rhoPoly(rhoPoly(x));
        p = ::gcd(labs(x-y), n);
    }
    if (p==n){
        return -1;
    }
    return p;
}

GFNumber* append(GFNumber* arr, int* length, GFNumber element)
{
    GFNumber* newArr = new GFNumber[*length+1];
    for (int i=0;i<*length;i++){
        newArr[i] = arr[i];
    }
    newArr[*length] = element;
    *length += 1;
    delete[] arr;
    return newArr;
}

GFNumber* directSearchFactorization(long n, int* length, const GField& gf){
    GFNumber *factors = new GFNumber[0];
    *length = 0;

    long i = 2;
    while (i <= floor(sqrt(n))){
        if (n % i == 0){
            factors = append(factors, length, gf.createNumber(i));
            n = n / floor(i);
        }else{
            i++;
        }
    }
    if (n > 1){
        factors = append(factors, length, gf.createNumber(n));
    }
    return factors;
}



GFNumber* GFNumber::getPrimeFactors(int* length) const
{
    GFNumber *factors = new GFNumber[0];
    *length = 0;

    long num = _n;
    GFNumber factor;
    while (!GField::isPrime(num))
    {
        if (num % 2 == 0){
            factor = _gf.createNumber(2);
        }else{
            factor = _gf.createNumber(rho(num));
            if (factor == -1) {
                delete[] factors;
                return directSearchFactorization(_n, length, _gf);
            }
        }
        factors = append(factors, length, factor);
        num /= factor.getNember();
    }
    return append(factors, length, _gf.createNumber(num));
}

void GFNumber::printFactors()
{
    std::cout << getNember() << "=";
    int* len;
    GFNumber* factors = getPrimeFactors(len);
    for (int i=0;i<*len;i++){
        std::cout << factors[i]._n;
        if (i != *len-1){
            std::cout << "*";
        }
    }
    std::cout << std::endl;
}


GFNumber& GFNumber::operator=(const GFNumber& other)
{
    assert(this->_gf == other.getField());
    this->_n = other.getNember();
    return *this;
}

// addition
GFNumber GFNumber::operator+(long other)
{
    return GFNumber(this->_n + other, this->_gf);
}

GFNumber GFNumber::operator+(const GFNumber& other)
{
    assert(this->_gf == other.getField());
    return *this + other.getNember();
}

GFNumber& GFNumber::operator+=(long other)
{
    this->_n = (this->_n + other) % _gf.gerOrder();
    return *this;
}

GFNumber& GFNumber::operator+=(const GFNumber& other){
    assert(this->_gf == other.getField());
    *this += other.getNember();
    return *this;
}

// substract
GFNumber GFNumber::operator-(long other)
{
    return GFNumber(this->_n - other, this->_gf);
}

GFNumber GFNumber::operator-(const GFNumber& other)
{
    assert(this->_gf == other.getField());
    return *this - other.getNember();
}

GFNumber& GFNumber::operator-=(long other)
{
    this->_n = (this->_n - other) % _gf.gerOrder();
    return *this;
}

GFNumber& GFNumber::operator-=(const GFNumber& other){
    assert(this->_gf == other.getField());
    *this -= other.getNember();
    return *this;
}

// multiply
GFNumber GFNumber::operator*(long other)
{
    return GFNumber(this->_n * other, this->_gf);
}

GFNumber GFNumber::operator*(const GFNumber& other)
{
    assert(this->_gf == other.getField());
    return *this * other.getNember();
}

GFNumber& GFNumber::operator*=(long other)
{
    this->_n = (this->_n * other) % _gf.gerOrder();
    return *this;
}

GFNumber& GFNumber::operator*=(const GFNumber& other){
    assert(this->_gf == other.getField());
    *this *= other.getNember();
    return *this;
}

// modulo
GFNumber GFNumber::operator%(long other)
{
    return GFNumber(this->_n % other, this->_gf);
}

GFNumber GFNumber::operator%(const GFNumber& other)
{
    assert(this->_gf == other.getField());
    return *this % other.getNember();
}

GFNumber& GFNumber::operator%=(long other)
{
    this->_n = (this->_n % other) % _gf.gerOrder();
    return *this;
}

GFNumber& GFNumber::operator%=(const GFNumber& other){
    assert(this->_gf == other.getField());
    *this %= other.getNember();
    return *this;
}

bool GFNumber::operator<(const GFNumber& other){
    assert(this->_gf == other.getField());
    return this->_n < other.getNember();
}
bool GFNumber::operator<=(const GFNumber& other){
    assert(this->_gf == other.getField());
    return this->_n <= other.getNember();

}
bool GFNumber::operator>(const GFNumber& other){
    assert(this->_gf == other.getField());
    return this->_n > other.getNember();
}
bool GFNumber::operator>=(const GFNumber& other){
    assert(this->_gf == other.getField());
    return this->_n >= other.getNember();
}

bool GFNumber::operator==(const GFNumber& other)
{
    return _gf == other.getField() and _n == other.getNember();
}

bool GFNumber::operator!=(const GFNumber& other)
{
    return _gf != other.getField() or _n != other.getNember();
}

std::istream& operator>>(std::istream& is, const GFNumber& gfn)
{
    is >> gfn._n >> gfn._gf;
    return is;
}

std::ostream& operator<<(std::ostream& os, const GFNumber& gfn)
{
    os << gfn._n << gfn._gf;
    return os;
}
