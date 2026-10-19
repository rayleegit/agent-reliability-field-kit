import { AuthorizationError, authorize, oauthChallenge } from "./policy.mjs";

export const RESOURCE = "https://agent-field-kit.example/mcp";
export const ISSUER = "https://identity.example";
export const RESOURCE_METADATA = `${RESOURCE}/.well-known/oauth-protected-resource`;

export const toolPolicies = {
  search_public_guidance: {
    allowAnonymous: true,
    requiredScopes: [],
    expectedAudience: RESOURCE,
    expectedIssuer: ISSUER,
  },
  read_private_case: {
    allowAnonymous: false,
    requiredScopes: ["cases.read"],
    expectedAudience: RESOURCE,
    expectedIssuer: ISSUER,
  },
  create_review_task: {
    allowAnonymous: false,
    requiredScopes: ["reviews.write"],
    expectedAudience: RESOURCE,
    expectedIssuer: ISSUER,
  },
};

export function invokeTool(name, claims, input = {}, nowSeconds) {
  const policy = toolPolicies[name];
  if (!policy) {
    throw new Error(`Unknown tool: ${name}`);
  }

  try {
    const principal = authorize({ claims, policy, nowSeconds });
    return {
      content: [{ type: "text", text: `Executed ${name}` }],
      structuredContent: { input, principal },
      isError: false,
    };
  } catch (error) {
    if (error instanceof AuthorizationError) {
      return oauthChallenge(error, RESOURCE_METADATA);
    }
    throw error;
  }
}

