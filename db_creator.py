import pymysql

# Подключение к базе данных
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    # Создание курсора для выполнения SQL-запросов
    with connection.cursor() as cursor:
        # Создание базы данных
        sql_create_db = "CREATE DATABASE IF NOT EXISTS HotelManagement"
        cursor.execute(sql_create_db)
    
    # Подключение к созданной базе данных
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='HotelManagement',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    # Создание курсора для выполнения SQL-запросов
    with connection.cursor() as cursor:
        # Создание таблицы Reservations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reservations (
                idReservation INT AUTO_INCREMENT PRIMARY KEY,
                idReservStatus INT NOT NULL,
                idReservType INT NOT NULL,
                idIndividual INT,
                idReservContract INT,
                idRoom INT NOT NULL,
                numOfPeople INT NOT NULL,
                arrivalDate DATE NOT NULL,
                departureDate DATE NOT NULL,
                price FLOAT NOT NULL,
                duty FLOAT NOT NULL
            )
        """)

        # Создание таблицы ReservationStatuses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ReservationStatuses (
                idReservStatus INT AUTO_INCREMENT PRIMARY KEY,
                status VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы ReservationTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ReservationTypes (
                idReservType INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(255) NOT NULL
            )
        """)
        
        # Создание таблицы Individuals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Individuals (
                idIndividual INT AUTO_INCREMENT PRIMARY KEY,
                fullName VARCHAR(255) NOT NULL,
                dateOfBirth DATE NOT NULL,
                idDocType INT NOT NULL,
                documentNumber INT NOT NULL,
                contactInfo VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы DocumentTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DocumentTypes (
                idDocType INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы ReservationContracts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ReservationContracts (
                idReservContract INT AUTO_INCREMENT PRIMARY KEY,
                idOrganization INT NOT NULL,
                numOfRooms INT NOT NULL,
                numOfPeople INT NOT NULL,
                dateOfSigning DATE NOT NULL,
                arrivalDate DATE NOT NULL,
                departureDate DATE NOT NULL,
                price FLOAT NOT NULL
            )
        """)

        # Создание таблицы Organizations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Organizations (
                idOrganization INT AUTO_INCREMENT PRIMARY KEY,
                idOrgType INT NOT NULL,
                orgName VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы OrganizationTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OrganizationTypes (
                idOrgType INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы ServicesSales
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ServicesSales (
                idServiceSale INT AUTO_INCREMENT PRIMARY KEY,
                idReservation INT NOT NULL,
                idService INT NOT NULL,
                saleDate DATE NOT NULL,
                amount INT NOT NULL,
                price FLOAT NOT NULL
            )
        """)

        # Создание таблицы Services
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Services (
                idService INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                idServiceType INT NOT NULL,
                price FLOAT NOT NULL
            )
        """)

        # Создание таблицы ServiceTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ServiceTypes (
                idServiceType INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы Complaints
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Complaints (
                idComplaint INT AUTO_INCREMENT PRIMARY KEY,
                idReservation INT NOT NULL,
                textOfTheComplaint TEXT NOT NULL,
                dateOfComplaint DATE NOT NULL,
                idComplaintStatus INT NOT NULL
            )
        """)

        # Создание таблицы ComplaintStatuses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ComplaintStatuses (
                idComplaintStatus INT AUTO_INCREMENT PRIMARY KEY,
                status VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы Rooms
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                idRoom INT AUTO_INCREMENT PRIMARY KEY,
                idBuilding INT NOT NULL,
                floor INT NOT NULL,
                idRoomType INT NOT NULL,
                price FLOAT NOT NULL,
                idRoomStatus INT NOT NULL
            )
        """)

        # Создание таблицы RoomTypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RoomTypes (
                idRoomType INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы RoomStatuses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RoomStatuses (
                idRoomStatus INT AUTO_INCREMENT PRIMARY KEY,
                status VARCHAR(255) NOT NULL
            )
        """)

        # Создание таблицы Buildings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Buildings (
                idBuilding INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                idHotelClass INT NOT NULL,
                numOfFloors INT NOT NULL,
                numOfRooms INT NOT NULL,
                numOfRoomsOnTheFloor INT NOT NULL
            )
        """)

        # Создание таблицы HotelClasses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS HotelClasses (
                idHotelClass INT AUTO_INCREMENT PRIMARY KEY,
                hotelClass VARCHAR(255) NOT NULL
            )
        """)
        
    # Подтверждение операций создания таблиц
    connection.commit()

    # Создание курсора для выполнения SQL-запросов
    with connection.cursor() as cursor:
        # Добавление внешнего ключа в таблицу Reservations, который ссылается на таблицу ReservationContracts
        cursor.execute("""
            ALTER TABLE Reservations
            ADD CONSTRAINT fk_org_contract
            FOREIGN KEY (idReservContract)
            REFERENCES ReservationContracts(idReservContract)
        """)

        # Добавление внешнего ключа в таблицу ReservationContracts, который ссылается на таблицу Organizations
        cursor.execute("""
            ALTER TABLE ReservationContracts
            ADD CONSTRAINT fk_org_id
            FOREIGN KEY (idOrganization)
            REFERENCES Organizations(idOrganization)
        """)

        # Добавление внешнего ключа в таблицу Organizations, который ссылается на таблицу OrganizationTypes
        cursor.execute("""
            ALTER TABLE Organizations
            ADD CONSTRAINT fk_org_type
            FOREIGN KEY (idOrgType)
            REFERENCES OrganizationTypes(idOrgType)
        """)

        # Добавление внешнего ключа в таблицу Reservations, который ссылается на таблицу Individuals
        cursor.execute("""
            ALTER TABLE Reservations
            ADD CONSTRAINT fk_individual
            FOREIGN KEY (idIndividual)
            REFERENCES Individuals(idIndividual)
        """)

        # Добавление внешнего ключа в таблицу Individuals, который ссылается на таблицу DocumentTypes
        cursor.execute("""
            ALTER TABLE Individuals
            ADD CONSTRAINT fk_doc_type
            FOREIGN KEY (idDocType)
            REFERENCES DocumentTypes(idDocType)
        """)

        # Добавление внешнего ключа в таблицу ServicesSales, который ссылается на таблицу Reservations
        cursor.execute("""
            ALTER TABLE ServicesSales
            ADD CONSTRAINT fk_reservs_sales
            FOREIGN KEY (idReservation)
            REFERENCES Reservations(idReservation)
        """)

        # Добавление внешнего ключа в таблицу ServicesSales, который ссылается на таблицу Services
        cursor.execute("""
            ALTER TABLE ServicesSales
            ADD CONSTRAINT fk_services
            FOREIGN KEY (idService)
            REFERENCES Services(idService)
        """)

        # Добавление внешнего ключа в таблицу Services, который ссылается на таблицу ServiceTypes
        cursor.execute("""
            ALTER TABLE Services
            ADD CONSTRAINT fk_service_types
            FOREIGN KEY (idServiceType)
            REFERENCES ServiceTypes(idServiceType)
        """)

        # Добавление внешнего ключа в таблицу Reservations, который ссылается на таблицу ReservationStatuses
        cursor.execute("""
            ALTER TABLE Reservations
            ADD CONSTRAINT fk_reserv_status
            FOREIGN KEY (idReservStatus)
            REFERENCES ReservationStatuses(idReservStatus)
        """)

        # Добавление внешнего ключа в таблицу Reservations, который ссылается на таблицу ReservationTypes
        cursor.execute("""
            ALTER TABLE Reservations
            ADD CONSTRAINT fk_reserv_type
            FOREIGN KEY (idReservType)
            REFERENCES ReservationTypes(idReservType)
        """)

        # Добавление внешнего ключа в таблицу Complaints, который ссылается на таблицу Reservations
        cursor.execute("""
            ALTER TABLE Complaints
            ADD CONSTRAINT fk_reservs_compl
            FOREIGN KEY (idReservation)
            REFERENCES Reservations(idReservation)
        """)

        # Добавление внешнего ключа в таблицу Complaints, который ссылается на таблицу ComplaintStatuses
        cursor.execute("""
            ALTER TABLE Complaints
            ADD CONSTRAINT fk_compl_status
            FOREIGN KEY (idComplaintStatus)
            REFERENCES ComplaintStatuses(idComplaintStatus)
        """)

        # Добавление внешнего ключа в таблицу Reservations, который ссылается на таблицу Rooms
        cursor.execute("""
            ALTER TABLE Reservations
            ADD CONSTRAINT fk_room
            FOREIGN KEY (idRoom)
            REFERENCES Rooms(idRoom)
        """)

        # Добавление внешнего ключа в таблицу Rooms, который ссылается на таблицу Buildings
        cursor.execute("""
            ALTER TABLE Rooms
            ADD CONSTRAINT fk_building
            FOREIGN KEY (idBuilding)
            REFERENCES Buildings(idBuilding)
        """)

        # Добавление внешнего ключа в таблицу Buildings, который ссылается на таблицу HotelClasses
        cursor.execute("""
            ALTER TABLE Buildings
            ADD CONSTRAINT fk_hotel_class
            FOREIGN KEY (idHotelClass)
            REFERENCES HotelClasses(idHotelClass)
        """)

        # Добавление внешнего ключа в таблицу Rooms, который ссылается на таблицу RoomTypes
        cursor.execute("""
            ALTER TABLE Rooms
            ADD CONSTRAINT fk_room_type
            FOREIGN KEY (idRoomType)
            REFERENCES RoomTypes(idRoomType)
        """)

        # Добавление внешнего ключа в таблицу Rooms, который ссылается на таблицу RoomStatuses
        cursor.execute("""
            ALTER TABLE Rooms
            ADD CONSTRAINT fk_room_status
            FOREIGN KEY (idRoomStatus)
            REFERENCES RoomStatuses(idRoomStatus)
        """)

    # Подтверждение операций создания связей
    connection.commit()

finally:
    # Закрытие подключения
    connection.close()
