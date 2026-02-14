---
name: database-skills
description: Design and manage database schemas including table creation, migrations, indexing, and relational structure. Use for building reliable and scalable data layers.
---

# Database Skills

## Instructions

1. **Schema Design**
   - Define clear table responsibilities
   - Use proper data types for each field
   - Normalize data to avoid duplication
   - Define primary keys and foreign keys
   - Enforce constraints (NOT NULL, UNIQUE)
   - Plan for scalability and future changes

2. **Table Creation**
   - Create tables with consistent naming conventions
   - Define indexes for frequently queried columns
   - Set default values where appropriate
   - Add timestamps for auditing (created_at, updated_at)
   - Use meaningful column names

3. **Relationships**
   - Model one-to-many and many-to-many relations correctly
   - Enforce referential integrity using foreign keys
   - Use cascading rules carefully
   - Avoid circular dependencies

4. **Migrations**
   - Generate versioned migration files
   - Apply migrations safely without data loss
   - Support rollback strategies
   - Keep migration history clean and documented
   - Never modify old migrations after production release

5. **Data Integrity & Performance**
   - Add indexes for search and filtering
   - Avoid unnecessary large fields
   - Optimize query patterns
   - Use transactions for critical operations
   - Prevent orphan records

6. **Environment Configuration**
   - Use environment variables for database URLs
   - Separate development and production databases
   - Secure credentials properly
   - Enable connection pooling if needed

## Best Practices
- Keep schemas simple and predictable
- Prefer explicit constraints over application-only validation
- Document schema changes clearly
- Test migrations in staging before production
- Back up databases regularly
- Avoid premature optimization

## Example Usage
```text
Use database-skills when implementing:
- Database schema design
- Creating tables and relationships
- Writing migrations
- Index optimization
- Data integrity rules
- SQLModel model definitions
