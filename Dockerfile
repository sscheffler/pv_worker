FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
ENV PYTHONPATH="."
ENV APP_HOME=/app
ENV HOME=/home/appuser

WORKDIR $APP_HOME

# Create non-root user and group
RUN adduser --disabled-password --gecos "" appuser

# Copy everything including installed Python packages
COPY --chown=appuser:appuser ./src ./src
COPY --chown=appuser:appuser start.sh ./start.sh

# Set permissions for the application and dependencies
RUN chmod +x start.sh && \
    chown -R appuser:appuser $APP_HOME && \
    chown -R appuser:appuser /usr/local

# Use the non-root user for uv-related steps so cache ownership is correct
USER appuser

RUN uv tool install --prerelease=allow azure-cli@latest

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-group migrations

EXPOSE 8000
CMD ["sh", "./start.sh"]
