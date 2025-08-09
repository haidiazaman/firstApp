from sqlmodel import Field, Session, SQLModel, create_engine, select  


class Hero(SQLModel, table=True):  
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)  


def select_heroes():
    with Session(engine) as session:  
        statement = select(Hero)  
        results = session.exec(statement)  
        for hero in results:  
            print(hero)  
    


def main():

    select_heroes()  


if __name__ == "__main__":
    main()