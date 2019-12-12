//
//  BigInteger.hpp
//  RSA
//
//  Created by Wang Jianmin on 2019/4/25.
//  Copyright © 2019年 Zhang Tianchen. All rights reserved.
//

#ifndef BigInteger_hpp
#define BigInteger_hpp

#include <iostream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <time.h>

typedef unsigned int uint;
typedef unsigned long long uint64;

#define MAX 1000000000
#define MAX_LEN 9
using namespace std;

class BigInteger {
private:
    vector<uint> data;
    void killZero();
    int compare(const BigInteger& target) const;
    bool isNumber(const string& targetStr);
    static uint partDivide(const BigInteger& beDivide, const BigInteger target);
    
public:
    //generators
    BigInteger();
    BigInteger(uint src);
    BigInteger(const string& srcStr);
    
    //operators
    BigInteger operator+(const BigInteger& target) const;
    BigInteger operator-(const BigInteger& target) const;
    BigInteger operator*(const BigInteger& target) const;
    BigInteger operator/(const BigInteger& target) const;
    BigInteger operator%(const BigInteger& target) const;
    
    BigInteger power(const BigInteger& pwr, const BigInteger& mod) const;
    bool isOdd() const;
    
    //relationship
    bool operator>(const BigInteger& target) const;
    bool operator<(const BigInteger& target) const;
    bool operator>=(const BigInteger& target) const;
    bool operator<=(const BigInteger& target) const;
    bool operator==(const BigInteger& target) const;
    bool operator!=(const BigInteger& target) const;
    
    string toString() const;
};

#endif /* BigInteger_hpp */
