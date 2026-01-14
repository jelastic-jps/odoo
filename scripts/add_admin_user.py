import os
import odoo
from odoo import api, SUPERUSER_ID


def main() -> None:
    db_name = os.environ["ODOO_DB_NAME"]
    odoo_conf = os.environ["ODOO_CONFIG"]
    master_pswd = os.environ["ODOO_MASTER_PSWD"]
    admin_email = os.environ.get("ODOO_ADMIN_EMAIL", "admin@example.com")

    odoo.tools.config.parse_config(["-c", odoo_conf])

    with odoo.api.Environment.manage():
        registry = odoo.registry(db_name)
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            users = env["res.users"]
            admin = users.search([("login", "=", "admin")], limit=1)
            if not admin:
                admin = users.create(
                    {
                        "name": "Administrator",
                        "login": "admin",
                        "email": admin_email,
                    }
                )
            if not admin.email:
                admin.email = admin_email
            admin._set_password(master_pswd)


if __name__ == "__main__":
    main()
