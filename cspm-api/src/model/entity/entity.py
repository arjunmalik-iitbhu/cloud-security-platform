from typing import Optional
import datetime

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Enum, ForeignKeyConstraint, JSON, PrimaryKeyConstraint, String, UniqueConstraint, text
from sqlmodel import Field, Relationship, SQLModel

class Cloud(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("name::text <> ''::text", name='cloud_name_check'),
        PrimaryKeyConstraint('id', name='cloud_primary_key'),
        UniqueConstraint('name', name='cloud_unique_name')
    )

    id: int = Field(sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(200), nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))

    credential: list['Credential'] = Relationship(back_populates='cloud')
    resource: list['Resource'] = Relationship(back_populates='cloud')


class Credential(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("name::text <> ''::text", name='credential_name_check'),
        ForeignKeyConstraint(['cloud_id'], ['cloud.id'], ondelete='CASCADE', onupdate='CASCADE', name='credential_foreign_key_cloud_id'),
        PrimaryKeyConstraint('id', name='credential_primary_key'),
        UniqueConstraint('name', name='credential_unique_name')
    )

    id: int = Field(sa_column=Column('id', BigInteger, primary_key=True))
    name: str = Field(sa_column=Column('name', String(1000), nullable=False))
    cloud_id: int = Field(sa_column=Column('cloud_id', BigInteger, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))

    cloud: Optional['Cloud'] = Relationship(back_populates='credential')
    analysis: list['Analysis'] = Relationship(back_populates='credential')


class Resource(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['cloud_id'], ['cloud.id'], ondelete='CASCADE', onupdate='CASCADE', name='resource_foreign_key_cloud_id'),
        PrimaryKeyConstraint('id', name='resource_primary_key')
    )

    id: int = Field(sa_column=Column('id', BigInteger, primary_key=True))
    type: str = Field(sa_column=Column('type', String(200), nullable=False, server_default=text("''::character varying")))
    details: dict = Field(sa_column=Column('details', JSON, nullable=False, server_default=text("'{}'::json")))
    cloud_id: int = Field(sa_column=Column('cloud_id', BigInteger, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    external_resource_id: Optional[str] = Field(default=None, sa_column=Column('external_resource_id', String(2000)))

    cloud: Optional['Cloud'] = Relationship(back_populates='resource')
    analysis: list['Analysis'] = Relationship(back_populates='resource')


class Analysis(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['credential_id'], ['credential.id'], ondelete='CASCADE', onupdate='CASCADE', name='analysis_foreign_key_credential_id'),
        ForeignKeyConstraint(['resource_id'], ['resource.id'], ondelete='CASCADE', onupdate='CASCADE', name='analysis_foreign_key_resource_id'),
        PrimaryKeyConstraint('id', name='analysis_primary_key')
    )

    id: int = Field(sa_column=Column('id', BigInteger, primary_key=True))
    credential_id: int = Field(sa_column=Column('credential_id', BigInteger, nullable=False))
    resource_id: int = Field(sa_column=Column('resource_id', BigInteger, nullable=False))
    created_at: datetime.datetime = Field(sa_column=Column('created_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime.datetime = Field(sa_column=Column('updated_at', DateTime(True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    current_resource_status: Optional[str] = Field(default=None, sa_column=Column('current_resource_status', Enum('running', 'stopped', name='resource_status')))
    current_resource_risk: Optional[str] = Field(default=None, sa_column=Column('current_resource_risk', Enum('low', 'high', name='resource_risk')))

    credential: Optional['Credential'] = Relationship(back_populates='analysis')
    resource: Optional['Resource'] = Relationship(back_populates='analysis')
