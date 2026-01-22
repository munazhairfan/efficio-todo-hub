"""Create tasks table with String user_id to match User model.

Revision ID: 002_create_tasks_table
Revises: 001_initial_migration
Create Date: 2026-01-22 14:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_create_tasks_table'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database to create the tasks table."""
    # Create tasks table with String user_id to match User model UUIDs
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=False),  # Using String to match UUIDs in User model
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_tasks_user_id', 'user_id'),
        sa.Index('ix_tasks_completed', 'completed')
    )


def downgrade():
    """Downgrade the database to drop the tasks table."""
    # Drop the tasks table
    op.drop_table('tasks')