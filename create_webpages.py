import mysql.connector
import re

# Function to sanitize a string for use as a filename
def sanitize_filename(filename):
    # Remove spaces and replace with underscores
    sanitized = re.sub(r'\s+', '_', filename)
    # Remove leading and trailing quotes
    sanitized = sanitized.strip("'")
    # Remove any remaining special characters
    sanitized = re.sub(r"[^\w.-]", "", sanitized)
    return sanitized

# Function to generate web pages for each individual
def generate_web_pages(filepath, output_directory):
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host='localhost',
            user='mysql',
            password='password',
            database='gedcom_website'
        )
        cursor = db.cursor()

        # Retrieve all individuals from the database
        cursor.execute("SELECT individual_id, given_name, surname, birth_date, death_date, FatherID AS father_id, MotherID AS mother_id FROM individuals LEFT JOIN children ON individuals.individual_id=children.ChildID")
        individuals = cursor.fetchall()
        print ('10')
        # Generate web page for each individual
        for individual in individuals:
            individual_id, given_name, surname, birth_date, death_date, father_id, mother_id = individual

            # Retrieve father's name
            father_name = ""
            if father_id is not None:
                cursor.execute("SELECT Given_Name FROM individuals WHERE Individual_ID=%s", (father_id,))
                father_result = cursor.fetchone()
                if father_result:
                    father_name = father_result[0]
            print ('20')
            # Retrieve mother's name
            mother_name = ""
            if mother_id is not None:
                cursor.execute("SELECT Given_Name FROM individuals WHERE Individual_ID=%s", (mother_id,))
                mother_result = cursor.fetchone()
                if mother_result:
                    mother_name = mother_result[0]
            print ('30')
            
            # Initialize spouse_name
            spouse_id=""
            spouse_name = ""
            marriage_date=""
            children_names=""

            

            # Generate the web page content
            page_content = f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<title>Ancestry</title>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css\">\n<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>\n<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js\"></script>\n</head>\n<body>\n<div class=\"container\">\n<div class=\"jumbotron\" style=\"background-color:#e7f1f4\"><div class=\"row\"><div class=\"col-sm-2\"></div><div class=\"col-sm-4\"><div class=\"row\"><h3>{given_name} {surname}</h3></div>\n<div class=\"row\">b. {birth_date}</div>\n<div class=\"row\">d. {death_date}</div>\n</div>\n<div class=\"col-sm-2\"></div>\n<div class=\"col-sm-2\"></div>\n<div class=\"col-sm-2\"></div></div></div>{given_name} {surname} was born {birth_date} to <a href=\"P{father_id}_{father_name}.html\">{father_name}</a> and <a href=\"P{mother_id}_{mother_name}.html\">{mother_name}</a></br>\n"

            print ('100')
            # Retrieve spouse's name and marriage date
            cursor.execute("SELECT individuals.Given_Name, Relationships.MarriageDate, Relationships.SpouseID "
                           "FROM Relationships "
                           "JOIN individuals ON individuals.Individual_ID=Relationships.SpouseID "
                           "WHERE Relationships.IndividualID=%s", (individual_id,))
            spouse_result = cursor.fetchone()
            print ('110')
            if spouse_result:
                spouse_name = spouse_result[0]
                spouse_id = spouse_result[2]
                marriage_date = spouse_result[1] if spouse_result[1] is not None else ""
                page_content += f" {given_name} {surname} married <a href=\"P{individual_id}_{spouse_name}.html\">{spouse_name}</a> {marriage_date}.</br>\n"
            else:
                page_content += " {given_name} {surname} did not get married.</br>\n"
            print ('120')
           
           
           # Consume unread results (if any)
            cursor.fetchall()
            # Retrieve children's names
            cursor.execute("SELECT individuals.Given_Name FROM children "
                        "JOIN individuals ON individuals.Individual_ID=children.ChildID "
                        "WHERE (children.FatherID=%s OR children.MotherID=%s )"
                        "AND (children.FatherID=%s OR children.MotherID=%s )", (individual_id, individual_id,spouse_id, spouse_id))
            children_results = cursor.fetchall()
            if children_results:
                children_names = [child[0] for child in children_results]
            print ('125')

           # Check if there are children and generate the children list
            if children_names:
                page_content += f"They had {len(children_names)} children: </br><ul>"
                for child in children_names:
                    page_content += f"<li>{child}</li>"
                page_content += "</ul>"
            else:
                page_content += "They had no children."          
            print ('130')
            
            # Close the HTML tags
            page_content += "</div></div></body></html>"

            # Sanitize the filename
            filename = f"P{individual_id}_{sanitize_filename(given_name)}_{sanitize_filename(surname)}.html"

            # Write the page_content to a separate HTML file
            filepath = output_directory + "/" + filename
            with open(filepath, 'w') as file:
                file.write(page_content)

        # Commit the changes to the database
        db.commit()

    except Exception as e:
        # Rollback the database changes in case of any errors
        db.rollback()
        print("An error occurred. Database changes have been rolled back.")
        print("Error message:", str(e))

    finally:
        # Close the database connection
        cursor.close()
        db.close()

def main():
    filepath = '/workspaces/gedcom-website/Dale_Poulter_Family_Tree_151120.ged'  # Replace with the actual file path
    output_directory = '/workspaces/gedcom-website/html'  # Replace with the actual output directory

    generate_web_pages(filepath, output_directory)

if __name__ == '__main__':
    main()
