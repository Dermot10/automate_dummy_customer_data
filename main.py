import random
import datetime
import sys
import time
import names
import database
import log


class FakeCustomerGenerator:
    def __init__(self, conn, logger, start_year=1923, end_year=2005):
        self.conn = conn
        self.logger = logger
        self.start_year = start_year
        self.end_year = end_year
        self.prefix = '44'
        self.city = 'LDN'

    def get_random_gender(self):
        """Helper function to randomly pick gender"""
        genders = ['M', 'F']
        gender = random.choice(genders)
        return gender

    def create_first_name(self):
        """Function will randomly choose gender and then a name from list based on gender"""
        gender = self.get_random_gender()
        first_name = None

        if gender == 'M':
            first_name = random.choice(names.male_first_names)
        elif gender == 'F':
            first_name = random.choice(names.female_first_names)
        else:
            print('No string recognised')

        return first_name

    def create_last_name(self):
        """Select random last name from list"""
        last_name = random.choice(names.last_names)
        return last_name

    def create_random_date_of_birth(self):
        """Function to randomly create date of birth between initialised start and end year"""
        year = random.randint(self.start_year, self.end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)

        date_of_birth = datetime.datetime(year, month, day)
        return date_of_birth.strftime('%Y-%m-%d')

    def create_dummy_phone_number(self):
        """Randomly generate phone number"""
        num = random.randint(1000000000, 9999999999)
        phone_number = int(self.prefix + str(num))
        return phone_number

    def create_dummy_address(self):
        """Function to create dummy address"""
        house_number = random.randint(1, 200)
        street_name = random.choice(names.commmon_street_names)
        address = (f"{house_number} {street_name}")
        return address

    def create_dummy_london_postcode(self):
        """Function to create dummy postcode"""
        alphabet = ["", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K",
                    "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        outward_code = random.choice(
            ["E", "EC", "N", "NW", "SE", "SW", "W", "WC"])  # London Area Codes
        inward_code = str(random.randint(0, 9))  # random
        postal_unit = ""
        i = 0
        while i < 2:
            postal_unit += random.choice(alphabet)
            i += 1

        return f"{outward_code}{inward_code} {random.randint(1, 99)}{postal_unit}"

    def build_dummy_email(self):
        """Function to create dummy email from first and last name"""
        first_name = self.create_first_name()
        last_name = self.create_last_name()
        email = (f"{first_name.lower()}.{last_name.lower()}@fakedomain.com")
        return email

    def create_sql_payload(self):
        """Function to create SQL payload, pools other return values"""

        first_name = self.create_first_name()
        last_name = self.create_last_name()
        date_of_birth = self.create_random_date_of_birth()
        gender = None
        address = self.create_dummy_address()
        post_code = self.create_dummy_london_postcode()
        if first_name in names.male_first_names:
            gender = 'M'
        elif first_name in names.female_first_names:
            gender = 'F'
        email = (f"{first_name.lower()}.{last_name.lower()}@fakedomain.com")
        phone_number = str(self.create_dummy_phone_number())
        now = datetime.datetime.now()  # get current datetime
        date_registered = now.date()

        customer_data_payload = [first_name, last_name, date_of_birth, gender,
                                 self.city, address, post_code, email, phone_number, date_registered]

        return customer_data_payload

    def sql_insert(self, conn):
        """
        insert dummy data into the table, 
        :param conn    
        """
        data_to_insert = self.create_sql_payload()
        sql = f"""
        INSERT INTO Customers(
            FirstName, LastName, DateOfBirth, Gender, City, Address1, PostCode, EmailAddress, PhoneNo, DateRegistered, TimestampOrdered
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, CURRENT_TIMESTAMP());
        """

        cursor.execute(sql, data_to_insert)
        conn.commit()
        conn.close()
        return data_to_insert

    def run(self, conn):
        """ Create 'x' amount of Customers based on inputted value"""
        input_value = int(sys.argv[1])
        print(f"Number of Customers being created - {input_value}")
        i = 1
        while i <= input_value:
            try:
                data = self.sql_insert(conn)
                print(data)
                print("Record successfully entered")
                time.sleep(2)
            except Exception as e:
                print(f"Failed to create record, error - {e}")
            i += 1


if __name__ == "__main__":
    conn = database.connection
    cursor = conn.cursor()
    logger = log.logger
    customer = FakeCustomerGenerator(conn, logger)
    print("")
    customer.run(conn)
