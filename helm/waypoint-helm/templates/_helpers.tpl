{{/*
Expand the name of the chart.
*/}}
{{- define "waypoint.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "waypoint.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "waypoint.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "waypoint.labels" -}}
helm.sh/chart: {{ include "waypoint.chart" . }}
{{ include "waypoint.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "waypoint.selectorLabels" -}}
app.kubernetes.io/name: {{ include "waypoint.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Enterprise billable-request metering. The client certificate identifies the
deployment to Waypoint's collector, so it is mounted read-only from an existing
Secret rather than passed through the environment.
*/}}
{{- define "waypoint.billingMetrics.certDir" -}}/etc/waypoint/billing-mtls{{- end -}}
{{- define "waypoint.billingMetrics.caDir" -}}/etc/waypoint/billing-mtls-ca{{- end -}}

{{- define "waypoint.billingMetricsEnv" -}}
- name: WAYPOINT_BILLING_METRICS_ENDPOINT
  value: {{ required "billingMetrics.endpoint is required when billingMetrics.enabled is true" .Values.billingMetrics.endpoint | quote }}
- name: WAYPOINT_BILLING_METRICS_CLIENT_CERT
  value: {{ printf "%s/tls.crt" (include "waypoint.billingMetrics.certDir" .) | quote }}
- name: WAYPOINT_BILLING_METRICS_CLIENT_KEY
  value: {{ printf "%s/tls.key" (include "waypoint.billingMetrics.certDir" .) | quote }}
{{- if .Values.billingMetrics.caSecretName }}
- name: WAYPOINT_BILLING_METRICS_CA_CERT
  value: {{ printf "%s/ca.crt" (include "waypoint.billingMetrics.caDir" .) | quote }}
{{- end }}
{{- with .Values.billingMetrics.exportIntervalMs }}
- name: WAYPOINT_BILLING_METRICS_EXPORT_INTERVAL_MS
  value: {{ . | quote }}
{{- end }}
{{- end -}}

{{- define "waypoint.billingMetricsVolumes" -}}
- name: billing-metrics-mtls
  secret:
    secretName: {{ required "billingMetrics.secretName is required when billingMetrics.enabled is true (an existing Secret with tls.crt and tls.key)" .Values.billingMetrics.secretName }}
{{- if .Values.billingMetrics.caSecretName }}
- name: billing-metrics-mtls-ca
  secret:
    secretName: {{ .Values.billingMetrics.caSecretName }}
{{- end }}
{{- end -}}

{{- define "waypoint.billingMetricsVolumeMounts" -}}
- name: billing-metrics-mtls
  mountPath: {{ include "waypoint.billingMetrics.certDir" . }}
  readOnly: true
{{- if .Values.billingMetrics.caSecretName }}
- name: billing-metrics-mtls-ca
  mountPath: {{ include "waypoint.billingMetrics.caDir" . }}
  readOnly: true
{{- end }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "waypoint.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "waypoint.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the service account name used by migration jobs.
When Helm hooks are enabled, pre-install/pre-upgrade hooks run before normal resources.
If this chart is creating the ServiceAccount, it is not yet available for the hook job,
so fall back to "default" (or an explicit override) to avoid a cyclic dependency.
*/}}
{{- define "waypoint.migrationServiceAccountName" -}}
{{- if and .Values.migrationJob.hooks.helm.enabled .Values.serviceAccount.create }}
{{- default "default" .Values.migrationJob.serviceAccountName }}
{{- else }}
{{- include "waypoint.serviceAccountName" . }}
{{- end }}
{{- end }}

{{/*
Get redis service name.
The bundled Redis subchart only serves sentinel in "replication" architecture
(it rejects standalone + sentinel outright), and in that mode the sentinel
Service is named "<release>-redis", not "<release>-redis-master".
*/}}
{{- define "waypoint.redis.serviceName" -}}
{{- if .Values.redis.sentinel.enabled -}}
{{- printf "%s-%s" .Release.Name (default "redis" .Values.redis.nameOverride | trunc 63 | trimSuffix "-") -}}
{{- else -}}
{{- printf "%s-%s-master" .Release.Name (default "redis" .Values.redis.nameOverride | trunc 63 | trimSuffix "-") -}}
{{- end -}}
{{- end -}}

{{/*
Get redis service port
*/}}
{{- define "waypoint.redis.port" -}}
{{- if .Values.redis.sentinel.enabled -}}
{{ .Values.redis.sentinel.service.ports.sentinel }}
{{- else -}}
{{ .Values.redis.master.service.ports.redis }}
{{- end -}}
{{- end -}}

{{/*
Reject an unpinned image tag for the bundled PostgreSQL.
A floating tag lets a chart upgrade start a newer PostgreSQL major against the
existing PersistentVolumeClaim. The server then refuses to start on a data
directory written by another major version, and the only way back is a dump
taken before the change, which by that point no longer exists.
*/}}
{{- define "waypoint.validateBundledPostgresImageTag" -}}
{{- $tag := .Values.postgresql.image.tag | default "" | toString -}}
{{- $digest := .Values.postgresql.image.digest | default "" | toString -}}
{{- if and (eq $digest "") (or (eq $tag "") (eq $tag "latest")) -}}
{{- fail (printf "postgresql.image.tag must be pinned to an explicit version when db.deployStandalone is true (got %q). An unpinned tag can start a different PostgreSQL major against the existing data directory, which makes the database unreadable and is not recoverable in place. Crossing a major version requires a dump and restore." $tag) -}}
{{- end -}}
{{- end -}}

{{/*
Environment shared by the proxy container and the opt-in collector sidecar:
database, pgbouncer, master key, redis, user envVars. Both containers must see
the same DATABASE_URL and REDIS_* so the sidecar reaches the pod's pgbouncer
and the same spend transaction buffer.
*/}}
{{- define "waypoint.proxyEnv" -}}
- name: HOST
  value: "{{ .Values.listen | default "0.0.0.0" }}"
- name: PORT
  value: {{ .Values.service.port | quote}}
{{- if .Values.db.deployStandalone }}
- name: DATABASE_USERNAME
  valueFrom:
    secretKeyRef:
      name: {{ include "waypoint.fullname" . }}-dbcredentials
      key: username
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "waypoint.fullname" . }}-dbcredentials
      key: password
- name: DATABASE_HOST
  value: {{ .Release.Name }}-postgresql
- name: DATABASE_NAME
  value: waypoint
{{- else if .Values.db.useExisting }}
- name: DATABASE_USERNAME
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.secret.name }}
      key: {{ .Values.db.secret.usernameKey }}
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.secret.name }}
      key: {{ .Values.db.secret.passwordKey }}
