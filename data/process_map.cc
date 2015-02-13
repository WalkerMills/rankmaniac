#include <iostream>

#include "tags.hh"


const int MAX_ITER = 50;

int main() {
    float iter;
    size_t delim;
    std::string key;
    std::string line;

    // While we have a line to process
    while ( std::getline(std::cin, line) ) {
        // Find the key delimiter
        delim = line.find(KEY_SEP);
        // Extract the key
        key = line.substr(0, delim);
        // Trim the line to exclude the key & delimiter
        line.erase(0, delim + 1);
        // Find the iteration count delimiter
        delim = key.find(ITER_SEP);
        // Extract the iteration number
        iter = std::stoi(key.substr(0, delim));
        // If this node has converged, or it's the last iteration
        if ( line[0] == CONV_MARKER ) {
            // Tag this node as converged
            std::cout << CONVERGED << KEY_SEP << key << KEY_SEP << line 
                      << std::endl;
        } else if ( iter == MAX_ITER ) {
            // Tag this node as converged
            std::cout << CONVERGED << KEY_SEP << key << KEY_SEP << CONV_MARKER
                      << CHILD_SEP << line << std::endl;
        } else {
            // Tag this node as diverged
            std::cout << DIVERGED << KEY_SEP << key << KEY_SEP << line 
                      << std::endl;
        }
    }
}