#include <iostream>
#include <tuple>
#include <vector>

#include "minmaxheap.hh"
#include "tags.hh"

const int RANKS = 20;


int main() {
    bool convergence = true;
    float rank;
    int node;
    size_t delim;
    std::string key;
    std::string line;
    std::vector<std::string> converged;
    std::vector<std::string>::iterator it;
    LimitedMaxHeap<std::tuple<float, int>> final(RANKS);
    std::tuple<float, int> item;

    // While we have a line to process
    while ( std::getline(std::cin, line) ) {
        // Find the key delimiter
        delim = line.find(KEY_SEP);
        // Extract the key
        key = line.substr(0, delim);
        // Trim the line to exclude the key & delimiter
        line.erase(0, delim + 1);
        // If we got a divergent node
        if ( key.compare(DIVERGED) == 0 ) {
            // Pass this line along for the next iteration
            std::cout << line << std::endl;
            // We have not globally converged
            convergence = false;
        // Or, if this node has converged & we have not gotten a divergent node
        } else if ( convergence ) {
            // Cache this line, possibly to become a final rank
            converged.push_back(line);
        } else {
            // Pass this line along for the next iteration
            std::cout << line << std::endl;
        }
    }

    // If all ranks have converged
    if ( convergence ) {
        for ( it = converged.begin(); it != converged.end(); ++it ) {
            line = *it;
            // Find the key delimiter
            delim = line.find(KEY_SEP);
            // Extract the key
            key = line.substr(0, delim);
            // Trim the line to exclude the key & delimiter
            line.erase(0, delim + 1);
            // Find the node ID delimiter
            delim = key.find(ID_SEP);
            // Extract the node id
            node = std::stoi(key.substr(delim + 1));
            // Find the convergence flag delimiter
            delim = line.find(CHILD_SEP);
            // Trim the line to exclude the convergence flag & delimiter
            line = line.erase(0, delim + 1);
            // Find the rank delimiter
            delim = line.find(CHILD_SEP);
            // Extract the node's rank
            rank = std::stof(line.substr(0, delim));
            // Push the (rank, node ID) tuple onto the limited-size max heap
            final.insert(std::make_tuple(rank, node));
        }
        // Extract the largest RANKS ranks & node ID's from the heap
        for ( int i = 0; i < RANKS; ++i ) {
            item = final.get_max();
            // Emit a final ranking for the node
            std::cout << "FinalRank" << ID_SEP << std::get<0>(item) << KEY_SEP << std::get<1>(item) << std::endl;
        }
    } else {
        // Emit all cached lines
        for ( it = converged.begin(); it != converged.end(); ++it ) {
            std::cout << *it << std::endl;
        }
    }
}