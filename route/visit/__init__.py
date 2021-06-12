from flask import Blueprint, jsonify
from app import db_reader

bp = Blueprint('visit', __name__, url_prefix='/')
correct_querys = ["all", "gender", "age", "race", "ethnicity"]


def visit_query(concept_id):
    if concept_id == "all":
        sql = '''
            select concept.concept_name, count(*)
            from visit_occurrence
            inner join concept
            on visit_occurrence.visit_concept_id = concept.concept_id
            group by concept_name;
        '''
        result = db_reader.db_search(sql)
    elif concept_id == "ethnicity":
        sql = '''
            select ethnicity_source_value, count(*)
            from visit_occurrence
            inner join person
            on visit_occurrence.person_id = person.person_id
            group by person.ethnicity_source_value;
        '''
        result = db_reader.db_search(sql)
    elif concept_id == "age":
        sql = '''
            select extract(
                year from age(
                    visit_occurrence.visit_start_datetime::date, 
                    person.birth_datetime::date
                )
            ), count(*)
            from visit_occurrence
            inner join person
            on visit_occurrence.person_id = person.person_id
            group by extract(
                year from age(
                    visit_occurrence.visit_start_datetime::date, 
                    person.birth_datetime::date
                )
            );
        '''
        result = {}
        rows = db_reader.db_search(sql)
        for row in rows:
            age = int(row[0])
            count = row[1]
            age_range = int(age / 10) * 10
            if age_range not in result:
                result[age_range] = 0
            result[age_range] += count
    else:
        sql = f'''
            select concept.concept_name, count(*)
            from visit_occurrence
            inner join person
            on visit_occurrence.person_id = person.person_id
            inner join concept
            on person.{concept_id}_concept_id = concept.concept_id
            group by concept.concept_name;
        '''
        result = db_reader.db_search(sql)
    return result


@bp.route('/visit/<concept_id>', methods=["GET"])
def index(concept_id):
    if concept_id not in correct_querys:
        return "invalid query!"
    result = visit_query(concept_id)
    return jsonify(result)
