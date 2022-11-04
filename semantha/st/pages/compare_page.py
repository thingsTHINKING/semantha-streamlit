import streamlit as st

from semantha.st.components.compare import SemanticCompare

example_sentences = {
    "fruits": ["I like to eat apples.", "I fancy fruit."],
    "multi language": ["Bananen schmecken mir.", "I like banana."],
    "newspaper": ["The vehicle was too fast.", "The car was going at excessive speed."],
    "job": ["I work for Microsoft.", "My job is in a software company."],
    "opposite meaning": ["I got hired.", "I got fired."], 
    "opposite meaning 2": ["These apples are damn good.", "I hate these apples."]
}


class SemanticComparePage:
    def build(self):
        compare = SemanticCompare()
        compare.build_title()
        option = st.selectbox("Select Example", ["fruits", "multi language", "newspaper", "job", "opposite meaning", "opposite meaning 2"])
        compare.build_input(sentences=example_sentences[option])
