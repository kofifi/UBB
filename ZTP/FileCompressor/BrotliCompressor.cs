using System.IO.Compression;

namespace FileCompressor;

public class BrotliCompressor : ICompressor
{
    public byte[] Compress(byte[] data, int quality)
    {
        if (quality < 0 || quality > 11)
            throw new CompressionException("quality must be between 0 and 11");

        var buffer = new byte[data.Length + 1024];

        if (!BrotliEncoder.TryCompress(data, buffer, out int written, quality, 22))
            throw new CompressionException("could not compress this file");

        return buffer[..written];
    }

    public byte[] Decompress(byte[] data)
    {
        byte[] result;

        try
        {
            using var source = new MemoryStream(data);
            using var brotli = new BrotliStream(source, CompressionMode.Decompress);
            using var target = new MemoryStream();
            brotli.CopyTo(target);
            result = target.ToArray();
        }
        catch (Exception error) when (error is InvalidDataException or InvalidOperationException)
        {
            throw new CompressionException("not a valid .br file");
        }

        if (result.Length == 0)
            throw new CompressionException("not a valid .br file");

        return result;
    }
}
