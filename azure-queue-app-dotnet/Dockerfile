# Builds either service: --build-arg APP=Orders.Api or APP=Orders.Worker
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG APP=Orders.Api
WORKDIR /src
COPY src/ src/
RUN dotnet publish src/${APP}/${APP}.csproj -c Release -o /out /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0
ARG APP=Orders.Api
ENV APP_DLL=${APP}.dll \
    ASPNETCORE_URLS=http://+:8080
WORKDIR /app
COPY --from=build /out .
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "exec dotnet $APP_DLL"]
