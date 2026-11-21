using System.Buffers.Binary;
using FileCompressor.Compression.Lz.Matching;

namespace FileCompressor.Compression.Lz;

public class HashChainMatchFinder
{
    private const int NiceMatch = 256;
    private const int MaxOffset = 65535;
    private const int WindowMask = 65535;
    private const int HashBits = 16;

    private readonly byte[] data;
    private readonly IMatchLengthCounter counter;
    private readonly int maxAttempts;
    private readonly int[] head = new int[1 << HashBits];
    private readonly int[] prev = new int[WindowMask + 1];

    public HashChainMatchFinder(byte[] data, IMatchLengthCounter counter, int maxAttempts)
    {
        this.data = data;
        this.counter = counter;
        this.maxAttempts = maxAttempts;
        Array.Fill(head, -1);
    }

    public Match Find(int pos)
    {
        int bestLength = 0;
        int bestOffset = 0;
        int candidate = head[Hash(pos)];
        var current = data.AsSpan(pos);

        for (int attempt = 0; attempt < maxAttempts && candidate >= 0 && pos - candidate <= MaxOffset; attempt++)
        {
            if (data[candidate + bestLength] == data[pos + bestLength])
            {
                int length = counter.Count(data.AsSpan(candidate, current.Length), current);
                if (length > bestLength)
                {
                    bestLength = length;
                    bestOffset = pos - candidate;
                    if (length >= NiceMatch || length == current.Length)
                        break;
                }
            }

            int next = prev[candidate & WindowMask];
            if (next >= candidate)
                break;

            candidate = next;
        }

        return new Match(bestLength, bestOffset);
    }

    public void Insert(int pos)
    {
        int hash = Hash(pos);
        prev[pos & WindowMask] = head[hash];
        head[hash] = pos;
    }

    private int Hash(int pos)
    {
        uint value = BinaryPrimitives.ReadUInt32LittleEndian(data.AsSpan(pos));
        return (int)((value * 2654435761u) >> (32 - HashBits));
    }
}
