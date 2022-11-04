from typing import Tuple, Optional

import streamlit as st
from semantha.st.components.semantha import Semantha


class SemanticCompare:

    __semantha_connector: Semantha
    __compare_domain: str
    
    __first_text = ""
    __second_text = ""

    def __init__(
        self,
        server_url: str = st.secrets["semantha"]["server_url"],
        api_key: str = st.secrets["semantha"]["api_key"],
        domain: str = st.secrets["semantha"]["domain"]
        
    ):
        self.__semantha_connector = Semantha(server_url, api_key)
        self.__compare_domain = domain

    def build(self):
        self.build_title()
        self.build_input()

    def build_title(self, md_title="Semantic Comparison", description="Directly compare two sentences by entering them below. The sentences will be compared using semantha's® semantic model."):
        st.title(md_title)
        st.write(description)
        
    def build_input(
        self, label_1="Sentence I", label_2="Sentence II", button="⇆ Compare", spinner_msg = "Wait for it...", 
        sentences: Optional[Tuple[str, str]] = ["", ""]
    ):
        self.__first_text = sentences[0]
        self.__second_text = sentences[1]
        input_0 = st.text_input(label=label_1, value=self.__first_text)
        input_1 = st.text_input(label=label_2, value=self.__second_text)
        _, col, _ = st.columns(3)
        if col.button(button, key="scbutton"):
            with st.spinner(spinner_msg):
                self.compute_and_display_similarity(input_0, input_1)

    def compute_and_display_similarity(self, input_0: str, input_1: str):
        similarity, contradictory = self.__semantha_connector.compare_with_omd(
            input_0, input_1, self.__compare_domain
        )
        sim = int(round(similarity, 2) * 100)

        if sim > 99:
            if contradictory:
                st.warning("⚠️ Texts are identical but have OPPOSITE meaning.")
            else:
                st.success("🕺 Texts are identical")
        elif 99 >= sim > 60:
            if contradictory:
                st.warning("⚠️ Texts are similar but have OPPOSITE meaning.")
            else:
                st.success("🕺 Texts are similar")
        elif 60 >= sim > 40:
            st.warning("🙋 Small connection between sentences.")
        elif sim <= 40:
            st.error("🙅‍♂️ Not similar.")
