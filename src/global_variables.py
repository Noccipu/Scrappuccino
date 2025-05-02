import streamlit as st
import requests
import os
import json
import networkx as nx
from streamlit.components.v1 import html
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

DEFAULT_DEPTH = 3
MAX_DEPTH = 10
DEFAULT_QUANTITY = 10
MAX_QUANTITY = 50
DEFAULT_INPUT = "Passive Acoustic Mapping"

# Link of the 'Look for' choices according to the 'From' choice
optionsLookFor = {
    "Paper"     : ["Papers", "Authors", "Fields", "Journals"],
    "Author"    : ["Papers", "Authors", "Journals"],
    "Field"     : ["Papers", "Authors"],
    "Journal"   : ["Papers"]
}

# Link of the parameters according to the 'Look for' and 'From' choices
optionsParameters = {
    ("Paper", "Papers")     : ["Input type", "Direction", "Year", "Quantity", "Tree depth"],
    ("Paper", "Authors")    : ["Input type", "All Authors"],
    ("Paper", "Fields")     : ["Input type", "Oui"],
    ("Field", "Papers")     : ["Input type", "Year", "Quantity", "Tree depth<"]
}

# Link of the 'Input type' according to the 'From choice'
optionsInputType = {
    "Paper"     : ["Name", "doi"],
    "Author"    : ["Name and First name"],
    "Field"     : ["Name"],
    "Journal"   : ["Name"]
}

userSearchConfig = {}