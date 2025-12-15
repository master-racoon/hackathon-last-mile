using System.Globalization;
using System.Text.RegularExpressions;

namespace LastMile.Common.Helpers;

public static partial class FormatHelper
{
    [GeneratedRegex(@"\B(?=(\d{3})+(?!\d))")]
    private static partial Regex NumberGroupingRegex();

    public static string FormatNumber(decimal number, int decimals = 0)
    {
        // Convert to string with requested decimal places
        string priceStr = number.ToString($"0.{new string('0', decimals)}", CultureInfo.InvariantCulture);

        // Split into integer and decimal parts
        string[] parts = priceStr.Split('.');

        // Add space as thousand separator to integer part
        string integerPart = NumberGroupingRegex().Replace(parts[0], " ");

        // Return formatted value
        return parts.Length > 1 ? $"{integerPart},{parts[1]}" : integerPart;
    }

    public static string FormatCurrency(string currency)
    {
        return currency.ToUpperInvariant();
    }

    public static string FormatPrice(decimal price, string currency, int decimals = 0)
    {
        return $"{FormatNumber(price, decimals)} {FormatCurrency(currency)}";
    }

    public static string FormatPricePerShare(decimal price, string currency)
    {
        return $"{FormatPrice(price, currency, 2)} / Share";
    }

    public static string FormatDate(DateTimeOffset? date)
    {
        return date?.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture) ?? "N/A";
    }

    public static string FormatPercent(decimal value)
    {
        var percent = value * 100;
        return $"{percent:0.##}%";
    }
}
