#include <cmath>
#include <iostream>
#include <map>

#include "tags.hh"


const float ALPHA = 0.85;
const float BETA = 0.15;
const float EPSILON = 0.002;

int main() {
    float rank;
    size_t delim;
    std::map<std::string, float> current;
    std::map<std::string, float> old;
    std::map<std::string, float>::iterator it;
    std::map<std::string, std::string> children;
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
        // If we got graph structure information
        if ( line[0] == GRAPH_MARKER ) {
            // Trim the graph information marker
            line.erase(0, 1);
            // If this node has converged
            if ( line[0] == CONV_MARKER ) {
                // Emit this line
                std::cout << key << KEY_SEP << line << std::endl;
                // Process the next node
                continue;
            }
            // Find the current rank delimiter
            delim = line.find(CHILD_SEP);
            // Extract the rank from the current iteration 
            rank = std::stof(line.substr(0, delim));
            // Store this rank as the node's old rank
            old[key] = rank;
            // Trim the line to exclude the rank & delimiter
            line.erase(0, delim + 1);
            // Find the previous rank delimiter
            delim = line.find(CHILD_SEP);
            // Trim the line to exclude the previous rank & delimiter
            line.erase(0, delim + 1 * (delim != std::string::npos));
            // Store the children of this node, if any
            children[key] = line;
        // Otherwise, we got a rank contribution
        } else {
            // Extract the inherited rank
            rank = std::stof(line);
            // Update this node's rank
            if ( current.count(key) > 0 ) {
                current[key] += rank;
            } else {
                current[key] = rank;
            }
        }
    }
    
    // For every unconverged node
    for ( it = old.begin(); it != old.end(); ++it ) {
        rank = BETA;
        // If we got rank contributions
        if ( current.count(it->first) > 0 ) {
            // Scale them, and add them to the new rank
            rank += ALPHA * current[it->first];
        }
        // Emit the key
        std::cout << it->first << KEY_SEP;
        // If the normalized difference in ranks is less than our threshold
        if ( std::abs(it->second - rank) / rank <= EPSILON ) {
            // Add a converged flag to the output
            std::cout << CONV_MARKER << ',';
        }
        // Emit the rest of the data for this node
        std::cout << rank << CHILD_SEP << it->second << CHILD_SEP 
                  << children[it->first] << std::endl;
    }
}