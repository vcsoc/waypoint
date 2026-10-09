use std::sync::Arc;

use waypoint_auth_gcp::{GoogleCredentials, VertexConfig};
use waypoint_auth_types::{InputSource, Sourced};
use waypoint_core_utils::settings::Lookup;
use waypoint_secrets_types::SecretValue;

pub(crate) fn credentials(
    project: Option<String>,
    credentials: Option<SecretValue>,
    environment: Arc<dyn Lookup + Send + Sync>,
) -> GoogleCredentials {
    GoogleCredentials::new(
        VertexConfig::new(
            credentials.map(|value| Sourced::new(value, InputSource::Environment)),
            project,
            None,
        ),
        Arc::new(move |name| environment.get(name)),
    )
}
