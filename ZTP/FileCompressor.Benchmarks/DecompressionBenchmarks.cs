using BenchmarkDotNet.Attributes;
using FileCompressor.Compression;

namespace FileCompressor.Benchmarks;

[MemoryDiagnoser]
[SimpleJob(launchCount: 1, warmupCount: 2, iterationCount: 5)]
public class DecompressionBenchmarks
{
    private ICompressor compressor;
    private byte[] compressed;

    [Params("lz", "brotli")]
    public string Algorithm;

    [Params("text", "random")]
    public string Data;

    [GlobalSetup]
    public void Setup()
    {
        compressor = TestData.Compressor(Algorithm);
        compressed = compressor.Compress(TestData.Create(Data), 5);
    }

    [Benchmark]
    public byte[] Decompress() => compressor.Decompress(compressed);
}
