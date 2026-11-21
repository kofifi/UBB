using BenchmarkDotNet.Attributes;
using FileCompressor.Compression.Lz;
using FileCompressor.Compression.Lz.Matching;

namespace FileCompressor.Benchmarks;

[MemoryDiagnoser]
[SimpleJob(launchCount: 1, warmupCount: 2, iterationCount: 5)]
public class LzCounterBenchmarks
{
    private LzCompressor compressor;
    private byte[] input;

    [Params("scalar", "simd")]
    public string Counter;

    [Params("text", "random")]
    public string Data;

    [Params(0, 5, 11)]
    public int Quality;

    [GlobalSetup]
    public void Setup()
    {
        IMatchLengthCounter counter = Counter == "simd" ? new SimdMatchLengthCounter() : new ScalarMatchLengthCounter();
        compressor = new LzCompressor(counter);
        input = TestData.Create(Data);
    }

    [Benchmark]
    public byte[] Compress() => compressor.Compress(input, Quality);
}
