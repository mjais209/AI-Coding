using Consumer;
using ProducerConsumer.Core;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddWorkQueue(builder.Configuration);
builder.Services.AddSingleton<IWorkItemHandler, WorkItemHandler>();
builder.Services.AddHostedService<ConsumerWorker>();

builder.Build().Run();
