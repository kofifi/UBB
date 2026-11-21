using BenchmarkDotNet.Attributes;
using FileCompressor.Compression.Lz.Matching;

namespace FileCompressor.Benchmarks;

[MemoryDiagnoser]
public class MatchLengthBenchmarks
{
    private readonly IMatchLengthCounter scalar = new ScalarMatchLengthCounter();
    private readonly IMatchLengthCounter simd = new SimdMatchLengthCounter();
    private byte[] left;
    private byte[] right;

    [Params(4, 32, 256, 4096)]
    public int Length;

    [GlobalSetup]
    public void Setup()
    {
        left = new byte[Length + 1];
        new Random(42).NextBytes(left);
        right = (byte[])left.Clone();
        right[Length] ^= 0xFF;
    }

    [Benchmark(Baseline = true)]
    public int Scalar() => scalar.Count(left, right);

    [Benchmark]
    public int Simd() => simd.Count(left, right);

    [Benchmark]
    public int CommonPrefixLength() => left.AsSpan().CommonPrefixLength(right);
}
