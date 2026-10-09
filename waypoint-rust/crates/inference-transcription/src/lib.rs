pub mod types;
pub use waypoint_inference::RouteError as Error;
mod constants;
mod handler;
mod prepare;
pub use handler::execute_audio_transcription_provider_call;
use waypoint_auth::AuthServices;
use waypoint_secrets::source::SecretSource;
pub use prepare::prepare_audio_transcription_provider_call;
use serde_json::Value;
use std::sync::Arc;

use crate::types::AudioTranscriptionRequest;

#[derive(Clone)]
pub struct AudioTranscriptionRoute {
    http: waypoint_http::Client,
    auth: Arc<AuthServices>,
    secrets: Arc<dyn SecretSource>,
}

impl AudioTranscriptionRoute {
    pub fn new(
        http: waypoint_http::Client,
        auth: Arc<AuthServices>,
        secrets: Arc<dyn SecretSource>,
    ) -> Self {
        Self {
            http,
            auth,
            secrets,
        }
    }

    #[tracing::instrument(name = "waypoint.route", skip_all, fields(
        route = "audio_transcription",
        model = request.model,
        provider,
        resolved_model,
        stream = false,
        outcome
    ))]
    pub async fn execute(&self, request: AudioTranscriptionRequest<'_>) -> Result<Value, Error> {
        waypoint_inference::diagnostic::unary(async {
            let request =
                prepare_audio_transcription_provider_call(request, self.secrets.as_ref()).await?;
            waypoint_inference::diagnostic::provider(&request.model, &request.custom_llm_provider);
            let execute: futures_util::future::BoxFuture<'_, Result<Value, Error>> = Box::pin(
                execute_audio_transcription_provider_call(&self.http, &self.auth, request),
            );
            execute.await
        })
        .await
    }
}
