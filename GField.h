//GField.h
#ifndef _GFIELD_H_
#define _GFIELD_H_

#include <iostream>
#include "GFNumber.h"

class GField
{
public:
    GField();
    GField(long);
    GField(long, long);
    GField(const GField&);
    ~GField();
    long getChar() const;
    long getDegree() const;
    long gerOrder() const;
    static bool isPrime(long);
    GFNumber gcd(GFNumber&, GFNumber&) const;
    GFNumber createNumber(long) const;
    GField& operator=(const GField&);
    friend std::istream& operator>>(std::istream&, const GField&);
    friend std::ostream& operator<<(std::ostream&, const GField&);
    bool operator==(const GField&);
    bool operator!=(const GField&);

private:
    long _p;
    long _l;
};

long gcd(long, long);

#endif // _GFIELD_H_