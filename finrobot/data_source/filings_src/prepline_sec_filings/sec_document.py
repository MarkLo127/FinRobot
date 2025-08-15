from functools import partial
import re
from typing import List, Optional, Iterable, Iterator, Any, Tuple
import sys

if sys.version_info < (3, 8):
    from typing_extensions import Final
else:
    from typing import Final

import numpy as np
import numpy.typing as npt
from sklearn.cluster import DBSCAN
from collections import defaultdict

from unstructured.cleaners.core import clean
from unstructured.documents.elements import (
    Text,
    ListItem,
    NarrativeText,
    Title,
    Element,
)
from unstructured.documents.html import HTMLDocument

from unstructured.nlp.partition import is_possible_title

# from src.prepline_sec_filings.title import is_possible_title
from finrobot.data_source.filings_src.prepline_sec_filings.sections import SECSection


VALID_FILING_TYPES: Final[List[str]] = [
    "10-K",
    "10-Q",
    "S-1",
    "10-K/A",
    "10-Q/A",
    "S-1/A",
]
REPORT_TYPES: Final[List[str]] = ["10-K", "10-Q", "10-K/A", "10-Q/A"]
S1_TYPES: Final[List[str]] = ["S-1", "S-1/A"]

ITEM_TITLE_RE = re.compile(r"(?i)item \d{1,3}(?:[a-z]|\([a-z]\))?(?:\.)?(?::)?")

# 注意(yuming)：clean_sec_text 是 clean 的部分清理器，
# 用於清理 SEC 申報文件中的一段文字。
clean_sec_text = partial(
    clean, extra_whitespace=True, dashes=True, trailing_punctuation=True
)


def _raise_for_invalid_filing_type(filing_type: Optional[str]):
    if not filing_type:
        raise ValueError("申報類型為空。")
    elif filing_type not in VALID_FILING_TYPES:
        raise ValueError(
            f"申報類型為 {filing_type}。預期為：{VALID_FILING_TYPES}"
        )