- name: DATABASE_HOST
  {{- if .Values.db.secret.endpointKey }}
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.secret.name }}
      key: {{ .Values.db.secret.endpointKey }}
  {{- else }}
  value: {{ .Values.db.endpoint }}
  {{- end }}
- name: DATABASE_NAME
  value: {{ .Values.db.database }}
- name: DATABASE_URL
  value: {{ .Values.db.url | quote }}
{{- end }}
{{- if and .Values.db.useExisting .Values.db.readReplicaUrl .Values.db.secret.readReplicaEndpointKey (not .Values.db.secret.readReplicaUrlKey) }}
- name: DATABASE_READER_HOST
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.secret.name }}
      key: {{ .Values.db.secret.readReplicaEndpointKey }}
{{- end }}
{{- if and .Values.db.useExisting .Values.db.secret.readReplicaUrlKey }}
- name: DATABASE_URL_READ_REPLICA
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.secret.name }}
      key: {{ .Values.db.secret.readReplicaUrlKey }}
{{- else if .Values.db.readReplicaUrl }}
- name: DATABASE_URL_READ_REPLICA
  value: {{ .Values.db.readReplicaUrl | quote }}
{{- end }}
{{- if .Values.db.connectionPool.enabled }}
- name: WAYPOINT_PGBOUNCER_ENABLED
  value: "true"
- name: WAYPOINT_PGBOUNCER_MAX_DB_CONNECTIONS
  value: {{ .Values.db.connectionPool.maxDbConnections | quote }}
