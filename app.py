from flask import Flask, render_template, request
import os
import database.db_connector as db
from helpers import well_id_accumulator, company_id_accumulator, basin_id_accumulator, formation_id_accumulator

# Configuration
app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes


@app.route('/')
@app.route('/home')
def root():
    return render_template("home.html")


@app.route('/wells', methods=['GET', 'POST'])
def wells():
    if request.method == 'GET':
        query = "SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Wells table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)
        return render_template("wells.html", wells=results, ids=ids)

    if request.method == 'POST':
        company_id = request.form['company_id']
        basin_id = request.form['basin_id']
        formation_id = request.form['formation_id']
        total_production_bbls = request.form['production_bbls']
        first_prod_date = request.form['first_prod_date']
        last_prod_date = request.form['last_prod_date']

        query = f'INSERT INTO Wells (company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date) VALUES (%s, %s, %s, %s, %s, %s);'

        data = (company_id, basin_id, formation_id, total_production_bbls, first_prod_date, last_prod_date)
        db.execute_query(db_connection, query, data)

        query = 'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Wells table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('wells.html', wells=results, ids=ids)


@app.route('/search-wells', methods=['GET', 'POST'])
def search_for_well():
    company_id = request.form['company_id']
    print(company_id)

    query = f'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells WHERE company_id = {company_id} ORDER BY well_id;'
    cursor = db.execute_query(db_connection, query)
    results = cursor.fetchall()

    query = 'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;'
    cursor = db.execute_query(db_connection, query)
    total_results = cursor.fetchall()

    # retrieves all current Wells table data for dropdown menu display purposes.
    ids = well_id_accumulator(total_results)

    return render_template('wells.html', wells=results, ids=ids)


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if request.method == 'GET':
        query = "SELECT company_id, company_name, total_wells, total_production_bbls, total_basins, total_formations FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Companies table data for dropdown menu display purposes.
        ids = company_id_accumulator(results)

        return render_template("companies.html", companies=results, ids=ids)

    if request.method == 'POST':
        company_name = request.form['company_name']
        total_wells = request.form['total_wells']
        total_production_bbls = request.form['total_production_bbls']
        total_basins = request.form['total_basins']
        total_formations = request.form['total_formations']

        query = f'INSERT INTO Companies (company_name, total_wells, total_production_bbls, total_basins, total_formations) VALUES (%s, %s, %s, %s, %s);'

        data = (company_name, total_wells, total_production_bbls, total_basins, total_formations)
        db.execute_query(db_connection, query, data)

        query = "SELECT company_id, company_name, total_wells, total_production_bbls, total_basins, total_formations FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Companies table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('companies.html', companies=results, ids=ids)


@app.route('/basins', methods=['GET', 'POST'])
def basins():
    if request.method == 'GET':
        query = "SELECT basin_id, basin_name, total_wells, total_formations, total_production_bbls FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Basins table data for dropdown menu display purposes.
        ids = basin_id_accumulator(results)

        return render_template("basins.html", basins=results, ids=ids)

    if request.method == 'POST':
        basin_name = request.form['basin_name']
        total_wells = request.form['total_wells']
        total_formations = request.form['total_formations']
        total_production_bbls = request.form['total_production_bbls']

        query = f'INSERT INTO Basins (basin_name, total_wells, total_formations, total_production_bbls) VALUES (%s, %s, %s, %s);'

        data = (basin_name, total_wells, total_formations, total_production_bbls)
        db.execute_query(db_connection, query, data)

        query = "SELECT basin_id, basin_name, total_wells, total_formations, total_production_bbls FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Basins table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('basins.html', basins=results, ids=ids)


