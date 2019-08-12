//
//  BigInteger.cpp
//  RSA
//
//  Created by Zhang Tianchen on 2019/4/25.
//  Copyright © 2019年 Zhang Tianchen. All rights reserved.
//

#include "BigInteger.hpp"

BigInteger Euclid(BigInteger a, BigInteger b) {
    if (a < b) return Euclid(b, a);
    BigInteger zero(0);
    while (a % b != zero) {
        BigInteger temp = b;
        b = a % b;
        a = temp;
    }
    return b;
}

bool BigInteger::isNumber(const string& targetStr) {
    for (auto digit = targetStr.begin(); digit != targetStr.end(); ++digit)
        if (!(*digit >= '0' && *digit <= '9')) return false;
    return true;
}

BigInteger::BigInteger() {}
BigInteger::BigInteger(uint src) {
    this->data.push_back(src % MAX);
    if (src >= MAX)
        this->data.push_back(src / MAX);
}
BigInteger::BigInteger(const string& srcStr) {
    if (!isNumber(srcStr)) return;
    int length = srcStr.length();
    while (length >= MAX_LEN) {
        string temp = srcStr.substr(length - MAX_LEN, MAX_LEN);
        this->data.push_back(stoi(temp));
        length -= MAX_LEN;
    }
    if (length > 0) {
        string temp = srcStr.substr(0, length);
        this->data.push_back(stoi(temp));
    }
    this->killZero();
}

int BigInteger::compare(const BigInteger& target) const {
    int len1 = this->data.size();
    int len2 = target.data.size();
    if (len1 != len2) return len1 > len2 ? 1 : -1;
    for (int cmp = len1 - 1; cmp >= 0; --cmp) {
        if (this->data[cmp] != target.data[cmp])
            return this->data[cmp] > target.data[cmp] ? 1 : -1;
    }
    return 0;
}

void BigInteger::killZero() {
    int len = this->data.size();
    while (--len >= 1) {
        if (this->data[len] > 0) break;
        else this->data.pop_back();
    }
}

bool BigInteger::operator<(const BigInteger &target) const {
    return compare(target) < 0;
}

bool BigInteger::operator>(const BigInteger &target) const {
    return compare(target) > 0;
}

bool BigInteger::operator==(const BigInteger &target) const {
    return compare(target) == 0;
}

bool BigInteger::operator!=(const BigInteger &target) const {
    return compare(target) != 0;
}

bool BigInteger::operator>=(const BigInteger &target) const {
    return compare(target) >= 0;
}

bool BigInteger::operator<=(const BigInteger &target) const {
    return compare(target) <= 0;
}

BigInteger BigInteger::operator+(const BigInteger &target) const {
    BigInteger result;
    int len1 = this->data.size();
    int len2 = target.data.size();
    int minLen = len1 < len2 ? len1 : len2;
    int maxLen = len1 < len2 ? len2 : len1;
    uint value = 0, carry = 0;
    for (int cnt = 0; cnt < minLen; ++cnt) {
        value = this->data[cnt] + target.data[cnt] + carry;
        if (value >= MAX) {
            result.data.push_back(value - MAX);
            carry = 1;
        }else {
            result.data.push_back(value);
            carry = 0;
        }
    }
    const BigInteger &bigger = len1 > len2 ? *this : target;
    for (int cnt = minLen; cnt < maxLen; ++cnt) {
        value = bigger.data[cnt] + carry;
        if (value >= MAX) {
            result.data.push_back(value - MAX);
            carry = 1;
        }else {
            result.data.push_back(value);
            carry = 0;
        }
    }
    if (carry > 0) result.data.push_back(carry);
    return result;
}

BigInteger BigInteger::operator-(const BigInteger &target) const {
    if (*this <= target) return BigInteger(0);
    int len1 = this->data.size();
    int len2 = target.data.size();
    uint value = 0, carry = 0;
    BigInteger result;
    for (int cnt = 0; cnt < len2; ++cnt) {
        if (this->data[cnt] < target.data[cnt] + carry) {
            value = this->data[cnt] + MAX - target.data[cnt] - carry;
            carry = 1;
        } else {
            value = this->data[cnt] - target.data[cnt] - carry;
            carry = 0;
        }
        result.data.push_back(value);
    }
    for (int cnt = len2; cnt < len1; ++cnt) {
        if (this->data[cnt] < carry) {
            value = this->data[cnt] + MAX - carry;
            carry = 1;
        } else {
            value = this->data[cnt] - carry;
            carry = 0;
        }
        result.data.push_back(value);
    }
    result.killZero();
    return result;
}

BigInteger BigInteger::operator*(const BigInteger &target) const {
    int len1 = this->data.size();
    int len2 = target.data.size();
    if (len1 < len2) return target.operator*(*this);
    uint64 value = 0, carry = 0;
    BigInteger result(0);
    for (int cnt2 = 0; cnt2 < len2; ++cnt2) {
        BigInteger temp;
        carry = 0;
        for (int shift = 0; shift < cnt2; ++shift)
            temp.data.push_back(0);
        for (int cnt1 = 0; cnt1 < len1; ++cnt1) {
            value = (uint64)(target.data[cnt2]) * (uint64)this->data[cnt1] + carry;
            temp.data.push_back((uint)(value % MAX));
            carry = value / MAX;
        }
        if (carry) temp.data.push_back((uint)carry);
        result = result + temp;
    }
    result.killZero();
    return result;
}

BigInteger BigInteger::operator/(const BigInteger &target) const {
    if (*this < target) return BigInteger(0);
    int len1 = this->data.size();
    int len2 = target.data.size();
    uint value;
    BigInteger result, beDivide;
    for (int cnt = len1 - len2 + 1; cnt < len1; ++cnt)
        beDivide.data.push_back(this->data[cnt]);
    for (int cnt = len1 - len2; cnt >= 0; --cnt) {
        beDivide.data.insert(beDivide.data.begin(), this->data[cnt]);
        beDivide.killZero();
        value = partDivide(beDivide, target);
        beDivide = beDivide - target * value;
        result.data.insert(result.data.begin(), value);
    }
    result.killZero();
    return result;
}

BigInteger BigInteger::operator%(const BigInteger &target) const {
    return *this - target * (*this / target);
}

uint BigInteger::partDivide(const BigInteger &beDivide, const BigInteger target) {
    BigInteger temp1 = beDivide;
    const BigInteger &temp2 = target;
    uint temp, partRes = 0;
    bool positive = true;
    while (temp1 >= temp2) {
        int len1 = temp1.data.size();
        int len2 = temp2.data.size();
        uint64 tmp1, tmp2;
        if (len1 == len2) {
            if (len1 > 1) {
                tmp1 = (uint64)temp1.data[len1 - 1] * MAX + temp1.data[len1 - 2];
                tmp2 = (uint64)temp2.data[len1 - 1] * MAX + temp2.data[len1 - 2];
            } else {
                tmp1 = (uint64)temp1.data[len1 - 1];
                tmp2 = (uint64)temp2.data[len2 - 1];
            }
        } else {
            tmp1 = (uint64)temp1.data[len1 - 1] * MAX + temp1.data[len1 - 2];
            tmp2 = (uint64)temp2.data[len2 - 1];
        }
        temp = (uint)(tmp1 / tmp2);
        temp1 = temp2 * temp - temp1;
        partRes = positive ? (partRes + temp) : (partRes - temp);
        positive = !positive;
    }
    while (partRes > 0 && target * partRes > beDivide) --partRes;
    return partRes;
}

string BigInteger::toString() const {
    int len = this->data.size();
    string result;
    for (int cnt = len - 1; cnt >= 0; --cnt) {
        result += to_string(this->data[cnt]);
    }
    return result;
}

bool BigInteger::isOdd() const {
    return this->data[0] & 1;
}

BigInteger BigInteger::power(const BigInteger &pwr, const BigInteger &mod) const {
    bool bin[3000];
    int length = -1;
    BigInteger p = pwr, result(1);
    BigInteger temp(2);
    while (p > 0) {
        bin[++length] = p.isOdd();
        p = p / temp;
    }
    for (int i = length; i >= 0; --i) {
        result = result * result;
        //cout<<result.toString()<<endl;
        if (bin[i]) result = result * (*this);
        //cout<<result.toString()<<endl;
        result = result % mod;
    }
    return result;
}
