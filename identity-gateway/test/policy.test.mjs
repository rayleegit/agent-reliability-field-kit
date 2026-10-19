import test from "node:test";
import assert from "node:assert/strict";

import { invokeTool, ISSUER, RESOURCE } from "../src/tools.mjs";

const now = 1_800_000_000;
const validClaims = {
  iss: ISSUER,
  aud: RESOURCE,
  exp: now + 60,
  profile_id: "prf_stable_123",
  scope: ["cases.read"],
};

test("allows explicitly anonymous tool", () => {
  const result = invokeTool("search_public_guidance", null, {}, now);
  assert.equal(result.isError, false);
  assert.equal(result.structuredContent.principal.mode, "anonymous");
});

test("returns OAuth challenge when token is missing", () => {
  const result = invokeTool("read_private_case", null, {}, now);
  assert.equal(result.isError, true);
  assert.match(result._meta["mcp/www_authenticate"][0], /invalid_token/);
});

test("enforces resource audience", () => {
  const result = invokeTool(
    "read_private_case",
    { ...validClaims, aud: "https://another-resource.example" },
    {},
    now,
  );
  assert.equal(result.isError, true);
  assert.match(result.content[0].text, /another resource/);
});

test("enforces expiry", () => {
  const result = invokeTool(
    "read_private_case",
    { ...validClaims, exp: now - 1 },
    {},
    now,
  );
  assert.equal(result.isError, true);
  assert.match(result.content[0].text, /expired/);
});

test("enforces least-privilege scopes", () => {
  const result = invokeTool("create_review_task", validClaims, {}, now);
  assert.equal(result.isError, true);
  assert.match(result._meta["mcp/www_authenticate"][0], /reviews.write/);
});

test("preserves stable profile identity on authorized call", () => {
  const result = invokeTool("read_private_case", validClaims, {}, now);
  assert.equal(result.isError, false);
  assert.equal(result.structuredContent.principal.profileId, "prf_stable_123");
});

