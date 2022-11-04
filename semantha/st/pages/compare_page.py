import streamlit as st

from semantha.st.components.compare import SemanticCompare

example_sentences = {
    "newspaper": ["The vehicle was too fast.", "The car was going at excessive speed."],
    "fruits": ["I like to eat apples.", "I fancy fruit."],
    "multi language": ["Bananen schmecken mir.", "I like banana."],
    "job": ["I work for Microsoft.", "My job is in a software company."]
}


class SemanticComparePage:
    def build(self):
        option = st.selectbox("Select Example", ["fruits", "multi language"])
        compare = SemanticCompare(sentences=example_sentences[option])
        compare.build()
