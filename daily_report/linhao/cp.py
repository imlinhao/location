#!/usr/bin/python
import os
print(os.path.dirname(__file__))
#os.system("xelatex -synctex=-1 -src-specials -interaction=nonstopmode "+os.path.dirname(__file__)+"/diss.tex")
os.system("xelatex -synctex=-1 -src-specials -interaction=nonstopmode diss.tex")

