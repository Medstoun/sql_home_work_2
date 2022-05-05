import sqlite3


def connect(query):
    connection = sqlite3.connect('animal.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result


def main():
    query_1 = """
        CREATE TABLE IF NOT EXISTS colors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        color VARCHAR(30)
        )
    """

    query_2 = """
            CREATE TABLE IF NOT EXISTS animals_colors (
            animals_id INTEGER, 
            colors_id INTEGER,
            FOREIGN KEY (animals_id) REFERENCES animals("index"),
            FOREIGN KEY (colors_id) REFERENCES colors(id)
            )
    """

    query_3 = """
                INSERT INTO colors (color)
                SELECT DISTINCT * FROM (
                SELECT DISTINCT
                color1 as color
                FROM animals 
                UNION ALL
                SELECT DISTINCT
                color2 as color
                FROM animals        
                )
     """

    query_4 = """
                    INSERT INTO animals_colors (animals_id, colors_id)
                    SELECT DISTINCT
                    animals."index", colors.id 
                    FROM animals
                    JOIN colors
                    ON colors.color = animals.color1
                    UNION ALL       
                    SELECT DISTINCT 
                    animals."index", colors.id 
                    FROM animals 
                    JOIN colors ON colors.color = animals.color2            
    """

    query_5 = """
                CREATE TABLE IF NOT EXISTS outcome (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                subtype VARCHAR(50),
                "type" VARCHAR(50),
                "month" INTEGER,
                "year" INTEGER 
                )
    """

    query_6 = """
                    INSERT INTO outcome (subtype, "type", "month", "year")
                    SELECT DISTINCT 
                    animals.outcome_subtype,
                    animals.outcome_type,
                    animals.outcome_month,
                    animals.outcome_year
                    FROM animals
    """

    query_7 = """
                    CREATE TABLE IF NOT EXISTS animals_final (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    age_upon_outcome VARCHAR(50),
                    animal_id VARCHAR(50),
                    animal_type VARCHAR(50),
                    name VARCHAR(50),
                    breed VARCHAR(50),
                    date_of_birth VARCHAR(50),
                    outcome_id INTEGER,
                    FOREIGN KEY (outcome_id) REFERENCES colors(id)
                    )
    """

    query_8 = """
                        INSERT INTO animals_final (age_upon_outcome, animal_id, animal_type, name, breed, date_of_birth,
                        outcome_id)
                        SELECT 
                        animals.age_upon_outcome, animals.animal_id, animals.animal_type, animals.name,
                        animals.breed, animals.date_of_birth, outcome.id
                        FROM animals
                        JOIN outcome
                        ON outcome.subtype = animals.outcome_subtype
                        AND outcome."type" = animals.outcome_type
                        AND outcome."month" = animals.outcome_month
                        AND outcome."year" = animals.outcome_year
    """

    query_9 = """
                            INSERT INTO animals_colors (animals_id, colors_id)
                            SELECT DISTINCT
                            animals_final.id, colors.id 
                            FROM animals
                            JOIN colors
                            ON colors.color = animals.color1
                            JOIN animals_final  
                            ON animals_final.animal_id = animals.animal_id
                            UNION ALL       
                            SELECT DISTINCT 
                            animals_final.id, colors.id 
                            FROM animals 
                            JOIN colors ON colors.color = animals.color2 
                            JOIN animals_final
                            ON animals_final.animal_id = animals.animal_id         
            """


if __name__ == '__main__':
    main()
