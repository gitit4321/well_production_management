from flask import Flask, flash, redirect, render_template, request, url_for
import os
from dotenv import load_dotenv, find_dotenv
import database.db_connector as db
from db_helpers import get_table_data, get_well_ids, get_company_ids_and_names, get_basin_ids_and_names, get_formation_ids_and_names

load_dotenv(find_dotenv())

# Configuration
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")

# Routes


@app.route('/')
@app.route('/home')
def root():
    return render_template("home.html")


@app.route('/wells', methods=['GET', 'POST'])
def wells():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Wells table.', 'updated': 'Data successfully updated in Wells table.', 'deleted': 'Data successfully deleted from Wells table.'}

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Wells table
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

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Wells table
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

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Wells table
        elif 'deletewell' in request.form:
            well_id = request.form['deletewell']

            query = 'DELETE FROM Wells WHERE well_id = %s'
            data = (well_id,)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('wells'))

    ### General display data for table and dropdown menus ###
    # Wells table for display purposes
    table_data = get_table_data('Wells')

    # data for dropdown menu display purposes
    well_data = get_well_ids()
    company_data = get_company_ids_and_names()
    basin_data = get_basin_ids_and_names()
    formation_data = get_formation_ids_and_names()

    return render_template('wells.html', table_data=table_data, well_data=well_data, company_data=company_data, basin_data=basin_data, formation_data=formation_data)


@app.route('/search-wells', methods=['GET', 'POST'])
def search_for_well():
    db_connection = db.connect_to_database()

    ### General display data for table and dropdown menus ###
    # Wells table for display purposes
    table_data = get_table_data('Wells')

    # data for dropdown menu display purposes
    well_data = get_well_ids()
    company_data = get_company_ids_and_names()
    basin_data = get_basin_ids_and_names()
    formation_data = get_formation_ids_and_names()

    # If 'Show all well' button clicked, return to wells page with all Well data displayed
    if 'showallwells' in request.form:
        return render_template('wells.html', table_data=table_data, well_data=well_data, company_data=company_data, basin_data=basin_data, formation_data=formation_data)

    # get company specific well data and render on search-wells page
    company_id = request.form['company_id']
    query = f'SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells WHERE company_id = {company_id} ORDER BY well_id;'
    cursor = db.execute_query(db_connection, query)
    search_result_data = cursor.fetchall()
    if not search_result_data:
        flash('The selected company has no wells in the system. Please select a different company.', 'warning')
        return redirect(url_for('wells'))

    return render_template('search-wells.html', table_data=search_result_data, well_data=well_data, company_data=company_data, basin_data=basin_data, formation_data=formation_data)


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Companies table.', 'updated': 'Data successfully updated in Companies table.', 'deleted': 'Data successfully deleted from Companies table.'}

    # iterate through all existing companies and run aggregate functions
    query = "SELECT company_id FROM Companies ORDER BY company_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    companies = cursor.fetchall()
    for company in companies:
        company_id = company['company_id']

        query = "UPDATE Companies SET total_wells = (SELECT COUNT(*) FROM Wells WHERE company_id = %s), total_production_bbls = (SELECT SUM(total_production_bbls) FROM Wells WHERE company_id = %s), total_basins = (SELECT COUNT(*) FROM Basins_Operators WHERE company_id = %s), total_formations = (SELECT COUNT(*) FROM Operators_Formations WHERE company_id = %s) WHERE company_id = %s;"
        data = (company_id, company_id, company_id, company_id, company_id)
        db.execute_query(db_connection, query, data)

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Companies table
        if 'addcompany' in request.form:
            company_name = request.form['company_name']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']
            total_basins = request.form['total_basins']
            total_formations = request.form['total_formations']

            query = 'INSERT INTO Companies (company_name, total_wells, total_production_bbls, total_basins, total_formations) VALUES (%s, %s, %s, %s, %s);'

            data = (company_name, total_wells, total_production_bbls, total_basins, total_formations)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Companies table
        elif 'updatecompany' in request.form:
            company_id = request.form['company_id']
            company_name = request.form['company_name']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']
            total_basins = request.form['total_basins']
            total_formations = request.form['total_formations']

            query = 'UPDATE Companies SET company_name = %s, total_wells = %s, total_production_bbls = %s, total_basins = %s, total_formations = %s WHERE company_id = %s;'

            data = (company_name, total_wells, total_production_bbls, total_basins, total_formations, company_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Companies table
        elif 'deletecompany' in request.form:
            company_id = request.form['deletecompany']

            query = 'DELETE FROM Companies WHERE company_id = %s'
            data = (company_id,)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('companies'))

    ### General display data for table and dropdown menus ###
    # Wells table for disaply purposes
    table_data = get_table_data('Companies')

    # data for dropdown menu display purposes
    company_data = get_company_ids_and_names()

    return render_template('companies.html', table_data=table_data, company_data=company_data)


