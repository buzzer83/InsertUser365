from hmac import new

from user import User
import psycopg
from datetime import date

lista_licenze = [3]

def get_data():
    with open('insert.txt') as f:
        lines = f.readlines()
        lines_clean = []

        for line in lines:
            lines_clean.append(line.replace("\n", ""))

        count = 0
        utente = User()
        for line in lines_clean:
            match count:
                case 0:
                    utente.name = line.strip()
                case 1:
                    utente.surname = line.strip()
                case 2:
                    utente.username_short = line.strip()
                case 3:
                    utente.username = line
                case 4:
                    utente.password = line
                case 5:
                    utente.password_citrix = line
                case 7:
                    utente.job_title = line
                case 8:
                    utente.entity_number = line
                case 9:
                    utente.data_start = line

            count = count + 1

        utente.print()
        return utente

def inserisci_utente(utente, lista_licenze):
    with psycopg.connect("dbname=matica user=postgres port=5432 password=zRZkXB!FCl?Sju2#Q4b3") as conn:
        with conn.cursor() as cur:
            sql_employee = "INSERT INTO employee (name, surname) VALUES ('{0}','{1}') RETURNING oid".format(
                utente.name, utente.surname)
            print(sql_employee)
            cur.execute(sql_employee)
            data_oid_user = cur.fetchone()
            utente.oid = data_oid_user[0]

            sql_employee2entity = "INSERT INTO employee2entity (oid_employee, oid_entity, data_start) " \
                                  "VALUES ('{0}','{1}', '{2}')".format(
                utente.oid, utente.entity_number, utente.data_start)
            print(sql_employee2entity)
            cur.execute(sql_employee2entity)

            for licenza in lista_licenze:
                sql_user = "INSERT INTO users (username, oid_license, oid_user) " \
                        "VALUES ('{0}', {1}, {2})".format(utente.username, licenza, utente.oid)
                print(sql_user)
                cur.execute(sql_user)

def create_mail_general(utente):
    print("Hi " + utente.name + ",\n")
    print("Welcome in Matica.\n")
    print("credentials to Matica services will be sent in a separate email.\n")
    print("the signature at the bottom of the e-mail is automatic, you don't need to set it.\n")
    print("signature of the e-mail sent inside Matica:\n\n")
    print("e-mail signature for contacts outside Matica:\n\n")
    print("All Matica documents must be saved:")
    print("on OneDrive if they are not shared with other colleagues")
    print("on SharePoint sites if these are shared with other colleagues.\n")
    print("write me for any doubt\n")
    print("good work")
    print("\n\n")

def create_mail_personal(utente):
    print("Hi " + utente.name + ",\n")
    print("below your credentials:\n")
    print("Windows (domain):")
    print("\t username: " + utente.username_short)
    print("\t password: " + utente.password + "\n")
    print("Microsoft Office 365:")
    print("\t username: " + utente.username)
    print("\t password: " + utente.password + "\n")

    if 1 in lista_licenze:
        print("Citrix:")
        print("\t username: " + utente.username_short + "_mtc")
        print("\t password: " + utente.password_citrix + "\n")
        print("SAP B1:")
        print("\t username: " + utente.username_short)
        print("\t password: 1234\n")

    print("changing passwords is strongly recommended\n")
    print("Best Regards")


if __name__ == '__main__':
    utente = get_data()
    inserisci_utente(utente, lista_licenze)
    create_mail_general(utente)
    create_mail_personal(utente)
