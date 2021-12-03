import database.db_connector as db

db_connection = db.connect_to_database()


def get_table_data(table):
    '''
    Returns all data from the given table name. This is in the form of a tuple containing dictionaries.
    Each dictionary corresponds to a row in the given table where each key:value pair is the column title:value for that row.
    The returned tuple of dictionaries are sorted by the given tables primary key.
    '''
    table_id = get_table_id(table)
    query = f"SELECT * FROM {table} ORDER BY {table_id};"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    return db_results


def get_relationship_table_data(table):
    '''
    Returns all data from thee given relationship table name. This is in the form of a tuple containing dictionaries.
    Each dictionary corresponds to a row in the given table where each key:value pair is the column title:value for that row.
    The returned tuple of dictionaries are first sorted by the given tables 'table_id' followed by the 'secondary_table_id'.
    '''
    table_id = get_table_id(table)
    if table == 'Basins_Operators':
        secondary_table_id = 'company_id'
    elif table == 'Operators_Formations':
        secondary_table_id = 'formation_id'
    query = f"SELECT * FROM {table} ORDER BY {table_id}, {secondary_table_id};"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    return db_results


def get_well_ids():
    '''
    Returns all well ids from Wells in a list of tuples. (Ex: [(well_id1), (well_id2)])   
    '''
    query = "SELECT well_id FROM Wells ORDER BY well_id;"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    well_data = []
    for table_row in db_results:
        well_data.append((table_row['well_id'],))

    return well_data


def get_company_ids_and_names():
    '''
    Returns all company names and ids from Companies in a list of tuples. (Ex: [(company_id, company_name)])
    '''
    query = "SELECT company_id, company_name FROM Companies ORDER BY company_id;"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    company_data = []
    for table_row in db_results:
        company_data.append((table_row['company_id'], table_row['company_name']))

    return company_data


def get_basin_ids_and_names():
    '''
    Returns all basin names and ids from Basins in a list of tuples. (Ex: [(basin_id, basin_name)])
    '''
    query = "SELECT basin_id, basin_name FROM Basins ORDER BY basin_id;"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    basin_data = []
    for table_row in db_results:
        basin_data.append((table_row['basin_id'], table_row['basin_name']))

    return basin_data


def get_formation_ids_and_names():
    '''
    Returns all formation names and ids from Formations in a list of tuples. (Ex: [(formation_id, formation_name)])
    '''
    query = "SELECT formation_id, formation_name FROM Formations ORDER BY formation_id;"
    cursor = db.execute_query(db_connection, query)
    db_results = cursor.fetchall()

    formation_data = []
    for table_row in db_results:
        formation_data.append((table_row['formation_id'], table_row['formation_name']))

    return formation_data


def get_table_id(table):
    '''
    Returns the primary key name of the given table. (Ex: 'Wells' -> 'well_id')
    '''
    table_id_order_map = {'Wells': 'well_id', 'Basins': 'basin_id', 'Formations': 'formation_id', 'Companies': 'company_id', 'Basins_Operators': 'basin_id', 'Operators_Formations': 'company_id'}

    return table_id_order_map[table]
