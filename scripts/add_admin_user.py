import os
import odoo
from odoo import api, SUPERUSER_ID


def main() -> None:
    db_name = os.environ["ODOO_DB_NAME"]
    odoo_conf = os.environ["ODOO_CONFIG"]
    admin_pswd = os.environ["ODOO_ADMIN_PSWD"]
    admin_user = os.environ["ODOO_ADMIN_USER"]
    admin_email = os.environ["ODOO_ADMIN_EMAIL"]

    # Load server configuration
    odoo.tools.config.parse_config(["-c", odoo_conf])

    registry = odoo.registry(db_name)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        users = env["res.users"]
        admin = users.search([("login", "=", admin_user)], limit=1)
        if admin:
            admin.write({"password": admin_pswd, "email": admin_email})
        else:
            admin = users.create(
                {
                    "name": "Administrator",
                    "login": admin_user,
                    "email": admin_email,
                    "password": admin_pswd,
                }
            )
        cr.commit()


if __name__ == "__main__":
    main()