@app.route('/basins', methods=['GET', 'POST'])
def basins():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Basins table.', 'updated': 'Data successfully updated in Basins table.', 'deleted': 'Data successfully deleted from Basins table.'}

    # iterate through all existing basins and run aggregate functions
    query = "SELECT basin_id FROM Basins ORDER BY basin_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    basins = cursor.fetchall()
    for basin in basins:
        basin_id = basin['basin_id']

        query = "UPDATE Basins SET total_wells = (SELECT COUNT(*) FROM Wells WHERE basin_id = %s), total_formations = (SELECT COUNT(DISTINCT formation_id) FROM Wells WHERE basin_id = %s), total_production_bbls = (SELECT SUM(total_production_bbls) FROM Wells WHERE basin_id = %s) WHERE basin_id = %s;"
        data = (basin_id, basin_id, basin_id, basin_id)
        db.execute_query(db_connection, query, data)

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Basins table
        if 'addbasin' in request.form:
            basin_name = request.form['basin_name']
            total_wells = request.form['total_wells']
            total_formations = request.form['total_formations']
            total_production_bbls = request.form['total_production_bbls']

            query = f'INSERT INTO Basins (basin_name, total_wells, total_formations, total_production_bbls) VALUES (%s, %s, %s, %s);'

            data = (basin_name, total_wells, total_formations, total_production_bbls)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Basins table
        elif 'updatebasin' in request.form:
            basin_id = request.form['basin_id']
            basin_name = request.form['basin_name']
            total_wells = request.form['total_wells']
            total_formations = request.form['total_formations']
            total_production_bbls = request.form['total_production_bbls']

            query = 'UPDATE Basins SET basin_name = %s, total_wells = %s, total_formations = %s, total_production_bbls = %s WHERE basin_id = %s;'

            data = (basin_name, total_wells, total_formations, total_production_bbls, basin_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Basin table
        elif 'deletebasin' in request.form:
            basin_id = request.form['deletebasin']

            query = 'DELETE FROM Basins WHERE basin_id = %s'
            data = (basin_id,)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('basins'))

    ### General display data for table and dropdown menus ###
    # Basins table for display purposes
    table_data = get_table_data('Basins')

    # retrieves all current Basins table data for dropdown menu display purposes
    basin_data = get_basin_ids_and_names()

    return render_template("basins.html", table_data=table_data, basin_data=basin_data)


@app.route('/formations', methods=['GET', 'POST'])
def formations():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Formations table.',
                      'updated': 'Data successfully updated in Formations table.', 'deleted': 'Data successfully deleted from Formations table.'}

    # iterate through all existing formations and run aggregate functions
    query = "SELECT formation_id FROM Formations ORDER BY formation_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    formations = cursor.fetchall()
    for formation in formations:
        formation_id = formation['formation_id']

        query = "UPDATE Formations SET total_wells = (SELECT COUNT(*) FROM Wells WHERE formation_id = %s),total_production_bbls = (SELECT SUM(total_production_bbls) FROM Wells WHERE formation_id = %s) WHERE formation_id = %s;"
        data = (formation_id, formation_id, formation_id)
        db.execute_query(db_connection, query, data)

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Formations table
        if 'addformation' in request.form:
            formation_name = request.form['formation_name']
            basin_id = request.form['basin_id']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']

            query = f'INSERT INTO Formations (formation_name, basin_id, total_wells, total_production_bbls) VALUES (%s, %s, %s, %s);'

            data = (formation_name, basin_id, total_wells, total_production_bbls)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Formations table
        elif 'updateformation' in request.form:
            formation_id = request.form['formation_id']
            formation_name = request.form['formation_name']
            basin_id = request.form['basin_id']
            total_wells = request.form['total_wells']
            total_production_bbls = request.form['total_production_bbls']

            query = 'UPDATE Formations SET formation_name = %s, basin_id = %s, total_wells = %s, total_production_bbls = %s WHERE formation_id = %s;'

            data = (formation_name, basin_id, total_wells, total_production_bbls, formation_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Formations table
        elif 'deleteformation' in request.form:
            formation_id = request.form['deleteformation']

            query = 'DELETE FROM Formations WHERE formation_id = %s'
            data = (formation_id,)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('formations'))

    ### General display data for table and dropdown menus ###
    # Formations table for display purposes
    table_data = get_table_data('Formations')

    # data for dropdown menu display purposes
    basin_data = get_basin_ids_and_names()
    formation_data = get_formation_ids_and_names()

    return render_template('formations.html', table_data=table_data, formation_data=formation_data, basin_data=basin_data)


