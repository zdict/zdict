import json
import requests

from collections import defaultdict

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import NotFoundError
from zdict.models import Record


class ApcDict(DictBase):
    BASE_URL = "https://e-dictionary.apc.gov.tw"

    # To get the result of APC online dictionary
    # We have to send a POST request to the POST_API first
    # (with the word we want to query in the JSON payload)
    # Then, the webpage will save result in the cookies
    # we use the cookies to request the API with GET
    # It will shows the result.
    # Then, we parse the webpage.
    POST_API = "{}/index.aspx/_crossTribes".format(BASE_URL)
    API = "{}/search/list.htm".format(BASE_URL)

    '''
    # Ref:
    #   http://ilrdc.tw/research/athousand/area16.php
    #   原住民族語言研究中心 - 16族族語學習詞表
    NOT_FOUND_WORD_INDIGENOUS = [
        "awaay",  # 南勢/秀姑巒/海岸/馬蘭/恆春阿美語
        "ungat",  # 賽考利克/澤敖/萬大/宜蘭澤敖利泰雅語
        "ukas",  # 汶水泰雅語
        "uka",  # 四季泰雅語
        "neka",  # 東/北/中/南排灣語
        "uka",  # 卓群/卡群/丹群/巒群/郡群布農語
        "uniyan",  # 南王/知本/初鹿/建和卑南語
        "iniyan",  # 知本/建和卑南語
        "kadrwa",  # 東/霧台魯凱語
        "kadruwa",  # 大武魯凱語
        "kadrowa",  # 多納魯凱語
        "tédra",  # 茂林魯凱語
        "akaodho",  # 萬山魯凱語
        "uk'a",  # 鄒語
        "'okay",  # 賽夏語
        "'oka'",  # 賽夏語
        "'inoka'",  # 賽夏語
        "abo",  # 雅美語
        "uka",  # 邵語
        "mai",  # 噶瑪蘭語
        "ini",  # 太魯閣語
        "ungat",  # 太魯閣語
        "nai'",  # 撒奇萊雅語
        "ungac",  # 都達語 (賽德克語)
        "uka",  # 都達語 (賽德克語)
        "ini",  # 德固達雅語 (賽德克語)
        "ungac",  # 德路固語 (賽德克語)
        "ungat",  # 德路固語 (賽德克語)
        "uka'a",  # 拉阿魯哇語
        "'akia",  # 卡那卡那富語
    ]
    '''

    @property
    def provider(self):
        return "apc"

    @property
    def title(self):
        return "原住民族委員會 - 原住民族語言線上詞典"

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        self.color.print("{}".format(content["title"]), "lyellow")
        print()

        self.color.print("精確搜尋結果", "lmagenta")
        for index, source in enumerate(content["exact_sources"]):
            self.color.print("{:-2d}. ".format(index + 1), end="")
            self.color.print(source, "lred", end=": ")
            self.color.print(
                content["exact_sources"][source]["title"],
                "lindigo",
            )
            for i, d in enumerate(content["exact_sources"][source]["defs"]):
                self.color.print("{i:-2d}. {d}".format(i=i + 1, d=d), indent=4)

            self.color.print("detail: ", "indigo", end="", indent=4)
            self.color.print(content["exact_sources"][source]["link"], "white")
            print()
        if not content["exact_sources"]:
            print()
            self.color.print("無精確搜尋結果", "green")
            print()

        self.color.print("模糊搜尋結果", "lmagenta")
        for index, source in enumerate(content["fuzzy_sources"]):
            self.color.print("{:-2d}. ".format(index + 1), end="")
            self.color.print(source, "red")

            for word in content["fuzzy_sources"][source]:
                self.color.print(word["title"], "lindigo", indent=5)
                for i, d in enumerate(word["defs"]):
                    self.color.print(
                        "{i:-2d}. {d}".format(i=i + 1, d=d),
                        indent=6,
                    )
            print()
        if not content["fuzzy_sources"]:
            print()
            self.color.print("無模糊搜尋結果", "green")
            print()

    def query(self, word: str):
        r = requests.post(
            self.POST_API,
            json={
                "c": "1",
                "t": "all",
                "q": word,
            },
        )
        content = self._get_raw(word, cookies=r.cookies)

        data = {
            "title": word,
            "exact_sources": defaultdict(list),
            "fuzzy_sources": defaultdict(list),
        }
        soup = BeautifulSoup(content, "html.parser")

        # Exact matching
        exact = soup.find(id="accordion_cross")
        if exact:
            for div in exact.find_all("div", {"class": "panel"}):
                title = div.find("div", {"class": "title"}).find("a").text
                defs = [
                    div.find("strong", {"class": "word"})
                    .find_all("span")[-1]
                    .text.strip()
                ]
                source = div.find("strong", {"class": "race"}).text

                for i in div.find_all("li")[1:]:
                    d = i.find("strong", {"class": "word"})
                    if d:
                        defs.append(d.find_all("span")[-1].text.strip())

                link = (
                    self.BASE_URL
                    + div.find("a", {"class": "btn-more"})["href"]
                )
                data["exact_sources"][source] = {
                    "title": title,
                    "defs": defs,
                    "link": link,
                }

        # Fuzzy matching
        fuzzy = soup.find(id="accordion")
        if fuzzy:
            for div in fuzzy.find_all("div", {"class": "panel"}):
                title = div.find("div", {"class": "title"}).find("a").text
                defs = [
                    div.find("strong", {"class": "word"})
                    .find_all("span")[-1]
                    .text.strip()
                ]
                source = div.find("strong", {"class": "race"}).text

                for i in div.find_all("li")[1:]:
                    d = i.find("strong", {"class": "word"})
                    if d:
                        defs.append(d.find_all("span")[-1].text.strip())

                link = (
                    self.BASE_URL
                    + div.find("div", {"class": "title"}).find("a")["href"]
                )
                data["fuzzy_sources"][source].append(
                    {"title": title, "defs": defs, "link": link}
                )

        if not exact and not fuzzy:
            raise NotFoundError(word)

        record = Record(
            word=word,
            content=json.dumps(data),
            source=self.provider,
        )
        return record
