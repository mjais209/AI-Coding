using Orders.Core;
using Orders.Worker;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddOrderStorage(builder.Configuration);
builder.Services.AddHostedService<OrderWorker>();

builder.Build().Run();
