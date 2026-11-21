namespace FileCompressor.Compression;

public interface ICompressor
{
    string Name { get; }

    byte[] Compress(byte[] data, int quality);

    byte[] Decompress(byte[] data);
}
