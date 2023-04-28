"""Add source parameter to insert_import procedure

Revision ID: 4ef917a13544
Revises: 90d6cd8b79bb
Create Date: 2023-04-28 20:18:31.757680

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '4ef917a13544'
down_revision = '90d6cd8b79bb'
branch_labels = None
depends_on = None


insert_import = text("""
CREATE PROCEDURE insert_import(IN p_category VARCHAR(30), 
                                IN p_reason VARCHAR(30), 
                                IN p_import DECIMAL(10,2), 
                                IN p_import_date DATE,
                                IN p_source VARCHAR(30))
BEGIN
    INSERT INTO import (category, reason, import, import_date)
                    VALUES (p_category,p_reason, p_import, p_import_date);
    IF p_source IS NOT NULL THEN
        INSERT INTO import (category, reason, import, import_date)
                        VALUES ('Input', p_source, -p_import, p_import_date);
    END IF;
END
""")


def upgrade():
    op.execute(insert_import)


def downgrade() -> None:
    pass
