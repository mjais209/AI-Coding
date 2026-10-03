using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Orders.Core;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddOrderStorage(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<StorageOptions>(configuration.GetSection(StorageOptions.SectionName));
        services.AddSingleton<OrderStorage>();
        services.AddSingleton<OrderProcessor>();
        return services;
    }
}
