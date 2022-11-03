from typing import Tuple, Optional

import streamlit as st
from semantha.st.components.semantha import Semantha


class SemanticCompare:
    def __init__(
        self,
        server_url: str = st.secrets["semantha"]["server_url"],
        api_key: str = st.secrets["semantha"]["api_key"],
        domain: str = st.secrets["semantha"]["domain"],
        sentences: Optional[Tuple[str, str]] = ["", ""],
    ):
        self._semantha_connector = Semantha(server_url, api_key)
        self.__compare_domain = domain
        self.__first_text = sentences[0]
        self.__second_text = sentences[1]

    def build(self, md_title = "## Direct Compare", description = "Directly compare two texts by entering them below. The texts will be compared using semantha's® semantic model."):
        st.markdown(md_title)
        st.write(description)
        self.build_input()

    def build_input(
        self, label_1="Input I", label_2="Input II", button="⇆ Semantic Compare", spinner_msg = "Wait for it..."
    ):
        input_0 = st.text_input(label=label_1, value=self.__first_text)
        input_1 = st.text_input(label=label_2, value=self.__second_text)
        _, col, _ = st.columns(3)
        if col.button(button, key="scbutton"):
            with st.spinner(spinner_msg):
                self.compute_and_display_similarity(input_0, input_1)

    def compute_and_display_similarity(self, input_0: str, input_1: str):
        similarity, contradictory = self._semantha_connector.compare_with_omd(
            input_0, input_1, self.__compare_domain
        )
        sim = int(round(similarity, 2) * 100)
        additional_text = " but opposite meaning." if contradictory else "."

        if sim > 99:
            st.markdown(f"### 🦸🏼‍♀️ IDENTICAL{additional_text}")
        elif sim <= 99 and sim > 60:
            st.markdown(f"### 🦸🏼‍♀️ SIMILAR{additional_text}")
        elif sim <= 60 and sim > 40:
            st.markdown("### 🦸🏼‍♀️ Small connection between sentences")
        elif sim <= 40:
            st.markdown("### 🦸🏼‍♀️ Not similar")
