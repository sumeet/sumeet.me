My very first [self-hosting compiler](https://en.wikipedia.org/wiki/Bootstrapping_(compilers))! This started as an experiment to see if sum types, pattern matching and generics would make Golang more fun to code in.

I eventually ended up implementing the compiler in the language itself, which ended up being a really weird experience because I realized I needed to keep around a compiled version of the compiler in order to compile new compilers. If you want to add a feature to the language, you can't start using it in your compiler until you compile the new version and save it somewhere.

It's a really bizarre experience that I recommend to anyone interested in making programming languages!
