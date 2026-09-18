#!/bin/bash
while IFS= read -r q; do
  [ -z "$q" ] && continue
  echo "=== QUERY: $q"
  for attempt in 1 2 3; do
    out=$(curl -s --max-time 40 -H "User-Agent: survey-bot/1.0 (mailto:research@example.org)" --get "https://api.crossref.org/works" \
      --data-urlencode "query.bibliographic=$q" --data-urlencode "rows=3" \
      --data-urlencode "select=DOI,title,author,container-title,issued,type,publisher,event,short-container-title")
    if echo "$out" | head -c 20 | grep -q '{'; then
      echo "$out" | python3 fmt.py
      break
    fi
    sleep 4
    [ "$attempt" = 3 ] && echo "  FETCH-FAILED"
  done
  sleep 2
done
