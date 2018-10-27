import pandas as pd
import html5lib
import json

df = pd.read_html("https://critique.gatech.edu/course.php?id=MATH3022", header=0, parse_dates=["GPA"])

print(df[0].to_json(orient='split'))
