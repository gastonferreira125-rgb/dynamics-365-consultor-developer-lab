"""Laboratorio real de Python + SQLite con datos FICTICIOS inspirados en F&O.
Ejecución en navegador usando GitHub Codespaces, sin instancia Dynamics ni X++.
python3 labs/DYN-02-vouchers-cloud/lab.py --company USMF --voucher VCH-2026-002
"""
import argparse
import sqlite3


def create_demo_db():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("""
        CREATE TABLE GeneralJournalEntry (
            RecId INTEGER PRIMARY KEY,
            SubledgerVoucher TEXT NOT NULL,
            Company TEXT NOT NULL,          -- CAMPO FICTICIO: sociedad simplificada
            AccountingDate TEXT NOT NULL
        );
        CREATE TABLE GeneralJournalAccountEntry (
            RecId INTEGER PRIMARY KEY,
            GeneralJournalEntry INTEGER NOT NULL,
            MainAccount TEXT NOT NULL,      -- CAMPO FICTICIO: en F&O usar LedgerDimension
            Department TEXT NOT NULL,       -- CAMPO FICTICIO
            CostCenter TEXT NOT NULL,       -- CAMPO FICTICIO
            AccountingCurrencyAmount REAL NOT NULL,
            FOREIGN KEY(GeneralJournalEntry) REFERENCES GeneralJournalEntry(RecId)
        );
        CREATE TABLE JournalLineExample (
            Voucher TEXT NOT NULL, Company TEXT NOT NULL,
            Vendor TEXT NOT NULL, OffsetMainAccount TEXT NOT NULL,
            Department TEXT NOT NULL, CostCenter TEXT NOT NULL
        );
        CREATE TABLE FixedDimensionExample (
            Company TEXT NOT NULL, MainAccount TEXT NOT NULL,
            FixedCostCenter TEXT NOT NULL, PRIMARY KEY (Company, MainAccount)
        );
    """)
    db.executemany("INSERT INTO GeneralJournalEntry VALUES (?, ?, ?, ?)", [
        (1001, "VCH-2026-001", "USMF", "2026-10-27"),
        (1002, "VCH-2026-002", "USMF", "2026-10-27"),
        (2001, "VCH-2026-001", "DEMF", "2026-10-27"),
    ])
    db.executemany("INSERT INTO GeneralJournalAccountEntry VALUES (?, ?, ?, ?, ?, ?)", [
        (5001, 1001, "606300", "022", "008", 1000.0),
        (5002, 1001, "201100", "022", "009", -1000.0),
        (5003, 1002, "606300", "022", "009", 750.0),  # discrepancia intencional
        (5004, 1002, "201100", "022", "009", -750.0),
        (6001, 2001, "606300", "022", "012", 200.0),
        (6002, 2001, "201100", "022", "012", -200.0),
    ])
    db.executemany("INSERT INTO JournalLineExample VALUES (?, ?, ?, ?, ?, ?)", [
        ("VCH-2026-001", "USMF", "US-111", "606300", "022", "009"),
        ("VCH-2026-002", "USMF", "US-111", "606300", "022", "009"),
        ("VCH-2026-001", "DEMF", "DE-111", "606300", "022", "012"),
    ])
    db.executemany("INSERT INTO FixedDimensionExample VALUES (?, ?, ?)", [
        ("USMF", "606300", "008"),
        ("DEMF", "606300", "012"),
    ])
    db.commit()
    return db


VOUCHER_QUERY = """
SELECT gje.Company, gje.SubledgerVoucher, gje.RecId AS HeaderRecId,
       gjae.RecId AS LineRecId, gjae.MainAccount, gjae.Department,
       gjae.CostCenter, gjae.AccountingCurrencyAmount
FROM GeneralJournalEntry AS gje
JOIN GeneralJournalAccountEntry AS gjae
  ON gjae.GeneralJournalEntry = gje.RecId
WHERE gje.Company = ? AND gje.SubledgerVoucher = ?
ORDER BY gjae.RecId;
"""


def get_voucher(db, company, voucher):
    return db.execute(VOUCHER_QUERY, (company, voucher)).fetchall()


def detect_fixed_dimension_mismatches(db):
    """ALERTA DIDÁCTICA: con una regla ficticia ACTUAL, no prueba cambios históricos."""
    return db.execute("""
       SELECT gje.Company, gje.SubledgerVoucher, gjae.MainAccount,
              gjae.CostCenter AS Actual, f.FixedCostCenter AS Expected
       FROM GeneralJournalAccountEntry AS gjae
       JOIN GeneralJournalEntry AS gje ON gje.RecId = gjae.GeneralJournalEntry
       JOIN FixedDimensionExample AS f
         ON f.Company = gje.Company AND f.MainAccount = gjae.MainAccount
       WHERE gjae.CostCenter <> f.FixedCostCenter
       ORDER BY gje.Company, gje.SubledgerVoucher
    """).fetchall()


def voucher_balance(db, company, voucher):
    return round(sum(x["AccountingCurrencyAmount"] for x in get_voucher(db, company, voucher)), 2)


def main():
    p = argparse.ArgumentParser(description="Practicar JOIN de asientos de Finance en SQLite")
    p.add_argument("--company", default="USMF")
    p.add_argument("--voucher", default="VCH-2026-001")
    a = p.parse_args()
    db = create_demo_db()
    rows = get_voucher(db, a.company, a.voucher)
    print(f"\n=== VOUCHER TRANSACTIONS (SIMULACIÓN) ===\nSociedad: {a.company} | Voucher: {a.voucher}")
    if not rows:
        print("No se encontró el comprobante en los datos simulados.")
    for row in rows:
        print(f"RecId {row['HeaderRecId']} -> línea {row['LineRecId']} | cuenta {row['MainAccount']} | "
              f"Dept {row['Department']} | CC {row['CostCenter']} | importe {row['AccountingCurrencyAmount']:.2f}")
    if rows:
        balance = voucher_balance(db, a.company, a.voucher)
        print(f"Balance débitos - créditos: {balance:.2f} | {'CUADRA' if abs(balance) < 0.005 else 'NO CUADRA'}")
    print("\n=== ANOMALÍAS SIMULADAS VS FIXED DIMENSION ===")
    for row in detect_fixed_dimension_mismatches(db):
        print(f"{row['Company']} | {row['SubledgerVoucher']} | cuenta {row['MainAccount']} | "
              f"CC real {row['Actual']} vs Fixed esperado {row['Expected']}")
    print("\nNota: los valores de dimensión están simplificados; NO son columnas directas de F&O.\n")


if __name__ == "__main__":
    main()
