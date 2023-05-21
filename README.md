# My Scratch Work

## [Crafting Interpreters](https://craftinginterpreters.com/contents.html)

I'm planning to work through the chapters of the book and write some code.

To start the interpreter:

> python py-loxi/loxi.py


### [Notes Chapter 01](notes.ch01.md)

### [Notes Chapter 02](notes.ch02.md)

### Notes Chapter 05

* derivatives (strings from the grammar) 
* productions (rules).

If we have productions, what code generates derivatives?

See also [py-loxi/tool/generate-ast.py]

Since python has pattern matching, should I implement using that instead of visitor pattern?


### Notes Chapter 06

Had to move around code for imports not to be circular.

### Notes Chapter 07

Evaluation

N. skipped detecting runtime errors
TODO handle runtime error
TODO add test cases for interpreter

### Notes Chapter 08

next is environments
basic environments implemented. need test cases

TODO
[] assignment
[] scopes