@app.route('/formations', methods=['GET', 'POST'])
def formations():
    if request.method == 'GET':
        query = "SELECT formation_id, formation_name, basin_id, total_wells, total_production_bbls FROM Formations ORDER BY formation_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # get basin_ids from Basins
        query = "SELECT basin_id FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        basin_id_results = cursor.fetchall()

        # retrieves all current Formations table data for dropdown menu display purposes.
        formation_ids = formation_id_accumulator(results)
        basin_ids = basin_id_accumulator(basin_id_results)

        return render_template("formations.html", formations=results, formation_ids=formation_ids, basin_ids=basin_ids)

    if request.method == 'POST':
        formation_name = request.form['formation_name']
        basin_id = request.form['basin_id']
        total_wells = request.form['total_wells']
        total_production_bbls = request.form['total_production_bbls']

        query = f'INSERT INTO Formations (formation_name, basin_id, total_wells, total_production_bbls) VALUES (%s, %s, %s, %s);'

        data = (formation_name, basin_id, total_wells, total_production_bbls)
        db.execute_query(db_connection, query, data)

        # get formation table data and store in 'formation_results'
        query = "SELECT formation_id, formation_name, basin_id, total_wells, total_production_bbls FROM Formations ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        formation_results = cursor.fetchall()

        # get basin_ids from Basins
        query = "SELECT basin_id FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        basin_id_results = cursor.fetchall()

        # retrieves all current Basins table data for dropdown menu display purposes.
        formation_ids = formation_id_accumulator(formation_results)
        basin_ids = basin_id_accumulator(basin_id_results)

        return render_template('formations.html', formations=formation_results, formation_ids=formation_ids, basin_ids=basin_ids)


@app.route('/operators-formations', methods=['GET', 'POST'])
def operators_formations():
    if request.method == 'GET':
        query = "SELECT company_id, formation_id FROM Operators_Formations ORDER BY company_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # get company ids
        query = "SELECT company_id FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        company_id_results = cursor.fetchall()

        # get formation ids
        query = "SELECT formation_id FROM Formations ORDER BY formation_id;"
        cursor = db.execute_query(db_connection, query)
        formation_id_results = cursor.fetchall()

        # retrieves all current Companies and Formations ids data for dropdown menu display purposes.
        company_ids = company_id_accumulator(company_id_results)
        formation_ids = formation_id_accumulator(formation_id_results)

        return render_template("operators-formations.html", operators_formations=results, company_ids=company_ids, formation_ids=formation_ids)

    if request.method == 'POST':
        company_id = request.form['company_id']
        formation_id = request.form['formation_id']

        query = 'INSERT INTO Operators_Formations (company_id, formation_id) VALUES (%s, %s)'
        data = (company_id, formation_id)
        db.execute_query(db_connection, query, data)

        query = 'SELECT company_id, formation_id FROM Operators_Formations ORDER BY company_id;'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # get company ids
        query = "SELECT company_id FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        company_id_results = cursor.fetchall()

        # get formation ids
        query = "SELECT formation_id FROM Formations ORDER BY formation_id;"
        cursor = db.execute_query(db_connection, query)
        formation_id_results = cursor.fetchall()

        # retrieves all current Companies and Formations ids data for dropdown menu display purposes.
        company_ids = company_id_accumulator(company_id_results)
        formation_ids = formation_id_accumulator(formation_id_results)

        return render_template("operators-formations.html", operators_formations=results, company_ids=company_ids, formation_ids=formation_ids)


@app.route('/basins-operators', methods=['GET', 'POST'])
def basins_operators():
    if request.method == 'GET':
        query = "SELECT basin_id, company_id FROM Basins_Operators ORDER BY basin_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # get basin ids
        query = "SELECT basin_id FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        basin_id_results = cursor.fetchall()

        # get company ids
        query = "SELECT company_id FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        company_id_results = cursor.fetchall()

        # retrieves all current Companies and Formations ids data for dropdown menu display purposes.
        basin_ids = basin_id_accumulator(basin_id_results)
        company_ids = company_id_accumulator(company_id_results)

        return render_template("basins-operators.html", basins_operators=results, basin_ids=basin_ids, company_ids=company_ids)

    if request.method == 'POST':
        basin_id = request.form['basin_id']
        company_id = request.form['company_id']

        query = 'INSERT INTO Basins_Operators (basin_id, company_id) VALUES (%s, %s)'
        data = (basin_id, company_id)
        db.execute_query(db_connection, query, data)

        query = 'SELECT basin_id, company_id FROM Basins_Operators ORDER BY basin_id;'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # get basin ids
        query = "SELECT basin_id FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        basin_id_results = cursor.fetchall()

        # get company ids
        query = "SELECT company_id FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        company_id_results = cursor.fetchall()

        # retrieves all current Companies and Formations ids data for dropdown menu display purposes.
        basin_ids = basin_id_accumulator(basin_id_results)
        company_ids = company_id_accumulator(company_id_results)

        return render_template("basins-operators.html", basins_operators=results, basin_ids=basin_ids, company_ids=company_ids)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7769))
    app.run(port=port, debug=True)
