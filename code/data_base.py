from pony.orm import Database, Required, Json
import secret_settings

db = Database()
db.bind(provider='postgres',
        user=secret_settings.USER,
        password=secret_settings.PASSWORD,
        host=secret_settings.HOST,
        database=secret_settings.DATABASE)


class UserState(db.Entity):
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    current_step = Required(str)
    context = Required(Json)


db.generate_mapping(create_tables=True)
