"""Simplify patients table

Revision ID: 002
Revises: 001
Create Date: 2025-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Criar nova tabela simplificada
    op.create_table(
        'patients_simple',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True)
    )
    
    # Criar índices
    op.create_index('ix_patients_simple_id', 'patients_simple', ['id'])
    op.create_index('ix_patients_simple_name', 'patients_simple', ['name'])
    op.create_index('ix_patients_simple_email', 'patients_simple', ['email'])
    op.create_unique_constraint('uq_patients_simple_email', 'patients_simple', ['email'])
    
    # Dropar tabela antiga se existir
    try:
        op.drop_table('patients')
    except:
        pass
    
    # Renomear nova tabela
    op.rename_table('patients_simple', 'patients')
    
    # Renomear índices
    try:
        op.execute("ALTER INDEX ix_patients_simple_id RENAME TO ix_patients_id")
        op.execute("ALTER INDEX ix_patients_simple_name RENAME TO ix_patients_name") 
        op.execute("ALTER INDEX ix_patients_simple_email RENAME TO ix_patients_email")
        op.execute("ALTER TABLE patients RENAME CONSTRAINT uq_patients_simple_email TO uq_patients_email")
    except:
        pass

def downgrade():
    # Simples rollback - não implementaremos reconstituição dos dados antigos
    # pois seria perda de dados anyway
    op.drop_table('patients')
    
    # Recriar tabela antiga vazia (estrutura de referência)
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=False),
        sa.Column('ssn', sa.String(length=11), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=50), nullable=True),
        sa.Column('zip_code', sa.String(length=10), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('synthea_id', sa.String(length=255), nullable=True),
        sa.Column('race', sa.String(length=50), nullable=True),
        sa.Column('ethnicity', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )
