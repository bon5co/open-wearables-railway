#!/usr/bin/env python3
"""Seed or rotate the admin developer account from ADMIN_EMAIL / ADMIN_PASSWORD.

Upstream's scripts/init/seed_admin.py creates an account only when the developers
table is empty, and it falls back to the published defaults in app/config.py when
the environment does not carry the variables. This script instead requires both
variables, refuses the upstream default password, and re-applies the password on
every boot so that a redeploy is a working password reset.

It runs before the API server binds its port.
"""

import os
import sys

from app.config import settings
from app.database import SessionLocal
from app.models import Developer
from app.schemas.model_crud.user_management import DeveloperCreate
from app.services import developer_service
from app.utils.security import get_password_hash

UPSTREAM_DEFAULT_PASSWORD = "your-secure-password"
UPSTREAM_DEFAULT_EMAIL = "admin@admin.com"


def main() -> None:
    email = (os.environ.get("ADMIN_EMAIL") or "").strip()
    password = os.environ.get("ADMIN_PASSWORD") or ""

    if not email or not password:
        sys.exit("FATAL: ADMIN_EMAIL and ADMIN_PASSWORD must both be set. Refusing to boot.")
    if password == UPSTREAM_DEFAULT_PASSWORD:
        sys.exit("FATAL: ADMIN_PASSWORD is the upstream default. Refusing to boot.")
    if len(password) < settings.min_password_length:
        sys.exit(f"FATAL: ADMIN_PASSWORD is shorter than {settings.min_password_length} characters. Refusing to boot.")

    with SessionLocal() as db:
        existing = (
            db.query(Developer).filter(Developer.email == email).one_or_none()
        )
        if existing is None:
            developer_service.register(db, DeveloperCreate(email=email, password=password))
            print(f"[railway] created admin developer {email}")
        else:
            existing.hashed_password = get_password_hash(password)
            db.add(existing)
            db.commit()
            print(f"[railway] rotated password for admin developer {email}")

        # An account seeded by an earlier boot of upstream's own script would carry
        # the published default credentials; remove it so those cannot be used.
        if email != UPSTREAM_DEFAULT_EMAIL:
            stale = (
                db.query(Developer).filter(Developer.email == UPSTREAM_DEFAULT_EMAIL).one_or_none()
            )
            if stale is not None:
                db.delete(stale)
                db.commit()
                print(f"[railway] removed stale default account {UPSTREAM_DEFAULT_EMAIL}")


if __name__ == "__main__":
    main()
