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
        # Создание хранимой процедуры 1 запроса
        cursor.execute("""          
            CREATE PROCEDURE GetFirmsByReservationVolume(
                IN min_reservation_volume INT,
                IN start_date DATE,
                IN end_date DATE
            )
            BEGIN
                DECLARE firm_names_list VARCHAR(1000);
                DECLARE total_firms INT;
                
                IF  min_reservation_volume < 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Значение минимального объема должно быть положительным';
                END IF;
                       
                IF  start_date > end_date THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата начала бронирования не может быть позже даты окончания';
                END IF;

                SELECT GROUP_CONCAT(Organizations.orgName SEPARATOR ', ') INTO firm_names_list
                FROM (
                    SELECT Organizations.idOrganization
                    FROM Organizations
                    INNER JOIN ReservationContracts ON Organizations.idOrganization = ReservationContracts.idOrganization
                    INNER JOIN Reservations ON ReservationContracts.idReservContract = Reservations.idReservContract
                    WHERE (start_date IS NULL OR Reservations.arrivalDate >= start_date)
                        AND (end_date IS NULL OR Reservations.departureDate <= end_date)
                        AND NOT (Reservations.idReservStatus = 3)
                    GROUP BY Organizations.idOrganization
                    HAVING SUM(ReservationContracts.numOfRooms) >= min_reservation_volume
                ) AS firms_with_min_reservation_volume
                INNER JOIN Organizations ON firms_with_min_reservation_volume.idOrganization = Organizations.idOrganization;

                SELECT COUNT(*) INTO total_firms
                FROM (
                    SELECT Organizations.idOrganization
                    FROM Organizations
                    INNER JOIN ReservationContracts ON Organizations.idOrganization = ReservationContracts.idOrganization
                    INNER JOIN Reservations ON ReservationContracts.idReservContract = Reservations.idReservContract
                    WHERE (start_date IS NULL OR Reservations.arrivalDate >= start_date)
                        AND (end_date IS NULL OR Reservations.departureDate <= end_date)
                    GROUP BY Organizations.idOrganization
                    HAVING SUM(ReservationContracts.numOfRooms) >= min_reservation_volume
                ) AS firms_with_min_reservation_volume;

                SELECT firm_names_list, total_firms;
            END;
        """)

        # Создание хранимой процедуры 2 запроса
        cursor.execute("""
            CREATE PROCEDURE GetGuestsByRoomCharacteristics(
                IN building_id INT,
                IN floor INT,
                IN room_type_name VARCHAR(255),
                IN price FLOAT,
                IN room_status_name VARCHAR(255),
                IN start_date DATE,
                IN end_date DATE
            )
            BEGIN
                DECLARE guest_list VARCHAR(1000);
                DECLARE total_guests INT;
                DECLARE type_count INT;
                DECLARE status_count INT;
                DECLARE build_count INT;
                DECLARE floor_num INT;
                
                       
                IF room_type_name IS NOT NULL THEN
                    SELECT COUNT(*) INTO type_count
                    FROM RoomTypes
                    WHERE type = room_type_name;
                    
                    IF type_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого типа номера не существует';
                    END IF;
                END IF;
                       
                IF room_status_name IS NOT NULL THEN
                    SELECT COUNT(*) INTO status_count
                    FROM RoomStatuses
                    WHERE status = room_status_name;
                    
                    IF status_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого статуса номера не существует';
                    END IF;
                END IF;

                IF building_id IS NOT NULL THEN
                    SELECT COUNT(*) INTO build_count
                    FROM Buildings
                    WHERE idBuilding = building_id;
                    
                    IF build_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого корпуса не существует';
                    END IF;
                END IF;
                       
                IF  floor IS NOT Null AND building_id IS NOT NULL THEN
                    SELECT numOfFloors INTO floor_num
                    FROM Buildings
                    WHERE idBuilding = building_id;
                    
                    IF floor_num < floor THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такой этаж не существует в заданном корпусе';
                    END IF;
                END IF;
                       
                IF  floor IS NOT Null AND floor <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Номер этажа должен быть больше нуля';
                END IF;
                    
                IF  price IS NOT Null AND price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительгным числом';
                END IF;
                       
                IF  start_date > end_date THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Начало периода не может быть после его конца';
                END IF;

                SELECT GROUP_CONCAT(Individuals.fullName SEPARATOR ', ') INTO guest_list
                FROM Individuals
                INNER JOIN Reservations ON Individuals.idIndividual = Reservations.idIndividual
                INNER JOIN Rooms ON Reservations.idRoom = Rooms.idRoom
                INNER JOIN RoomTypes ON Rooms.idRoomType = RoomTypes.idRoomType
                INNER JOIN RoomStatuses ON Rooms.idRoomStatus = RoomStatuses.idRoomStatus
                WHERE (building_id IS NULL OR Rooms.idBuilding = building_id)
                    AND (floor IS NULL OR Rooms.floor = floor)
                    AND (room_type_name IS NULL OR RoomTypes.type = room_type_name)
                    AND (price IS NULL OR Rooms.price = price)
                    AND (room_status_name IS NULL OR RoomStatuses.status = room_status_name)
                    AND (start_date IS NULL OR Reservations.arrivalDate >= start_date)
                    AND (end_date IS NULL OR Reservations.departureDate <= end_date)
                    AND (Reservations.idReservStatus = 4);

                SELECT SUM(Reservations.numOfPeople) INTO total_guests
                FROM Individuals
                INNER JOIN Reservations ON Individuals.idIndividual = Reservations.idIndividual
                INNER JOIN Rooms ON Reservations.idRoom = Rooms.idRoom
                INNER JOIN RoomTypes ON Rooms.idRoomType = RoomTypes.idRoomType
                INNER JOIN RoomStatuses ON Rooms.idRoomStatus = RoomStatuses.idRoomStatus
                WHERE (building_id IS NULL OR Rooms.idBuilding = building_id)
                    AND (floor IS NULL OR Rooms.floor = floor)
                    AND (room_type_name IS NULL OR RoomTypes.type = room_type_name)
                    AND (price IS NULL OR Rooms.price = price)
                    AND (room_status_name IS NULL OR RoomStatuses.status = room_status_name)
                    AND (start_date IS NULL OR Reservations.arrivalDate >= start_date)
                    AND (end_date IS NULL OR Reservations.departureDate <= end_date)
                    AND (Reservations.idReservStatus = 4);

                SELECT guest_list, total_guests;
            END;
        """)

        # Создание хранимой процедуры 3 запроса
        cursor.execute("""
            CREATE PROCEDURE GetAvailableRoomsWithParams(
                IN building_id INT,
                IN floor INT,
                IN room_type_name VARCHAR(255),
                IN price FLOAT
            )
            BEGIN
                DECLARE available_rooms_count INT;
                DECLARE type_count INT;
                DECLARE build_count INT;
                DECLARE floor_num INT;
                    
                       
                IF room_type_name IS NOT NULL THEN
                    SELECT COUNT(*) INTO type_count
                    FROM RoomTypes
                    WHERE type = room_type_name;
                    
                    IF type_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого типа номера не существует';
                    END IF;
                END IF;
                       
                IF building_id IS NOT NULL THEN
                    SELECT COUNT(*) INTO build_count
                    FROM Buildings
                    WHERE idBuilding = building_id;
                    
                    IF build_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого корпуса не существует';
                    END IF;
                END IF;
                       
                IF  floor IS NOT Null AND building_id IS NOT NULL THEN  
                    SELECT numOfFloors INTO floor_num
                    FROM Buildings
                    WHERE idBuilding = building_id;
                    
                    IF floor_num < floor THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такой этаж не существует в заданном корпусе';
                    END IF;
                END IF;
                       
                IF  floor IS NOT Null AND floor <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Номер этажа должен быть больше нуля';
                END IF;
                    
                IF  price IS NOT Null AND price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительгным числом';
                END IF;

                SELECT COUNT(*) INTO available_rooms_count
                FROM Rooms
                INNER JOIN RoomTypes ON Rooms.idRoomType = RoomTypes.idRoomType
                INNER JOIN RoomStatuses ON Rooms.idRoomStatus = RoomStatuses.idRoomStatus
                WHERE (building_id IS NULL OR Rooms.idBuilding = building_id)
                    AND (floor IS NULL OR Rooms.floor = floor)
                    AND (room_type_name IS NULL OR RoomTypes.type = room_type_name)
                    AND (price IS NULL OR Rooms.price = price)
                    AND RoomStatuses.status = 'свободен';

                SELECT available_rooms_count;
            END;
        """)
        
        # Создание хранимой процедуры 4 запроса
        cursor.execute("""
            CREATE PROCEDURE GetRoomsToBeVacantOnTheDate(
                IN end_date DATE
            )
            BEGIN
                IF end_date IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Указание даты обязательно';
                END IF;
                    
                SELECT Rooms.idRoom
                FROM Rooms
                INNER JOIN RoomStatuses ON Rooms.idRoomStatus = RoomStatuses.idRoomStatus
                INNER JOIN Reservations ON Rooms.idRoom = Reservations.idRoom
                WHERE RoomStatuses.status = 'занят' AND Reservations.departureDate <= end_date AND NOT (Reservations.idReservStatus = 3);
            END
        """)

        # Создание хранимой процедуры 5 запроса
        cursor.execute("""
            CREATE PROCEDURE GetReservationVolumeAndPreferredRooms(
                IN firm_name VARCHAR(255),
                IN start_date DATE,
                IN end_date DATE
            )
            BEGIN
                DECLARE firm_count INT;

                IF firm_name IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ввод фирмы обязателен';
                END IF;

                IF firm_name IS NOT NULL THEN
                    SELECT COUNT(*) INTO firm_count
                    FROM Organizations
                    WHERE orgName = firm_name;

                    IF firm_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такой фирмы не существует';
                    END IF;
                END IF;

                IF start_date > end_date THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Начало периода не может быть после его конца';
                END IF;

                SELECT
                    orgName AS Organization,
                    COUNT(*) AS ReservationVolume,
                    GROUP_CONCAT(RoomTypes.type) AS PreferredRoomTypes
                FROM ReservationContracts
                INNER JOIN Organizations ON ReservationContracts.idOrganization = Organizations.idOrganization
                INNER JOIN Reservations ON ReservationContracts.idReservContract = Reservations.idReservContract
                INNER JOIN Rooms ON Reservations.idRoom = Rooms.idRoom
                INNER JOIN RoomTypes ON Rooms.idRoomType = RoomTypes.idRoomType
                WHERE Organizations.orgName = firm_name
                    AND ReservationContracts.arrivalDate >= start_date
                    AND ReservationContracts.departureDate <= end_date
                    AND NOT (Reservations.idReservStatus = 3)
                GROUP BY Organizations.orgName;
            END;
        """)

        # Создание хранимой процедуры 6 запроса
        cursor.execute("""
            CREATE PROCEDURE GetGuestInformation(
                IN room_id INT
            )
            BEGIN
                DECLARE guest_name VARCHAR(255);
                DECLARE guest_bill FLOAT;
                DECLARE guest_complaint TEXT;
                DECLARE guest_services VARCHAR(255);
                DECLARE room_count INT;
                       
                IF room_id IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Вводить номер комнаты обязательно';
                END IF;
                       
                IF room_id IS NOT NULL THEN
                    SELECT COUNT(*) INTO room_count
                    FROM Rooms
                    WHERE idRoom = room_id;
                    
                    IF room_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого номера не существует';
                    END IF;
                END IF;
                
                SELECT Individuals.fullName INTO guest_name
                FROM Individuals
                INNER JOIN Reservations ON Individuals.idIndividual = Reservations.idIndividual
                WHERE Reservations.idRoom = room_id;
                
                SELECT SUM(Services.price) INTO guest_bill
                FROM Reservations
                INNER JOIN ServicesSales ON Reservations.idReservation = ServicesSales.idReservation
                INNER JOIN Services ON ServicesSales.idService = Services.idService
                WHERE Reservations.idRoom = room_id
                AND ServicesSales.saleDate BETWEEN Reservations.arrivalDate AND Reservations.departureDate
                AND CURDATE() BETWEEN Reservations.arrivalDate AND Reservations.departureDate;
                
                SELECT Complaints.textOfTheComplaint INTO guest_complaint
                FROM Reservations
                INNER JOIN Complaints ON Reservations.idReservation = Complaints.idReservation
                WHERE Reservations.idRoom = room_id;
                
                SELECT GROUP_CONCAT(Services.title) INTO guest_services
                FROM Reservations
                INNER JOIN ServicesSales ON Reservations.idReservation = ServicesSales.idReservation
                INNER JOIN Services ON ServicesSales.idService = Services.idService
                WHERE Reservations.idRoom = room_id
                AND ServicesSales.saleDate BETWEEN Reservations.arrivalDate AND Reservations.departureDate
                AND CURDATE() BETWEEN Reservations.arrivalDate AND Reservations.departureDate;
                
                SELECT guest_name AS GuestName,
                    guest_bill AS Bill,
                    guest_complaint AS Complaint,
                    guest_services AS ServicesUsed;
            END;
        """)

        # Создание хранимой процедуры 7 запроса
        cursor.execute("""
            CREATE PROCEDURE GetFirmsWithReservationContracts(
                IN start_date DATE,
                IN end_date DATE
            )
            BEGIN    
                IF  start_date > end_date THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Начало периода не может быть после его конца';
                END IF;
                       
                SELECT Organizations.orgName, OrganizationTypes.type
                FROM Organizations
                INNER JOIN OrganizationTypes ON Organizations.idOrgType = OrganizationTypes.idOrgType
                INNER JOIN ReservationContracts ON Organizations.idOrganization = ReservationContracts.idOrganization
                WHERE ReservationContracts.arrivalDate >= start_date AND ReservationContracts.departureDate <= end_date;
            END;
        """)

        # Создание хранимой процедуры 8 запроса
        cursor.execute("""
            CREATE PROCEDURE GetRoomStatistics(
                IN room_id INT
            )
            BEGIN
                DECLARE total_stays INT;
                DECLARE total_complaints INT;
                DECLARE success_rate DECIMAL(5,2);
                DECLARE room_count INT;
                
                IF room_id IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Вводить номер комнаты обязательно';
                END IF;
                       
                IF room_id IS NOT NULL THEN
                    SELECT COUNT(*) INTO room_count
                    FROM Rooms
                    WHERE idRoom = room_id;
                    
                    IF room_count = 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такого номера не существует';
                    END IF;
                END IF;

                SELECT COUNT(*) INTO total_stays
                FROM Reservations
                WHERE idRoom = room_id;

                SELECT COUNT(*) INTO total_complaints
                FROM Reservations
                INNER JOIN Complaints ON Reservations.idReservation = Complaints.idReservation
                WHERE Reservations.idRoom = room_id AND (Reservations.idReservStatus = 4);

                IF total_stays > 0 THEN
                        IF total_complaints > 0 THEN
                            SET success_rate = (total_complaints / total_stays) * 100;
                        ELSE
                            SET success_rate = 100;
                        END IF;
                    ELSE
                        SET success_rate = 100;
                END IF;

                SELECT total_stays, total_complaints, success_rate;
            END;
        """)

        # Создание хранимой процедуры 9 запроса
        cursor.execute("""
           CREATE PROCEDURE CalculateHotelRevenue(
                IN start_date DATE,
                IN end_date DATE
            )
            BEGIN
                DECLARE total_revenue FLOAT;

                IF start_date > end_date THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Начало периода не может быть после его конца';
                END IF;

                SELECT SUM(ss.price) INTO total_revenue
                FROM ServicesSales ss
                INNER JOIN Reservations r ON ss.idReservation = r.idReservation
                WHERE r.arrivalDate BETWEEN start_date AND end_date AND r.idReservStatus != 3;

                SELECT total_revenue + SUM(r.price)
                INTO total_revenue
                FROM Reservations r
                WHERE r.arrivalDate BETWEEN start_date AND end_date AND r.idReservStatus != 3;

                SELECT total_revenue;
            END;
        """)

        # Создание хранимой процедуры 10 запроса
        cursor.execute("""
            CREATE PROCEDURE CheckInClientByReservationId(IN reservation_id INT)
            BEGIN
                DECLARE room_id INT;
                
                IF EXISTS (SELECT 1 FROM Reservations WHERE idReservation = reservation_id) THEN
                    SELECT idRoom INTO room_id
                    FROM Reservations
                    WHERE idReservation = reservation_id;
                
                    UPDATE Rooms
                    SET idRoomStatus = 1
                    WHERE idRoom = room_id;
                    
                    SELECT 'Клиент успешно заселен' AS Result;
                ELSE
                    SELECT 'Клиент не заселен. Такой брони не существует' AS Result;
                END IF;
            END;
        """)       

        # Создание хранимой процедуры 11 запроса
        cursor.execute("""
            CREATE PROCEDURE CheckOutClientByRoomId(IN room_id INT)
            BEGIN
                IF EXISTS (SELECT 1 FROM Rooms WHERE idRoom = room_id) THEN
                    UPDATE Rooms
                    SET idRoomStatus = 1
                    WHERE idRoom = room_id;
                    
                    SELECT 'Клиент выселен успешно' AS Result;
                ELSE
                    SELECT 'Произошла ошибка выселения. Такой комнаты не существует' AS Result;
                END IF;
            END;
        """)

     # Подтверждение операций создания процедур
    connection.commit()

finally:
    # Закрытие подключения
    connection.close()