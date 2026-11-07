namespace FileCompressor;

public interface ICompressorProvider
{
    ICompressor Get(string name);
}

public class CompressorProvider : ICompressorProvider
{
    private readonly Dictionary<string, ICompressor> compressors;

    public CompressorProvider(IEnumerable<ICompressor> compressors)
    {
        this.compressors = compressors.ToDictionary(c => c.Name, StringComparer.OrdinalIgnoreCase);
    }

    public ICompressor Get(string name)
    {
        if (!compressors.TryGetValue(name, out var compressor))
            throw new CompressionException("unknown algorithm: " + name);

        return compressor;
    }
}
