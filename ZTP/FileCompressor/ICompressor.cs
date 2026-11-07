namespace FileCompressor;

public interface ICompressor
{
    string Name { get; }

    byte[] Compress(byte[] data, int quality);

    byte[] Decompress(byte[] data);
}

public class CompressionException : Exception
{
    public CompressionException(string message) : base(message) { }
}
