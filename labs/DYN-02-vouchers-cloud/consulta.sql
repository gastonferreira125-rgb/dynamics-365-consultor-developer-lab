-- Consulta SQL para nuestra base SQLite DIDÁCTICA. No es SQL de producción F&O.
-- La unión es por identificador de encabezado (RecId), NO por voucher:
SELECT gje.Company, gje.SubledgerVoucher,
       gjae.MainAccount, gjae.Department, gjae.CostCenter,
       gjae.AccountingCurrencyAmount
FROM GeneralJournalEntry AS gje
JOIN GeneralJournalAccountEntry AS gjae
  ON gjae.GeneralJournalEntry = gje.RecId
WHERE gje.Company = 'USMF'
  AND gje.SubledgerVoucher = 'VCH-2026-001';

-- Desafío A: pasar voucher 001 a 002.
-- Desafío B: quitar el filtro de Company para ver un voucher repetido entre USMF y DEMF.
-- La cuenta/dimensión real en F&O no está representada por columnas planas como aquí.
