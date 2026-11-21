namespace FileCompressor.Compression;

public interface ICompressorProvider
{
    ICompressor Get(string name);
}
