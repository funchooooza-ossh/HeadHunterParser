from pathlib import Path
import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = Path('.','.env')
load_dotenv(dotenv_path)

class db:

    def connect():
        connection = psycopg2.connect(
            host = os.getenv('host'),
            user = os.getenv('user'),
            password = os.getenv('password'),
            dbname = os.getenv('db_name')
            )
        if connection: return connection
        else: return ("Connection failed")
    
    def inputdata(vacancy,salary,company,location,description,url):
        try:
            connection = db.connect()
            with connection.cursor() as c:
                c.execute(f"SELECT * FROM vacancies WHERE vacancy = '{vacancy}' AND company = '{company}' AND location = '{location}' ")
                if c.fetchone() == None:
                    print('Done\n')
                    c.execute(f"INSERT INTO vacancies (vacancy, salary, company, location, description, url) VALUES ('{vacancy}', '{salary}', '{company}', '{location}', '{description}', '{url}')")
                else:
                    print('Vacancy already in base\n')    

        except Exception as ex:
            print(ex)
        finally:
            connection.commit()
            c.close()
            connection.close()



