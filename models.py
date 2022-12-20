from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import String
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import Integer 
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime


from db import Base

class Snapshot(Base):
    __tablename__ = "snapshots"
    date_taken: Mapped[datetime.date] = mapped_column(DateTime, primary_key=True)

class Company(Base):
    __tablename__ = "companies"
    ds: Mapped[datetime.date] = mapped_column(ForeignKey("snapshots.date_taken"), primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String)
    site: Mapped[str] = mapped_column(String, nullable=True)
    long_name = mapped_column(String, nullable=True)
    corporate_number: Mapped[str] = mapped_column(String, nullable=True)

class Security(Base):
    __tablename__ = "securities"
    ds: Mapped[datetime.date] = mapped_column(ForeignKey("snapshots.date_taken"), primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    type: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)


class Shareholder(Base):
    __tablename__ = "shareholders"
    ds: Mapped[datetime.date] = mapped_column(DateTime, ForeignKey("snapshots.date_taken"), primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped["Company"] = relationship("Company", foreign_keys=[ds, company_id], viewonly=True)

    holder_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    holder: Mapped["Company"] = relationship("Company", foreign_keys=[ds, holder_id], viewonly=True)

    holder_company_id: Mapped[int] = mapped_column(Integer, nullable=True)
#    holder_company: Mapped["Company"] = relationship("Company", foreign_keys=[ds, holder_company_id], viewonly=True)
    holder_company: Mapped["Company"] = relationship("Company", viewonly=True, primaryjoin='(Company.ds == Shareholder.ds) and (Company.id == Shareholder.holder_company_id)',)

    __table_args__ = (
        ForeignKeyConstraint([ds, company_id], [Company.ds, Company.id]),
        ForeignKeyConstraint([ds, holder_id], [Company.ds, Company.id]),
        #ForeignKeyConstraint([ds, holder_company_id], [Company.ds, Company.id]),
    )

    security_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    remark: Mapped[str] = mapped_column(String, nullable=True)
    is_trade_written: Mapped[bool] = mapped_column(Boolean)

    # pcts are x100 (51.85% saved as 5185)
    capital_pct: Mapped[int] = mapped_column(Integer)
    end_balance: Mapped[int] = mapped_column(BigInteger)
    last_update_date: Mapped[datetime.date] = mapped_column(DateTime)
    market_value: Mapped[float] = mapped_column(Float)
    vote_capital: Mapped[float] = mapped_column(Float)
