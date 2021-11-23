from flask import Flask, render_template, request
import os
import database.db_connector as db
from helpers import well_id_accumulator, company_id_accumulator, basin_id_accumulator, formation_id_accumulator

# Configuration
app = Flask(__name__)
# db_connection = db.connect_to_database()

# Routes


@app.route('/')
@app.route('/home')
def root():
    return render_template("home.html")


@app.route('/wells', methods=['GET', 'POST'])
def wells():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Wells table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)
        return render_template("wells.html", wells=results, ids=ids)

    # Add and Update functionalities
    if request.method == 'POST':
        # add row data to Wells table
        if 'addwell' in request.form:
            company_id = request.form['company_id']
            basin_id = request.form['basin_id']
            formation_id = request.form['formation_id']
            total_production_bbls = request.form['total_production_bbls']
            first_prod_date = request.form['first_prod_date']
            last_prod_date = request.form['last_prod_date']

            query = f'INSERT INTO Wells (company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date) VALUES (%s, %s, %s, %s, %s, %s);'

            data = (company_id, basin_id, formation_id, total_production_bbls, first_prod_date, last_prod_date)
            db.execute_query(db_connection, query, data)

        # Update row data in Wells table
        elif 'updatewell' in request.form:
            well_id = request.form['well_id']
            company_id = request.form['company_id']
            basin_id = request.form['basin_id']
            formation_id = request.form['formation_id']
            total_production_bbls = request.form['total_production_bbls']
            first_prod_date = request.form['first_prod_date']
            last_prod_date = request.form['last_prod_date']

            query = f'UPDATE Wells SET company_id = %s, basin_id = %s, formation_id = %s, total_production_bbls = %s, 1st_prod_date = %s, last_prod_date = %s WHERE well_id = %s;'

            data = (company_id, basin_id, formation_id, total_production_bbls, first_prod_date, last_prod_date, well_id)
            db.execute_query(db_connection, query, data)

        # Delete row data in Well table
        elif 'deletewell' in request.form:
            well_id = request.form['deletewell']

            query = 'DELETE FROM Wells WHERE well_id = %s'
            data = (well_id,)
            db.execute_query(db_connection, query, data)

        # query for displying table after alterations are complete
        query = 'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;'
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Wells table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('wells.html', wells=results, ids=ids)


@app.route('/search-wells', methods=['GET', 'POST'])
def search_for_well():
    db_connection = db.connect_to_database()

    query = 'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;'
    cursor = db.execute_query(db_connection, query)
    total_results = cursor.fetchall()

    # retrieves all current Wells table data for dropdown menu display purposes.
    ids = well_id_accumulator(total_results)

    # Return to wells page with all Well data
    if 'showallwells' in request.form:
        return render_template('wells.html', wells=total_results, ids=ids)

    # get company specific well data and render on search-wells page
    company_id = request.form['company_id']
    query = f'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells WHERE company_id = {company_id} ORDER BY well_id;'
    cursor = db.execute_query(db_connection, query)
    results = cursor.fetchall()

    return render_template('search-wells.html', wells=results, ids=ids)


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT company_id, company_name, total_wells, total_production_bbls, total_basins, total_formations FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Companies table data for dropdown menu display purposes.
        ids = company_id_accumulator(results)

        return render_template("companies.html", companies=results, ids=ids)

    # Add and Update functionalities
    if request.method == 'POST':
        # Add row data to Companies table
        if 'addcompany' in request.form:
            company_name = request.form['company_name']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']
            total_basins = request.form['total_basins']
            total_formations = request.form['total_formations']

            query = 'INSERT INTO Companies (company_name, total_wells, total_production_bbls, total_basins, total_formations) VALUES (%s, %s, %s, %s, %s);'

            data = (company_name, total_wells, total_production_bbls, total_basins, total_formations)
            db.execute_query(db_connection, query, data)

        # Update row data in Comapanies table
        elif'updatecompany' in request.form:
            company_id = request.form['company_id']
            company_name = request.form['company_name']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']
            total_basins = request.form['total_basins']
            total_formations = request.form['total_formations']

            query = 'UPDATE Companies SET company_name = %s, total_wells = %s, total_production_bbls = %s, total_basins = %s, total_formations = %s WHERE company_id = %s;'

            data = (company_name, total_wells, total_production_bbls, total_basins, total_formations, company_id)
            db.execute_query(db_connection, query, data)

         # Delete row data in Companies table
        elif 'deletecompany' in request.form:
            company_id = request.form['deletecompany']

            query = 'DELETE FROM Companies WHERE company_id = %s'
            data = (company_id,)
            db.execute_query(db_connection, query, data)

        # query for displying table after alterations are complete
        query = "SELECT company_id, company_name, total_wells, total_production_bbls, total_basins, total_formations FROM Companies ORDER BY company_id;"
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Companies table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('companies.html', companies=results, ids=ids)


