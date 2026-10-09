ARG WAYPOINT_BUILD_IMAGE=cgr.dev/chainguard/wolfi-base@sha256:1d95114038f76513a9ace6fca107d5582b08c65981f81f61cb56bf7fd2ef216d
ARG WAYPOINT_RUNTIME_IMAGE=cgr.dev/chainguard/wolfi-base@sha256:1d95114038f76513a9ace6fca107d5582b08c65981f81f61cb56bf7fd2ef216d

FROM $WAYPOINT_BUILD_IMAGE AS builder
RUN apk add --no-cache rust build-base cmake perl pkgconf openssl-dev libseccomp-dev python-3.13
WORKDIR /src
COPY .cargo/ .cargo/
COPY waypoint-rust/ waypoint-rust/
COPY waypoint/proxy/lens/prompts/ waypoint/proxy/lens/prompts/
WORKDIR /src/waypoint-rust
ENV CARGO_PROFILE_RELEASE_DEBUG=0 CARGO_PROFILE_RELEASE_STRIP=symbols
RUN cargo build --locked --release -p waypoint-lens
COPY deploy/lens/python_policy.c /tmp/python_policy.c
RUN cc -std=c11 -D_GNU_SOURCE -O2 -Wall -Wextra -Werror /tmp/python_policy.c -lseccomp -o /tmp/python-policy && \
    /tmp/python-policy /tmp/python.seccomp

FROM builder AS test-builder
RUN cargo test --locked --release -p waypoint-lens --test sandbox --no-run --message-format=json > /tmp/test-artifacts.json && \
    python3.13 -c 'import json, pathlib, shutil; rows = [json.loads(line) for line in pathlib.Path("/tmp/test-artifacts.json").read_text().splitlines()]; artifact, = [r["executable"] for r in rows if r.get("executable") and r["target"]["name"] == "sandbox"]; shutil.copyfile(artifact, "/tmp/lens-sandbox-tests")' && \
    chmod 755 /tmp/lens-sandbox-tests

FROM $WAYPOINT_RUNTIME_IMAGE AS service
ARG WAYPOINT_RELEASE_TAG=""
RUN : "${WAYPOINT_RELEASE_TAG:?Pass --build-arg WAYPOINT_RELEASE_TAG matching the gateway}"
RUN apk add --no-cache python-3.13 setpriv libgcc libstdc++ openssl ca-certificates
ENV WAYPOINT_RELEASE_TAG=${WAYPOINT_RELEASE_TAG} PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY --from=builder /src/waypoint-rust/target/release/waypoint-lens /usr/local/bin/waypoint-lens
COPY --from=builder /tmp/python.seccomp /app/lens/python.seccomp
COPY deploy/lens/python_runtime.py /tmp/python_runtime.py
RUN python3.13 -S /tmp/python_runtime.py /app/lens/python-runtime.json && rm /tmp/python_runtime.py
USER 65532:65532
EXPOSE 4318
ENTRYPOINT ["/usr/local/bin/waypoint-lens"]

FROM service AS smoke
COPY --from=test-builder /tmp/lens-sandbox-tests /usr/local/bin/lens-sandbox-tests
ENTRYPOINT ["/usr/local/bin/lens-sandbox-tests"]
CMD ["--ignored", "--nocapture", "--test-threads=1"]

FROM service AS runtime
