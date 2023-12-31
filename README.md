# NORM Programming language

**Norm** is a simple,basic programming language implemented in python.

## Installation

Simply run the `shell.py` script and after you can just write a one line statement and just press Enter for execution or create a `.norm` file with multi-line program statements and run `RUN("filename.norm")`.

## Usage

Create a new file `test.norm`

Edit the created file.

```
VAR x = "Hello World"
PRINT(x)

```
Run

```
RUN("test.norm")

```
Output

```
Hello World
```

## Documentation

- **General:** There is no specific entrypoint for the program. For writing comments use `@`.

```
@ This is a comment

// Write your code

```

- **Variables:** Variables(int,float,string,list,functions,bool) are declared using `VAR` keyword. If you want to change a declared variable you still will have to use the `VAR` keyword,else it throws an error.

```
VAR a = 100
VAR b = "norm"
VAR c = [1,2,3,4,5]
VAR d = ["hello","world","again"]
VAR e = TRUE

VAR a = a*3
VAR b = "language"
VAR e = FALSE

```
- **Types:** 

-1.INTEGER: You can use normal binary operators(+,-,*,/,==,!=,>,<,>=,<=). Other than these you can use `^` for power and `%` for modulo. Also you can use `NOT,AND,OR` keywords.


-2.STRING: You can use '+' operator to join two strings. You can also use '*' operator for concatenating a string to itself x number of times.

```
VAR name = "Naruto"
VAR surname = "Uzumaki"
VAR ninja = name + surname
VAR ninjas = name*3
PRINT(ninja)
PRINT(ninjas)

```
Output

```
NarutoUzumaki
NarutoNarutoNaruto
```

-3.LIST or ARRAY: Following code will help you understand methods of list class.

```
VAR arr = [1,2,3,4]
VAR x = arr + 5
VAR y = arr * [5,6,7,8]
VAR z = arr - 2  
VAR w = arr : 0 
@ 2 and 3 indices of elements which we want to delete and get
PRINT(x)
PRINT(y)
PRINT(z)
PRINT(w)

```
Output

```
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5, 6, 7, 8]
[1, 2, 4]
4

```

-4.FUNCTIONS: We can make one line functions as well as multi-line.They have a bit different syntax.First let's see one line functions.In one line functions you can only write one expression and these functions don't have `RETURN` keyword. 

```
FUNC mul(a,b) -> a*b
VAR result = mul(4,5)
PRINT(result)
```
Output

```
20
```
Now for multi-line functions you can write as many expressions as you need. You can also use the `RETURN` keyword.But in multi-line functions after writing your function you should use the `END` keyword else it throws an error.(In multi-line statements, it is ok to not give indentations, but giving them will help us understand better)

```
FUNC foo(a)
    VAR x = a+1
    VAR x = x*2
    RETURN x
    END
VAR ans = foo(3)
PRINT(ans) 
```
Output

```
8
```

-5.BUILT-IN FUNCTIONS: Given are some built-in functions.(You know two already -> PRINT and RUN)

-**INPUT():** This takes input from the user in form of string.

```
VAR name = INPUT()
```
-**INTINPUT():** Takes input in integer or float datatype.

-**CLEAR():** Clears our terminal.

-**ISNUM(arg):** Checks if given argument is int or float.

Similarly there are `ISSTR,ISLIST,ISFUNC` for checking string, list and function.

-**NUM(arg):** Converts string argument which can be converted to int into an integer dtype.(not float though)

Similarly there is `STR` function

There are `LEN` and `LENSTR` functions for checking length of lists and strings.

There are `GINT` and `ROUND` functions to get floor and to get rounded int.

FOR NOW, THESE ARE THE ONLY BUILT-IN FUNCTIONS DEFINED.


- **Conditionals:** `If-else` conditions are almost similar like other languages.Just remember one thing -> If you are writing multi lines IF-ELSE then you have to specify `END` keyword at last.Also remember to use the `THEN` keyword after every condition

```
VAR age = INTINPUT()
IF age<18 THEN
    PRINT("You cannot drink")
ELIF age>=18 AND age<=22 THEN 
    PRINT("You have to drink")
ELSE
    PRINT("You can drink")
    END
```
I'd suggest to write multi-lines and use `END` keyword,but if you want to just write one IF which has just one expression, don't include `END` as it would be a one liner.

- **Loops:** Let's see FOR and WHILE loops one-by-one

- 1.WHILE LOOP: Given below is the syntax.Remember the last points told in Conditionals here too.

```
VAR a = 0
WHILE a<5 THEN
    VAR a = a+1
    END
PRINT(a)
```
Output

```
5
```
- 2.FOR LOOP: Using the `STRIDE` keyword is optional,by default it will be 1.Remember the last points told in Conditionals here too.

```
FOR i=0 TO 5 STRIDE 2 THEN 
    PRINT("LUFFY")
    END
```
Output

```
LUFFY
LUFFY
LUFFY
```

## Example

I've included an example.norm script , you can check it for understanding the `END` keyword more better.

## NOTE

Remember to use `RUN` keyword for running external files.

## Keywords

These are the only keywords in the language.

```
VAR, AND, OR, NOT, IF, ELSE, ELIF, THEN, WHILE, FOR, TO, STRIDE, FUNC, END, RETURN, NULL, TRUE, FALSE
```










