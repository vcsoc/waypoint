use std::time::Duration;

use waypoint_http::outbound::OutboundRequest;
use waypoint_llms::base_llm::auth::Authenticated;
use serde_json::Value;

#[tracing::instrument(
    name = "waypoint.provider.send",
    level = "debug",
    skip_all,
    fields(status)
)]
pub async fn send(
    request: OutboundRequest,
    client: &waypoint_http::Client,
) -> Result<reqwest::Response, reqwest::Error> {
    request.send(client).await.inspect(|response| {
        tracing::Span::current().record("status", response.status().as_u16());
    })
}

/// Header credentials are already in `headers`; SigV4 is applied here, over the
/// bytes that are sent.
pub fn outbound_request(
    authenticated: Authenticated,
    url: String,
    body: &Value,
    timeout: Option<Duration>,
) -> Result<OutboundRequest, waypoint_http::Error> {
    let Authenticated { headers, signer } = authenticated;
    match signer {
        None => OutboundRequest::json(url, headers, body, timeout),
        Some(signer) => OutboundRequest::signed_json(url, headers, body, timeout, &signer),
    }
}
