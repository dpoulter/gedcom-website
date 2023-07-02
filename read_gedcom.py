import mysql.connector

def parse_gedcom_file(filename, cursor):
    individuals = []
    families = []
    children = []
    relationships = []

    with open(filename, 'r') as file:
        current_individual = {}
        current_family = {}
        current_relationship1 = {}
        current_relationship2 = {}

        for line in file:
            tokens = line.strip().split(' ')
            # print ('tokens='.join(tokens))
            level = int(tokens[0])
            if level == 0:
                    if len(tokens) >= 3 and tokens[2]:
                        tag = tokens[2]
                        arguments = tokens[1]
                        # print ('arguments='+str(arguments))
                    else:
                        tag = None
                        arguments = None
            else:
                
                    tag = tokens[1]
                    arguments = ' '.join(tokens[2:])
                    # print ('arguments='+str(arguments))
                
          #   if tag:
           #      print ('tag='+tag)
           #  else:
           #      print ('tag=None')

            # print('40')
            if level == 0:
                if tag == 'INDI':
                    #level0_tag = 'INDI'
                    individual_id = arguments.strip('@')
                    # print('individual_id='+individual_id)

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

                # print ('level0_tag='+level0_tag)
           
            elif level == 1:
                level1_tag = tag

                if tag == 'BIRT':
                
                        current_individual['birth_date'] = None
                elif tag == 'DEAT':
                
                        current_individual['death_date'] = None
                elif tag == 'HUSB':
                    if current_family is not None:
                        current_family['husband_id'] = arguments.strip('@')
                        relationships.append({'individual_id': current_family['husband_id'], 'spouse_id': None, 'date': None, 'event': None})
                        current_relationship1 = relationships[-1]
                        
                elif tag == 'WIFE':
                    if current_family is not None:
                        current_family['wife_id'] = arguments.strip('@')
                        relationships.append({'individual_id': current_family['wife_id'], 'spouse_id': None, 'date': None, 'event': None})
                        current_relationship2 = relationships[-1]
                elif tag == 'MARR':
                    print('50 - Tag='+tag)
                    if current_family is not None:
                       
                            current_family['marriage_date'] = None

                            
        
                    # Find the corresponding relationship and update the spouse_id
                    print ('MARR - Find the corresponding relationship and update the spouse_id')
                    for rel in relationships:
                        if rel['individual_id'] == current_family['husband_id']:
                            rel['spouse_id'] = current_family['wife_id']
                        elif rel['individual_id'] == current_family['wife_id']:
                            rel['spouse_id'] = current_family['husband_id']
                    print('66')
                    current_relationship1['event'] = 'MARR'
                    current_relationship2['event'] = 'MARR'
                    
              

                elif tag == 'DIV':
                    print('70')
                    if current_family is not None:
                     
                            current_family['divorce_date'] = None

                    print ('105:Check if current relationship is not none')
                             
                    # Find the corresponding relationship and update the spouse_id
                    print ('DIV -  Find the corresponding relationship and update the spouse_id')
                    for rel in relationships:
                        if rel['individual_id'] == current_family['husband_id']:
                            rel['spouse_id'] = current_family['wife_id']
                        elif rel['individual_id'] == current_family['wife_id']:
                            rel['spouse_id'] = current_family['husband_id']
                    print('75')
                    current_relationship1['event'] = 'DIV'
                    current_relationship2['event'] = 'DIV'
                    

                elif tag == 'CHIL':
                    # print('80')
                    if current_family is not None:
                        children.append({'child_id': arguments.strip('@'), 'father_id': current_family['husband_id'], 'mother_id': current_family['wife_id']})

            elif level == 2:

                if tag == 'DATE':
                    print('90')
                    if current_individual and current_individual.get('birth_date') is None:
                        current_individual['birth_date'] = arguments
                    elif current_individual and current_individual.get('death_date') is None:
                        current_individual['death_date'] = arguments
                    elif level1_tag=='MARR' or level1_tag=='DIV':
                            current_relationship1['date']= arguments
                            current_relationship2['date']= arguments
                            print(current_relationship1)
                            print(current_relationship2)

                elif tag == 'SURN':
                    current_individual['surname'] = arguments
                elif tag == 'GIVN':
                    current_individual['given_name'] = arguments
                


    print('insert individuals')
    for individual_data in individuals:
        #print ('insert individual_id='+individual_data['individual_id']+' given_name='+individual_data['given_name']+' surname='+individual_data['surname'])
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

    print('insert relationships')
    for rel_data in relationships:
        
        if rel_data['event']=='MARR':
            cursor.execute("""
                INSERT INTO Relationships (IndividualID, SpouseID, MarriageDate)
                VALUES (%s, %s, %s)
                """, (rel_data['individual_id'], rel_data['spouse_id'], rel_data['date']))
        elif rel_data['event']=='DIV':
            cursor.execute("""
                INSERT INTO Relationships (IndividualID, SpouseID, DivorceDate)
                VALUES (%s, %s, %s)
                """, (rel_data['individual_id'], rel_data['spouse_id'], rel_data['date']))


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
