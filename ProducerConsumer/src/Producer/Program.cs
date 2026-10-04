using Producer;
using ProducerConsumer.Core;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddWorkQueue(builder.Configuration);
builder.Services.Configure<ProducerOptions>(builder.Configuration.GetSection(ProducerOptions.SectionName));
builder.Services.AddHostedService<ProducerWorker>();

builder.Build().Run();