@app.route('/basins', methods=['GET', 'POST'])
def basins():
    db_connection = db.connect_to_database()
    if request.method == 'GET':
        query = "SELECT basin_id, basin_name, total_wells, total_formations, total_production_bbls FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # retrieves all current Basins table data for dropdown menu display purposes.
        ids = basin_id_accumulator(results)

        return render_template("basins.html", basins=results, ids=ids)

    # Add and Update functionalities
    if request.method == 'POST':
        # Add row data to Basins table
        if 'addbasin' in request.form:
            basin_name = request.form['basin_name']
            total_wells = request.form['total_wells']
            total_formations = request.form['total_formations']
            total_production_bbls = request.form['total_production_bbls']

            query = f'INSERT INTO Basins (basin_name, total_wells, total_formations, total_production_bbls) VALUES (%s, %s, %s, %s);'

            data = (basin_name, total_wells, total_formations, total_production_bbls)
            db.execute_query(db_connection, query, data)

        # Update row data in Basins table
        elif 'updatebasin' in request.form:
            basin_id = request.form['basin_id']
            basin_name = request.form['basin_name']
            total_wells = request.form['total_wells']
            total_formations = request.form['total_formations']
            total_production_bbls = request.form['total_production_bbls']

            query = 'UPDATE Basins SET basin_name = %s, total_wells = %s, total_formations = %s, total_production_bbls = %s WHERE basin_id = %s;'

            data = (basin_name, total_wells, total_formations, total_production_bbls, basin_id)
            db.execute_query(db_connection, query, data)

        # Delete row data in Basin table
        elif 'deletebasin' in request.form:
            basin_id = request.form['deletebasin']

            query = 'DELETE FROM Basins WHERE basin_id = %s'
            data = (basin_id,)
            db.execute_query(db_connection, query, data)

        # query for displying table after alterations are complete
        query = "SELECT basin_id, basin_name, total_wells, total_formations, total_production_bbls FROM Basins ORDER BY basin_id;"
        cursor = db.execute_query(db_connection, query)
        results = cursor.fetchall()

        # retrieves all current Basins table data for dropdown menu display purposes.
        ids = well_id_accumulator(results)

        return render_template('basins.html', basins=results, ids=ids)


@app.route('/formations', methods=['GET', 'POST'])
def formations():
    db_connection = db.connect_to_database()
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

    # Add and Update functionalities
    if request.method == 'POST':
        # Add row data to Formations table
        if 'addformation' in request.form:
            formation_name = request.form['formation_name']
            basin_id = request.form['basin_id']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']

            query = f'INSERT INTO Formations (formation_name, basin_id, total_wells, total_production_bbls) VALUES (%s, %s, %s, %s);'

            data = (formation_name, basin_id, total_wells, total_production_bbls)
            db.execute_query(db_connection, query, data)

        # Update row data in Formations table
        elif 'updateformation' in request.form:
            formation_id = request.form['formation_id']
            formation_name = request.form['formation_name']
            basin_id = request.form['basin_id']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']

            query = 'UPDATE Formations SET formation_name = %s, basin_id = %s, total_wells = %s, total_production_bbls = %s WHERE formation_id = %s;'

            data = (formation_name, basin_id, total_wells, total_production_bbls, formation_id)
            db.execute_query(db_connection, query, data)

        # Delete row data in Formations table
        elif 'deleteformation' in request.form:
            formation_id = request.form['deleteformation']

            query = 'DELETE FROM Formations WHERE formation_id = %s'
            data = (formation_id,)
            db.execute_query(db_connection, query, data)

        # get formation table data and store in 'formation_results'
        query = "SELECT formation_id, formation_name, basin_id, total_wells, total_production_bbls FROM Formations ORDER BY formation_id;"
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
    db_connection = db.connect_to_database()
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

    # Add and Update functionalities
    if request.method == 'POST':
        # Add row data to Operators_Formations table
        if 'addoperatorsformations' in request.form:
            company_id = request.form['company_id']
            formation_id = request.form['formation_id']

            query = 'INSERT INTO Operators_Formations (company_id, formation_id) VALUES (%s, %s)'
            data = (company_id, formation_id)
            db.execute_query(db_connection, query, data)

        # update row data in Operators_Formations table
        elif 'updateoperatorsformations' in request.form:
            company_id = request.form['company_id']
            formation_id = request.form['formation_id']

            query = 'UPDATE Operators_Formations SET company_id = %s, formation_id = %s WHERE company_id = %s'
            data = (company_id, formation_id, company_id)
            db.execute_query(db_connection, query, data)

        # Delete row data in Operators_Formations table
        elif 'deleteoperatorformation' in request.form:
            company_id = request.form['deleteoperatorformation'][1]
            formation_id = request.form['deleteoperatorformation'][4]

            query = 'DELETE FROM Operators_Formations WHERE company_id = %s'
            data = (company_id,)
            db.execute_query(db_connection, query, data)

        # query for displying table after alterations are complete
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
    db_connection = db.connect_to_database()
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

    # Add and Update functionalities
    if request.method == 'POST':
        # Add row data to Basins_Operators table
        if 'addbasinsoperators' in request.form:
            basin_id = request.form['basin_id']
            company_id = request.form['company_id']

            query = 'INSERT INTO Basins_Operators (basin_id, company_id) VALUES (%s, %s)'
            data = (basin_id, company_id)
            db.execute_query(db_connection, query, data)

        # update row data in Basins_Operators table
        elif 'updatebasinsoperators' in request.form:
            basin_id = request.form['basin_id']
            company_id = request.form['company_id']

            query = 'UPDATE Basins_Operators SET basin_id = %s, company_id = %s WHERE basin_id = %s'
            data = (basin_id, company_id, basin_id)
            db.execute_query(db_connection, query, data)

        # Delete row data in Basins_Operators table
        elif 'deletebasinoperator' in request.form:
            basin_id = request.form['deletebasinoperator'][1]
            company_id = request.form['deletebasinoperator'][4]

            query = 'DELETE FROM Basins_Operators WHERE basin_id = %s AND company_id = %s'
            data = (basin_id, company_id)
            db.execute_query(db_connection, query, data)

        # query for displying table after alterations are complete
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
    port = int(os.environ.get('PORT', 7770))
    app.run(port=port, debug=True)
