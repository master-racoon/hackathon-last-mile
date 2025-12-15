namespace LastMile.Common.Configs;

public class WhiteListConfig
{
    public bool Enabled { get; set; }

    public List<string> AllowedPersonalNumbers { get; set; } = [];
}