- name: WAYPOINT_PGBOUNCER_MAX_CLIENT_CONN
  value: {{ .Values.db.connectionPool.maxClientConn | quote }}
{{- end }}
- name: PROXY_MASTER_KEY
  valueFrom:
    secretKeyRef:
      name: {{ .Values.masterkeySecretName | default (printf "%s-masterkey" (include "waypoint.fullname" .)) }}
      key: {{ .Values.masterkeySecretKey | default "masterkey" }}
{{- if .Values.redis.enabled }}
- name: REDIS_HOST
  value: {{ include "waypoint.redis.serviceName" . }}
- name: REDIS_PORT
  value: {{ include "waypoint.redis.port" . | quote }}
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "redis.secretName" .Subcharts.redis }}
      key: {{include "redis.secretPasswordKey" .Subcharts.redis }}
{{- end }}
{{- /*
  Inject WAYPOINT_LOG only when envVars does not already define it.
*/}}
{{- if and .Values.logLevel (not (hasKey (default dict .Values.envVars) "WAYPOINT_LOG")) }}
- name: WAYPOINT_LOG
  value: {{ .Values.logLevel | quote }}
{{- end }}
{{- if .Values.envVars }}
{{- range $key, $val := .Values.envVars }}
- name: {{ $key }}
  value: {{ $val | quote }}
{{- end }}
{{- end }}
{{- with .Values.extraEnvVars }}
{{ toYaml . }}
{{- end }}
{{- if .Values.migrationJob.enabled }}
# Schema updates are owned by the dedicated migrations Job; skip
# the proxy's startup `prisma db push` so N replicas don't race
# one DB on every rollout. Placed last (after envVars and
# extraEnvVars) so this override can't be silently shadowed by a
# user-supplied DISABLE_SCHEMA_UPDATE under last-wins duplicate-env
# semantics — same pattern the migrations Job uses.
- name: DISABLE_SCHEMA_UPDATE
  value: "true"
{{- end }}
{{- end -}}

{{/*
Proxy-only metering and metrics env. The collector sidecar serves no HTTP
traffic, so it gets neither.
*/}}
{{- define "waypoint.proxyMetricsEnv" -}}
{{- if .Values.billingMetrics.enabled }}
{{ include "waypoint.billingMetricsEnv" . }}
{{- end }}
{{- if .Values.metricsServer.enabled }}
{{- if eq (int .Values.metricsServer.port) (int .Values.service.port) }}
{{- fail "metricsServer.port must differ from service.port" }}
{{- end }}
- name: PROMETHEUS_METRICS_PORT
  value: {{ .Values.metricsServer.port | quote }}
{{- end }}
{{- end -}}

{{/*
Directory of the collector's unix socket, shared between the two containers
through an emptyDir. Empty when the sidecar is off or uses 127.0.0.1 TCP.
*/}}
{{- define "waypoint.collector.socketDir" -}}
{{- if and .Values.collector.enabled (hasPrefix "unix://" .Values.collector.address) -}}
{{- dir (trimPrefix "unix://" .Values.collector.address) -}}
{{- end -}}
{{- end -}}

{{- define "waypoint.collectorEnv" -}}
- name: WAYPOINT_COLLECTOR_ENABLED
  value: "true"
- name: WAYPOINT_COLLECTOR_ADDRESS
  value: {{ .Values.collector.address | quote }}
- name: WAYPOINT_COLLECTOR_BUFFER_SIZE
  value: {{ .Values.collector.bufferSize | quote }}
- name: WAYPOINT_COLLECTOR_ON_UNAVAILABLE
  value: {{ .Values.collector.onUnavailable | quote }}
- name: WAYPOINT_COLLECTOR_DRAIN_TIMEOUT_SECONDS
  value: {{ .Values.collector.drainTimeoutSeconds | quote }}
{{- end -}}

