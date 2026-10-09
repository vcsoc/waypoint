mod common_utils;
mod constants;
mod handler;
mod prepare;
pub mod route;
mod types;

use futures_util::FutureExt;
use waypoint_auth::AuthServices;
use waypoint_host::interceptors::{ExecutionFacts, Interceptors, ResultSource};

use waypoint_inference::{caching::CallCache, context::CallContext};
use waypoint_secrets::source::SecretSource;
use std::sync::Arc;

pub use waypoint_inference::RouteError as Error;
pub use types::{
    MessagesCall, MessagesCallResponse, MessagesSettings, MessagesShaping, messages_body,
};

#[derive(Clone)]
pub struct MessagesRoute {
    http: waypoint_http::Client,
    auth: Arc<AuthServices>,
    secrets: Arc<dyn SecretSource>,
    cache: Option<waypoint_cache_response::ScopedCache>,
}

impl MessagesRoute {
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

    #[must_use]
    pub fn with_cache(self, cache: waypoint_cache_response::ScopedCache) -> Self {
        Self {
            cache: Some(cache),
            ..self
        }
    }

    pub async fn execute(
        &self,
        call: MessagesCall,
        interceptors: &impl waypoint_host::interceptors::Interceptors<Error>,
        options: impl Into<waypoint_inference::CallOptions>,
    ) -> Result<MessagesCallResponse, Error> {
        let context = CallContext::new(interceptors, options.into());
        waypoint_host::lifecycle::observe_call(context.observers.clone(), self.run(call, context))
            .await
    }

    #[tracing::instrument(name = "waypoint.route", skip_all, fields(
        route = "messages",
        model = %call.body.model,
        provider,
        resolved_model,
        stream = call.body.params.stream == Some(true),
        outcome
    ))]
    async fn run(
        &self,
        call: MessagesCall,
        context: CallContext<'_, impl Interceptors<Error>>,
    ) -> Result<MessagesCallResponse, Error> {
        waypoint_inference::diagnostic::call(async {
            let prepared = prepare::prepare(call, self.secrets.as_ref()).await?;
            waypoint_inference::diagnostic::provider(
                &prepared.body.model,
                prepared.provider.as_str(),
            );
            let request = self.prepare_outbound(prepared, &context).boxed().await?;
            let cache = CallCache::<route::Messages>::from_wire(
                self.cache.as_ref().filter(|_| request.cacheable()),
                context.cache,
                &request.identity,
                &request.wire,
            );
            let identity = request.identity.clone();
            let (output, source) = match cache.lookup().await {
                Some(hit) => hit,
                None => (
                    self.call_provider(request, &context).await?,
                    ResultSource::Provider,
                ),
            };
            context
                .result_ready(ExecutionFacts {
                    provider: identity,
                    source: source.clone(),
                })
                .await?;
            Ok(cache.finish(output, &source).await)
        })
        .await
    }
}
