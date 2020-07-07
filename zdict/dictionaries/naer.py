import json

from collections import defaultdict

from bs4 import BeautifulSoup

from zdict.dictionary import DictBase
from zdict.exceptions import QueryError, NotFoundError
from zdict.models import Record


class NaerDict(DictBase):
    API = "https://terms.naer.edu.tw/search?q={word}&field=ti&match=smart"

    @property
    def provider(self):
        return "NAER"

    @property
    def title(self):
        return "國家教育研究院"

    def _get_url(self, word) -> str:
        return self.API.format(word=word)

    def show(self, record: Record):
        content = json.loads(record.content)

        self.color.print("Query: {}".format(content["title"]), "lyellow")
        print()

        for index, source in enumerate(content["sources"]):
            self.color.print("{:-2d}. ".format(index + 1), end="")
            self.color.print(source, "lred")
            for en, zhtw in content["sources"][source]:
                if len(zhtw) < 30:
                    self.color.print(zhtw, "lindigo", indent=5, end=":  ")
                    print(en)
                else:
                    self.color.print(zhtw, "lindigo", indent=5)
                    self.color.print(en, indent=5)

    def query(self, word: str):
        try:
            content = self._get_raw(word, verify=False)
        except QueryError as exception:
            raise NotFoundError(exception.word)

        data = {"title": word, "sources": defaultdict(list)}
        soup = BeautifulSoup(content, "html.parser")
        for tr in soup.find_all("tr", {"class": "dash"}):
            source = (
                tr.find("td", attrs={"class": "sourceW"}).find("a").text
            ).strip()
            en = tr.find("td", attrs={"class": "ennameW"}).text.strip()
            zhtw = tr.find("td", attrs={"class": "zhtwnameW"}).text.strip()
            data["sources"][source].append((en, zhtw))

        if len(data["sources"]) == 0:
            raise NotFoundError(word)

        record = Record(
            word=word, content=json.dumps(data), source=self.provider
        )
        return record
