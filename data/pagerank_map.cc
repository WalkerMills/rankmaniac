#include <iostream>
#include <map>
#include <vector>

#include "tags.hh"


int main() {
    bool converged;
    float current;
    float inheritance;
    int child;
    int iter = 1;
    size_t delim;
    std::string key;
    std::string line;
    std::map<int, float> updates;
    std::map<int, float>::iterator uit;
    std::vector<int> children;
    std::vector<int>::iterator cit;

    // While we have a line to process
    while ( std::getline(std::cin, line) ) {
        // Find the key delimiter
        delim = line.find(KEY_SEP);
        // Extract the key
        key = line.substr(0, delim);
        // Trim the line to exclude the key & delimiter
        line.erase(0, delim + 1);
        // If this is not the first iteration
        if ( key[0] != 'N' ) {
            // Find the iteration delimiter
            delim = key.find(ITER_SEP);
            // Extract the iteration number
            iter = std::stoi(key.substr(0, delim));
            // Increment to current iteration
            ++iter;
            // Trim the key to exclude the iteration & delimiter
            key.erase(0, delim + 1);
        }
        // Prepend the current iteration to the key
        key.insert(0, std::to_string(iter) + ITER_SEP);
        // Propagate local graph info
        std::cout << key << KEY_SEP << GRAPH_MARKER << line << std::endl;
        // Check for a convergence flag
        converged = line[0] == CONV_MARKER;
        // Remove the convergence flag, if it exists
        if ( converged ) {
            line.erase(0, 2);
        }
        // Find the current rank delimiter
        delim = line.find(CHILD_SEP);
        // Extract the current rank
        current = std::stof(line.substr(0, delim));
        // Trim the line to exclude the current rank & delimiter
        line.erase(0, delim + 1);
        // Find the previous rank delimiter
        delim = line.find(CHILD_SEP);
        // Trim the line to exclude the previous rank & delimiter
        line.erase(0, delim + 1 * (delim != std::string::npos));
        // Check if this node has any children
        delim = line.find(CHILD_SEP);
        // If no delimiter was found, and the line is empty, or it only
        // contains an interpolation term
        if ( delim == std::string::npos && 
             (line.size() == 0 || line.find(INTERP_SEP) == 0) ) {
            // If this node has not converged
            if ( ! converged ) {
                // Send this node all of its current rank
                std::cout << key << KEY_SEP << current << std::endl;
            }
            // Process the next node
            continue;
        }
        // While there is more than one child
        for ( ; delim != std::string::npos; delim = line.find(CHILD_SEP) ) {
            // Extract the child's index
            child = std::stoi(line.substr(0, delim));
            // Trim this child from the input
            line.erase(0, delim + 1);
            // Add this child to the vector of children
            children.push_back(child);
        }
        // Find the interpolation separator, which may be std::string::npos
        delim = line.find(INTERP_SEP);
        // Extract the last child
        child = std::stoi(line.substr(0, delim));
        // Add this child to the vector of children
        children.push_back(child);
        
        // Calculate the per-child inherited rank
        inheritance = current / children.size();
        // Aggregate the children's ranks locally
        for ( cit = children.begin(); cit != children.end(); ++cit ) {
            if ( updates.count(*cit) > 0 ) {
                updates[*cit] += inheritance;
            } else {
                updates[*cit] = inheritance;
            }
        }
        // Reset the children
        children.clear();
    }

    // Emit the aggregated ranks
    for ( uit = updates.begin(); uit != updates.end(); ++uit ) {
        std::cout << iter << ITER_SEP + "NodeId" + ID_SEP << uit->first
                  << KEY_SEP << uit->second << std::endl;
    }
}