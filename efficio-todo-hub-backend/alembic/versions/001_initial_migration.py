"""Initial migration for conversation and message models.

Revision ID: 001_initial_migration
Revises:
Create Date: 2026-01-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '001_initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade the database to this revision."""
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_conversations_id', 'id'),
        sa.Index('ix_conversations_user_id', 'user_id')
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('metadata_json', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_messages_id', 'id'),
        sa.Index('ix_messages_conversation_id', 'conversation_id'),
        sa.Index('ix_messages_user_id', 'user_id'),
        sa.Index('ix_messages_timestamp', 'timestamp')
    )


def downgrade():
    """Downgrade the database from this revision."""
    # Drop messages table first (due to foreign key constraint)
    op.drop_table('messages')

    # Drop conversations table
    op.drop_table('conversations')