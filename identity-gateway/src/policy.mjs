export class AuthorizationError extends Error {
  constructor(code, description, requiredScopes = []) {
    super(description);
    this.name = "AuthorizationError";
    this.code = code;
    this.requiredScopes = requiredScopes;
  }
}

export function authorize({ claims, policy, nowSeconds = Math.floor(Date.now() / 1000) }) {
  if (policy.allowAnonymous && !claims) {
    return { profileId: null, scopes: [], mode: "anonymous" };
  }

  if (!claims) {
    throw new AuthorizationError(
      "invalid_token",
      "A valid access token is required.",
      policy.requiredScopes,
    );
  }

  if (claims.iss !== policy.expectedIssuer) {
    throw new AuthorizationError("invalid_token", "Unexpected token issuer.");
  }

  const audiences = Array.isArray(claims.aud) ? claims.aud : [claims.aud];
  if (!audiences.includes(policy.expectedAudience)) {
    throw new AuthorizationError("invalid_token", "Token was minted for another resource.");
  }

  if (!Number.isFinite(claims.exp) || claims.exp <= nowSeconds) {
    throw new AuthorizationError("invalid_token", "Token is missing an expiry or has expired.");
  }

  if (typeof claims.profile_id !== "string" || claims.profile_id.trim() === "") {
    throw new AuthorizationError("invalid_token", "Stable profile identity is required.");
  }

  const granted = new Set(Array.isArray(claims.scope) ? claims.scope : []);
  const missing = policy.requiredScopes.filter((scope) => !granted.has(scope));
  if (missing.length > 0) {
    throw new AuthorizationError(
      "insufficient_scope",
      `Missing required scope: ${missing.join(", ")}`,
      policy.requiredScopes,
    );
  }

  return {
    profileId: claims.profile_id,
    scopes: [...granted].sort(),
    mode: "authenticated",
  };
}

export function oauthChallenge(error, resourceMetadataUrl) {
  const scope = error.requiredScopes.length
    ? `, scope="${error.requiredScopes.join(" ")}"`
    : "";
  const challenge = `Bearer resource_metadata="${resourceMetadataUrl}", error="${error.code}", error_description="${error.message}"${scope}`;

  return {
    content: [{ type: "text", text: `Authorization required: ${error.message}` }],
    _meta: { "mcp/www_authenticate": [challenge] },
    isError: true,
  };
}

