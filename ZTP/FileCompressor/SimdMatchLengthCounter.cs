using System.Numerics;
using System.Runtime.Intrinsics;

namespace FileCompressor;

public class SimdMatchLengthCounter : IMatchLengthCounter
{
    public int Count(ReadOnlySpan<byte> left, ReadOnlySpan<byte> right)
    {
        int length = Math.Min(left.Length, right.Length);
        int i = 0;

        if (Vector256.IsHardwareAccelerated)
        {
            while (i + Vector256<byte>.Count <= length)
            {
                var a = Vector256.Create(left.Slice(i, Vector256<byte>.Count));
                var b = Vector256.Create(right.Slice(i, Vector256<byte>.Count));
                uint mismatch = ~Vector256.Equals(a, b).ExtractMostSignificantBits();
                if (mismatch != 0)
                    return i + BitOperations.TrailingZeroCount(mismatch);

                i += Vector256<byte>.Count;
            }
        }

        if (Vector128.IsHardwareAccelerated)
        {
            while (i + Vector128<byte>.Count <= length)
            {
                var a = Vector128.Create(left.Slice(i, Vector128<byte>.Count));
                var b = Vector128.Create(right.Slice(i, Vector128<byte>.Count));
                uint mismatch = ~Vector128.Equals(a, b).ExtractMostSignificantBits() & 0xFFFF;
                if (mismatch != 0)
                    return i + BitOperations.TrailingZeroCount(mismatch);

                i += Vector128<byte>.Count;
            }
        }

        while (i < length && left[i] == right[i])
            i++;

        return i;
    }
}
