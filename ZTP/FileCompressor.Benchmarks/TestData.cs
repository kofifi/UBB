using System.Text;

namespace FileCompressor.Benchmarks;

public static class TestData
{
    public const int Size = 1024 * 1024;

    public static byte[] Create(string kind)
    {
        var random = new Random(42);

        if (kind == "random")
        {
            var bytes = new byte[Size];
            random.NextBytes(bytes);
            return bytes;
        }

        var words = new string[3000];
        for (int i = 0; i < words.Length; i++)
        {
            var letters = new char[random.Next(2, 10)];
            for (int j = 0; j < letters.Length; j++)
                letters[j] = (char)('a' + random.Next(10));
            words[i] = new string(letters);
        }

        var text = new StringBuilder(Size + 16);
        while (text.Length < Size)
            text.Append(words[random.Next(words.Length)]).Append(' ');

        return Encoding.ASCII.GetBytes(text.ToString(0, Size));
    }

    public static ICompressor Compressor(string algorithm) =>
        algorithm == "lz" ? new LzCompressor(new SimdMatchLengthCounter()) : new BrotliCompressor();
}
