# The Java solution
## Starting the program
Firstly make sure you are in the `java` directory then run this command to compile the program:
```
javac src/*.java -d bin
```
*Explanation: the `src/*.java` searches the java files in the `src` directory and the `-d bin` generates the `.class` files into the `bin` directory*

Next run the program with the following command:
```
java -cp bin Main
```
*Explanation: the `-cp bin` sets the `bin` directory to `classpath` where calls the `Main` class*

If you would like to load the input from the `input.txt` then simply add the `FILE` argument:

*Please mind that the `input.txt` should be in the root of the `java` directory*
```
java -cp bin Main FILE
```
