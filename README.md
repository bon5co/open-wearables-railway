# open-wearables-railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/open-wearables-or-just-updated-wearable-?referralCode=Z1xivh&utm_medium=integration&utm_source=template&utm_campaign=generic)

**Deploy on Railway:** [Open Wearables template](https://railway.com/deploy/open-wearables-or-just-updated-wearable-?referralCode=Z1xivh&utm_medium=integration&utm_source=template&utm_campaign=generic)

Wrapper images for deploying [Open Wearables](https://github.com/the-momentum/open-wearables)
(unified API for wearable health data — Garmin, Oura, Strava, Fitbit, Apple Health, Samsung
Health and more) on Railway.

Upstream publishes no container image, so the workflow in `.github/workflows/publish.yml`
builds upstream's own Dockerfiles at a pinned tag and layers two fixes on top.

## `ghcr.io/bon5co/open-wearables-railway` (backend, worker, beat)

* **The admin account is seeded from `ADMIN_EMAIL` / `ADMIN_PASSWORD`, and the container
  refuses to boot without them.** Upstream's `scripts/init/seed_admin.py` falls back to
  `app/config.py`'s defaults — `admin@admin.com` / `your-secure-password`, both published in
  the upstream repository — when the variables are absent from the environment.
* **The password is re-applied on every boot**, so a redeploy is a working password reset.
  Upstream's seed step is a no-op once any developer account exists, and the product's only
  other recovery path is an emailed link.
* **The API listens on the port Railway injects** (`API_PORT` is set from `PORT`).

## `ghcr.io/bon5co/open-wearables-railway-frontend`

`VITE_API_URL` is substituted into the JavaScript bundle at build time, so the image is built
with a placeholder and the entrypoint rewrites it to the deployment's own backend URL at boot,
restoring a pristine copy of the build output first and failing closed if any placeholder
survives.

## Licence

Open Wearables is MIT-licensed; these wrapper files are published under the same terms.
