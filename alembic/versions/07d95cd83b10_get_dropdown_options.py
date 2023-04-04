"""get_dropdown_options

Revision ID: 07d95cd83b10
Revises: 941de5aac40f
Create Date: 2023-04-04 14:53:47.103885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07d95cd83b10'
down_revision = '941de5aac40f'
branch_labels = None
depends_on = None


get_meta_info_dropdown_options = """
CREATE PROCEDURE `get_meta_info_dropdown_options` ()
BEGIN
    SELECT category, GROUP_CONCAT(reason SEPARATOR ',') AS reasons
    FROM life_cost_management.meta_info
    GROUP BY category;
END
"""


def upgrade():
    op.execute(get_meta_info_dropdown_options)


def downgrade() -> None:
    pass
