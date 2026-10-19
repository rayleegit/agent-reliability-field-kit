import { invokeTool, ISSUER, RESOURCE } from "./src/tools.mjs";

const now = 1_800_000_000;
const readClaims = {
  iss: ISSUER,
  aud: RESOURCE,
  exp: now + 300,
  profile_id: "prf_demo_work",
  scope: ["cases.read"],
};

const scenarios = [
  ["anonymous public read", "search_public_guidance", null],
  ["missing token", "read_private_case", null],
  ["least privilege blocks write", "create_review_task", readClaims],
  ["authorized private read", "read_private_case", readClaims],
];

for (const [label, tool, claims] of scenarios) {
  const result = invokeTool(tool, claims, { caseId: "case_demo" }, now);
  console.log(`\n${label}`);
  console.log(JSON.stringify(result, null, 2));
}

