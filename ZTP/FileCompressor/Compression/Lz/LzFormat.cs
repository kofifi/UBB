namespace FileCompressor.Compression.Lz;

public static class LzFormat
{
    public const int MinMatch = 4;
    public const int HeaderSize = 8;
    public const int MaxOutputSize = 256 * 1024 * 1024;
    public static ReadOnlySpan<byte> Magic => "LZK1"u8;
}
