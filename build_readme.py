from python_graphql_client import GraphqlClient
import feedparser
import httpx
import json
import pathlib
import re
import os
import datetime

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")


TOKEN = os.environ.get("GH_TOKEN", "")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)

def formatGMTime(timestamp):
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    dateStr = datetime.datetime.strptime(timestamp, GMT_FORMAT) + datetime.timedelta(hours=8)
    return dateStr.date()


def fetch_code_time():
    return httpx.get(
        "https://gist.github.com/fipped/20c85123b212bf4aff9b1d3ce176dd0a/raw/"
    )


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    code_time_text = "\n```text\n"+fetch_code_time().text+"\n```\n"
    rewritten = replace_chunk(readme_contents, "code_time", code_time_text)
    readme.open("w").write(rewritten)
