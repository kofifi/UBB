using BenchmarkDotNet.Running;
using FileCompressor.Benchmarks;

BenchmarkSwitcher.FromAssembly(typeof(TestData).Assembly).Run(args);
