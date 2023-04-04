"""insert_into_import_table

Revision ID: 90d6cd8b79bb
Revises: 07d95cd83b10
Create Date: 2023-04-04 15:51:49.418330

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '90d6cd8b79bb'
down_revision = '07d95cd83b10'
branch_labels = None
depends_on = None

insert_import = text("""
CREATE PROCEDURE insert_import(IN p_category VARCHAR(30), 
                                IN p_reason VARCHAR(30), 
                                IN p_import DECIMAL(10,2), 
                                IN p_import_date DATE)
BEGIN
    INSERT INTO import (category, reason, import, import_date)
                    VALUES (p_category,p_reason, p_import, p_import_date);
END
""")


def upgrade():
    op.execute(insert_import)


def downgrade() -> None:
    pass
