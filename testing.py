import json

from django.db import connections


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def databaseTest(query,data):
    return query.lower() == data.lower()


if __name__ == "__main__":
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    # cursor1 = connections["provinces"].cursor()
    from datetime import datetime   
    print()

    # f = open(
    #     "app.json",
    # )
    # data = json.load(f)
    # datas = data["rajaongkir"]["results"]
    # error = []
    # for data in datas:
    #     query = f"SELECT city FROM db_postal_code_data WHERE city_id={data.get('city_id')};"
            
    # #     changeTabel = (
    # #         f"UPDATE db_postal_code_data"
    # #         + f" SET city_id={data.get('city_id')}"
    # #         + f" WHERE city LIKE '%{data.get('city_name')}%'"
    # #     )
    #     appDict = dictfetchall(cursor1.execute(query))
    #     try:
    #         result = appDict[0]['city']
    #         if databaseTest(result,data.get('city_name')):
    #             print(f"TEST {data.get('city_name')} PASS ......")
    #         else:
    #             print(f"TEST {data.get('city_name')} FAILED ......")
    #             error.append(data.get('city_id'))
    #     except IndexError:
    #         error.append(data.get('city_id'))
    #         print(data.get('city_id') + " ga ada")

    # print(error)
        

    #         # query = """
    #         # SELECT * FROM db_postal_code_data WHERE id=1;
    #         # """
    #         # name = input('masukkan')
    #         # query2 = f'SELECT id, province_code, province_name, province_name_en FROM db_province_data WHERE province_name LIKE "%{"Aceh Barat"}%" ;'
    #         # addTable = 'ALTER TABLE db_postal_code_data ADD city_id INT ;'
    #         # with open('app.json', 'w', encoding='utf-8') as f:
    #         #     json.dump(appDict, f, ensure_ascii=False, indent=4)
    #         # with open('PostCode.json', 'w') as json_file:
    #         #     json.dump(appDict, json_file)
    #     # print(data.get("city_id"))
    # # query3 = """SELECT city_id FROM db_postal_code_data WHERE city LIKE '%Aceh Barat%' """
    # # with cursor1 as cursor:
        
    # #     appDict = dictfetchall(cursor.execute(query))
    # #     print(json.dumps(appDict[0]))