{{- define "waypoint.lensWorker.image" -}}
{{- if .Values.lensWorker.image.digest -}}
{{- if not (regexMatch "^sha256:[0-9a-f]{64}$" .Values.lensWorker.image.digest) -}}
{{- fail "lensWorker.image.digest must be sha256 followed by 64 lowercase hex characters" -}}
{{- end -}}
{{- printf "%s@%s" .Values.lensWorker.image.repository .Values.lensWorker.image.digest -}}
{{- else -}}
{{- $backendTag := .Values.image.tag | default .Chart.AppVersion -}}
{{- $releaseTag := ternary (printf "v%s" $backendTag) $backendTag (regexMatch "^[0-9]" $backendTag) -}}
{{- $tag := .Values.lensWorker.image.tag | default $releaseTag -}}
{{- $repository := .Values.lensWorker.image.repository -}}
{{- if and (hasPrefix "sha-" $tag) (eq $repository "ghcr.io/berriai/litellm-lens-worker") -}}
{{- $repository = "ghcr.io/berriai/litellm-lens-worker-dev" -}}
{{- end -}}
{{- printf "%s:%s" $repository $tag -}}
{{- end -}}
{{- end -}}

{{- define "waypoint.gateway.collectorSocketDir" -}}
{{- if and .Values.gateway.collector.enabled (hasPrefix "unix://" .Values.gateway.collector.address) -}}
{{- dir (trimPrefix "unix://" .Values.gateway.collector.address) -}}
{{- end -}}
{{- end -}}

{{/*
WAYPOINT_COLLECTOR_* env shared by the producer (gateway container) and the
consumer (collector container), so both agree on the transport and the
shutdown drain window.
*/}}
{{- define "waypoint.gateway.collectorEnv" -}}
{{- with .Values.gateway.collector }}
- name: WAYPOINT_COLLECTOR_ENABLED
  value: "true"
- name: WAYPOINT_COLLECTOR_ADDRESS
  value: {{ .address | quote }}
- name: WAYPOINT_COLLECTOR_BUFFER_SIZE
  value: {{ .bufferSize | quote }}
- name: WAYPOINT_COLLECTOR_ON_UNAVAILABLE
  value: {{ .onUnavailable | quote }}
- name: WAYPOINT_COLLECTOR_DRAIN_TIMEOUT_SECONDS
  value: {{ .drainTimeoutSeconds | quote }}
{{- end }}
{{- end -}}

{{- define "waypoint.lensWorker.labels" -}}
{{- $labels := include "waypoint.labels" . | fromYaml -}}
{{- $_ := set $labels "app.kubernetes.io/name" (printf "%s-lens-worker" (include "waypoint.name" . | trunc 51 | trimSuffix "-")) -}}
{{- toYaml $labels -}}
{{- end -}}

{{- define "waypoint.lensWorker.serviceTokenSecretName" -}}
{{- .Values.lensWorker.serviceTokenSecret.name | default (printf "%s-lens-service" (include "waypoint.fullname" .)) -}}
{{- end -}}

{{- define "waypoint.lensWorker.bundledClickhouse" -}}
{{- if and .Values.lensWorker.enabled .Values.lensWorker.clickhouse.enabled (not .Values.lensWorker.clickhouseSecret.name) -}}true{{- end -}}
{{- end -}}

{{- define "waypoint.lensWorker.publicUrl" -}}
{{- if .Values.lensWorker.publicUrl -}}
{{- .Values.lensWorker.publicUrl -}}
{{- else if .Values.lensWorker.ingress.enabled -}}
{{- $tls := or (not (empty .Values.lensWorker.ingress.tls)) (hasKey .Values.lensWorker.ingress.annotations "alb.ingress.kubernetes.io/certificate-arn") -}}
{{- printf "%s://%s" (ternary "https" "http" $tls) (required "lensWorker.ingress.host is required" .Values.lensWorker.ingress.host) -}}
{{- else if and .Values.ingress.enabled (eq (len .Values.ingress.hosts) 1) -}}
{{- $host := required "ingress.hosts[0].host is required" (first .Values.ingress.hosts).host -}}
{{- $tls := or (not (empty .Values.ingress.tls)) (hasKey .Values.ingress.annotations "alb.ingress.kubernetes.io/certificate-arn") -}}
{{- printf "%s://%s/lens-ingest" (ternary "https" "http" $tls) $host -}}
{{- else -}}
{{- fail "lensWorker.publicUrl is required when there is no single ingress hostname" -}}
{{- end -}}
{{- end -}}

{{- define "waypoint.lensWorker.clickhouseName" -}}
{{- printf "%s-lens-clickhouse" (include "waypoint.fullname" . | trunc 47 | trimSuffix "-") -}}
{{- end -}}
