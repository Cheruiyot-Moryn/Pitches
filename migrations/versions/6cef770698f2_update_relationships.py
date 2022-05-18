"""update relationships

Revision ID: 6cef770698f2
Revises: dd7b4c96598d
Create Date: 2022-05-18 18:18:52.693008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cef770698f2'
down_revision = 'dd7b4c96598d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upvote', sa.Integer(), nullable=True),
    sa.Column('downvote', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pitches_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pitches_id'], ['pitches.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('likes')
    op.add_column('comments', sa.Column('opinion', sa.String(length=255), nullable=True))
    op.add_column('comments', sa.Column('time_posted', sa.DateTime(), nullable=True))
    op.add_column('comments', sa.Column('pitches_id', sa.Integer(), nullable=True))
    op.drop_constraint('comments_pitch_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'pitches', ['pitches_id'], ['id'])
    op.drop_column('comments', 'comment')
    op.drop_column('comments', 'pitch_id')
    op.add_column('pitches', sa.Column('pitch_title', sa.String(), nullable=True))
    op.add_column('pitches', sa.Column('pitch_category', sa.String(), nullable=True))
    op.drop_column('pitches', 'text')
    op.drop_column('pitches', 'category')
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('bio', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('profile_pic_path', sa.String(), nullable=True))
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.drop_column('users', 'password_encrypt')
    op.drop_column('users', 'avatar')
    op.drop_column('users', 'about')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('password_encrypt', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.drop_column('users', 'profile_pic_path')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'password_hash')
    op.add_column('pitches', sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('pitches', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('pitches', 'pitch_category')
    op.drop_column('pitches', 'pitch_title')
    op.add_column('comments', sa.Column('pitch_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('comments', sa.Column('comment', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_pitch_id_fkey', 'comments', 'pitches', ['pitch_id'], ['id'])
    op.drop_column('comments', 'pitches_id')
    op.drop_column('comments', 'time_posted')
    op.drop_column('comments', 'opinion')
    op.create_table('likes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('pitch_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pitch_id'], ['pitches.id'], name='likes_pitch_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='likes_pkey')
    )
    op.drop_table('votes')
    # ### end Alembic commands ###
