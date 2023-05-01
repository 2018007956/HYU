# Apriori

## Implementations
Command: python [executable file name] [minimum support (%)] [input file name] [output file name]
```
python apriori.py 5 input.txt output.txt
```

## Specification
The output file is outputted by overwriting the file, so when you run it again, you must reset the existing output file (or change the output file name).  
When Minimum support is set to 0, division by zero error appears in the confidence calculation part. 
I assumed that minimum support is not be zero.