#!/bin/sh

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z "$host" "$port"; do
  echo "Esperando a que la base de datos esté lista en $host:$port..."
  sleep 1
done

exec $cmd
