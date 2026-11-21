namespace FileCompressor.Compression.Lz.Matching;

public interface IMatchLengthCounter
{
    int Count(ReadOnlySpan<byte> left, ReadOnlySpan<byte> right);
}
