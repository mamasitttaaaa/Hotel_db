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
        # Создание триггера на обновление или изменение данных в таблице Reservations
        cursor.execute("""
            CREATE TRIGGER check_reservation_data_ins
            BEFORE INSERT ON Reservations
            FOR EACH ROW
            BEGIN
                IF NEW.arrivalDate >= NEW.departureDate THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата начала проживания должна быть раньше даты окончания';
                END IF;

                IF NEW.price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительным числом';
                END IF;

                IF NEW.idIndividual IS NULL AND NEW.idReservContract IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Необходимо указать idIndividual или idReservContract';
                END IF;
            END;
        """)
        
        cursor.execute("""
            CREATE TRIGGER check_reservation_data_upd
            BEFORE UPDATE ON Reservations
            FOR EACH ROW
            BEGIN
                IF NEW.arrivalDate >= NEW.departureDate THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата начала проживания должна быть раньше даты окончания';
                END IF;

                IF NEW.price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительным числом';
                END IF;

                IF NEW.idIndividual IS NULL AND NEW.idReservContract IS NULL THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Необходимо указать idIndividual или idReservContract';
                END IF;
            END;
        """)

        # Триггер на изменение или добавление данных в таблицу ReservationContracts проверка дат и цены
        cursor.execute("""
            CREATE TRIGGER check_reservation_contract_upd
            BEFORE UPDATE ON ReservationContracts
            FOR EACH ROW
            BEGIN
                -- Проверяем условие: arrivalDate < departureDate
                IF NEW.arrivalDate >= NEW.departureDate THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата заезда должна быть раньше даты выезда';
                END IF;

                -- Проверяем условие: price > 0
                IF NEW.price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительным числом';
                END IF;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER check_reservation_contract_ins
            BEFORE INSERT ON ReservationContracts
            FOR EACH ROW
            BEGIN
                -- Проверяем условие: arrivalDate < departureDate
                IF NEW.arrivalDate >= NEW.departureDate THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Дата заезда должна быть раньше даты выезда';
                END IF;

                -- Проверяем условие: price > 0
                IF NEW.price <= 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Цена должна быть положительным числом';
                END IF;
            END;
        """)

        # Триггер на запрет удаления записей из таблицы Reservations, ServicesSales, Complaints
        cursor.execute("""
            CREATE TRIGGER prevent_delete_trigger_reservs
            BEFORE DELETE ON Reservations
            FOR EACH ROW
            BEGIN
                DECLARE table_name VARCHAR(255);
                IF EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'Reservations') THEN
                    SET table_name = 'Reservations';
                END IF;

                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Запрещено удаление данных из таблицы Resrvations';
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER prevent_delete_trigger_sales
            BEFORE DELETE ON ServicesSales
            FOR EACH ROW
            BEGIN
                DECLARE table_name VARCHAR(255);
                ELSEIF EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'ServicesSales') THEN
                    SET table_name = 'ServicesSales';
                END IF;

                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Запрещено удаление данных из таблицы ServicesSales';
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER prevent_delete_trigger_compls
            BEFORE DELETE ON Complaints
            FOR EACH ROW
            BEGIN
                DECLARE table_name VARCHAR(255);
                ELSEIF EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'Complaints') THEN
                    SET table_name = 'Complaints';
                END IF;

                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Запрещено удаление данных из таблицы Complaints';
            END;
        """)

        # Триггер на проверку заполнения только одного из полей о клиенте и проверка ссылочной ценности
        cursor.execute("""
            CREATE TRIGGER check_reservation_references_ins
            BEFORE INSERT ON Reservations
            FOR EACH ROW
            BEGIN
                DECLARE total_references INT;
                
                SET total_references = 
                    IF(NEW.idIndividual IS NOT NULL, 1, 0) +
                    IF(NEW.idReservContract IS NOT NULL, 1, 0);
                
                IF total_references != 1 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Необходимо заполнить ровно одно поле idIndividual или idReservContract';
                END IF;
                
                IF NEW.idIndividual IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Individuals WHERE idIndividual = NEW.idIndividual) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Неверное значение idIndividual';
                END IF;
                
                IF NEW.idReservContract IS NOT NULL AND NOT EXISTS (SELECT 1 FROM ReservationContracts WHERE idReservContract = NEW.idReservContract) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Неверное значение idReservContract';
                END IF;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER check_reservation_references_upd
            BEFORE UPDATE ON Reservations
            FOR EACH ROW
            BEGIN
                DECLARE total_references INT;
                
                SET total_references = 
                    IF(NEW.idIndividual IS NOT NULL, 1, 0) +
                    IF(NEW.idReservContract IS NOT NULL, 1, 0);
                
                IF total_references != 1 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Необходимо заполнить ровно одно поле idIndividual или idReservContract';
                END IF;
                
                IF NEW.idIndividual IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Individuals WHERE idIndividual = NEW.idIndividual) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Неверное значение idIndividual';
                END IF;
                
                IF NEW.idReservContract IS NOT NULL AND NOT EXISTS (SELECT 1 FROM ReservationContracts WHERE idReservContract = NEW.idReservContract) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Неверное значение idReservContract';
                END IF;
            END;
        """)

        # Триггер на проверку оригинальности значений в таблице Organizations
        cursor.execute("""
            CREATE TRIGGER check_organization_uniqueness
            BEFORE INSERT ON Organizations
            FOR EACH ROW
            BEGIN
                DECLARE org_count INT;
                
                SELECT COUNT(*) INTO org_count
                FROM Organizations
                WHERE orgName = NEW.orgName;

                IF org_count > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Организация с таким именем уже существует';
                END IF;
            END;
        """)

        # Триггер на проверку уникальности значения перед вставкой в таблицу Individuals
        cursor.execute("""
            CREATE TRIGGER check_individual_uniqueness
            BEFORE INSERT ON Individuals
            FOR EACH ROW
            BEGIN
                DECLARE individual_count INT;
                
                SELECT COUNT(*) INTO individual_count
                FROM Individuals
                WHERE fullName = NEW.fullName;

                IF individual_count > 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Физическое лицо с таким именем уже существует';
                END IF;
            END;
        """)

        # Триггер на проверку ссылочной целостности при добалении или изменении таблицы ReservationContracts
        cursor.execute("""
            CREATE TRIGGER check_reference_integrity_ins
            BEFORE INSERT ON ReservationContracts
            FOR EACH ROW
            BEGIN
                DECLARE org_count INT;
                
                SELECT COUNT(*) INTO org_count
                FROM Organizations
                WHERE idOrganization = NEW.idOrganization;
                
                IF org_count = 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такой организации не существует';
                END IF;
            END;
        """)

        cursor.execute("""
            CREATE TRIGGER check_reference_integrity_upd
            BEFORE UPDATE ON ReservationContracts
            FOR EACH ROW
            BEGIN
                DECLARE org_count INT;
                
                SELECT COUNT(*) INTO org_count
                FROM Organizations
                WHERE idOrganization = NEW.idOrganization;
                
                IF org_count = 0 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Такой организации не существует';
                END IF;
            END;
        """)

    # Подтверждение операций создания процедур
    connection.commit()

finally:
    # Закрытие подключения
    connection.close()