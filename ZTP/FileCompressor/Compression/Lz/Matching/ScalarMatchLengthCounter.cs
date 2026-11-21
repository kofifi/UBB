namespace FileCompressor.Compression.Lz.Matching;

public class ScalarMatchLengthCounter : IMatchLengthCounter
{
    public int Count(ReadOnlySpan<byte> left, ReadOnlySpan<byte> right)
    {
        int length = Math.Min(left.Length, right.Length);
        int i = 0;

        while (i < length && left[i] == right[i])
            i++;

        return i;
    }
}
