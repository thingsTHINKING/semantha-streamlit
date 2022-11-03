import json
import io
from typing import Dict, Optional, Tuple

import requests

from types import SimpleNamespace
from semantha.st.components.semantha_connection_exception import (
    SemanthaConnectionException,
)


def _build_headers_for_json_request(api_key) -> Dict[str, str]:
    __headers = {"Accept": "application/json", "Authorization": f"Bearer {api_key}"}
    return __headers


def _to_text_file(text: str):
    input_file = io.BytesIO(text.encode("utf-8"))
    input_file.name = "input.txt"
    return input_file


class Semantha:
    __server_base_url: str
    __api_key: str

    def __init__(
        self,
        server_base_url,
        api_key: Optional[str] = None,
    ):
        self.__server_base_url = server_base_url
        self.__api_key = api_key

    def compare_with_omd(
        self, input_0: str, input_1: str, domain: str
    ) -> Tuple[float, bool]:
        json_response = self.__get_references(input_0, input_1, domain)
        if hasattr(json_response, "references"):
            reference = json_response.pages[0].contents[0].paragraphs[0].references[0]
            if hasattr(reference, "hasOppositeMeaning"):
                contradictory = reference.hasOppositeMeaning
            else:
                contradictory = False
            similarity = float(json_response.references[0].similarity)
            return similarity, contradictory

    def __get_references(self, input_0, input_1, domain):
        url = f"{self.__server_base_url}/api/domains/{domain}/references"
        headers = _build_headers_for_json_request(self.__api_key)
        payload = {
            "file": _to_text_file(input_1),
            "referencedocument": _to_text_file(input_0),
            "similaritythreshold": str(0.01),
            "maxreferences": str(1),
            "withcontext": str(False),
        }
        response = requests.post(url, headers=headers, files=payload)
        if response.status_code != 200:
            raise SemanthaConnectionException(
                f"Unable to execute semantic compare using domain {domain}\n"
                f"1st input string was: {input_0}\n"
                f"2nd input string was: {input_1}\n"
                f"Status code is: {response.status_code}"
            )

        return json.loads(
            response.content.decode(), object_hook=lambda d: SimpleNamespace(**d)
        )
