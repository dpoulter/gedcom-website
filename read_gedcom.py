import mysql.connector

def parse_gedcom_file(filename, cursor):
    individuals = []
    families = []
    children = []

    with open(filename, 'r') as file:
        current_individual = {}
        current_family = {}

        for line in file:
            tokens = line.strip().split(' ')
            print ('tokens='.join(tokens))
            level = int(tokens[0])
            if level == 0:
                    if len(tokens) >= 3 and tokens[2]:
                        tag = tokens[2]
                        arguments = tokens[1]
                        print ('arguments='+str(arguments))
                    else:
                        tag = None
                        arguments = None
            else:
                if len(tokens) >= 3 and tokens[1]:
                    tag = tokens[1]
                    arguments = ' '.join(tokens[2:])
                    print ('arguments='+str(arguments))
                else:
                    tag = None
                    arguments = None

            if tag:
                print ('tag='+tag)
            else:
                print ('tag=None')

            if level == 0:
                if tag == 'INDI':
                    level0_tag = 'INDI'
                    individual_id = arguments.strip('@')
                    print('individual_id='+individual_id)

                    if current_individual and individual_id != current_individual['individual_id']:
                        individuals.append({'individual_id': current_individual['individual_id'] , 'given_name': current_individual['given_name'], 'surname': current_individual['surname'], 'birth_date': current_individual['birth_date'], 'death_date': current_individual['death_date']})
                    current_individual = {'individual_id': individual_id, 'given_name': '', 'surname': '', 'birth_date': '', 'death_date': ''}
                elif tag == 'FAM':
                    level0_tag = 'FAM'
                    family_id = arguments.strip('@')
                    families.append({'family_id': family_id, 'husband_id': None, 'wife_id': None, 'marriage_date': None})
                    current_family = families[-1]
                else:
                    level0_tag = ''

                print ('level0_tag='+level0_tag)

            elif level == 1:
                
                if tag == 'BIRT':
                    if 'birth_date' not in current_individual:
                        current_individual['birth_date'] = None
                elif tag == 'DEAT':
                    if 'death_date' not in current_individual:
                        current_individual['death_date'] = None
                elif tag == 'HUSB':
                    if current_family is not None:
                        current_family['husband_id'] = arguments.strip('@')
                elif tag == 'WIFE':
                    if current_family is not None:
                        current_family['wife_id'] = arguments.strip('@')
                elif tag == 'MARR':
                    if 'marriage_date' not in current_family:
                        current_family['marriage_date'] = None
                elif tag == 'CHIL':
                    if current_family is not None:
                        children.append({'child_id': arguments.strip('@'), 'father_id': current_family['husband_id'], 'mother_id': current_family['wife_id']})

            elif level == 2:
                if tag == 'DATE':
                    if current_individual and current_individual.get('birth_date') is None:
                        current_individual['birth_date'] = arguments
                    elif current_individual and current_individual.get('death_date') is None:
                        current_individual['death_date'] = arguments
                    elif current_family and current_family.get('marriage_date') is None:
                        current_family['marriage_date'] = arguments
                elif tag == 'SURN':
                    current_individual['surname'] = arguments
                elif tag == 'GIVN':
                    current_individual['given_name'] = arguments

    print('insert individuals')
    for individual_data in individuals:
        print ('insert individual_id='+individual_data['individual_id']+' given_name='+individual_data['given_name']+' surname='+individual_data['surname'])
        cursor.execute("""
            INSERT INTO individuals (individual_id, given_name, surname, birth_date, death_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (individual_data['individual_id'], individual_data['given_name'], individual_data['surname'], individual_data['birth_date'], individual_data['death_date']))
    
    print('insert families')
    for family_data in families:
        cursor.execute("""
            INSERT INTO families (family_id, husband_id, wife_id, marriage_date)
            VALUES (%s, %s, %s, %s)
        """, (family_data['family_id'], family_data['husband_id'], family_data['wife_id'], family_data['marriage_date']))

    print('insert children')
    for child_data in children:
        cursor.execute("""
            INSERT INTO children (ChildID, FatherID, MotherID)
            VALUES (%s, %s, %s)
        """, (child_data['child_id'], child_data['father_id'], child_data['mother_id']))




def main():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host='localhost',
            user='mysql',
            password='password',
            database='gedcom_website'
        )
        cursor = db.cursor()


        # Parse the GEDCOM file and store the data in the database
        filename = '/workspaces/gedcom-website/Dale_Poulter_Family_Tree_151120.ged'
        parse_gedcom_file(filename, cursor)
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

if __name__ == '__main__':
    main()
