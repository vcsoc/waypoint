use waypoint_host::observation::ObservationSender;
pub mod route;
pub mod types;
pub use waypoint_inference::RouteError as Error;
mod common_utils;
pub mod constants;
pub(crate) mod handler;
mod prepare;
use waypoint_llms_types::formats::chat_completions::ChatCompletionsResponse;
use prepare::{prepare_provider_request, resolve_request};

use waypoint_auth::AuthServices;
use waypoint_secrets::source::SecretSource;
use std::sync::Arc;
use types::ChatCompletionsRequest;

#[derive(Clone)]
pub struct ChatCompletionsRoute {
    http: waypoint_http::Client,
    auth: Arc<AuthServices>,
    secrets: Arc<dyn SecretSource>,
    cache: Option<waypoint_cache_response::ScopedCache>,
}

impl ChatCompletionsRoute {
    pub fn new(
        http: waypoint_http::Client,
        auth: Arc<AuthServices>,
        secrets: Arc<dyn SecretSource>,
    ) -> Self {
        Self {
            http,
            auth,
            secrets,
            cache: None,
        }
    }

    pub fn with_cache(self, cache: waypoint_cache_response::ScopedCache) -> Self {
        Self {
            cache: Some(cache),
            ..self
        }
    }

    pub async fn execute(
        &self,
        request: ChatCompletionsRequest<'_>,
        interceptors: &impl waypoint_host::interceptors::Interceptors<Error>,
        options: impl Into<waypoint_inference::CallOptions>,
    ) -> Result<ChatCompletionsResponse, Error> {
        let waypoint_inference::CallOptions {
            cache: cache_options,
            observers,
        } = options.into();
        waypoint_host::lifecycle::observe_unary(
            observers.clone(),
            self.run_call(
                request.into(),
                cache_options,
                interceptors,
                observers.as_ref(),
            ),
        )
        .await
    }

    async fn run(
        &self,
        request: ChatCompletionsRequest<'_>,
        cache_options: Option<waypoint_cache_response::CachePolicy>,
        interceptors: &impl waypoint_host::interceptors::Interceptors<Error>,
        observers: Option<&ObservationSender>,
    ) -> Result<ChatCompletionsResponse, Error> {
        let resolved = resolve_request(request)?;
        let snapshot = self
            .secrets
            .resolve(&resolved.config.secret_names())
            .await?;
        let prepared = prepare_provider_request(resolved, snapshot)?;
        waypoint_inference::diagnostic::provider(&prepared.model, &prepared.custom_llm_provider);
        let execute: futures_util::future::BoxFuture<'_, Result<ChatCompletionsResponse, Error>> =
            Box::pin(handler::execute(
                &self.http,
                &self.auth,
                prepared,
                self.cache.clone(),
                cache_options,
                interceptors,
                observers,
            ));
        execute.await
    }
}
