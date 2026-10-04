# Builds either app: --build-arg APP=Producer or APP=Consumer
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG APP=Consumer
WORKDIR /src
COPY src/ src/
RUN dotnet publish src/${APP}/${APP}.csproj -c Release -o /out /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/runtime:8.0
ARG APP=Consumer
ENV APP_DLL=${APP}.dll
WORKDIR /app
COPY --from=build /out .
ENTRYPOINT ["sh", "-c", "exec dotnet $APP_DLL"]
