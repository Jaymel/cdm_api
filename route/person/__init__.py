from flask import Blueprint, jsonify
from app import db_reader

bp = Blueprint('person', __name__, url_prefix='/')


def person_query(concept_id):
    if concept_id == "all":
        sql = '''
            select count(*)
            from person;
        '''
        result = db_reader.db_search(sql)
    elif concept_id == "ethnicity":
        # 인종에 대한 concept_id는 전부 0이다.
        # concept 테이블에서 concept_id = 0으로 조회 결과
        # No matching concept라고 한다.
        # 따라서 부득이하게 ethnicity_source_value로 조회하도록 한다.
        sql = '''
            select ethnicity_source_value, count(*)
            from person
            group by ethnicity_source_value;
        '''
        result = db_reader.db_search(sql)
    elif concept_id == "death":
        sql = '''
            select count(*)
            from person
            inner join death
            on person.person_id = death.person_id;
        '''
        result = db_reader.db_search(sql)
    else:
        sql = f'''
            select concept.concept_name, count(*)
            from person
            inner join concept
            on person.{concept_id}_concept_id = concept.concept_id
            group by concept.concept_name; 
        '''
        result = db_reader.db_search(sql)
    return result


@bp.route('/person/<concept_id>', methods=["GET"])
def index(concept_id):
    result = person_query(concept_id)
    return jsonify(result)
