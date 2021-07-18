from my_types import NotionPage, ParentDatabase
import typing
from datetime import datetime, timedelta

from notion_client import Client

from constants import init_headers, DATABASE_ID, notion_secret

headers = init_headers()
notion = Client(auth=notion_secret)
period_starts_days = [5, 15, 23]


def make_bullet_points(*args: typing.List[str]) -> typing.List[typing.Dict[str, typing.Any]]:
    """
    make from strings bullet point objects
    :param args:
    :return:
    """
    res = []
    for arg in args:
        d = {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item":
                {
                    "text": [{
                        "type": "text",
                        "text": {
                            "content": str(arg),
                        }
                    }]
                }
        }
        res.append(d)
    return res


def notion_page_builder(
        title: str,
        tag_id: str,
        sum_of_spend: int,
        remain_value: int,
        remain_flag: typing.Optional[bool],
        bullets: typing.Optional[typing.List[str]],
        spend: typing.Optional[bool] = True, 
) -> typing.Dict[str, typing.Any]:
    return NotionPage(
        parent=ParentDatabase(database_id=DATABASE_ID)._asdict(),
        properties={
            "Name": {
                "type": 'title',
                "title": [
                    {
                        'plain_text': title,
                        'text': {
                            'content': title,
                            'link': None},
                        'type': 'text'
                    }
                ]
            },
            "Tags": {
                'multi_select': [{
                    'id': tag_id,
                }],
                'type': 'multi_select'
            },
            "Date": {"date": {"start": datetime.now().isoformat()}, 'type': 'date'},
            "Spent": {'number': -sum_of_spend if spend else sum_of_spend, 'type': 'number'},
            "For current period": {'number': remain_value, 'type': 'number'} if remain_flag else None,
        },
        children=make_bullet_points(*bullets) if bullets else []
    )._asdict()


def prepare_filter_tags(tag_name: str):
    filter_by_tag = dict(property="Tags", multi_select=dict(contains=tag_name))
    return filter_by_tag


def prepare_filter_date(date_for_filter: datetime):
    filter_by_date = dict(
        property="Date",
        date=dict(
            after=date_for_filter.isoformat()
        )
    )
    return filter_by_date


def prepare_sort() -> typing.List[typing.Dict[str, str]]:
    sort = dict(property="Date", timestamp="created_time", direction="descending")
    return [sort]


def prepare_query_kwargs(tag_name: str):
    query_kwargs = dict(
        database_id=DATABASE_ID,
        filter=prepare_filter_tags(tag_name),
        sorts=prepare_sort(),
    )
    return query_kwargs


def check_if_card_exist(tag_name: str, date_for_filter: datetime) -> typing.Optional[dict]:
    res = notion.databases.query(
        database_id=DATABASE_ID,
        filter={"and": [prepare_filter_tags(tag_name), prepare_filter_date(date_for_filter)]},
        sorts=prepare_sort(),
    )
    if len(res["results"]) > 0:
        card_for_edit = res["results"][0]
        return card_for_edit
    else:
        return None


def update_card(card: typing.Dict[str, typing.Any]):
    pass


def get_remain_from_res(res: typing.Dict[str, typing.Any]) -> int:
    result = 0
    remain = True
    try:
        result = int(res["results"][0]["properties"]["Remain"]["formula"]["number"])
    except KeyError:
        remain = False

    return result, remain


def main():
    pass


if __name__ == "__main__":
    main()
