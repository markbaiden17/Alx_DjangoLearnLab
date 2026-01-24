An introduction to setting up a Django Development Environment.

Permissions and Groups Setup

1. Custom Permissions: Defined in the Book model (can_view, can_create, can_edit, can_delete).
2. Groups:
   - Viewers: Can only view books.
   - Editors: Can view, create, and edit books.
   - Admins: Full CRUD permissions.
3. Enforcement: Used `@permission_required` decorators in views.py with 'bookshelf.permission_name'.