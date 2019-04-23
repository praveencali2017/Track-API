from sqlalchemy import create_engine
from utils import log_msg

class DBHelper:
    """
    Class that holds all the DB (Database) operations
    """
    def get_connection(self):
        """
        Initializes the database connection object
        :return: connection object
        """
        db_conn=create_engine("sqlite:///data_dump.db")
        return db_conn

    def query_builder(self, columns, table, where=None, statement="select"):
        """
        Builds the SQL query based on the given statement and conditions
        :param columns: Table columns
        :param table: Table name
        :param where: Conditions in plain string
        :param statement: Select|Update|Delete|Insert
        :return: Sql Query string
        """
        if statement== "select":
            select_template = "select {} from {}"
            query=select_template.format(columns, table)
            if where:
                query=query+" where {}".format(where)
            log_msg(query)
            return query

        elif statement== "update":
            update_template="update {} set {} where {}"
            columns_builder=""
            for i, column in enumerate(columns):
                columns_builder += column + "= '" + str(columns[column])+"'"
                if i!=len(columns)-1:
                    columns_builder+=" ,"
            query = update_template.format(table, columns_builder, where)
            log_msg(query)
            return query

        elif statement== "delete":
            delete_template="delete from {} where {}"
            query=delete_template.format(table, where)
            return query

        elif statement== "post":
            insert_template="INSERT INTO {} ({}) VALUES({})"
            query=insert_template.format(table, ','.join(map(str,columns.keys())), ','.join(map(lambda x: "'"+str(x)+"'",columns.values())))
            return query

    def get_all(self,table,columns, where=None):
        """
        Fetches all the records for the given table
        :param table: Table name
        :param columns: Table columns
        :param where: Conditions
        :return: Result set | Exception object (if error)
        """
        try:
            if table:
               query = self.query_builder(columns, table, where)
               result=self.get_connection().execute(query)
               return [dict(zip(tuple(result.keys()), record)) for record in result.cursor]
        except Exception as e:
            log_msg("Wrong columns or table name, please check the values")
            return e

    def update(self, table, columns, where):
        """
        Updates the record for the given where clause
        :param table: Table name
        :param columns: Table columns
        :param where: conditions
        :return: Msg (Success | Failed)
        """
        query=self.query_builder(columns,table,where,"update")
        result = self.get_connection().execute(query)
        if result.rowcount>=1:
           return "Updated the Record!!!"
        else:
           return "Not able to update the Record!!!"

    def delete(self, table, columns, where):
        """
        Deletes the given record
        :param table: Table name
        :param columns: Table columns
        :param where: condition (primary key)
        :return: Msg (Success | Failed)
        """
        query = self.query_builder(columns, table, where, "delete")
        result=self.get_connection().execute(query)
        if result.rowcount>=1:
           return "Deleted the Record!!!"
        else:
           return "Not able to delete the Record!!!"

    def insert(self, table, columns):
        """
        Inserts the new record
        :param table: Table name
        :param columns: Table columns
        :return: Msg (Success | Failed)
        """
        query = self.query_builder(columns, table, statement="post")
        result = self.get_connection().execute(query)
        if result.rowcount >= 1:
            return "Record has been added!!!"
        else:
            return "Unable to add record, please check values' type or record columns"




