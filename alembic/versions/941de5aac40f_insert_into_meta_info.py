"""insert into meta_info

Revision ID: 941de5aac40f
Revises: 8d97be337903
Create Date: 2023-04-04 11:23:04.148162

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '941de5aac40f'
down_revision = '8d97be337903'
branch_labels = None
depends_on = None

insert_meta_info_list = [('Input', 'The last balance Post bank'),
                         ('Input', 'The last balance Revolut bank'),
                         ('Input', 'The last balanc San Paolo bank'),
                         ('Input', 'The last balance Satispay'),
                         ('Input', 'Other'),
                         ('Income', 'Salary'),
                         ('Income', 'Ticket restaurant'),
                         ('Income', 'Awards'),
                         ('Income', 'Bonuses'),
                         ('Income', 'INPS'),
                         ('Income', 'Other'),
                         ('Cost', 'Travelling'),
                         ('Cost', 'Food'),
                         ('Cost', 'Medical reason'),
                         ('Cost', 'Funny day'),
                         ('Cost', 'Car maintenance'),
                         ('Cost', 'Home insurance'),
                         ('Cost', 'Gas bill'),
                         ('Cost', 'Electricity bill'),
                         ('Cost', 'Internet'),
                         ('Cost', 'Clothes'),
                         ('Cost', 'Traveling'),
                         ('Cost', 'Fuel'),
                         ('Cost', 'School'),
                         ('Cost', 'Car insurance'),
                         ('Cost', 'Public transportation'),
                         ('Cost', 'TARI'),
                         ('Cost', 'Other')
                         ]


insert_query = text("""
INSERT INTO meta_info (category, reason) VALUES (:category, :reason)
""")


def executeQueryList(query):
    conn = op.get_bind()
    for category, reason in insert_meta_info_list:
        # print(category)
        conn.execute(query, {"category": category, "reason": reason})


def upgrade():
    executeQueryList(insert_query)


def downgrade() -> None:
    pass
