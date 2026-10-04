using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace ProducerConsumer.Core;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddWorkQueue(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<QueueOptions>(configuration.GetSection(QueueOptions.SectionName));
        services.AddSingleton(TimeProvider.System);
        services.AddSingleton<WorkQueue>();
        services.AddSingleton<QueueProducer>();
        services.AddSingleton<QueueConsumer>();
        return services;
    }
}
