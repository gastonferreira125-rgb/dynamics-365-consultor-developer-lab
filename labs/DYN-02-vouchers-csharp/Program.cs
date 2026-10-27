// Dynamics 365 Finance learning lab — C# / LINQ, no packages, no ERP connection.
// IMPORTANT: These are simplified, fictitious records; not real F&O schema columns.
// Developed for .NET 8. Execute in Visual Studio or: dotnet run --project labs/DYN-02-vouchers-csharp

using System;
using System.Linq;
using System.Collections.Generic;

if (args.Contains("--test", StringComparer.OrdinalIgnoreCase))
{
    LabTests.Run();
    return;
}

string ArgumentOrDefault(string option, string fallback)
{
    var index = Array.FindIndex(args, value => value.Equals(option, StringComparison.OrdinalIgnoreCase));
    return index >= 0 && index + 1 < args.Length ? args[index + 1] : fallback;
}

var company = ArgumentOrDefault("--company", "USMF").ToUpperInvariant();
var voucher = ArgumentOrDefault("--voucher", "VCH-2026-001").ToUpperInvariant();

Console.WriteLine("=== DYNAMICS 365 FINANCE — SIMULATED VOUCHER INVESTIGATION ===");
Console.WriteLine($"Legal entity: {company} | Voucher: {voucher}");
var rows = VoucherDiagnostics.FindVoucher(company, voucher);
if (rows.Count == 0)
{
    Console.WriteLine("No matching voucher found in the fictitious data.");
}
else
{
    foreach (var row in rows)
    {
        Console.WriteLine(
            $"Header RecId {row.HeaderRecId} | Line RecId {row.LineRecId} | " +
            $"Main account {row.MainAccount} | Department {row.Department} | " +
            $"Cost center {row.CostCenter} | Accounting amount {row.Amount:N2}");
    }

    var balance = rows.Sum(row => row.Amount);
    Console.WriteLine($"Reconciliation / Balance: {balance:N2} " +
                      (balance == 0m ? "(BALANCED)" : "(OUT OF BALANCE)"));
}

Console.WriteLine("\n=== SIMULATED FIXED DIMENSION MISMATCHES ===");
var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();
foreach (var issue in mismatches)
{
    Console.WriteLine($"{issue.Company} / {issue.Voucher} | " +
                      $"Main account {issue.MainAccount} | " +
                      $"Posted CC {issue.Actual} vs. currently configured Fixed CC {issue.Expected}");
}
if (mismatches.Count == 0) Console.WriteLine("No discrepancies in demo data.");

Console.WriteLine("\nThis is NOT a real Finance query. In F&O, ledger dimensions are normalized.");
Console.WriteLine("Current settings alone do not prove the configuration used when an old voucher was posted.");
Console.WriteLine("Run with --test to verify the five diagnostic checks.");

record GeneralJournalEntry(long RecId, string SubledgerVoucher, string Company);
record GeneralJournalAccountEntry(long RecId, long GeneralJournalEntryId, string MainAccount,
                                  string Department, string CostCenter, decimal AccountingCurrencyAmount);
record FixedDimensionExample(string Company, string MainAccount, string FixedCostCenter);
record VoucherRow(long HeaderRecId, long LineRecId, string MainAccount,
                  string Department, string CostCenter, decimal Amount);
record Mismatch(string Company, string Voucher, string MainAccount, string Actual, string Expected);

static class DemoData
{
    public static readonly GeneralJournalEntry[] Headers =
    {
        new(1001, "VCH-2026-001", "USMF"),
        new(1002, "VCH-2026-002", "USMF"),
        new(2001, "VCH-2026-001", "DEMF"), // Same voucher text, different legal entity
    };

    public static readonly GeneralJournalAccountEntry[] Lines =
    {
        new(5001, 1001, "606300", "022", "008",  1000m),
        new(5002, 1001, "201100", "022", "009", -1000m),
        new(5003, 1002, "606300", "022", "009",   750m), // Deliberate mismatch
        new(5004, 1002, "201100", "022", "009",  -750m),
        new(6001, 2001, "606300", "022", "012",   200m),
        new(6002, 2001, "201100", "022", "012",  -200m),
    };

    // Didactic table of the CURRENT configuration — not historical evidence.
    public static readonly FixedDimensionExample[] FixedRules =
    {
        new("USMF", "606300", "008"),
        new("DEMF", "606300", "012"),
    };
}

static class VoucherDiagnostics
{
    // LINQ JOIN: GeneralJournalAccountEntry.GeneralJournalEntryId -> GeneralJournalEntry.RecId.
    // In the actual F&O table, the foreign key is GeneralJournalAccountEntry.GeneralJournalEntry.
    public static List<VoucherRow> FindVoucher(string company, string voucher) =>
        (from header in DemoData.Headers
         join line in DemoData.Lines
             on header.RecId equals line.GeneralJournalEntryId
         where header.Company == company && header.SubledgerVoucher == voucher
         orderby line.RecId
         select new VoucherRow(header.RecId, line.RecId, line.MainAccount,
                               line.Department, line.CostCenter,
                               line.AccountingCurrencyAmount)).ToList();

    public static List<Mismatch> FindFixedDimensionMismatches() =>
        (from header in DemoData.Headers
         join line in DemoData.Lines on header.RecId equals line.GeneralJournalEntryId
         join rule in DemoData.FixedRules
             on new { header.Company, line.MainAccount }
             equals new { rule.Company, rule.MainAccount }
         where line.CostCenter != rule.FixedCostCenter
         orderby header.Company, header.SubledgerVoucher
         select new Mismatch(header.Company, header.SubledgerVoucher, line.MainAccount,
                             line.CostCenter, rule.FixedCostCenter)).ToList();
}

static class LabTests
{
    static void Check(bool condition, string description)
    {
        if (!condition) throw new Exception("FAILED: " + description);
        Console.WriteLine("PASS: " + description);
    }

    public static void Run()
    {
        Console.WriteLine("Running five checks on SIMULATED data...");
        var first = VoucherDiagnostics.FindVoucher("USMF", "VCH-2026-001");
        Check(first.Count == 2, "Header JOIN returns two accounting entries");

        Check(first.Single(row => row.MainAccount == "606300").CostCenter == "008",
              "Expense account on voucher 001 has fixed cost center 008");

        var otherCompany = VoucherDiagnostics.FindVoucher("DEMF", "VCH-2026-001");
        Check(first[0].HeaderRecId == 1001 && otherCompany[0].HeaderRecId == 2001,
              "Filter by legal entity prevents cross-company voucher confusion");

        Check(new[] { ("USMF", "VCH-2026-001"), ("USMF", "VCH-2026-002"),
                      ("DEMF", "VCH-2026-001") }
              .All(key => VoucherDiagnostics.FindVoucher(key.Item1, key.Item2)
                  .Sum(row => row.Amount) == 0m),
              "All three fictitious vouchers balance");

        var mismatches = VoucherDiagnostics.FindFixedDimensionMismatches();
        Check(mismatches.Count == 1 && mismatches[0].Voucher == "VCH-2026-002" &&
              mismatches[0].Actual == "009" && mismatches[0].Expected == "008",
              "A discrepancy is detected for voucher 002");
        Console.WriteLine("\n5/5 checks passed. Not an F&O integration test.");
    }
}
