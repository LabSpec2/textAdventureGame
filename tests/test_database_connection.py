import unittest

from sqlalchemy import create_engine, MetaData, Table, select


class TestDatabase(unittest.TestCase):
    db_string = f"db2://gvs78140:x6v72xdc0%5Eh5h9tj@dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net:50000/BLUDB"

    tables_names = ['games', 'heroes', 'monsters', 'objects', 'rooms',
                    'rooms_monsters', 'rooms_object', 'stats', 'users']

    engine = None
    metadata = MetaData()

    def test_00_engine_connection(self):
        TestDatabase.engine = create_engine(self.db_string)
        self.assertIsNotNone(self.engine)

    def test_01_table_name_check(self):
        for table in self.engine.table_names():
            self.assertIn(table, self.tables_names)

            t = Table(table, self.metadata, autoload=True, autoload_with=self.engine)

            self.assertGreater(len(t.columns.keys()), 0)

            print("\n Table name: {}".format(table))
            print("Keys: ", t.columns.keys())


if __name__ == "__main__":
    unittest.main()