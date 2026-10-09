#[derive(Default)]
pub struct AuthServices {
    #[cfg(feature = "aws")]
    pub aws: waypoint_auth_aws::AwsAuthService,
    #[cfg(feature = "azure")]
    pub azure: waypoint_auth_azure::AzureAuthService,
    #[cfg(feature = "gcp")]
    pub gcp: waypoint_auth_gcp::VertexAuth,
}
