//‫‪GFNumber.h
#ifndef _GFNumber_H_
#define _GFNumber_H_

#include "GField.h"

class GFNumber{
public:
    GFNumber();
    GFNumber(long);
    GFNumber(long, const GField);
    GFNumber(const GFNumber&);

    GFNumber(long i, const GField field);

    GFNumber(long i, const GField field);

    ~GFNumber();
    long getNember() const;
    GField getField() const;
    GFNumber* getPrimeFactors(int*) const;
    void printFactors();
    bool getIsPrime() const;

    GFNumber& operator=(const GFNumber&);

    GFNumber operator+(const GFNumber&);
    GFNumber operator+(long);
    GFNumber& operator+=(const GFNumber&);
    GFNumber& operator+=(long);

    GFNumber operator-(const GFNumber&);
    GFNumber operator-(long);
    GFNumber& operator-=(const GFNumber&);
    GFNumber& operator-=(long);

    GFNumber operator*(const GFNumber&);
    GFNumber operator*(long);
    GFNumber& operator*=(const GFNumber&);
    GFNumber& operator*=(long);

    GFNumber operator%(const GFNumber&);
    GFNumber operator%(long);
    GFNumber& operator%=(const GFNumber&);
    GFNumber& operator%=(long);

    bool operator==(const GFNumber&);
    bool operator!=(const GFNumber&);
    bool operator<(const GFNumber&);
    bool operator<=(const GFNumber&);
    bool operator>(const GFNumber&);
    bool operator>=(const GFNumber&);
    friend std::istream& operator>>(std::istream&, const GFNumber&);
    friend std::ostream& operator<<(std::ostream&, const GFNumber&);


private:
    long _n;
    GField _gf;
};

#endif //_‫‪GFNumber_H_