class SECDocument(HTMLDocument):
    filing_type = None

    def _filter_table_of_contents(self, elements: List[Text]) -> List[Text]:
        """使用關鍵字搜尋篩選掉目錄中不必要的元素。"""
        if self.filing_type in REPORT_TYPES:
            # 注意(yuming)：將目錄縮小為
            # 包含關鍵字「part i\b」的前兩個標題中的所有元素。
            start, end = None, None
            for i, element in enumerate(elements):
                if bool(re.match(r"(?i)part i\b", clean_sec_text(element.text))):
                    if start is None:
                        # 注意(yuming)：找到目錄部分的開頭。
                        start = i
                    else:
                        # 注意(yuming)：找到目錄部分的結尾。
                        end = i - 1
                        filtered_elements = elements[start:end]
                        return filtered_elements
        elif self.filing_type in S1_TYPES:
            # 注意(yuming)：將目錄縮小為
            # 包含關鍵字「prospectus」的第一對重複標題中的所有元素。
            title_indices = defaultdict(list)
            for i, element in enumerate(elements):
                clean_title_text = clean_sec_text(element.text).lower()
                title_indices[clean_title_text].append(i)
            duplicate_title_indices = {
                k: v for k, v in title_indices.items() if len(v) > 1
            }
            for title, indices in duplicate_title_indices.items():
                # 注意(yuming)：確保我們找到重複標題的配對。
                if "prospectus" in title and len(indices) == 2:
                    start = indices[0]
                    end = indices[1] - 1
                    filtered_elements = elements[start:end]
                    return filtered_elements
        # 注意(yuming)：可能有更好的方法來改善目錄，
        # 但現在如果找不到關鍵字，我們就傳回 []。
        return []

    def get_table_of_contents(self) -> HTMLDocument:
        """識別可能是目錄的文字部分。"""
        out_cls = self.__class__
        _raise_for_invalid_filing_type(self.filing_type)
        title_locs = to_sklearn_format(self.elements)
        if len(title_locs) == 0:
            return out_cls.from_elements([])
        # 注意(alan)：可能有辦法做到同樣的事情，而不需要為了
        # 將其轉換為 sklearn 格式而進行必要的轉換。我們只是在尋找密集排列的標題。
        res = DBSCAN(eps=6.0).fit_predict(title_locs)
        for i in range(res.max() + 1):
            idxs = cluster_num_to_indices(i, title_locs, res)
            cluster_elements: List[Text] = [self.elements[i] for i in idxs]
            if any(
                [
                    # TODO(alan)：也許可以將風險標題換成更通用的東西？不過我認為有
                    # 兩個標記會比較好。
                    is_risk_title(el.text, self.filing_type)
                    for el in cluster_elements
                    if isinstance(el, Title)
                ]
            ) and any(
                [
                    is_toc_title(el.text)
                    for el in cluster_elements
                    if isinstance(el, Title)
                ]
            ):
                return out_cls.from_elements(
                    self._filter_table_of_contents(cluster_elements)
                )
        return out_cls.from_elements(self._filter_table_of_contents(self.elements))

    def get_section_narrative_no_toc(self, section: SECSection) -> List[NarrativeText]:
        """在不使用目錄的情況下，識別屬於給定章節標題下的敘述性文字部分。"""
        _raise_for_invalid_filing_type(self.filing_type)
        # 注意(robinson) - 我們沒有跳過表格文字，因為風險敘述部分
        # 通常不包含任何表格，有時表格會用於
        # 標題格式化
        section_elements: List[NarrativeText] = list()
        in_section = False
        for element in self.elements:
            is_title = is_possible_title(element.text)
            if in_section:
                if is_title and is_item_title(element.text, self.filing_type):
                    if section_elements:
                        return section_elements
                    else:
                        in_section = False
                elif isinstance(element, NarrativeText) or isinstance(
                    element, ListItem
                ):
                    section_elements.append(element)

            if is_title and is_section_elem(section, element, self.filing_type):
                in_section = True

        return section_elements

    def _get_toc_sections(
        self, section: SECSection, toc: HTMLDocument
    ) -> Tuple[Text, Text]:
        """識別目錄中給定章節標題下的章節標題和下一個章節標題"""
        # 注意(yuming)：匹配的章節和匹配章節之後的章節
        # 可以被視為尋找目錄下方匹配內容的佔位符。
        section_toc = first(
            el for el in toc.elements if is_section_elem(section, el, self.filing_type)
        )
        if section_toc is None:
            # 注意(yuming)：無法在目錄中識別該章節
            return (None, None)

        after_section_toc = toc.after_element(section_toc)
        next_section_toc = first(
            el
            for el in after_section_toc.elements
            if not is_section_elem(section, el, self.filing_type)
        )
        if next_section_toc is None:
            # 注意(yuming)：無法識別目錄中的下一個章節標題，
            # 將導致無法找到章節的結尾
            return (section_toc, None)
        return (section_toc, next_section_toc)

    def get_section_narrative(self, section: SECSection) -> List[NarrativeText]:
        """識別屬於給定章節標題下的敘述性文字部分"""
        _raise_for_invalid_filing_type(self.filing_type)
        # 注意(robinson) - 我們沒有跳過表格文字，因為風險敘述部分
        # 通常不包含任何表格，有時表格會用於
        # 標題格式化
        toc = self.get_table_of_contents()
        if not toc.pages:
            return self.get_section_narrative_no_toc(section)

        # 注意(yuming)：section_toc 是目錄中的章節標題，
        # next_section_toc 是目錄中 section_toc 之後的章節標題
        section_toc, next_section_toc = self._get_toc_sections(section, toc)
        if section_toc is None:
            # 注意(yuming)：在目錄中找不到章節標題
            return []

        # 注意(yuming)：我們使用 next_section_toc 之後的文件而不是 toc 之後的文件
        # 來解決目錄抓取太多元素的問題，
        # 方法是在目錄中匹配的章節之後開始解析
        doc_after_section_toc = self.after_element(
            next_section_toc if next_section_toc else section_toc
        )
        # 注意(yuming)：將 section_toc 映射到目錄之後的章節標題
        # 以找到章節的開頭
        section_start_element = get_element_by_title(
            reversed(doc_after_section_toc.elements), section_toc.text, self.filing_type
        )
        if section_start_element is None:
            return []
        doc_after_section_heading = self.after_element(section_start_element)

        # 注意(yuming)：根據
        # 報告申報的結構或在目錄中找不到章節標題，檢查 section_toc 是否為目錄中的最後一個章節。
        # 傳回下一個標題元素之前的所有內容
        # 以避免傳回整個文件的最壞情況。
        if self._is_last_section_in_report(section, toc) or next_section_toc is None:
            # 傳回文件中 section_start_element 之後的所有內容
            return get_narrative_texts(doc_after_section_heading, up_to_next_title=True)

        # 注意(yuming)：將 next_section_toc 映射到目錄之後的章節標題
        # 以找到下一個章節的開頭，這也是我們想要的章節的結尾
        section_end_element = get_element_by_title(
            doc_after_section_heading.elements, next_section_toc.text, self.filing_type
        )

        if section_end_element is None:
            # 注意(yuming)：傳回下一個標題元素之前的所有內容
            # 以避免傳回整個文件的最壞情況。
            return get_narrative_texts(doc_after_section_heading, up_to_next_title=True)

        return get_narrative_texts(
            doc_after_section_heading.before_element(section_end_element)
        )

    def get_risk_narrative(self) -> List[NarrativeText]:
        """識別「風險」標題下的敘述性文字部分"""
        return self.get_section_narrative(SECSection.RISK_FACTORS)

    def doc_after_cleaners(
        self, skip_headers_and_footers=False, skip_table_text=False, inplace=False
    ) -> HTMLDocument:
        new_doc = super().doc_after_cleaners(
            skip_headers_and_footers, skip_table_text, inplace
        )
        if not inplace:
            # 注意(alan)：複製 filing_type，因為此屬性不在基底類別中
            new_doc.filing_type = self.filing_type
        return new_doc

    def _read_xml(self, content):
        super()._read_xml(content)
        # 注意(alan)：從 xml 取得申報類型，因為這與基底類別無關。
        type_tag = self.document_tree.find(".//type")
        if type_tag is not None:
            self.filing_type = type_tag.text.strip()
        return self.document_tree

    def _is_last_section_in_report(
        self, section: SECSection, toc: HTMLDocument
    ) -> bool:
        """檢查該章節是否為報告類型申報的目錄中的最後一個章節。"""
        # 注意(yuming)：此方法假設該章節已存在於目錄中。
        if self.filing_type in ["10-K", "10-K/A"]:
            # 嘗試取得 FORM_SUMMARY 作為最後一個章節，否則嘗試取得 EXHIBITS。
            if section == SECSection.FORM_SUMMARY:
                return True
            if section == SECSection.EXHIBITS:
                form_summary_section = first(
                    el
                    for el in toc.elements
                    if is_section_elem(SECSection.FORM_SUMMARY, el, self.filing_type)
                )
                # 如果 FORM_SUMMARY 不在目錄中，則最後一個章節是 EXHIBITS
                if form_summary_section is None:
                    return True
        if self.filing_type in ["10-Q", "10-Q/A"]:
            # 嘗試取得 EXHIBITS 作為最後一個章節。
            if section == SECSection.EXHIBITS:
                return True
        return False


