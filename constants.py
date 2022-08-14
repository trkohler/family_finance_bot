from envparse import env

env.read_envfile()
notion_secret = env("NOTION_SECRET")
telegram_token = env('TELEGRAM_TOKEN')
environment = env('BOT_ENV')
rapid_api_key = env('RAPID_API_KEY')
rapid_api_host = env('RAPID_API_HOST')

our_home_chat_id = -1001423120580
test_chat_id = -1001171091439

DATABASE_ID = "a27c68e4c1d8481c913b2d4fabefc4c9"

RAPID_API_URL = "https://currency-converter5.p.rapidapi.com/currency/convert"
MONOBANK_API_URL = "https://api.monobank.ua/bank/currency"

NOTION_URL_MAP = {
    "query_db": f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
    "retrieve_db_data": f"https://api.notion.com/v1/databases/{DATABASE_ID}",
}

types_of_spends = dict(
    rashodniki=dict(
        id="de702077-821a-4b59-9ab0-949ca954c4a6",
        title="Расходники",
        autoadd=True,
        period_map={
            1: 155,
            15: 155,
        },
        remain=True
    ),
    strannyi_rashody=dict(
        id="3e392471-bd4a-4cde-befb-e52e8f31b26d",
        title="Странные расходы",
        autoadd=True,
        period_map={
            1: 250,
            15: 250,
        },
        remain=True
    ),
    ekstrennyi_rashody=dict(
        id="7f39e4c2-db17-42d9-91c1-8c7a7be224f6",
        title="Экстренные расходы",
        autoadd=False,
        period_map=None,
        remain=False
    ),
    prihod=dict(
        id="8b88c40f-78be-4b44-a955-ea8365a70ae4",
        title="Приход",
        autoadd=False,
        period_map=None,
        remain=False
    ),
    prioritetnyi_rashody=dict(
        id="fb488835-f2fa-4246-bde3-7f9baea30005",
        title="Приоритетные расходы",
        autoadd=False,
        period_map=None,
        remain=False
    ),
    arenda=dict(
        id="278a679f-cde4-44aa-be5a-2876b67d080b",
        title="Аренда",
        autoadd=True,
        period_map={
            1: 1100,
        },
        remain=True
    ),
    is_sekonomlennogo=dict(
        id="b01d729c-6451-46ef-ab07-bcd0ad0fef27",
        title="Из сэкономленного",
        autoadd=False,
        period_map=None,
        remain=True
    ),
    ukrainian_commitment=dict(
        id="M?[|",
        title="Обязательства в Украине",
        period_map={
            1: 310,
        },
        remain=True
    )
)
