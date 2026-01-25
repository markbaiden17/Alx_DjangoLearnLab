An introduction to setting up a Django Development Environment.

Permissions and Groups Setup

1. Custom Permissions: Defined in the Book model (can_view, can_create, can_edit, can_delete).
2. Groups:
   - Viewers: Can only view books.
   - Editors: Can view, create, and edit books.
   - Admins: Full CRUD permissions.
3. Enforcement: Used `@permission_required` decorators in views.py with 'bookshelf.permission_name'.

Security Review - HTTPS Implementation
1. HTTPS Enforcement: `SECURE_SSL_REDIRECT` ensures no unencrypted traffic reaches the app.
2. HSTS: `SECURE_HSTS_SECONDS` prevents "man-in-the-middle" attacks by forcing browsers to use HTTPS globally.
3. Cookie Hardening: `SESSION_COOKIE_SECURE` prevents session hijacking over insecure networks.
4. Clickjacking Protection: `X_FRAME_OPTIONS = 'DENY'` prevents the site from being rendered in an <iframe>.