def get_narrative_texts(
    doc: HTMLDocument, up_to_next_title: Optional[bool] = False
) -> List[Text]:
    """從文件中傳回 NarrativeText 或 ListItem 的清單，
    可選擇只傳回下一個 Title 元素之前的敘述性文字。"""
    if up_to_next_title:
        narrative_texts = []
        for el in doc.elements:
            if isinstance(el, NarrativeText) or isinstance(el, ListItem):
                narrative_texts.append(el)
            else:
                break
        return narrative_texts
    else:
        return [
            el
            for el in doc.elements
            if isinstance(el, NarrativeText) or isinstance(el, ListItem)
        ]


def is_section_elem(
    section: SECSection, elem: Text, filing_type: Optional[str]
) -> bool:
    """檢查文字元素是否符合指定申報類型的章節標題"""
    _raise_for_invalid_filing_type(filing_type)
    if section is SECSection.RISK_FACTORS:
        return is_risk_title(elem.text, filing_type=filing_type)
    else:

        def _is_matching_section_pattern(text):
            return bool(
                re.search(section.pattern, clean_sec_text(text, lowercase=True))
            )

        if filing_type in REPORT_TYPES:
            return _is_matching_section_pattern(
                remove_item_from_section_text(elem.text)
            )
        else:
            return _is_matching_section_pattern(elem.text)


