import pymysql

try:
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='',
                                 db='HotelManagement',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    # Создание курсора для выполнения SQL-запросов
    with connection.cursor() as cursor:
        # Создание пользователей
        cursor.execute("""
            CREATE USER 'admin'@'localhost' IDENTIFIED BY '123';
        """)

        # Подтверждение операций создания пользователей
        connection.commit()

        # Создание пользователей
        cursor.execute("""
            CREATE USER 'economist'@'localhost' IDENTIFIED BY '00000';
        """)

        # Подтверждение операций создания пользователей
        connection.commit()

        # Создание пользователей
        cursor.execute("""
            CREATE USER 'director'@'localhost' IDENTIFIED BY 'extra_hard_password';
        """)

        # Подтверждение операций создания пользователей
        connection.commit()

        # Награждение пользователей правами
        queries = [
            "GRANT SELECT ON HotelManagement.Reservations TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.Reservations TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.Reservations TO 'admin'@'localhost';",

            "GRANT SELECT ON HotelManagement.Individuals TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.Individuals TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.Individuals TO 'admin'@'localhost';",

            "GRANT SELECT ON HotelManagement.ReservationContracts TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.ReservationContracts TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.ReservationContracts TO 'admin'@'localhost';",

            "GRANT SELECT ON HotelManagement.Organizations TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.Organizations TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.Organizations TO 'admin'@'localhost';",

            "GRANT SELECT ON HotelManagement.ServicesSales TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.ServicesSales TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.ServicesSales TO 'admin'@'localhost';",

            "GRANT SELECT ON HotelManagement.Complaints TO 'admin'@'localhost';",
            "GRANT INSERT ON HotelManagement.Complaints TO 'admin'@'localhost';",
            "GRANT UPDATE ON HotelManagement.Complaints TO 'admin'@'localhost';",

            "GRANT SELECT(idRoomStatus) ON HotelManagement.Rooms TO 'admin'@'localhost';",
            "GRANT UPDATE(idRoomStatus) ON HotelManagement.Rooms TO 'admin'@'localhost';",

            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetAvailableRoomsWithParams TO 'admin'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetRoomsToBeVacantOnTheDate TO 'admin'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetGuestInformation TO 'admin'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetFirmsWithReservationContracts TO 'admin'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetGuestPaymentInfo TO 'admin'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE hotelmanagement.CheckInClientByReservationId TO 'admin'@'localhost';",


            "GRANT SELECT ON HotelManagement.Reservations TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.Individuals TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.ReservationContracts TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.Organizations TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.ServicesSales TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.Complaints TO 'economist'@'localhost';",
            "GRANT SELECT ON HotelManagement.Rooms TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetFirmsByReservationVolume TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetGuestsByRoomCharacteristics TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetReservationVolumeAndPreferredRooms TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetFirmsWithReservationContracts TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.GetRoomStatistics TO 'economist'@'localhost';",
            "GRANT EXECUTE ON PROCEDURE HotelManagement.CalculateHotelRevenue TO 'economist'@'localhost';",

            "GRANT ALL PRIVILEGES ON HotelManagement.* TO 'director'@'localhost';"
        ]

        for query in queries:
            cursor.execute(query)


         # Подтверждение операций создания пользователей
        connection.commit()

finally:
    # Закрытие подключения
    connection.close()
