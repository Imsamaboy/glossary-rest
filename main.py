from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel

app = FastAPI(
    title="Tech Terms API",
    description="API для управления техническими терминами и их определениями",
    version="1.0.0"
)


class TermCreate(BaseModel):
    """
    Модель для создания нового термина
    """
    title: str
    definition: str
    source_link: Optional[str] = None


class TermUpdate(BaseModel):
    """
    Модель для обновления существующего термина
    """
    definition: Optional[str] = None
    source_link: Optional[str] = None


# Словарь с терминологией: ключ - keyword, значение - Term
terms_db: Dict[str, TermCreate] = {
    "fps": TermCreate(
        title="fps",
        definition="Количество сменяемых на интерфейсе кадров за одну секунду.",
        source_link="https://developer.mozilla.org/ru/docs/Glossary/FPS"
    ),
    "fcp": TermCreate(
        title="fcp",
        definition="Время, за которое пользователь увидит какое-то содержимое веб-страницы, например, текст или картинку.",
        source_link="https://developer.mozilla.org/ru/docs/Glossary/First_contentful_paint"
    ),
    "fid": TermCreate(
        title="fid",
        definition="Время ожидания до первого взаимодействия с контентом.",
        source_link="https://habr.com/ru/companies/timeweb/articles/714280/"
    ),
    "tbt": TermCreate(
        title="tbt",
        definition="Общее количество времени, когда основной поток заблокирован достаточно долго, чтобы реагировать на взаимодействия пользователя.",
        source_link="https://habr.com/ru/companies/domclick/articles/549098/"
    ),
    "cls": TermCreate(
        title="cls",
        definition="Какое количество содержимого во viewport двигалось во время загрузки страницы.",
        source_link="https://habr.com/ru/companies/domclick/articles/549098/"
    ),
}


@app.get("/", response_model=Dict[str, TermCreate], summary="Получить все термины")
async def list_all_terms():
    """
    Возвращает список всех технических терминов в базе данных.
    """
    return terms_db


@app.get("/terms/{keyword}", response_model=TermCreate, summary="Получить термин по ключу")
async def get_term_by_keyword(keyword: str):
    """
    Получить термин по его ключевому слову.

    - **keyword**: ключ термина
    """
    term = terms_db.get(keyword)
    if not term:
        raise HTTPException(status_code=404, detail=f"Термин '{keyword}' не найден")
    return term


@app.post("/terms/{keyword}", response_model=TermCreate, summary="Создать новый термин")
async def create_new_term(keyword: str, term: TermCreate):
    """
    Добавить новый термин в базу данных.

    - **keyword**: уникальный идентификатор термина
    - **term**: объект с описанием термина
    """
    if keyword in terms_db:
        raise HTTPException(status_code=400, detail=f"Термин '{keyword}' уже существует")
    terms_db[keyword] = term
    return term


@app.put("/terms/{keyword}", response_model=TermCreate, summary="Обновить термин")
async def update_existing_term(keyword: str, term_update: TermUpdate):
    """
    Обновляет существующий термин.

    - **keyword**: ключ термина
    - **term_update**: объект с новыми данными термина
    """
    term = terms_db.get(keyword)
    if not term:
        raise HTTPException(status_code=404, detail=f"Термин '{keyword}' не найден")

    if term_update.definition is not None:
        term.definition = term_update.definition
    if term_update.source_link is not None:
        term.source_link = term_update.source_link

    terms_db[keyword] = term
    return term


@app.delete("/terms/{keyword}", response_model=TermCreate, summary="Удалить термин")
async def delete_term_by_keyword(keyword: str):
    """
    Удаляет термин из базы данных по ключевому слову.

    - **keyword**: ключ термина
    """
    term = terms_db.pop(keyword, None)
    if not term:
        raise HTTPException(status_code=404, detail=f"Термин '{keyword}' не найден")
    return term
