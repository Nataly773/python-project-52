#!/usr/bin/env bash
# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости, статику, миграции
make install && make collectstatic && make migrate