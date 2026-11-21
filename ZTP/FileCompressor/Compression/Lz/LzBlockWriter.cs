using System.Buffers.Binary;

namespace FileCompressor.Compression.Lz;

public class LzBlockWriter
{
    private readonly MemoryStream output;

    public LzBlockWriter(int originalLength)
    {
        output = new MemoryStream(originalLength / 2 + LzFormat.HeaderSize);
        output.Write(LzFormat.Magic);

        Span<byte> size = stackalloc byte[4];
        BinaryPrimitives.WriteInt32LittleEndian(size, originalLength);
        output.Write(size);
    }

    public void WriteSequence(ReadOnlySpan<byte> literals, Match match)
    {
        int matchCode = match.Length - LzFormat.MinMatch;
        output.WriteByte((byte)(Math.Min(literals.Length, 15) << 4 | Math.Min(matchCode, 15)));
        WriteLength(literals.Length);
        output.Write(literals);
        output.WriteByte((byte)match.Offset);
        output.WriteByte((byte)(match.Offset >> 8));
        WriteLength(matchCode);
    }

    public void WriteLastLiterals(ReadOnlySpan<byte> literals)
    {
        output.WriteByte((byte)(Math.Min(literals.Length, 15) << 4));
        WriteLength(literals.Length);
        output.Write(literals);
    }

    public byte[] ToArray() => output.ToArray();

    private void WriteLength(int value)
    {
        if (value < 15)
            return;

        value -= 15;
        while (value >= 255)
        {
            output.WriteByte(255);
            value -= 255;
        }

        output.WriteByte((byte)value);
    }
}