@app.route('/operators-formations', methods=['GET', 'POST'])
def operators_formations():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Operators_Formations table.',
                      'updated': 'Data successfully updated in Operators_Formations table.', 'deleted': 'Data successfully deleted from Operators_Formations table.'}

    ### reagrdless of request method, rebuild Operators_Formations table ###
    # remove all data from Operators_Formations, without dropping table
    query = "DELETE FROM Operators_Formations;"
    db.execute_query(db_connection=db_connection, query=query)

    # repopulate table with current data
    query = "INSERT INTO Operators_Formations (company_id, formation_id) SELECT DISTINCT company_id, formation_id FROM Wells;"
    db.execute_query(db_connection=db_connection, query=query)

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Operators_Formations table
        if 'addoperatorsformations' in request.form:
            company_id = request.form['company_id']
            formation_id = request.form['formation_id']

            query = 'INSERT INTO Operators_Formations (company_id, formation_id) VALUES (%s, %s)'
            data = (company_id, formation_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Operators_Formations table
        elif 'updateoperatorsformations' in request.form:
            company_id = request.form['company_id']
            formation_id = request.form['formation_id']

            query = 'UPDATE Operators_Formations SET company_id = %s, formation_id = %s WHERE company_id = %s'
            data = (company_id, formation_id, company_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Operators_Formations table
        elif 'deleteoperatorformation' in request.form:
            company_id = request.form['deleteoperatorformation'][1]
            formation_id = request.form['deleteoperatorformation'][4]

            query = 'DELETE FROM Operators_Formations WHERE company_id = %s AND formation_id = %s'
            data = (company_id, formation_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('operators_formations'))

    ### General display data for table and dropdown menus ###
    # Wells table for display purposes
    table_data = get_table_data('Operators_Formations')

    # data for dropdown menu display purposes
    company_data = get_company_ids_and_names()
    formation_data = get_formation_ids_and_names()

    return render_template("operators-formations.html", table_data=table_data, company_data=company_data, formation_data=formation_data)


@app.route('/basins-operators', methods=['GET', 'POST'])
def basins_operators():
    db_connection = db.connect_to_database()
    flash_messages = {'added': 'Data successfully added to Basins_Operators table.',
                      'updated': 'Data successfully updated in Basins_Operators table.', 'deleted': 'Data successfully deleted from Basins_Operators table.'}

    ### reagrdless of request method, rebuild Basins_Operators table ###
    # remove all data from Basins_Operators, without dropping table
    query = "DELETE FROM Basins_Operators;"
    db.execute_query(db_connection=db_connection, query=query)

    # repopulate table with current data
    query = "INSERT INTO Basins_Operators (basin_id, company_id) SELECT DISTINCT basin_id, company_id FROM Wells;"
    db.execute_query(db_connection=db_connection, query=query)

    # Insert, Update, and Delete functionalities
    if request.method == 'POST':
        # INSERT row data into Basins_Operators table
        if 'addbasinsoperators' in request.form:
            basin_id = request.form['basin_id']
            company_id = request.form['company_id']

            query = 'INSERT INTO Basins_Operators (basin_id, company_id) VALUES (%s, %s)'
            data = (basin_id, company_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['added']

        # UPDATE row data in Basins_Operators table
        elif 'updatebasinsoperators' in request.form:
            basin_id = request.form['basin_id']
            company_id = request.form['company_id']

            query = 'UPDATE Basins_Operators SET basin_id = %s, company_id = %s WHERE basin_id = %s'
            data = (basin_id, company_id, basin_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['updated']

        # DELETE row data in Basins_Operators table
        elif 'deletebasinoperator' in request.form:
            basin_id = request.form['deletebasinoperator'][1]
            company_id = request.form['deletebasinoperator'][4]

            query = 'DELETE FROM Basins_Operators WHERE basin_id = %s AND company_id = %s'
            data = (basin_id, company_id)
            db.execute_query(db_connection, query, data)

            # set relevant flash message
            flash_message = flash_messages['deleted']

        flash(flash_message, 'success')
        return redirect(url_for('basins_operators'))

    ### General display data for table and dropdown menus ###
    # Wells table for display purposes
    table_data = get_table_data('Basins_Operators')

    # data for dropdown menu display purposes
    company_data = get_company_ids_and_names()
    basin_data = get_basin_ids_and_names()

    return render_template("basins-operators.html", table_data=table_data, basin_data=basin_data, company_data=company_data)


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7769))
    app.run(port=port, debug=True)
