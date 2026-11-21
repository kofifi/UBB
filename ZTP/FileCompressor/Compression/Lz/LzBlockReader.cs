using System.Buffers.Binary;

namespace FileCompressor.Compression.Lz;

public static class LzBlockReader
{
    public static byte[] Read(byte[] data)
    {
        if (data.Length < LzFormat.HeaderSize || !data.AsSpan(0, LzFormat.Magic.Length).SequenceEqual(LzFormat.Magic))
            throw Invalid();

        int size = BinaryPrimitives.ReadInt32LittleEndian(data.AsSpan(LzFormat.Magic.Length));
        if (size < 0 || size > LzFormat.MaxOutputSize)
            throw Invalid();

        var result = new byte[size];
        int input = LzFormat.HeaderSize;
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
            int length = ReadLength(data, ref input, token & 15) + LzFormat.MinMatch;
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
            if (value > LzFormat.MaxOutputSize)
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
