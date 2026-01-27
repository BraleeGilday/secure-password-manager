"""empty message

Revision ID: ec275506cb94
Revises: e8ec14fd60cb
Create Date: 2026-01-26 20:03:43.311208

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ec275506cb94"
down_revision: Union[str, Sequence[str], None] = "e8ec14fd60cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade User schema."""
    with op.batch_alter_table("user") as batch_op:
        batch_op.create_unique_constraint("uq_user_username", ["username"])


def downgrade() -> None:
    """Downgrade User schema."""
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_constraint("uq_user_username", type_="unique")
