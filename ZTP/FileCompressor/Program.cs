using System.Diagnostics;
using FileCompressor;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<ICompressor, BrotliCompressor>();

var app = builder.Build();

app.UseDefaultFiles();
app.UseStaticFiles();

app.MapPost("/api/compress", async (HttpRequest request, HttpResponse response, ICompressor compressor, int quality = 11) =>
{
    byte[] input = await ReadBody(request);
    if (input.Length == 0)
        return Results.BadRequest(new { error = "empty file" });

    return Run(response, input, () => compressor.Compress(input, quality));
});

app.MapPost("/api/decompress", async (HttpRequest request, HttpResponse response, ICompressor compressor) =>
{
    byte[] input = await ReadBody(request);
    if (input.Length == 0)
        return Results.BadRequest(new { error = "empty file" });

    return Run(response, input, () => compressor.Decompress(input));
});

app.Run();

static async Task<byte[]> ReadBody(HttpRequest request)
{
    using var buffer = new MemoryStream();
    await request.Body.CopyToAsync(buffer);
    return buffer.ToArray();
}

static IResult Run(HttpResponse response, byte[] input, Func<byte[]> work)
{
    byte[] output;
    var clock = Stopwatch.StartNew();

    try
    {
        output = work();
    }
    catch (CompressionException error)
    {
        return Results.BadRequest(new { error = error.Message });
    }

    clock.Stop();

    response.Headers["X-Original-Size"] = input.Length.ToString();
    response.Headers["X-Result-Size"] = output.Length.ToString();
    response.Headers["X-Elapsed-Ms"] = clock.ElapsedMilliseconds.ToString();

    return Results.Bytes(output, "application/octet-stream");
}
