# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_files", nargs = "+", 
    help = "Input files (.json) containing data for CSS generator")
args = parser.parse_args()


for file_name in args.input_files:

    if not file_name.endswith(".json"):
        print(file_name, "is not .json file")
        continue 

    data = None
    try:
        with open(file_name) as input_file:
            data = json.load(input_file)
    except:
        print (file_name, ": Malformed JSON file", sep = "")
        continue
        
    css = """
body {
  background: %s !important;
}
body > div a {
  color: %s !important;
}
.navbar-inverse {
  background: %s !important;
  color: %s !important;
  border-color: %s !important;
}
#bj-what-is-box {
  background: %s !important;
}
h1,
h2,
h3,
h4,
h5,
h6,
.h1,
.h2,
.h3,
.h4,
.h5,
.h6 {
  color: %s !important;
}
.btn-info, .btn-primary {
  background: %s !important;
  border-color: %s !important;
  color: %s !important;
}
.btn-success{
  background: %s !important;
  border-color: %s !important;
  color: %s !important;
}
.nav > li > a:hover,
.nav > li > a:focus {
  background-color: %s !important;
}
.alert-info {
  background-color: %s !important;;
  border-color: %s !important;
  color: %s !important;
}
.alert-info a {
  color: %s !important;
}
.alert-warning {
  background-color: %s;
  border-color: %s;
  color: %s;
}
.alert-warning a {
  color: %s !important;
}
""" % (
       data["pageBackgroundColor"], 
       data["linkFontColor"],
       data["menuBackgroundColor"],
       data["menuBorderColor"],
       data["menuLinkFontColor"],
       data["whatIsBoxBackgroundColor"],
       data["headlinesFontColor"],
       data["classicButtonBackgroundColor"],
       data["classicButtonBorderColor"],
       data["classicButtonFontColor"],
       data["successButtonBackgroundColor"],
       data["successButtonBorderColor"],
       data["successButtonFontColor"],
       data["menuLinkHoverBackgroundColor"],
       data["alertInfoBoxBackgroundColor"],
       data["alertInfoBoxBorderColor"],
       data["alertInfoBoxFontColor"],
       data["alertInfoLinkFontColor"],
       data["alertWarningBoxBackgroundColor"],
       data["alertWarningBoxBorderColor"],
       data["alertWarningBoxFontColor"],
       data["alertWarningLinkFontColor"]
)

    output_file_name = file_name[:-5]
    print(css, file=open(output_file_name + ".css", "w"))
    
