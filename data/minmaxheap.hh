#include <cmath>
#include <iostream>
#include <vector>

/*
 * Min-Max heap, as described here:
 * http://www.cs.otago.ac.nz/staffpriv/mike/Papers/MinMaxHeaps/MinMaxHeaps.pdf 
 * Also, a limited size max heap, implemented using a min-max heap
 */

template <typename T>
class MinMaxHeap {
private:
    void bubble_up(int index) {
        int dir = this->direction(index);
        int parent = (index - 1) / 2;

        if ( index > 0 && this->compare(index, parent) == -dir ) {
            T tmp = this->values[parent];
            this->values[parent] = this->values[index];
            this->values[index] = tmp;

            this->bubble_up_dir(parent, -dir);
        } else {
            this->bubble_up_dir(index, dir);
        }
    }

    void bubble_up_dir(int index, int dir) {
        if ( index > 2 ) {
            int grandparent = ((index - 1) / 2 - 1) / 2;
            if ( this->compare(index, grandparent) == dir ) {
                T tmp = this->values[grandparent];
                this->values[grandparent] = this->values[index];
                this->values[index] = tmp;

                this->bubble_up_dir(grandparent, dir);
            }
        }
    }

    int direction(int index) {
        return pow(-1, (int) floor(log2(index + 1) + 1) % 2);
    }

    int max_id() {
        int max = 0;
        if ( this->size() >= 2 ) {
            ++max;
            if ( this->size() >= 3 && this->compare(2, 1) == 1 ) {
                ++max;
            }
        }

        return max;
    }

    void trickle_down(int index) {
        int dir = this->direction(index);
        this->trickle_down_dir(index, dir);
    }

    void trickle_down_dir(int index, int dir) {
        int m = 2 * index + 1;
        int k, first_grandchild, last_grandchild;
        T tmp;

        if ( this->size() > m ) {
            k = m + 1;
            first_grandchild = 4 * index + 3;
            last_grandchild = first_grandchild + 3;

            if ( this->size() > k && this->compare(k, m) == dir ) {
                m = k;
            }
            for ( k = first_grandchild; k < this->size() && 
                 k <= last_grandchild; ++k ) {
                if ( this->compare(k, m) == dir ) {
                    m = k;
                }
            }

            if ( this->compare(m, index) == dir ) {
                tmp = this->values[m];
                this->values[m] = this->values[index];
                this->values[index] = tmp;

                if ( m >= first_grandchild ) {
                    int parent = (m - 1) / 2;
                    if ( this->compare(m, parent) == -dir ) {
                        tmp = this->values[m];
                        this->values[m] = this->values[parent];
                        this->values[parent] = tmp;
                    }

                    this->trickle_down_dir(m, dir);
                }
            }
        }
    }

protected:
    std::vector<T> values;

    int compare(int i, int j) {
        if ( i == j || this->values[i] == this->values[j] ) return 0;
        return pow(-1, this->values[i] < this->values[j]);
    }

public:
    MinMaxHeap() { }
    ~MinMaxHeap() { }

    T get_max() {
        int max = this->max_id();
        T ret = this->values[max];
        T last = this->values.back();
        this->values.pop_back();

        if ( this->size() > max ) {
            this->values[max] = last;
            this->trickle_down(max);
        }

        return ret;
    }

    T get_min() {
        T ret = this->values[0];
        T last = this->values.back();
        this->values.pop_back();

        if ( this->size() ) {
            this->values[0] = last;
            this->trickle_down(0);
        }

        return ret;
    }

    void insert(T value) {
        this->values.push_back(value);
        this->bubble_up(this->size() - 1);
    }

    T peek_max() {
        return this->values[this->max_id()];
    }

    T peek_min() {
        return this->values[0];
    }

    int size() {
        return this->values.size();
    }
};

template <typename T>
class LimitedMaxHeap : public MinMaxHeap<T> {
private:
    unsigned capacity;

public:
    LimitedMaxHeap(unsigned capacity) {
        this->capacity = capacity;
    }
    ~LimitedMaxHeap() { }

    void insert(T value) {
        if ( this->size() >= this->capacity ) {
            if ( value <= this->peek_min() ) return;
            this->get_min();
        }

        MinMaxHeap<T>::insert(value);
    }
};
