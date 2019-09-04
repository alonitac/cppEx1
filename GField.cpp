#include <cmath>
#include "GField.h"
#include <cassert>
#include <iostream>
#include "GFNumber.h"


long gcd(long a, long b)
{
    // pseudo-code from http://www.programming-algorithms.net/article/43434/Greatest-common-divisor
    long r = 0;

    do
    {
        r = a % b;
        a = b;
        b = r;
    } while (b != 0);
    return a;
}


GField::GField(): GField(2, 1){}

GField::GField(long p): GField(p, 1){}

GField::GField(long p, long l)
{
    assert(l>=0);
    assert(p>= 2 and isPrime(p));
    _l = l;
    _p = p;
}

GField::GField(const GField& gf): GField(gf.getChar(), gf.getDegree()){}

GField::~GField() {}

long GField::getChar() const{ return _p;}

long GField::getDegree() const{ return _l;}

long GField::gerOrder() const{ return (long)std::pow(_p, _l);}

bool GField::isPrime(long p)
{
    if (p < 0){
        p *= -1;
    }
    // with the help of https://softwareengineering.stackexchange
    // .com/questions/197374/what-is-the-time-complexity-of-the-algorithm-to-check-if-a-number-is-prime
    if (p < 2) return false;
    if (p == 2) return true;
    if (p % 2 == 0) return false;
    for (int i=3; (i*i) <= p; i+=2) {
        if (p % i == 0 ) return false;
    }
    return true;
}

GFNumber GField::gcd(GFNumber& a, GFNumber& b) const
{
    assert(a.getField() == b.getField());
    assert(a.getNember() > 0 and b.getNember() > 0);
    long x = ::gcd(a.getNember(), b.getNember());
    return GFNumber(x, a.getField());
}

GFNumber GField::createNumber(long k) const
{
    return GFNumber(k % gerOrder(), *this);
}

GField& GField::operator=(const GField& other)
{
    this->_l = other._l;
    this->_p = other._p;
    return *this;
}

bool GField::operator==(const GField& other)
{
    return this->_l == other._l and this->_p == other._p;
}
bool GField::operator!=(const GField& other)
{
    return this->_l != other._l or this->_p != other._p;
}

std::ostream& operator<<(std::ostream& os, const GField& gf)
{
    os << "GF(" << gf._p << "**" << gf._l << ")";
    return os;
}

std::istream& operator>>(std::istream& is, const GField& gf)
{
    is >> gf._p >> gf._l;
    return is;
}


