#!/usr/bin/env bash
set -euo pipefail

readonly CONTEXT7_BASE_URL="${CONTEXT7_BASE_URL:-https://context7.com}"
readonly CONTEXT7_KEYCHAIN_SERVICE="${CONTEXT7_KEYCHAIN_SERVICE:-autocompany-context7-key}"

usage() {
  printf '%s\n' \
    'Usage:' \
    '  context7_docs.sh check' \
    '  context7_docs.sh search <library-name> <specific-query>' \
    '  context7_docs.sh docs <library-id> <specific-query> [json|txt]'
}

get_api_key() {
  if [[ -n "${CONTEXT7_API_KEY:-}" ]]; then
    printf '%s' "${CONTEXT7_API_KEY}"
    return
  fi

  if command -v security >/dev/null 2>&1; then
    security find-generic-password -s "${CONTEXT7_KEYCHAIN_SERVICE}" -w 2>/dev/null
    return
  fi

  printf 'Context7 API key unavailable. Set CONTEXT7_API_KEY or configure Keychain service %s.\n' \
    "${CONTEXT7_KEYCHAIN_SERVICE}" >&2
  return 1
}

request() {
  local endpoint="$1"
  shift
  local api_key
  api_key="$(get_api_key)"
  curl --silent --show-error --fail-with-body --get \
    "${CONTEXT7_BASE_URL}${endpoint}" \
    --header "Authorization: Bearer ${api_key}" \
    "$@"
}

command_name="${1:-}"
case "${command_name}" in
  check)
    response="$(request '/api/v2/libs/search' \
      --data-urlencode 'libraryName=cloudflare workers' \
      --data-urlencode 'query=official Workers documentation')"
    if command -v jq >/dev/null 2>&1; then
      printf '%s' "${response}" | jq '{ok: (.results | type == "array"), firstLibraryId: .results[0].id}'
    else
      printf 'Context7 authentication and search request succeeded.\n'
    fi
    ;;
  search)
    [[ "$#" -eq 3 ]] || { usage >&2; exit 2; }
    request '/api/v2/libs/search' \
      --data-urlencode "libraryName=$2" \
      --data-urlencode "query=$3"
    ;;
  docs)
    [[ "$#" -ge 3 && "$#" -le 4 ]] || { usage >&2; exit 2; }
    output_type="${4:-json}"
    [[ "${output_type}" == 'json' || "${output_type}" == 'txt' ]] || {
      printf 'Output type must be json or txt.\n' >&2
      exit 2
    }
    request '/api/v2/context' \
      --data-urlencode "libraryId=$2" \
      --data-urlencode "query=$3" \
      --data-urlencode "type=${output_type}"
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