def is_item_title(title: str, filing_type: Optional[str]) -> bool:
    """判斷標題是否對應於項目標題。"""
    if filing_type in REPORT_TYPES:
        return is_10k_item_title(title)
    elif filing_type in S1_TYPES:
        return is_s1_section_title(title)
    return False


def is_risk_title(title: str, filing_type: Optional[str]) -> bool:
    """檢查標題是否符合風險標題的模式。"""
    if filing_type in REPORT_TYPES:
        return is_10k_risk_title(clean_sec_text(title, lowercase=True))
    elif filing_type in S1_TYPES:
        return is_s1_risk_title(clean_sec_text(title, lowercase=True))
    return False


def is_toc_title(title: str) -> bool:
    """檢查標題是否符合目錄的模式。"""
    clean_title = clean_sec_text(title, lowercase=True)
    return (clean_title == "table of contents") or (clean_title == "index")


def is_10k_item_title(title: str) -> bool:
    """判斷標題是否對應於 10-K 項目標題。"""
    return ITEM_TITLE_RE.match(clean_sec_text(title, lowercase=True)) is not None


def is_10k_risk_title(title: str) -> bool:
    """檢查標題是否符合風險標題的模式。"""
    return ("1a" in title.lower() or "risk factors" in title.lower()) and not (
        "summary" in title.lower()
    )


def is_s1_section_title(title: str) -> bool:
    """判斷標題是否對應於章節標題。"""
    return title.strip().isupper()


def is_s1_risk_title(title: str) -> bool:
    """檢查標題是否符合風險標題的模式。"""
    return title.strip().lower() == "risk factors"


def to_sklearn_format(elements: List[Element]) -> npt.NDArray[np.float32]:
    """叢集的輸入必須是歐幾里得空間中的位置，因此我們需要將
    元素序列中標題的位置解釋為一維空間中的位置
    """
    is_title: npt.NDArray[np.bool_] = np.array(
        [is_possible_title(el.text) for el in elements][: len(elements)], dtype=bool
    )
    title_locs = np.arange(len(is_title)).astype(np.float32)[is_title].reshape(-1, 1)
    return title_locs


def cluster_num_to_indices(
    num: int, elem_idxs: npt.NDArray[np.float32], res: npt.NDArray[np.int_]
) -> List[int]:
    """請記住，叢集的輸入是元素清單中的索引，解釋為
    一維空間中的位置，此函式會傳回屬於
    具有給定編號的叢集的元素的原始索引。
    """
    idxs = elem_idxs[res == num].astype(int).flatten().tolist()
    return idxs


def first(it: Iterable) -> Any:
    """從迭代器中取得第一個項目。"""
    try:
        out = next(iter(it))
    except StopIteration:
        out = None
    return out


def match_s1_toc_title_to_section(text: str, title: str) -> bool:
    """將目錄中的 S-1 樣式標題與文件
    本文中的相關標題進行比對"""
    return text == title


def match_10k_toc_title_to_section(text: str, title: str) -> bool:
    """將目錄中的 10-K 樣式標題與文件
    本文中的相關標題進行比對"""
    if re.match(ITEM_TITLE_RE, title):
        return text.startswith(title)
    else:
        text = remove_item_from_section_text(text)
        return text.startswith(title)


def remove_item_from_section_text(text: str) -> str:
    """從 10-K/Q 表格的章節文字中移除「項目」標題，以準備其他比對
    技巧"""
    return re.sub(ITEM_TITLE_RE, "", text).strip()


def get_element_by_title(
    elements: Iterator[Element],
    title: str,
    filing_type: Optional[str],
) -> Optional[Element]:
    """從元素清單中取得文字約略符合標題的元素"""
    _raise_for_invalid_filing_type(filing_type)
    if filing_type in REPORT_TYPES:
        match = match_10k_toc_title_to_section
    elif filing_type in S1_TYPES:
        match = match_s1_toc_title_to_section
    return first(
        el
        for el in elements
        if match(
            clean_sec_text(el.text, lowercase=True),
            clean_sec_text(title, lowercase=True),
        )
    )