#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

APP_NAME="RADAR-AS"
WORKDIR="test/test_general"
LOG_DIR="./logs"
PID_DIR="./pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

LOG_FILE="$LOG_DIR/${APP_NAME}_$(date +%Y-%m-%d).log"
PID_FILE="$PID_DIR/${APP_NAME}.pid"

timestamp() {
  date +'%Y-%m-%d %H:%M:%S'
}

start_app() {
  stop_app

  echo "[$(timestamp)] 🚀 Avvio $APP_NAME..."

  nohup pipenv run bash -c "cd $WORKDIR && python3 run.py" >> "$LOG_FILE" 2>&1 &
  pid=$!
  echo "$pid" > "$PID_FILE"

  echo "[$(timestamp)] ✅ $APP_NAME avviata (PID $pid). Log: $LOG_FILE"

  echo "[$(timestamp)] ⏳ In attesa che l'app indichi la porta in uso..."

  MAX_WAIT=30
  elapsed=0
  PORT=""

  while [[ $elapsed -lt $MAX_WAIT ]]; do
    if grep -q "Listening on http://0.0.0.0:" "$LOG_FILE"; then
      PORT=$(grep -oP 'Listening on http://0.0.0.0:\K[0-9]+' "$LOG_FILE" | head -1)
      break
    fi
    sleep 1
    ((elapsed++))
  done

  echo "[$(timestamp)] 📄 Ultime righe di log:"
  tail -n 10 "$LOG_FILE"

  if [[ -n "$PORT" ]]; then
    echo "[$(timestamp)] 🌐 $APP_NAME è in esecuzione sulla porta: $PORT"
  else
    echo "[$(timestamp)] ⚠️ Porta non trovata nei log entro ${MAX_WAIT}s."
  fi
}

stop_app() {
  if [[ -f "$PID_FILE" ]]; then
    pid=$(<"$PID_FILE")
    if ps -p "$pid" > /dev/null 2>&1; then
      echo "[$(timestamp)] 🛑 Arresto processo $APP_NAME (PID $pid)..."
      kill "$pid"
      sleep 2
      if ps -p "$pid" > /dev/null 2>&1; then
        echo "[$(timestamp)] ⚠️ Processo non terminato, forzo kill..."
        kill -9 "$pid"
      fi
      echo "[$(timestamp)] ✅ Processo arrestato."
    else
      echo "[$(timestamp)] ℹ️ PID trovato ma processo non attivo, pulisco pidfile."
    fi
    rm -f "$PID_FILE"
  else
    echo "[$(timestamp)] ℹ️ Nessun PID file trovato, niente da fermare."
  fi
}

status_app() {
  if [[ -f "$PID_FILE" ]]; then
    pid=$(<"$PID_FILE")
    if ps -p "$pid" > /dev/null 2>&1; then
      echo "[$(timestamp)] ✅ $APP_NAME è in esecuzione (PID $pid)."
      if [[ -f "$LOG_FILE" ]]; then
        PORT=$(grep -oP 'Listening on http://0.0.0.0:\K[0-9]+' "$LOG_FILE" | head -1 || true)
        [[ -n "$PORT" ]] && echo "🌐 In ascolto sulla porta: $PORT"
      fi
    else
      echo "[$(timestamp)] ⚠️ PID file presente ma processo non attivo."
    fi
  else
    echo "[$(timestamp)] ❌ $APP_NAME non è in esecuzione."
  fi
}

case "${1:-}" in
  start)
    start_app
    ;;
  stop)
    stop_app
    ;;
  restart)
    stop_app
    start_app
    ;;
  status)
    status_app
    ;;
  *)
    echo "Uso: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac
