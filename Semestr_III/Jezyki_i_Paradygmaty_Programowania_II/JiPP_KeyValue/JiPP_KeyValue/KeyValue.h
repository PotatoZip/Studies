#pragma once

#include <iostream>
#include <vector>

template <typename T1, typename T2>
class KeyValue {
private:
	std::vector<T1> keys;
	std::vector<T2> values;

public:
	KeyValue() : keys(), values() {}
	KeyValue(const T1& newKeys, const T2& newValues) : keys(1, newKeys), values(1, newValues) {}

	T1 getKeys(size_t indx) const {
		if (indx < keys.size()) {
			return keys[indx];
		}
		else {
			return T1();
		}
	}

	T2 getValues(size_t indx) const {
		if (indx < values.size()) {
			return values[indx];
		}
		else {
			return T2();
		}
	}

	void setKeys(const T1& newKeys, size_t indx) const {
		if (indx < keys.size()) {
			keys[indx] = newKeys;
		}
		else {
			std::cerr << "Error: cannot set keys\n" << std::endl;
		}
	}

	void setValues(const T2& newValues, size_t indx) const {
		if (indx < values.size()) {
			values[indx] = newValues;
		}
		else {
			std::cerr << "Error: cannot set values\n" << std::endl;
		}
	}
};

//Wiktor Zmiendak

