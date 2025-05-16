"""add measurement_type and user_notes to continuous_body_temperature

Revision ID: add_measurement_type_and_user_notes_to_cbt
Revises: 
Create Date: 2024-03-16 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_measurement_type_and_user_notes_to_cbt'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 添加measurement_type字段
    op.add_column('continuous_body_temperature',
        sa.Column('measurement_type', sa.String(20), nullable=True, comment='测量类型')
    )
    
    # 添加user_notes字段
    op.add_column('continuous_body_temperature',
        sa.Column('user_notes', sa.Text, nullable=True, comment='用户备注')
    )

def downgrade():
    # 删除measurement_type字段
    op.drop_column('continuous_body_temperature', 'measurement_type')
    
    # 删除user_notes字段
    op.drop_column('continuous_body_temperature', 'user_notes') 