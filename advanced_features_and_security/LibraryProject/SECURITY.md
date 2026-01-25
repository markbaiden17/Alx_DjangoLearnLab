Security Implementation Details:
- DEBUG=False: Prevents leaking sensitive traceback info.
- SECURE_BROWSER_XSS_FILTER: Enables browser-side XSS protection.
- CSRF_COOKIE_SECURE/SESSION_COOKIE_SECURE: Ensures cookies only travel over HTTPS.
- SQL Injection Prevention: All database queries use Django ORM (parameterized queries).
- X_FRAME_OPTIONS: Set to DENY to prevent Clickjacking attacks.