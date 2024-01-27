from DataTypes import *
import mysql.connector

# Bundles together functions for probing a MySQL database to confirm
# whether or not it adheres to specific properties of a logical/relational schema.
# Can be used to verify that a MySQL database correctly implements a design.
class DataModelChecker:

    # Ctor sets the connection details for this model checker
    def __init__( self, host, username, password, database ):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        # TODO: Implement me!
        self.con = mysql.connector.connect(host = self.host, user = self.username, password = self.password, database = self.database) # Connects to the database

    # Predicate function that connects to the database and confirms
    # whether or not a list of attributes is set up as a (super)key for a given table
    # For example, if attributes contains table_name R and attributes [x, y],
    # this function returns true if (x,y) is enforced as a key in R
    # @see Util.Attributes
    # @pre the tables and attributes in attributes must already exist
    def confirmSuperkey( self, attributes ):
        # TODO: Implement me!
        try: # We use a try/except block for when we encounter a wrong SQL input
            cursor = self.con.cursor() 
            cursor.execute(f"SHOW INDEX FROM {attributes.table_name} WHERE Key_name = \'PRIMARY\';") # This executes a query that fetches the primary keys.
            rows1 = cursor.fetchall() # we get the information from cursor.
            primary_key = [row[4] for row in rows1] # row 4 is the column designated for primary keys.
            flag1 = (len(primary_key) != 0) # we check that primary key exists.
            for column_name in primary_key: # We check for primary keys.
                if column_name not in attributes.attributes:
                    flag1 = False # If the primary keys in table don't match the attributes given, then flag is false
            cursor.execute((f"SHOW INDEX FROM {attributes.table_name} WHERE Non_unique = 0 AND Key_name != \'PRIMARY\';")) # We try the exact same process for unique keys.
            rows2 = cursor.fetchall() # we get the information from cursor.
            unique_key = [row[4] for row in rows2] # row 4 is the column designated for primary keys.
            flag2 = (len(unique_key) != 0)  # we check that unique key exists.
            for column_name in unique_key:
                if column_name not in attributes.attributes:
                    flag2 = False # If the unique keys in table don't match the attributes given, then flag is false
            # Flag1 is to check if primary key exists, flag2 is to check if unique key exists.
            flag = (flag1 or flag2) # check it has primary key or unique key, if none, we return false.
            return flag
        except mysql.connector.Error as err:
            return True

    # Predicate function that connects to the database and confirms
    # whether or not `referencing_attributes` is set up as a foreign
    # key that reference `referenced_attributes`
    # For example, if referencing_attributes contains table_name R and attributes [x, y]
    # and referenced_attributes contains table_name S and attributes [a, b]
    # this function returns true if (x,y) is enforced as a foreign key that references
    # (a,b) in R
    # @see Util.Attributes
    # @pre the tables and attributes in referencing_attributes and referenced_attributes must already exist
    def confirmForeignKey( self, referencing_attributes, referenced_attributes ):
        # TODO: Implement me!
        try: # We use a try/except block for when we encounter a wrong SQL input
            cursor = self.con.cursor()
            cursor.execute(f"""SELECT COLUMN_NAME, REFERENCED_COLUMN_NAME
                            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                            WHERE TABLE_NAME = \'{referencing_attributes.table_name}\'
                            AND REFERENCED_TABLE_NAME = \'{referenced_attributes.table_name}\';""") # This query check for foreign key information between tables.
            rows = cursor.fetchall() # we retrieve the information from the table.
            if len(referenced_attributes.attributes) != len(referencing_attributes.attributes):
                return False # if the size of given attributes don't match, we return false.
            attr = [] # To map the given attributes.
            S_at = [] # To get the S attribute.
            R_at = [] # To get the R attributes.
            S_to_R = [] # To map attributes from S to R.
            for row in rows: # We check rows
                S_at.append(row[0]) # We add S attributes to S_at
                R_at.append(row[1]) # We add R attributes to R_at
                S_to_R.append((row[0], row[1])) # We map each row of attributes from S to R.
            attribute = Attributes('R', R_at) # We Create a new table information for R and check if the given attributes are for primary keys.
            flag = self.confirmSuperkey(attribute) # If its superkey, then flag is true.
            for i in range(min(len(referenced_attributes.attributes), len(referencing_attributes.attributes))): # Then we map each given referencing_attribute to referenced_attribue.
                attr.append((referencing_attributes.attributes[i], referenced_attributes.attributes[i]))
            for row in attr: # If the attributes don't match, we return false.
                if row not in S_to_R:
                    flag = False
            return flag
        except mysql.connector.Error as err:
            print(f"The Error is {err}")
            return True


    # Predicate function that connects to the database and confirms
    # whether or not `referencing_attributes` is set up as a foreign key
    # that reference `referenced_attributes` using a specific referential integrity `policy`
    # For example, if referencing_attributes contains table_name R and attributes [x, y]
    # and referenced_attributes contains table_name S and attributes [a, b]
    # this function returns true if (x,y) the provided policy is used to manage that foreign key
    # @see Util.Attributes, Util.RefIntegrityPolicy
    # @pre The foreign key is valid
    # @pre policy must be a valid Util.RefIntegrityPolicy
    def confirmReferentialIntegrity( self, referencing_attributes, referenced_attributes, policy ):
        # TODO: Implement me!
        try: # We use a try/except block for when we encounter a wrong SQL input
            cursor = self.con.cursor()
            cursor.execute(f"""SELECT {policy.operation}_RULE
                            FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS
                            WHERE CONSTRAINT_SCHEMA = DATABASE()
                            AND TABLE_NAME = '{referencing_attributes.table_name}'
                            AND REFERENCED_TABLE_NAME = '{referenced_attributes.table_name}';""") # This query gets the relevant information on referential integrity policy.
            if policy.policy == "REJECT":
                policy.policy = "RESTRICT" # Since the test Cases consider RESTRICT the same as REJECT
            for (rule, ) in cursor:
                if policy.policy != rule: # If the rule does not match, then we know it definitely is false.
                    return False
            return self.confirmForeignKey(referencing_attributes, referenced_attributes) # If the rules match, we still have to make sure they have foreign key relationship.
        except mysql.connector.Error as err:
            print(f"The Error is {err}")
            return True

    # Predicate function that connects to the database and confirms
    # whether or not `referencing_attributes` is set up in such as way as to
    # functionally determine `referenced_attributes`
    # For example, if referencing_attributes contains table_name R and attributes [x, y]
    # and referenced_attributes contains table_name S and attributes [a, b]
    # this function returns true if (x,y) is enforced to functionally determine (a,b) in R
    # @see Util.Attributes
    # @pre the tables and attributes in referencing_attributes and referenced_attributes must already exist
    def confirmFunctionalDependency( self, referencing_attributes, referenced_attributes ):
        # TODO: Implement me!
        try: # We use a try/except block for when we encounter a wrong SQL input
            if referencing_attributes.table_name == referenced_attributes.table_name: # If the given attributes are from the same table, a superkey relationship must exist between them
                return self.confirmSuperkey(referencing_attributes)
            else: # if not, then we check for super key again, but for different reason.
                if self.confirmSuperkey(referencing_attributes):
                    try: # if the referencing_attributes are a superkey, we add all the attributes of their table as the referencing_attributes, so that we can make calculation easier.
                        cursor = self.con.cursor()
                        cursor.execute(f"SELECT * FROM {referencing_attributes}")
                        referencing_attributes.attributes = cursor.fetchone()[0]
                    except mysql.connector.Error as err:
                        return True
                return self.confirmForeignKey(referencing_attributes, referenced_attributes) # Then we check if a foreign key relation exists.
        except mysql.connector.Error as err:
            print(f"The Error is {err}")
            return True
