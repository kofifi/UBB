using FileCompressor.Compression.Lz.Matching;

namespace FileCompressor.Compression.Lz;

public class LzCompressor : ICompressor
{
    private const int FastModeMaxQuality = 5;
    private const int SkipShift = 6;

    private readonly IMatchLengthCounter counter;

    public LzCompressor(IMatchLengthCounter counter)
    {
        this.counter = counter;
    }

    public string Name => "lz";

    public byte[] Compress(byte[] data, int quality)
    {
        if (quality < 0 || quality > 11)
            throw new CompressionException("quality must be between 0 and 11");

        bool thorough = quality > FastModeMaxQuality;
        var writer = new LzBlockWriter(data.Length);
        var finder = new HashChainMatchFinder(data, counter, 1 << quality);

        int pos = 0;
        int anchor = 0;

        while (pos + LzFormat.MinMatch <= data.Length)
        {
            var match = finder.Find(pos);
            finder.Insert(pos);

            if (match.Length < LzFormat.MinMatch)
            {
                pos += thorough ? 1 : 1 + ((pos - anchor) >> SkipShift);
                continue;
            }

            writer.WriteSequence(data.AsSpan(anchor, pos - anchor), match);

            if (thorough)
            {
                for (int i = pos + 1; i < pos + match.Length && i + LzFormat.MinMatch <= data.Length; i++)
                    finder.Insert(i);
            }
            else if (pos + match.Length - 2 + LzFormat.MinMatch <= data.Length)
            {
                finder.Insert(pos + match.Length - 2);
            }

            pos += match.Length;
            anchor = pos;
        }

        writer.WriteLastLiterals(data.AsSpan(anchor));
        return writer.ToArray();
    }

    public byte[] Decompress(byte[] data) => LzBlockReader.Read(data);
}
