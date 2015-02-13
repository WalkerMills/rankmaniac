# Default shell
SHELL = /bin/sh

# Default C++ compiler
CXX = g++

# Default compiler flags (for C and C++)
override CFLAGS += -O3 -mtune=generic

# Default compiler flags for C++
override CXXFLAGS += $(CFLAGS) -std=c++11

# Default linker flags
override LD_FLAGS += -Wl,-O1,--sort-common,--as-needed,-z,relro -static

HDRS = tags.hh

BINS = pagerank_map pagerank_reduce process_map

# Clear allowed target suffixes
.SUFFIXES:
# Set allowed target suffixes
.SUFFIXES: .cc .hh

# Declare all phony targets
.PHONY: all clean

all: $(BINS)

clean:
	rm -f $(BINS)

%: %.cc $(HDRS)
	$(CXX) $(LD_FLAGS) $(CXXFLAGS) $< -o $@
