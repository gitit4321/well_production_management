import database.db_connector as db

db_connection = db.connect_to_database()


def well_id_accumulator(db_data):
    ids = {'well_ids': [], 'company_ids': [], 'basin_ids': [], 'formation_ids': []}

    for d in db_data:
        for k, v in d.items():
            if k == 'well_id' and v not in ids['well_ids']:
                ids['well_ids'].append(v)
            elif k == 'company_id' and v not in ids['company_ids']:
                ids['company_ids'].append(v)
            elif k == 'basin_id' and v not in ids['basin_ids']:
                ids['basin_ids'].append(v)
            elif k == 'formation_id' and v not in ids['formation_ids']:
                ids['formation_ids'].append(v)

    for lists in ids.values():
        lists.sort()

    return ids


def company_id_accumulator(db_data):
    ids = {'company_ids': []}

    for d in db_data:
        for k, v in d.items():
            if k == 'company_id' and v not in ids['company_ids']:
                ids['company_ids'].append(v)

    for lists in ids.values():
        lists.sort()

    return ids


def basin_id_accumulator(db_data):
    ids = {'basin_ids': []}

    for d in db_data:
        for k, v in d.items():
            if k == 'basin_id' and v not in ids['basin_ids']:
                ids['basin_ids'].append(v)

    for lists in ids.values():
        lists.sort()

    return ids


def formation_id_accumulator(db_data):
    ids = {'formation_ids': [], 'basin_ids': []}
    print(db_data)
    for d in db_data:
        for k, v in d.items():
            if k == 'formation_id' and v not in ids['formation_ids']:
                ids['formation_ids'].append(v)
            elif k == 'basin_id' and v not in ids['basin_ids']:
                ids['basin_ids'].append(v)

    for lists in ids.values():
        lists.sort()

    return ids
