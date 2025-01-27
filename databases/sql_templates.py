CREATE_DIRECTORS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS "directors" (
        "id" serial NOT NULL,
        "name" text NOT NULL,
        "country" text NOT NULL,
        PRIMARY KEY ("id")
    )
"""

CREATE_ACTORS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS "actors" (
        "id" serial NOT NULL,
        "name" text NOT NULL,
        "country" text NOT NULL,
        PRIMARY KEY ("id")
    )
"""

CREATE_GENRES_TABLE: str = """
    CREATE TABLE IF NOT EXISTS "genres" (
        "id" serial NOT NULL,
        "name" text NOT NULL,
        PRIMARY KEY ("id"),
        CONSTRAINT "un_genres_name" UNIQUE ("name")
    )
"""

CREATE_FILMS_TABLE: str = """
    CREATE TABLE IF NOT EXISTS "films" (
        "id" serial NOT NULL,
        "name" text NOT NULL,
        "description" text NOT NULL,
        "director_id" integer NOT NULL,
        "genre_id" integer,
        "actors_id" integer[] NOT NULL,
        PRIMARY KEY ("id"),
        CONSTRAINT "fk_film_director" 
            FOREIGN KEY ("director_id")
                REFERENCES "directors"("id") MATCH SIMPLE
                ON UPDATE NO ACTION 
                ON DELETE CASCADE,
        CONSTRAINT "fk_film_genre" 
            FOREIGN KEY ("genre_id")
                REFERENCES "genres"("id") MATCH SIMPLE
                ON UPDATE NO ACTION 
                ON DELETE SET NULL
    )
"""
