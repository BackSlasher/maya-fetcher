import argparse
import models
import db
import json
from sqlalchemy.orm import Session
import datetime


def unique_by(inp, unique_extractor, score=None):
    ret=[]
    s=set()
    if score:
        inp = sorted(inp, key=score, reverse=True)
    for i in inp:
        un = unique_extractor(i)
        if un not in s:
            s.add(un)
            ret.append(i)
    return ret

def import_file():
    with open("test/maya_tase_companies_current_shareholders.json", "r") as f:
        data = json.load(f)
    session = Session(db.engine)
    with session.begin():
        # Create new snapshot
        date_taken = datetime.date(2022,12,19)
        sn = models.Snapshot(date_taken=date_taken)
        session.add(sn)
        # Ensures snapshots land first, for FK constraints
        session.flush()
        # Itereate over objects
        companies=[]
        securities=[]

        for item in data:

            # Companies
            companies.append(models.Company(
                ds=date_taken,
                id=int(item["CompanyTaseId"]),
                name=item["CompanyName"],
                site=item["Site"],
                long_name=item["CompanyLongName"],
                corporate_number=item["CorporateNo"],
            ))
            companies.append(models.Company(
                ds=date_taken,
                id=int(item["HolderId"]),
                name=item["HolderName"],
            ))
            
            # Security
            securities.append(models.Security(
                ds=date_taken,
                id=item["SecurityId"],
                type=item["SecurityType"],
                name=item["SecurityName"],
            ))

            # Shareholder
            session.add(models.Shareholder(
                ds=date_taken,
                company_id = item["CompanyTaseId"],
                holder_id = item["HolderId"],
                security_id = int(item["SecurityId"]),
                holder_company_id = item["ShareHolderCompanyId"],

                capital_pct = item["CapitalPercent"]*100,
                end_balance = item["EndBalance"],
                remark=item["Remark"],
                is_trade_written = bool(item["IsTradeWritten"]),
                last_update_date = datetime.date.fromisoformat(item["LastUpdateDate"]),
                market_value = item["MarketValue"],
                vote_capital = item["VoteCapital"],
            ))

        [session.add(i) for i in unique_by(companies, lambda c: (c.ds, c.id), score=lambda c:(c.long_name or "", c.corporate_number or 0, c.site or ""))]
        session.flush()
        [session.add(i) for i in unique_by(securities, lambda c: (c.ds, c.id))]



def init():
    db.reset_db()

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'ProgramName',
        description = 'What the program does',
        epilog = 'Text at the bottom of help')
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init")
    parser_import = subparsers.add_parser("import")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == "init":
        init()
    elif args.command == "import":
        import_file()

main()
