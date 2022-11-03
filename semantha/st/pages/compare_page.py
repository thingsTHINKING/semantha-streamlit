import streamlit as st

from semantha.st.components.compare import SemanticCompare

example_sentences = {
    "fruits": ["I like to eat apples.", "I fancy fruit."],
    "multi language": ["Bananen schmecken mir.", "I like banana."],
}


class SemanticComparePage:
    def build(self):
        option = st.selectbox("Select Example", ["fruits", "multi language"])
        compare = SemanticCompare(sentences=example_sentences[option])
        compare.build()
