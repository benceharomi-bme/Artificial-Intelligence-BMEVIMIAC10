# Pallet loading problem
## The task
You can find the details of the task in the pdf
## Input
The input is multiple lines of text, with the individual elements being tab separated. The first line
contains the length and width of the store. The second line contains the number of pillars. The third
line contains the number of pallets. Then each subsequent row contains the position of a single pillar
then each subsequent row contains the length and width of a single pallet. So for the above example, the input
would look like this:
```
5 2
7
2
3 4
3 1
2 2
2 3
7 2
4 2
2 2
5 2
1 1
```
## Output
Output
Output the entire P matrix to the standard output, with values on each line separated by tabs. (A
common mistake is to have extra tabs at the end of the lines, and we will not accept solutions that make
this error).
```
1 1 1 1 4 4 6
1 1 1 1 4 4 6
2 2 3 3 4 4 7
2 2 5 5 4 4 7
2 2 5 5 4 4 7
```
