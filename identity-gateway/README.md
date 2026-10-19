# Scoped Identity Gateway

A credential-free authorization-policy simulator for MCP-style tools. It demonstrates the decisions a resource server must make after an identity provider has issued and cryptographically signed a token.

## Run

```bash
node demo.mjs
node --test test/*.test.mjs
```

## Demonstrated behavior

- anonymous access to explicitly public tools;
- required-audience validation;
- token-expiry validation;
- per-tool scope checks;
- least-privilege separation between read and write tools; and
- an `mcp/www_authenticate` challenge for missing or insufficient authorization.

## Security boundary

This demo uses plain JavaScript objects as **mock verified claims** so the policy decisions are easy to inspect. It does not parse or verify JWTs and is not an authorization server.

In production:

- use an established identity provider;
- validate the signed token before passing claims to this policy layer;
- verify issuer, audience, expiry, and scopes on every invocation;
- use authorization-code flow with PKCE; and
- publish protected-resource and authorization-server metadata.

The sample resource metadata is in `metadata/oauth-protected-resource.json`.

