using System.Diagnostics;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5080");
builder.WebHost.ConfigureKestrel(o => o.Limits.MaxRequestBodySize = null);

var app = builder.Build();
app.UseDefaultFiles();
app.UseStaticFiles();

var kept = new List<byte[]>();

app.MapPost("/api/grayscale", async (HttpContext ctx, int repeat = 1, bool keep = false) =>
{
    using var ms = new MemoryStream();
    await ctx.Request.Body.CopyToAsync(ms);
    byte[] input = ms.ToArray();

    var sw = Stopwatch.StartNew();
    byte[] output = input;
    for (int r = 0; r < repeat; r++)
    {
        output = ToGrayscale(input);
        if (keep)
            lock (kept) kept.Add(output);
    }
    sw.Stop();

    ctx.Response.Headers["X-Elapsed-Ms"] = sw.ElapsedMilliseconds.ToString();
    lock (kept) ctx.Response.Headers["X-Kept-Count"] = kept.Count.ToString();
    return Results.Bytes(output, "application/octet-stream");
});

app.MapPost("/api/clear", () =>
{
    lock (kept) kept.Clear();
    return Results.NoContent();
});

app.Run();

static byte[] ToGrayscale(byte[] rgba)
{
    var result = new byte[rgba.Length];
    for (int i = 0; i < rgba.Length; i += 4)
    {
        byte gray = (byte)(0.299 * rgba[i] + 0.587 * rgba[i + 1] + 0.114 * rgba[i + 2]);
        result[i] = result[i + 1] = result[i + 2] = gray;
        result[i + 3] = rgba[i + 3];
    }
    return result;
}
