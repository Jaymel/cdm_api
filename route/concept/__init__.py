from flask import Blueprint, jsonify, request
from app import db_reader

bp = Blueprint('concept', __name__, url_prefix='/')

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


def concept_query(table, concept_target):
    result = []

    sql = f'''
        select * 
        from (
            select distinct({table}.{concept_target}_concept_id) as concept_id
            from {table}
        ) as distinct_table
        inner join concept
        on distinct_table.concept_id = concept.concept_id;
    '''

    result = db_reader.db_search(sql)
    return result


@bp.route('/concept', methods=["GET"])
def index():
    table_keyword = request.args.get('table')
    concept_keyword = request.args.get('concept')
    page = int(request.args.get('page'))
    result = {}
    for table in concept_ids:
        result[table] = {}
        for concept_target in concept_ids[table]:
            rows = concept_query(table, concept_target)
            result[table][concept_target] = rows

    if table_keyword:
        if concept_keyword:
            result = result[table_keyword][concept_keyword]
        else:
            result = result[table_keyword]
    elif concept_keyword:
        for table in result:
            if result[table][concept_keyword]:
                result = result[table][concept_keyword]
                break
    if page is not None:
        page_result = []
        if isinstance(result, dict):
            for key in result.keys():
                if isinstance(result[key], dict):
                    for sub_key in result[key]:
                        for row in result[key][sub_key]:
                            page_result.append(row)
                else:
                    for row in result[key]:
                        page_result.append(row)
        else:
            for row in result:
                page_result.append(row)
        page = (page * 5) - 5
        result = page_result[page:min(len(page_result), page + 5)]
    return jsonify(result)

