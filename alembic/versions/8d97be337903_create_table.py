"""create_table

Revision ID: 8d97be337903
Revises: 
Create Date: 2023-04-04 10:55:10.348488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d97be337903'
down_revision = None
branch_labels = None
depends_on = None


def create_meta_info_table():
    op.create_table(
        "meta_info",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('category', sa.String(30), nullable=False),
        sa.Column('reason', sa.String(30), nullable=False)
    )


def create_import_table():
    op.create_table(
        'import',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('category', sa.String(30), nullable=False),
        sa.Column('reason', sa.String(30), nullable=False),
        sa.Column('import', sa.Numeric(precision=12, scale=2,
                  asdecimal=False, decimal_return_scale=None), nullable=False),
        sa.Column('import_date', sa.Date, nullable=False)
    )


def upgrade():
    create_import_table()
    create_meta_info_table()


def downgrade() -> None:
    pass
