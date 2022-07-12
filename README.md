# Transition-Based-Dependency-Parsing

**Transition-based dependency parsing**: is a fast and effective approach for dependency parsing. Traditionally, a transitionbased dependency parser processes an input sentence and predicts a sequence of parsing actions in a left-to-right manner.

*Transition-based parsing*  which architecture draws on shift-reduce parsing, a paradigm originally developed for analyzing programming languages. 
In transition-based parsing we’ll have a stack on which we build the parse, a buffer of tokens to be parsed, and a parser which takes actions on the parse via a predictor called an oracle

## Required libraries:
- python 3.7
- argparse

## Model details:

|     Training Sentences:    	|     3914     	|
|----------------------------	|--------------	|
|     Tokens                 	|     94084    	|
|     Số loại POS tags       	|     45       	|
|     Left-Arcs              	|     46061    	|
|     Right-Arcs             	|     44109    	|
|     Root-Arcs              	|     3914     	|

## Instructions for compiling code:
python main.py --corpus=wsj-clean.txt --pos=piper.txt

## Results returned:
- Display to the screen (cmd) or via file **piper.txt**

![image](https://user-images.githubusercontent.com/55480300/178409732-9dc90650-8c1c-4c60-b9bc-d6c80ff2cf65.png)

- File **piper.txt**

![image](https://user-images.githubusercontent.com/55480300/178409818-84f0fa37-3ef1-489d-a550-4fbc8267f77e.png)
