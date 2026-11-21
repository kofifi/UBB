using BenchmarkDotNet.Attributes;
using FileCompressor.Compression;

namespace FileCompressor.Benchmarks;

[MemoryDiagnoser]
[SimpleJob(launchCount: 1, warmupCount: 2, iterationCount: 5)]
public class CompressionBenchmarks
{
    private ICompressor compressor;
    private byte[] input;

    [Params("lz", "brotli")]
    public string Algorithm;

    [Params("text", "random")]
    public string Data;

    [Params(0, 5, 11)]
    public int Quality;

    [GlobalSetup]
    public void Setup()
    {
        compressor = TestData.Compressor(Algorithm);
        input = TestData.Create(Data);
    }

    [Benchmark]
    public byte[] Compress() => compressor.Compress(input, Quality);
}
