#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    Http(#[from] waypoint_http::Error),
    #[error("environment_variables values must be strings, numbers or booleans")]
    Environment,
    #[error("MCP host does not yet support configured setting {0}")]
    McpSetting(String),
    #[error(transparent)]
    Mcp(#[from] waypoint_gateway_mcp::ConnectError),
    #[error("MCP requires a configured master key")]
    Auth(#[from] waypoint_gateway_auth::Error),
}
