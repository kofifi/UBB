using System.Buffers.Binary;

namespace FileCompressor;

public class LzCompressor : ICompressor
{
    private const int MinMatch = 4;
    private const int NiceMatch = 256;
    private const int MaxOffset = 65535;
    private const int WindowMask = 65535;
    private const int HashBits = 16;
    private const int HeaderSize = 8;
    private const int MaxOutputSize = 256 * 1024 * 1024;
    private static readonly byte[] Magic = "LZK1"u8.ToArray();

    private readonly IMatchLengthCounter counter;

    public LzCompressor(IMatchLengthCounter counter)
    {
        this.counter = counter;
    }

    public string Name => "lz";

    public byte[] Compress(byte[] data, int quality)
    {
        if (quality < 0 || quality > 11)
            throw new CompressionException("quality must be between 0 and 11");

        int maxAttempts = 1 << quality;
        var output = new MemoryStream(data.Length / 2 + HeaderSize);
        output.Write(Magic);
        WriteInt32(output, data.Length);

        var head = new int[1 << HashBits];
        Array.Fill(head, -1);
        var prev = new int[WindowMask + 1];

        int pos = 0;
        int anchor = 0;

        while (pos + MinMatch <= data.Length)
        {
            var (length, offset) = FindMatch(data, pos, head, prev, maxAttempts);
            Insert(data, pos, head, prev);

            if (length < MinMatch)
            {
                pos++;
                continue;
            }

            WriteSequence(output, data.AsSpan(anchor, pos - anchor), offset, length);

            for (int i = pos + 1; i < pos + length && i + MinMatch <= data.Length; i++)
                Insert(data, i, head, prev);

            pos += length;
            anchor = pos;
        }

        WriteLastLiterals(output, data.AsSpan(anchor));
        return output.ToArray();
    }

    public byte[] Decompress(byte[] data)
    {
        if (data.Length < HeaderSize || !data.AsSpan(0, Magic.Length).SequenceEqual(Magic))
            throw Invalid();

        int size = BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(Magic.Length));
        if (size < 0 || size > MaxOutputSize)
            throw Invalid();

        var result = new byte[size];
        int input = HeaderSize;
        int written = 0;

        while (true)
        {
            byte token = ReadByte(data, ref input);

            int literals = ReadLength(data, ref input, token >> 4);
            if (literals > data.Length - input || literals > size - written)
                throw Invalid();

            data.AsSpan(input, literals).CopyTo(result.AsSpan(written));
            input += literals;
            written += literals;

            if (written == size)
                break;

            int offset = ReadByte(data, ref input) | ReadByte(data, ref input) << 8;
            int length = ReadLength(data, ref input, token & 15) + MinMatch;
            if (offset == 0 || offset > written || length > size - written)
                throw Invalid();

            for (int i = 0; i < length; i++)
                result[written + i] = result[written - offset + i];

            written += length;
        }

        if (input != data.Length)
            throw Invalid();

        return result;
    }

    private (int Length, int Offset) FindMatch(byte[] data, int pos, int[] head, int[] prev, int maxAttempts)
    {
        int bestLength = 0;
        int bestOffset = 0;
        int candidate = head[Hash(data, pos)];
        var current = data.AsSpan(pos);

        for (int attempt = 0; attempt < maxAttempts && candidate >= 0 && pos - candidate <= MaxOffset; attempt++)
        {
            int length = counter.Count(data.AsSpan(candidate, current.Length), current);
            if (length > bestLength)
            {
                bestLength = length;
                bestOffset = pos - candidate;
                if (length >= NiceMatch)
                    break;
            }

            int next = prev[candidate & WindowMask];
            if (next >= candidate)
                break;

            candidate = next;
        }

        return (bestLength, bestOffset);
    }

    private static void Insert(byte[] data, int pos, int[] head, int[] prev)
    {
        int hash = Hash(data, pos);
        prev[pos & WindowMask] = head[hash];
        head[hash] = pos;
    }

    private static int Hash(byte[] data, int pos)
    {
        uint value = BinaryPrimitives.ReadUInt32LittleEndian(data.AsSpan(pos));
        return (int)((value * 2654435761u) >> (32 - HashBits));
    }

    private static void WriteSequence(MemoryStream output, ReadOnlySpan<byte> literals, int offset, int length)
    {
        int matchCode = length - MinMatch;
        output.WriteByte((byte)(Math.Min(literals.Length, 15) << 4 | Math.Min(matchCode, 15)));
        WriteLength(output, literals.Length);
        output.Write(literals);
        output.WriteByte((byte)offset);
        output.WriteByte((byte)(offset >> 8));
        WriteLength(output, matchCode);
    }

    private static void WriteLastLiterals(MemoryStream output, ReadOnlySpan<byte> literals)
    {
        output.WriteByte((byte)(Math.Min(literals.Length, 15) << 4));
        WriteLength(output, literals.Length);
        output.Write(literals);
    }

    private static void WriteLength(MemoryStream output, int value)
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

    private static void WriteInt32(MemoryStream output, int value)
    {
        Span<byte> bytes = stackalloc byte[4];
        BinaryPrimitives.WriteInt32LittleEndian(bytes, value);
        output.Write(bytes);
    }

    private static int ReadLength(byte[] data, ref int input, int code)
    {
        if (code < 15)
            return code;

        int value = 15;
        byte next;
        do
        {
            next = ReadByte(data, ref input);
            value += next;
            if (value > MaxOutputSize)
                throw Invalid();
        } while (next == 255);

        return value;
    }

    private static byte ReadByte(byte[] data, ref int input)
    {
        if (input >= data.Length)
            throw Invalid();

        return data[input++];
    }

    private static CompressionException Invalid() => new("not a valid .lzk file");
}
