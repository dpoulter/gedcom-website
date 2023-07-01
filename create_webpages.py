import sqlite3

# Function to generate web pages for each individual
def generate_web_pages():
    # Connect to the SQLite database
    conn = sqlite3.connect('gedcom.db')
    cursor = conn.cursor()

    # Retrieve all individuals from the database
    cursor.execute("SELECT * FROM Individuals")
    individuals = cursor.fetchall()

    # Generate web page for each individual
    for individual in individuals:
        individual_id, give_name, surname, birth_date, death_date, father_id, mother_id = individual

        # Retrieve father's name
        father_name = ""
        if father_id is not None:
            cursor.execute("SELECT Given_Name FROM Individuals WHERE IndividualID=?", (father_id,))
            father_name = cursor.fetchone()[0]

        # Retrieve mother's name
        mother_name = ""
        if mother_id is not None:
            cursor.execute("SELECT Given_Name FROM Individuals WHERE IndividualID=?", (mother_id,))
            mother_name = cursor.fetchone()[0]

        # Retrieve spouse's name and marriage date
        cursor.execute("SELECT Individuals.Given_Name, Relationships.MarriageDate "
                       "FROM Relationships "
                       "JOIN Individuals ON Individuals.IndividualID=Relationships.SpouseID "
                       "WHERE Relationships.IndividualID=?", (individual_id,))
        spouse = cursor.fetchone()
        spouse_name = spouse[0] if spouse is not None else ""
        marriage_date = spouse[1].strftime('%d %B %Y') if spouse is not None and spouse[1] is not None else ""

        # Retrieve children's names
        cursor.execute("SELECT Individuals.Given_Name FROM Children "
                       "JOIN Individuals ON Individuals.IndividualID=Children.ChildID "
                       "WHERE Children.FatherID=? OR Children.MotherID=?", (individual_id, individual_id))
        children = cursor.fetchall()
        children_names = [child[0] for child in children]

        # Generate the web page content
        page_content = f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<title>Ancestry</title>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css\">\n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>\n<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js\"></script>\n</head>\n<body>\n<div class=\"container\">\n<div class=\"jumbotron\" style=\"background-color:#e7f1f4\"><div class=\"row\"><div class=\"col-sm-2\"></div><div class=\"col-sm-4\"><div class=\"row\"><h3>{name}</h3></div>\n<div class=\"row\">b. {birth_date}</div>\n<div class=\"row\">d. {death_date}</div>\n</div>\n<div class=\"col-sm-2\"></div>\n<div class=\"col-sm-2\"></div>\n<div class=\"col-sm-2\"></div></div></div>{name} was born {birth_date} to <a href=\"P{father_id}_{father_name}.html\">{father_name}</a> and <a href=\"P{mother_id}_{mother_name}.html\">{mother_name}</a>. {name} married <a href=\"P{individual_id}_{spouse_name}.html\">{spouse_name}</a> {marriage_date}.</br>\n"

