import models
models.init_db()
models.create_user("admin", "changeme", is_admin=True)