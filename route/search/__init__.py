from flask import Blueprint, jsonify, request
from app import db_reader

bp = Blueprint('result', __name__, url_prefix='/')


concept_ids = {
    "person": [
        "gender",
        "race",
    ],
    "visit_occurrence": [
        "visit",
        "visit_type",
    ],
    "condition_occurrence": [
        "condition",
        "condition_type",
    ],
    "drug_exposure": [
        "drug",
        "drug_type",
        "drug_source"
    ],
    "death": [
        "death_type"
    ]
}


def search(table, columns=None, values=None, page=None):

    sql = f'''
        select {table}.*, concept.concept_name
        from {table}, concept
    '''

    for idx, concept_target in enumerate(concept_ids[table]):
        if idx:
            sql += f''' or {concept_target}_concept_id = concept.concept_id'''
        else:
            sql += f''' where {concept_target}_concept_id = concept.concept_id'''
    page_cnt = 0
    for idx, column in enumerate(columns):
        if column == "page":
            page_cnt = int(values[idx])
            continue
        sql += f''' and {column} = {values[idx]}'''
    if page_cnt:
        sql += f''' limit 10 offset {page_cnt * 10 - 10}'''
    sql += ";"
    print(sql)
    result = db_reader.db_search(sql)
    return result


@bp.route('/search/<table>', methods=["GET"])
def index(table):
    query_string = request.query_string.decode('utf-8')
    query_strings = query_string.split("&")
    columns = []
    values = []
    for query_string in query_strings:
        column, value = query_string.split("=")
        columns.append(column)
        values.append(value)
    result = search(table, columns, values)
    return jsonify(result)

