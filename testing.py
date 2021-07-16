
import json


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    from costumer.api.serializers import provinceSerializer
    from django.db import connections

    cursor1 = connections["provinces"].cursor()
    idPro = 12
    query4 = f"SELECT * FROM db_postal_code_data WHERE province_code={idPro}"
    query3 = """SELECT * FROM db_postal_code_data WHERE province_code=11"""
    with cursor1 as cursor:
        query = """
        SELECT * FROM db_postal_code_data WHERE id=1;
        """
        name = input('masukkan')
        query2 = f'SELECT id, province_code, province_name, province_name_en FROM db_province_data WHERE province_name LIKE "%{name}%" ;'
        appDict = dictfetchall(cursor.execute(query2))
        print(provinceSerializer(appDict))

        print(json.dumps(appDict))
        # with open('app.json', 'w', encoding='utf-8') as f:
        #     json.dump(appDict, f, ensure_ascii=False, indent=4)
        # with open('PostCode.json', 'w') as json_file:
        #     json.dump(appDict, json_file)
